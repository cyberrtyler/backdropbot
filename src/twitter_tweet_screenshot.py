import asyncio
from playwright.async_api import async_playwright

async def screenshot_tweet(tweet_url_or_id, output="tweet_screenshot.png", theme="dark", viewport={"width": 1280, "height": 800}):
    """
    Take a screenshot of a single tweet by URL or tweet ID.
    Args:
        tweet_url_or_id (str): Full URL or just Tweet ID
        output (str): Path to save screenshot
        theme (str): "dark" or "light"
        viewport (dict): Browser viewport size
    """
    # If just tweet ID is passed, build full URL
    if tweet_url_or_id.isdigit():
        url = f"https://twitter.com/i/web/status/{tweet_url_or_id}"
    else:
        url = tweet_url_or_id

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport=viewport)
        await page.emulate_media(color_scheme=theme)
        await page.goto(url, wait_until="networkidle")

        # Wait for tweet container to load - the article with role="article" is usually the tweet itself
        tweet_selector = 'article[role="article"]'
        tweet = await page.wait_for_selector(tweet_selector, timeout=15000)

        if tweet:
            # Take screenshot of just the tweet element
            await tweet.screenshot(path=output)
            print(f"Tweet screenshot saved to {output}")
        else:
            print("Tweet element not found")

        await browser.close()

# Example usage for testing
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python twitter_tweet_screenshot.py <tweet_url_or_id> [output]")
        sys.exit(1)

    tweet_arg = sys.argv[1]
    out_file = sys.argv[2] if len(sys.argv) > 2 else "tweet_screenshot.png"

    asyncio.run(screenshot_tweet(tweet_arg, output=out_file))
