from playwright.sync_api import sync_playwright
import time

COOKIES_PATH = "linkedin_cookies.json"

def save_login_session():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print("Opening LinkedIn login page...")
        page.goto("https://www.linkedin.com/login")

        print("Please log in manually. You have 60 seconds...")
        time.sleep(60)

        print("Saving session cookies...")
        context.storage_state(path=COOKIES_PATH)
        browser.close()

def scrape_latest_post(profile_url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(storage_state=COOKIES_PATH)
        page = context.new_page()

        print(f"Visiting profile: {profile_url}")
        page.goto(profile_url)
        page.wait_for_timeout(5000)

        posts = page.locator('div.feed-shared-update-v2__description')
        if posts.count() == 0:
            print("No recent post found.")
            return None

        text = posts.nth(0).inner_text()
        browser.close()
        return text
