from pathlib import Path
from playwright.sync_api import sync_playwright

def check_homepage(url: str) -> dict:
    Path("artifacts").mkdir(exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")
        title = page.title()
        screenshot_path = "artifacts/homepage.png"
        page.screenshot(path=screenshot_path, full_page=True)
        browser.close()

    return {
        "tool": "browser_check",
        "url": url,
        "title": title,
        "screenshot": screenshot_path,
    }