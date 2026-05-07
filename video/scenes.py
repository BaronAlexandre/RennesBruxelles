import os
import numpy as np
from PIL import Image, ImageDraw
from moviepy.editor import VideoClip, ImageClip, VideoFileClip

from video.constants import (
    COLORS, WIN_W, WIN_H, WIN_OFFSET_X, WIN_OFFSET_Y,
    WINDOW_DELAYS, WINDOW_FREEZE_DURATION, WINDOWS,
    BLACKOUT_DURATION,
    CHAR_DELAY, PHILOSOPHICAL_QUESTION, SPINNER_CHARS, THINK_DURATION, FADE_DURATION,
    ANNOUNCEMENT_LINES, LINE_DELAY, HANDLE,
)
from video.window_renderer import render_window, _load_font
from video.map_generator import generate_route_map

FPS = 30


def _np(img: Image.Image) -> np.ndarray:
    return np.array(img)


def _black(w: int, h: int) -> Image.Image:
    return Image.new("RGB", (w, h), COLORS["canvas_bg"])


def make_intro_clip(w: int, h: int, asset_path: str = "assets/intro.mp4") -> VideoClip:
    ext = os.path.splitext(asset_path)[1].lower()
    duration = 3.0
    if ext in (".mp4", ".mov", ".avi"):
        clip = VideoFileClip(asset_path).subclip(0, duration).resize((w, h))
    else:
        img = Image.open(asset_path).convert("RGB").resize((w, h))
        clip = ImageClip(_np(img)).set_duration(duration)
    return clip.set_fps(FPS)


def _window_appear_times() -> list:
    t, times = 0.0, []
    for delay in WINDOW_DELAYS:
        t += delay
        times.append(t)
    return times


def make_windows_clip(w: int, h: int) -> VideoClip:
    appear_times = _window_appear_times()
    total = appear_times[-1] + WINDOW_FREEZE_DURATION

    # Scale windows to fit canvas horizontally even for narrow formats (9:16)
    max_span_x = WIN_W + WIN_OFFSET_X * (len(WINDOWS) - 1)
    scale = min(1.0, (w - 40) / max_span_x)
    win_w = int(WIN_W * scale)
    win_h = int(WIN_H * scale)
    off_x = int(WIN_OFFSET_X * scale)
    off_y = int(WIN_OFFSET_Y * scale)

    # Pre-render all windows once
    rendered = [render_window(q, r, width=win_w, height=win_h) for q, r in WINDOWS]

    start_x = max(10, (w - win_w - off_x * (len(WINDOWS) - 1)) // 2)
    start_y = max(10, (h - win_h - off_y * (len(WINDOWS) - 1)) // 2)

    def make_frame(t):
        canvas = _black(w, h)
        for i, at in enumerate(appear_times):
            if t >= at:
                x = start_x + i * off_x
                y = start_y + i * off_y
                if x + win_w <= w and y + win_h <= h:
                    canvas.paste(rendered[i], (x, y))
        return _np(canvas)

    return VideoClip(make_frame, duration=total).set_fps(FPS)
