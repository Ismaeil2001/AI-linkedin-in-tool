import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from linkedin_scraper import scrape_relevant_posts

# CONFIGURATION
search_url = "https://www.linkedin.com/search/results/content/?keywords=graduate%20program%20Saudi"
COOKIE_FILE = "linkedin_cookies.json"
RELEVANCE_THRESHOLD = 3.0
DEBUG = True

def load_valid_cookies(driver, cookie_path, domain_filter="www.linkedin.com"):
    with open(cookie_path, "r", encoding="utf-8") as f:
        cookie_data = json.load(f)

    driver.get("https://www.linkedin.com")
    added = 0
    for cookie in cookie_data.get("cookies", []):
        if cookie.get("domain") and domain_filter not in cookie["domain"]:
            continue
        cookie.pop("expiry", None)
        try:
            driver.add_cookie(cookie)
            added += 1
        except Exception as e:
            print(f"⚠️ Skipped invalid cookie: {cookie.get('name')} → {str(e)}")
    print(f"✅ Loaded {added} cookies into browser.")

def main():
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")  # New headless mode
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument(f"--user-data-dir=/tmp/chrome-user-data-{time.time()}")  # unique dir
        chrome_options.add_argument("--window-size=1920,1080")

        # chrome_options.add_argument("--headless")  # Optional

        driver = webdriver.Chrome(options=chrome_options)

        # Load LinkedIn cookies securely
        load_valid_cookies(driver, COOKIE_FILE)

        # Call scraper with correct arguments
        posts = scrape_relevant_posts(driver, search_url, debug=DEBUG, min_score=RELEVANCE_THRESHOLD)

        if not posts:
            print("❌ No relevant posts found.")

        driver.quit()

    except Exception as e:
        print("❌ Unexpected error:", str(e))

if __name__ == "__main__":
    main()
