from PIL import Image, ImageDraw, ImageFilter, ImageColor
import numpy as np
import os
import random

class BlendedBackgroundGenerator:
    def __init__(
            self,
            base_color="#4f46e5",
            radius=20):
        """
        base_color: str - a hex string or color name used as the main theme color
        """
        self.base_color = base_color
        self.palette = self._generate_palette_from_base(base_color)

    def _generate_palette_from_base(self, base_color):
        """
        Generate a list of colors based on the base color.
        For simplicity, create variations in brightness and saturation.
        """
        base_rgb = ImageColor.getrgb(base_color)

        def clamp(x):
            return max(0, min(255, x))

        def brighten(color, factor=1.2):
            return tuple(clamp(int(c * factor)) for c in color)

        def darken(color, factor=0.8):
            return tuple(clamp(int(c * factor)) for c in color)

        # Generate simple variations around the base color
        palette = [
            base_color,                      # base
            ImageColor.getrgb(base_color),  # base as RGB tuple
            brighten(base_rgb, 1.5),        # brighter
            brighten(base_rgb, 1.2),
            darken(base_rgb, 0.8),
            darken(base_rgb, 0.6),
            (10, 10, 10),                   # very dark for contrast
            (255, 255, 255)                 # white for highlights
        ]

        # Convert all to hex strings for consistency
        hex_palette = []
        for c in palette:
            if isinstance(c, tuple):
                hex_palette.append('#{:02x}{:02x}{:02x}'.format(*c))
            else:
                hex_palette.append(c)

        return hex_palette

    def round_corners(self, image, radius):
        mask = Image.new("L", image.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle((0, 0, image.size[0], image.size[1]), radius=radius, fill=255)
        image.putalpha(mask)
        return image

    def generate_random_blended_background(self, size, noise_scale=0.1, blur_radius=50):
        """
        size: (width, height)
        noise_scale: float, fraction of width/height for noise pixel size (smaller = more detail)
        blur_radius: how much to blur for smooth blend
        """
        width, height = size
        noise_w = max(2, int(width * noise_scale))
        noise_h = max(2, int(height * noise_scale))

        noise_img = Image.new("RGB", (noise_w, noise_h))
        noise_pixels = noise_img.load()

        rgb_colors = [ImageColor.getrgb(c) for c in self.palette]

        for y in range(noise_h):
            for x in range(noise_w):
                noise_pixels[x, y] = random.choice(rgb_colors)

        large_noise = noise_img.resize((width, height), resample=Image.NEAREST)
        blurred = large_noise.filter(ImageFilter.GaussianBlur(radius=blur_radius))

        return blurred

    def composite_image(self, foreground_path, output="output.png", radius=20, margin_pct=0.1):
        if not os.path.exists(foreground_path):
            raise FileNotFoundError(f"Image not found: {foreground_path}")

        original = Image.open(foreground_path).convert("RGBA")
        rounded = self.round_corners(original, radius)

        orig_w, orig_h = original.size
        margin = int(min(orig_w * margin_pct, orig_h * margin_pct))

        bg_w = orig_w + 2 * margin
        bg_h = orig_h + 2 * margin

        background = self.generate_random_blended_background((bg_w, bg_h))
        background = background.convert("RGBA")

        background.paste(rounded, (margin, margin), rounded)

        background.save(output)
        print(f"Saved to {output}")
