import asyncio
from playwright.async_api import async_playwright
from PIL import Image
import numpy as np

async def screenshot_and_crop(
    username,
    output_file="profile_cropped.png",
    theme="dark",
    viewport={"width": 1280, "height": 1600},
    crop_box=(2, 53, 600, 550)):
    """Take screen shot of given Twitter Profile"""

    url = f"https://twitter.com/{username}"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport=viewport)
        await page.emulate_media(color_scheme=theme)
        await page.goto(url, wait_until="domcontentloaded", timeout=60000)
        
        # Wait for the primary column to appear
        try:
            primary_column = await page.wait_for_selector('div[data-testid="primaryColumn"]', timeout=30000)
            screenshot_path = output_file
            await primary_column.screenshot(path=screenshot_path)
            print(f"Full profile screenshot saved to {screenshot_path}")
        except Exception as e:
            print(f"Could not find primaryColumn div: {e}")
            # Try alternative selectors or full page screenshot
            print("Attempting full page screenshot instead...")
            screenshot_path = output_file
            await page.screenshot(path=screenshot_path)
            print(f"Full page screenshot saved to {screenshot_path}")

        await browser.close()

    # Crop the screenshot
    with Image.open(screenshot_path) as img:
        cropped = img.crop(crop_box)  # (left, top, right, bottom)
        cropped.save(output_file)
        print(f"Cropped profile screenshot saved to {output_file}")

def average_color_top_half(image_path):
    with Image.open(image_path) as img:
        width, height = img.size
        top_half = img.crop((0, 0, width, height // 2))

        # Convert to numpy array
        np_img = np.array(top_half)

        # If image has alpha channel, ignore it for average color
        if np_img.shape[2] == 4:
            np_img = np_img[:, :, :3]

        # Calculate average RGB
        avg_color = np_img.mean(axis=(0,1))

        # Convert to int tuple
        avg_color = tuple(map(int, avg_color))

        # Convert to hex string
        hex_color = '#{:02x}{:02x}{:02x}'.format(*avg_color)

        return hex_color


if __name__ == "__main__":
    # Adjust crop_box pixel values depending on what exact area you want to crop
    # Example: (left, top, right, bottom)
    asyncio.run(screenshot_and_crop("cyberrtyler", crop_box=(2, 53, 600, 550)))

    # Example usage
    avg = average_color_top_half("profile_cropped.png")
    print("Average color of top half:", avg)
