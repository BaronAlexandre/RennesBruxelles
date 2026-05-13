import math
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import VideoClip, ImageClip, VideoFileClip

from video.constants import (
    COLORS, WIN_W, WIN_H, WIN_OFFSET_X, WIN_OFFSET_Y,
    WINDOW_DELAYS, WINDOW_FREEZE_DURATION, WINDOWS,
    BLACKOUT_DURATION,
    CHAR_DELAY, PHILOSOPHICAL_QUESTION, SPINNER_CHARS, THINK_DURATION, FADE_DURATION,
    ANNOUNCEMENT_LABEL, ANNOUNCEMENT_LINES, ANNOUNCEMENT_STATS, ANNOUNCEMENT_DATE,
    LINE_DELAY, HANDLE, ROUTE_CITIES,
    FONT_PATH, FONT_PATH_FALLBACK,
)
from video.window_renderer import render_window, _load_font

FPS = 30


# ── tiny helpers ─────────────────────────────────────────────────────────────

def _np(img: Image.Image) -> np.ndarray:
    return np.array(img)


def _black(w: int, h: int) -> Image.Image:
    return Image.new("RGB", (w, h), COLORS["canvas_bg"])


def _hex_rgb(color: str) -> tuple:
    c = color.lstrip("#")
    return tuple(int(c[i:i+2], 16) for i in (0, 2, 4))


def _load_sans(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    _win = os.environ.get("WINDIR", "C:\\Windows")
    if bold:
        paths = ["ariblk.ttf", "arialbd.ttf", "impact.ttf"]
    else:
        paths = ["arial.ttf", "verdana.ttf"]
    candidates = [os.path.join(_win, "Fonts", p) for p in paths] + [FONT_PATH, FONT_PATH_FALLBACK]
    for p in candidates:
        try:
            return ImageFont.truetype(p, size)
        except (OSError, IOError):
            continue
    return ImageFont.load_default()


# ── route drawing ─────────────────────────────────────────────────────────────

def _dashed_gradient_line(draw, x1, y1, x2, y2, c_start, c_end, width=3, dash=10, gap=7):
    dx, dy = x2 - x1, y2 - y1
    length = math.sqrt(dx*dx + dy*dy)
    if length == 0:
        return
    ux, uy = dx / length, dy / length
    r0, g0, b0 = _hex_rgb(c_start)
    r1, g1, b1 = _hex_rgb(c_end)
    pos, on = 0.0, True
    while pos < length:
        seg = dash if on else gap
        end = min(pos + seg, length)
        if on:
            f = pos / length
            col = (int(r0+(r1-r0)*f), int(g0+(g1-g0)*f), int(b0+(b1-b0)*f))
            draw.line([(int(x1+ux*pos), int(y1+uy*pos)),
                       (int(x1+ux*end), int(y1+uy*end))], fill=col, width=width)
        pos = end
        on = not on


def _draw_route(draw, canvas_w, route_y, pad_x, f_city_big, f_city_small):
    x0, x1 = pad_x, canvas_w - pad_x
    slope   = 60
    y0, y1  = route_y + slope // 2, route_y - slope // 2
    _dashed_gradient_line(draw, x0, y0, x1, y1, "#E8521A", "#FFD700", width=3)
    for name, frac, dot_col, radius, bold in ROUTE_CITIES:
        cx = int(x0 + frac * (x1 - x0))
        cy = int(y0 + frac * (y1 - y0))
        draw.ellipse([cx-radius, cy-radius, cx+radius, cy+radius], fill=_hex_rgb(dot_col))
        color = (255, 255, 255) if bold else (80, 80, 80)
        font  = f_city_big if bold else f_city_small
        draw.text((cx, cy + radius + 5), name, fill=color, font=font, anchor="mt")


def _draw_stats(draw, canvas_w, top_y, bot_y, pad_x, f_sv, f_su, f_sl):
    LINE_C  = (26, 26, 26)
    WHITE   = (255, 255, 255)
    DIM_COL = (68, 68, 68)
    zone_w  = (canvas_w - 2 * pad_x) // len(ANNOUNCEMENT_STATS)
    mid_y   = (top_y + bot_y) // 2
    draw.line([(pad_x, top_y), (canvas_w - pad_x, top_y)], fill=LINE_C, width=1)
    draw.line([(pad_x, bot_y), (canvas_w - pad_x, bot_y)], fill=LINE_C, width=1)
    for i, (val, unit, label) in enumerate(ANNOUNCEMENT_STATS):
        zx = pad_x + i * zone_w
        cx = zx + zone_w // 2
        if i > 0:
            draw.line([(zx, top_y + 8), (zx, bot_y - 8)], fill=LINE_C, width=1)
        try:
            val_w  = f_sv.getlength(val)
            unit_w = f_su.getlength(unit) if unit else 0
        except AttributeError:
            val_w = unit_w = 0
        gap    = 4 if unit else 0
        total  = val_w + gap + unit_w
        sx     = cx - total // 2
        draw.text((sx, mid_y - 2), val, fill=WHITE, font=f_sv, anchor="ld")
        if unit:
            draw.text((sx + val_w + gap, mid_y - 2), unit, fill=DIM_COL, font=f_su, anchor="ld")
        draw.text((cx, bot_y - 8), label, fill=DIM_COL, font=f_sl, anchor="mb")


# ── clips ─────────────────────────────────────────────────────────────────────

def make_intro_clip(w: int, h: int, asset_path: str = "assets/intro.mp4") -> VideoClip:
    ext = os.path.splitext(asset_path)[1].lower()
    duration = 3.0
    if ext in (".mp4", ".mov", ".avi"):
        clip = VideoFileClip(asset_path).subclip(0, duration).resize((w, h))
    else:
        img = Image.open(asset_path).convert("RGB").resize((w, h))
        clip = ImageClip(_np(img)).set_duration(duration)
    return clip.set_fps(FPS)


def make_windows_clip(w: int, h: int) -> VideoClip:
    t_acc, times = 0.0, []
    for delay in WINDOW_DELAYS:
        t_acc += delay
        times.append(t_acc)
    total = times[-1] + WINDOW_FREEZE_DURATION

    scale  = min(1.0, (w - 40) / (WIN_W + WIN_OFFSET_X * (len(WINDOWS) - 1)))
    win_w  = int(WIN_W * scale)
    win_h  = int(WIN_H * scale)
    off_x  = int(WIN_OFFSET_X * scale)
    off_y  = int(WIN_OFFSET_Y * scale)

    rendered = [render_window(q, r, width=win_w, height=win_h) for q, r in WINDOWS]
    sx = max(10, (w - win_w - off_x * (len(WINDOWS)-1)) // 2)
    sy = max(10, (h - win_h - off_y * (len(WINDOWS)-1)) // 2)

    def make_frame(t):
        canvas = _black(w, h)
        for i, at in enumerate(times):
            if t >= at:
                x = sx + i * off_x
                y = sy + i * off_y
                if x + win_w <= w and y + win_h <= h:
                    canvas.paste(rendered[i], (x, y))
        return _np(canvas)

    return VideoClip(make_frame, duration=total).set_fps(FPS)


def make_blackout_clip(w: int, h: int) -> VideoClip:
    arr = np.zeros((h, w, 3), dtype=np.uint8)
    return ImageClip(arr).set_duration(BLACKOUT_DURATION).set_fps(FPS)


def make_philosophical_clip(w: int, h: int) -> VideoClip:
    BG     = COLORS["bg"]
    BAR_BG = COLORS["titlebar"]
    SEP    = COLORS["border"]
    TEXT_W = COLORS["text_white"]
    TEXT_D = COLORS["text_dim"]
    TEXT_T = COLORS["text_teal"]
    TEXT_O = COLORS["text_orange"]

    type_dur = len(PHILOSOPHICAL_QUESTION) * CHAR_DELAY
    pause    = 0.5
    total    = type_dur + pause + THINK_DURATION + FADE_DURATION

    font_ui   = _load_font(13)
    font_mono = _load_font(16)
    bar_h = 28
    sb_y  = h - 26

    def make_frame(t):
        canvas = Image.new("RGB", (w, h), BG)
        draw   = ImageDraw.Draw(canvas)

        # top bar
        draw.rectangle([0, 0, w, bar_h], fill=BAR_BG)
        draw.line([(0, bar_h), (w, bar_h)], fill=SEP, width=1)
        draw.text((16, bar_h//2), "Claude Code", fill=TEXT_T, font=font_ui, anchor="lm")
        draw.text((w-16, bar_h//2), "Sonnet 4.6  ·  Claude Pro",
                  fill=TEXT_D, font=font_ui, anchor="rm")

        # bottom bar
        draw.rectangle([0, sb_y, w, h], fill=BAR_BG)
        draw.line([(0, sb_y), (w, sb_y)], fill=SEP, width=1)
        bx = 16
        draw.text((bx, sb_y+13), "Sonnet 4.6", fill=TEXT_T, font=font_ui, anchor="lm"); bx += 110
        draw.text((bx, sb_y+13), "|",          fill=TEXT_D, font=font_ui, anchor="lm"); bx += 18
        draw.text((bx, sb_y+13), "think/high", fill=TEXT_O, font=font_ui, anchor="lm")

        # typed text
        content_y = bar_h + 28
        if t < type_dur + pause:
            n = min(int(t / CHAR_DELAY), len(PHILOSOPHICAL_QUESTION))
            draw.text((24, content_y), "> " + PHILOSOPHICAL_QUESTION[:n],
                      fill=TEXT_W, font=font_mono)
        else:
            draw.text((24, content_y), "> " + PHILOSOPHICAL_QUESTION,
                      fill=TEXT_W, font=font_mono)
            think_t = t - type_dur - pause
            if think_t < THINK_DURATION:
                spin = SPINNER_CHARS[int(think_t * 8) % len(SPINNER_CHARS)]
                draw.text((24, content_y + 28), f"{spin} Thinking...",
                          fill=TEXT_D, font=font_mono)

        # fade to black
        if t > type_dur + pause + THINK_DURATION:
            alpha = min(1.0, (t - (type_dur + pause + THINK_DURATION)) / FADE_DURATION)
            arr = _np(canvas).astype(float)
            return (arr * (1.0 - alpha)).astype(np.uint8)

        return _np(canvas)

    return VideoClip(make_frame, duration=total).set_fps(FPS)


def make_announcement_clip(w: int, h: int) -> VideoClip:
    ORANGE   = (232, 82, 26)
    WHITE    = (255, 255, 255)
    DIM_COL  = (68, 68, 68)
    HAND_COL = (50, 50, 50)

    base  = min(w, h)
    pad_x = int(w * 0.07)

    # fonts
    f_label  = _load_sans(int(base * 0.018))
    f_h1     = _load_sans(int(base * 0.09),  bold=True)
    f_h23    = _load_sans(int(base * 0.075), bold=True)
    f_sv     = _load_sans(int(base * 0.055), bold=True)
    f_su     = _load_sans(int(base * 0.020))
    f_sl     = _load_sans(int(base * 0.013))
    f_date   = _load_sans(int(base * 0.022))
    f_handle = _load_sans(int(base * 0.016))
    f_city_b = _load_sans(int(base * 0.016), bold=True)
    f_city_s = _load_sans(int(base * 0.012))

    # layout
    label_y     = int(h * 0.07)
    h1_y        = int(h * 0.14)
    h2_y        = h1_y + int(base * 0.10) + 10
    h3_y        = h2_y + int(base * 0.085) + 10
    route_y     = int(h * 0.57)
    stats_top_y = int(h * 0.64)
    stats_bot_y = int(h * 0.74)
    date_y      = int(h * 0.78)
    handle_y    = int(h * 0.94)

    fonts_h = [f_h1, f_h23, f_h23]
    ys_h    = [h1_y, h2_y, h3_y]

    # ── orange glow baked into the base background ────────────────
    y_idx, x_idx = np.mgrid[0:h, 0:w]
    gx, gy = int(w * 0.88), int(h * 0.08)
    dist = np.sqrt((x_idx - gx).astype(float)**2 + (y_idx - gy).astype(float)**2)
    glow_s = np.clip(1.0 - dist / (w * 0.45), 0, 1) ** 2 * 0.11
    base_np = np.zeros((h, w, 3), dtype=float)
    base_np[..., :] = 8
    base_np[..., 0] += glow_s * 232
    base_np[..., 1] += glow_s * 82
    base_np[..., 2] += glow_s * 26
    base_np = np.clip(base_np, 0, 255).astype(np.uint8)

    # ── pre-render the "revealed" overlay (route + stats on same bg) ──
    overlay = Image.fromarray(base_np.copy())
    draw_ov = ImageDraw.Draw(overlay)
    _draw_route(draw_ov, w, route_y, pad_x, f_city_b, f_city_s)
    _draw_stats(draw_ov, w, stats_top_y, stats_bot_y, pad_x, f_sv, f_su, f_sl)
    overlay_np = _np(overlay).astype(float)

    # ── timing ───────────────────────────────────────────────────────
    text_phase = len(ANNOUNCEMENT_LINES) * LINE_DELAY + 0.6
    fade_in    = 1.5
    hold       = 2.5
    total      = text_phase + fade_in + hold

    def make_frame(t):
        # blend base → overlay
        if t < text_phase:
            c_arr = base_np.astype(float)
        else:
            alpha = min(1.0, (t - text_phase) / fade_in)
            c_arr = base_np.astype(float) * (1 - alpha) + overlay_np * alpha

        canvas = Image.fromarray(np.clip(c_arr, 0, 255).astype(np.uint8))
        draw   = ImageDraw.Draw(canvas)

        # text drawn on top so it never gets blended away
        draw.text((pad_x, label_y), ANNOUNCEMENT_LABEL, fill=ORANGE, font=f_label)
        for i, (line, font, y) in enumerate(zip(ANNOUNCEMENT_LINES, fonts_h, ys_h)):
            if t >= i * LINE_DELAY:
                draw.text((pad_x, y), line, fill=WHITE, font=font)

        if t >= text_phase + fade_in:
            draw.text((pad_x, date_y), ANNOUNCEMENT_DATE, fill=DIM_COL, font=f_date)
            draw.text((w // 2, handle_y), HANDLE, fill=HAND_COL, font=f_handle, anchor="mt")

        return _np(canvas)

    return VideoClip(make_frame, duration=total).set_fps(FPS)
