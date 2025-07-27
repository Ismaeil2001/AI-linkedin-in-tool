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

        # Wait for the user to fully log in
        print("Please log in manually. Waiting for successful login...")

        # ✅ Wait until user reaches the LinkedIn feed (after login)
        page.wait_for_url("https://www.linkedin.com/feed/", timeout=120_000)  # 2 minutes max

        print("✅ Login successful! Saving cookies.")
        context.storage_state(path=COOKIES_PATH)
        browser.close()
        print("✅ Login session saved to", COOKIES_PATH)
