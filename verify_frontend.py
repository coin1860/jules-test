from playwright.sync_api import sync_playwright
import time
import os

def verify_frontend():
    os.makedirs("/home/jules/verification", exist_ok=True)
    with sync_playwright() as p:
        print("Launching browser...")
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("Navigating to http://localhost:3000")
        try:
            page.goto("http://localhost:3000", timeout=120000) # Give it time to compile
        except Exception as e:
            print(f"Error navigating: {e}")
            return

        # Wait for title
        print("Waiting for title...")
        try:
            page.wait_for_selector("text=FX Quant POC", timeout=60000)
        except Exception as e:
            print(f"Title not found: {e}")
            page.screenshot(path="/home/jules/verification/failed_load.png")
            browser.close()
            return

        print("Dashboard loaded.")

        # Click Start
        print("Clicking Start...")
        try:
            page.click("text=Start", timeout=10000)
        except Exception as e:
             print(f"Start button failed: {e}")

        # Wait for some updates
        print("Waiting for updates...")
        time.sleep(10)

        # Take screenshot
        output_path = "/home/jules/verification/verification.png"
        page.screenshot(path=output_path, full_page=True)
        print(f"Screenshot saved to {output_path}")

        browser.close()

if __name__ == "__main__":
    verify_frontend()
