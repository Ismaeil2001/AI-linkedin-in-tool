from linkedin_scraper import scrape_latest_post
from huggingface_utils import score_relevance
from twilio_alert import send_whatsapp_via_twilio

# ✅ Step 1: Define the profile to scan
profile_url = "https://www.linkedin.com/in/lilittshughuryan/"  # Replace with any LinkedIn profile

# ✅ Step 2: Scrape latest post
post = scrape_latest_post(profile_url)

if post:
    print("\n🔎 Scraped Post Content:")
    print(post)

    # ✅ Step 3: Score relevance using Hugging Face
    relevance = score_relevance(post)

    # ✅ Step 4: Decide on suggested action
    if relevance >= 4:
        action = "High-priority outreach"
    elif relevance >= 2:
        action = "Observe or follow up later"
    else:
        action = "Not relevant — skip"

    print(f"\n📊 Relevance score (1–5): {relevance}")
    print(f"\n📩 Suggested Action: {action}")

    # ✅ Step 5: Compile summary for alert
    summary = f"""
🔎 Lead Profile:
{profile_url}

📝 Post: {post[:300]}...

📊 Relevance Score: {relevance}

📩 Action: {action}
"""
    # ✅ Step 6: Send via Twilio WhatsApp Sandbox
    send_whatsapp_via_twilio(summary)

else:
    print("❌ Could not find a recent post for this profile.")
