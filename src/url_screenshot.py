import asyncio
from playwright.async_api import async_playwright
from PIL import Image
import numpy as np

async def screenshot_url(
    url,
    output_file="url_screenshot.png",
    viewport={"width": 1920, "height": 1080},
    crop_box=None):
    """Take a screenshot of the given URL and save it to the specified file."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport=viewport)
        await page.goto(url, wait_until="networkidle")

        # Take screenshot of full page
        screenshot_path = output_file
        await page.screenshot(path=screenshot_path)
        print(f"Full page screenshot saved to {screenshot_path}")
        await browser.close()

    # Crop the screenshot if crop_box is provided
    if crop_box:
        with Image.open(screenshot_path) as img:
            cropped = img.crop(crop_box)  # (left, top, right, bottom)
            cropped.save(output_file)
            print(f"Cropped screenshot saved to {output_file}")
