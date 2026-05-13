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
    BG        = COLORS["bg"]
    BAR_BG    = COLORS["titlebar"]
    SEP       = COLORS["border"]
    TEXT_W    = COLORS["text_white"]
    TEXT_D    = COLORS["text_dim"]
    TEXT_T    = COLORS["text_teal"]
    TEXT_O    = COLORS["text_orange"]

    img  = Image.new("RGB", (width, height), BG)
    draw = ImageDraw.Draw(img)

    font_ui   = _load_font(11)
    font_mono = _load_font(13)

    # ── top status bar ──────────────────────────────────────────────
    bar_h = 26
    draw.rectangle([0, 0, width, bar_h], fill=BAR_BG)
    draw.line([(0, bar_h), (width, bar_h)], fill=SEP, width=1)
    draw.text((10, bar_h // 2), "Claude Code", fill=TEXT_T, font=font_ui, anchor="lm")
    draw.text((width - 10, bar_h // 2), "Sonnet 4.6", fill=TEXT_D, font=font_ui, anchor="rm")

    # ── bottom status bar ───────────────────────────────────────────
    sb_y = height - 24
    draw.rectangle([0, sb_y, width, height], fill=BAR_BG)
    draw.line([(0, sb_y), (width, sb_y)], fill=SEP, width=1)
    x = 10
    draw.text((x, sb_y + 12), "Sonnet 4.6", fill=TEXT_T, font=font_ui, anchor="lm"); x += 90
    draw.text((x, sb_y + 12), "|",          fill=TEXT_D, font=font_ui, anchor="lm"); x += 16
    draw.text((x, sb_y + 12), "think/high", fill=TEXT_O, font=font_ui, anchor="lm")

    # ── content ─────────────────────────────────────────────────────
    content_top = bar_h + 12
    content_bot = sb_y - 8
    y = content_top

    prompt   = "> " + question
    char_w   = 8
    max_chars = max(20, (width - 32) // char_w)
    for line in textwrap.wrap(prompt, width=max_chars) or [prompt]:
        if y + 18 > content_bot:
            break
        draw.text((16, y), line, fill=TEXT_W, font=font_mono)
        y += 20

    y += 6
    for line in response_lines:
        if y + 18 > content_bot:
            break
        draw.text((16, y), line, fill=TEXT_D, font=font_mono)
        y += 20

    return img
