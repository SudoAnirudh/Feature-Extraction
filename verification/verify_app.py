import os
from playwright.sync_api import sync_playwright

def verify(page):
    # Navigate to the frontend
    page.goto("http://localhost:5173")

    # Wait for the app to load
    page.wait_for_selector("#root")

    # Take a screenshot of the initial state
    page.screenshot(path="verification/initial_load.png")

    # Check if we can find the upload input
    # Based on general knowledge, it might be an input[type='file']
    # Let's try to upload a file if possible
    try:
        # Locate file input
        file_input = page.locator("input[type='file']")
        if file_input.count() > 0:
            current_dir = os.getcwd()
            image_path = os.path.join(current_dir, "demo1.jpg")
            file_input.set_input_files(image_path)

            # Wait for some processing or result
            # We don't know the exact UI state change, but let's wait a bit and take another screenshot
            page.wait_for_timeout(3000)
            page.screenshot(path="verification/after_upload.png")
        else:
            print("No file input found.")
    except Exception as e:
        print(f"Upload failed: {e}")

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        verify(page)
        browser.close()
