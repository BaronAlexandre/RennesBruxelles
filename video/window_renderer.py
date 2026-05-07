import textwrap
from PIL import Image, ImageDraw, ImageFont
from video.constants import COLORS, FONT_PATH, FONT_PATH_FALLBACK


def _load_font(size: int) -> ImageFont.FreeTypeFont:
    for path in [FONT_PATH, FONT_PATH_FALLBACK]:
        try:
            return ImageFont.truetype(path, size)
        except (OSError, IOError):
            continue
    return ImageFont.load_default()


def render_window(question: str, response_lines: list, width: int = 800, height: int = 500) -> Image.Image:
    img = Image.new("RGB", (width, height), COLORS["bg"])
    draw = ImageDraw.Draw(img)

    # Outer border
    draw.rectangle([0, 0, width - 1, height - 1], outline=COLORS["border"])

    # Title bar
    bar_h = 36
    draw.rectangle([1, 1, width - 2, bar_h], fill=COLORS["titlebar"])

    # macOS dots
    for i, color in enumerate([COLORS["dot_red"], COLORS["dot_yellow"], COLORS["dot_green"]]):
        cx = 16 + i * 22
        cy = bar_h // 2
        draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=color)

    # Title text
    font_ui = _load_font(12)
    draw.text((width // 2, bar_h // 2), "claude  —  bash", fill="#888888", font=font_ui, anchor="mm")

    # Content area
    font_mono = _load_font(13)
    y = bar_h + 16

    # Prompt (may wrap on narrow windows)
    prompt = "> " + question
    char_w = 8
    max_chars = max(20, (width - 40) // char_w)
    for line in textwrap.wrap(prompt, width=max_chars) or [prompt]:
        if y + 18 > height - 8:
            break
        draw.text((20, y), line, fill=COLORS["text_white"], font=font_mono)
        y += 20

    y += 4

    # Response lines
    for line in response_lines:
        if y + 18 > height - 8:
            break
        draw.text((20, y), line, fill=COLORS["text_dim"], font=font_mono)
        y += 20

    return img
