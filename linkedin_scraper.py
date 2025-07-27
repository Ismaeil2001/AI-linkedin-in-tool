import time
import json
import hashlib
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from relevance_model import score_post_relevance
from twilio_alert import send_whatsapp_via_twilio
from google_sheets_logger import append_to_google_sheet
import os
from datetime import datetime

SCROLL_PAUSE_TIME = 2
MAX_SCROLL = 5
SEEN_POSTS_FILE = os.path.abspath("seen_posts.json")

print(f"\n🗂 Using seen posts file: {SEEN_POSTS_FILE}")

# Load previously seen posts
if os.path.exists(SEEN_POSTS_FILE):
    with open(SEEN_POSTS_FILE, "r") as f:
        try:
            seen_hashes = set(json.load(f))
        except Exception as e:
            print(f"⚠️ Error loading seen_posts.json: {e}")
            seen_hashes = set()
else:
    seen_hashes = set()

print(f"📦 Seen hashes loaded: {len(seen_hashes)}")

def save_seen_post(post_hash):
    seen_hashes.add(post_hash)
    try:
        with open(SEEN_POSTS_FILE, "w") as f:
            json.dump(list(seen_hashes), f, indent=2)
        print(f"✅ Saved post hash: {post_hash[:8]}... to seen_posts.json")
    except Exception as e:
        print(f"❌ Error saving seen_posts.json: {e}")

def generate_post_hash(text, profile_url):
    unique_str = f"{text.strip()}::{profile_url.strip()}"
    return hashlib.sha256(unique_str.encode("utf-8")).hexdigest()

def extract_profile_info(post_div):
    try:
        actor_section = post_div.find("div", class_="update-components-actor__container")
        if not actor_section:
            return "N/A", "Unknown"

        # Profile URL
        profile_url = None
        profile_anchor = actor_section.find("a", href=True)
        while profile_anchor:
            href = profile_anchor.get("href", "")
            if "/in/" in href or "/company/" in href:
                profile_url = urljoin("https://www.linkedin.com", href)
                break
            profile_anchor = profile_anchor.find_next("a", href=True)

        # Profile Name
        name_wrapper = actor_section.select_one("span.update-components-actor__title span[dir='ltr']")
        name_text = name_wrapper.get_text(strip=True) if name_wrapper else "Unknown"

        if profile_url and "/company/" in profile_url:
            name_text = f"Company Post: {name_text}"

        return profile_url or "N/A", name_text

    except Exception as e:
        print("⚠️ Error extracting profile info:", e)
        return "N/A", "Unknown"

def scrape_relevant_posts(driver, search_url, debug=False, min_score=3.0):
    print(f"Visiting search page: {search_url}")
    driver.get(search_url)
    time.sleep(SCROLL_PAUSE_TIME)

    for i in range(MAX_SCROLL):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print(f"Scrolling... ({i + 1}/{MAX_SCROLL})")
        time.sleep(SCROLL_PAUSE_TIME)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    post_divs = soup.find_all("div", class_="feed-shared-update-v2")
    print(f"🔍 Found {len(post_divs)} post containers.")

    relevant_posts = []

    for i, post_div in enumerate(post_divs):
        try:
            post_text_element = post_div.select_one("span[dir='ltr']")
            if not post_text_element:
                continue

            post_text = post_text_element.get_text(separator=" ", strip=True)
            if not post_text or len(post_text) < 30:
                continue

            profile_url, _ = extract_profile_info(post_div)
            post_hash = generate_post_hash(post_text, profile_url)

            if post_hash in seen_hashes:
                print(f"🔁 Skipping already-seen post {i+1}.")
                continue

            relevance_score, nli_score, matched_keywords = score_post_relevance(post_text)

            print(f"\n📝 Post {i+1} | Score: {relevance_score:.2f}")
            print("Text:", post_text[:400].strip())

            if relevance_score >= min_score:
                profile_url, profile_name = extract_profile_info(post_div)

                if profile_name.strip().lower() == "unknown" or len(profile_name.strip()) <= 2:
                    print("⚠️ Skipping post due to missing or invalid profile name.")
                    continue

                print("👤 Profile URL:", profile_url)
                print("💼 Profile Name:", profile_name)

                post_data = {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "profile_name": profile_name,
                    "profile_url": profile_url,
                    "text": post_text,
                    "score": relevance_score,
                    "action": "Observe or follow up later",
                }

                relevant_posts.append(post_data)

                message = f"""
🔎 Lead Profile:
{post_data['profile_name']}
{post_data['profile_url']}

📝 Post Snippet:
{post_data['text'][:500]}

📊 Relevance Score: {post_data['score']:.2f}

📩 Action: {post_data['action']}
                """.strip()

                print(f"\n🔎 Relevant LinkedIn Post #{len(relevant_posts)}\n")
                print(message)

                try:
                    send_whatsapp_via_twilio(message)
                except Exception as twilio_error:
                    print(f"❌ Twilio Error: {twilio_error}")

                try:
                    append_to_google_sheet(
                        post_data["timestamp"],
                        post_data["profile_name"],
                        post_data["profile_url"],
                        post_data["text"][:500],
                        post_data["score"],
                        post_data["action"]
                    )
                except Exception as sheet_error:
                    print(f"❌ Google Sheets Logging Error: {sheet_error}")

                save_seen_post(post_hash)

                if debug:
                    os.makedirs("debug_posts", exist_ok=True)
                    with open(f"debug_posts/post_{i+1}.html", "w", encoding="utf-8") as f:
                        f.write(str(post_div))

        except Exception as e:
            print(f"❌ Error processing post {i+1}: {e}")

    return relevant_posts
