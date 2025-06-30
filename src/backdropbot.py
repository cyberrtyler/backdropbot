import argparse
import asyncio
import random
import sys

from twitter_profile_screenshot import screenshot_and_crop, average_color_top_half
from twitter_tweet_screenshot import screenshot_tweet
from screenshot_drop import BlendedBackgroundGenerator
from url_screenshot import screenshot_url

def add_background(input_image, output="output.png", color=None):
    generator = BlendedBackgroundGenerator(base_color=color)
    generator.composite_image(input_image, output=output)
    print(f"Final composited image saved as {output}")

def run_profile(username, output="profile_output.png", color=None):
    asyncio.run(screenshot_and_crop(username, output_file=output))
    if not color:
        color = average_color_top_half(image_path=output)
    add_background(output, output=output, color=color)

def run_screenshot(image_path, output="screenshot_output.png", color=None):
    if not color:
        color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
    add_background(image_path, output=output, color=color)

def run_tweet(url, output="tweet_output.png", color=None):
    asyncio.run(screenshot_tweet(url, output=output))
    if not color:
        color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
    add_background(output, output=output, color=color)

def run_url(url, output="url_output.png", color=None):
    asyncio.run(screenshot_url(url, output_file=output))
    if not color:
        color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
    add_background(output, output=output, color=color)

def main():
    parser = argparse.ArgumentParser(description="Generate a stylized image from Twitter profile, screenshot, or tweet.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcommand: profile
    profile_parser = subparsers.add_parser("profile", help="Generate from a Twitter profile")
    profile_parser.add_argument("username", help="Twitter username")
    profile_parser.add_argument("--output", default="profile_output.png", help="Final output file")
    profile_parser.add_argument("--color", help="Base color for background")

    # Subcommand: screenshot
    screenshot_parser = subparsers.add_parser("screenshot", help="Use existing image file")
    screenshot_parser.add_argument("image_path", help="Path to screenshot image")
    screenshot_parser.add_argument("--output", default="screenshot_output.png", help="Final output file")
    screenshot_parser.add_argument("--color", help="Base color for background")

    # Subcommand: tweet
    tweet_parser = subparsers.add_parser("tweet", help="Generate from a tweet URL (TODO)")
    tweet_parser.add_argument("url", help="Tweet URL")
    tweet_parser.add_argument("--output", default="tweet_output.png", help="Final output file")
    tweet_parser.add_argument("--color", help="Base color for background")

    # Subcommand: url
    url_parser = subparsers.add_parser("url", help="Generate from a URL")
    url_parser.add_argument("url", help="URL to screenshot")
    url_parser.add_argument("--output", default="url_output.png", help="Final output file")
    url_parser.add_argument("--color", help="Base color for background")
    args = parser.parse_args()

    if args.command == "profile":
        run_profile(args.username, output=args.output, color=args.color)
    elif args.command == "screenshot":
        run_screenshot(args.image_path, output=args.output, color=args.color)
    elif args.command == "tweet":
        run_tweet(args.url, output=args.output, color=args.color)
    elif args.command == "url":
        run_url(args.url, output=args.output, color=args.color)

if __name__ == "__main__":
    main()
