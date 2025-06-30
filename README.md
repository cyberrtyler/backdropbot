# Backdrop Bot

A Python CLI tool that generates aesthetic images by capturing Twitter profiles, tweets, or screenshots, and overlaying them onto beautiful, randomly-blended backgrounds.

## Features

- 🧑‍💻 Screenshot a Twitter profile and stylize it
- 📸 Use an existing screenshot and apply a custom background
- 🐦 Capture and stylize a tweet by URL
- 🎨 Customize the background color theme
- 🪄 Rounded corners and soft blur effects

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/cyberrtyler/backdropbot.git
   cd backdropbot
    ```

2. Install dependencies:

    ```
    pip install -r requirements.txt
    ```

3. Install Playwright browser binaries:

    ```
    playwright install
    ```

## Usage
```python backdropbot.py <command> [options]```

### Commands

**profile**
Capture and style a Twitter profile.

`python backdropbot.py profile <username> [--output OUTPUT] [--color COLOR]`

- `username`: Twitter username (e.g. cyberrtyler)
- `--output`: Output image filename (default: final_output.png)
- `--color`: Base color for the background (default: #10b981)

**screenshot**
Use a local image file and apply a background.

`python backdropbot.py screenshot <image_path> [--output OUTPUT] [--color COLOR]`

- `image_path`: Path to the local screenshot
- `--output`: Output image filename (default: final_output.png)
- `--color`: Base color for the background

**tweet**
Capture a tweet by URL (feature coming soon).

`python backdropbot.py tweet <url> [--output OUTPUT] [--color COLOR]`

**url**
Capture a full website page.

`python backdropbot.py url <url> [--output OUTPUT] [--color COLOR]`

### Examples
- `python run.py profile cyberrtyler --output=tyler.png --color="#4f46e5"`
- `python run.py screenshot profile_cropped.png --output=fancy.png --color="#1e293b"`

## Development
The code is organized into:
- `backdropbot.py` – Main CLI entry point
- `screenshot_drop.py` – Blends images with background and styles
- `twitter_profile_screenshot.py` – Handles async Twitter profile screenshotting
- `twitter_profile_screenshot.py` – Handles async Twitter tweet screenshotting
- `url_screenshot.py` - Handles async URL screenshotting

You can extend the tool by implementing tweet capture logic or enabling other platform integrations.
