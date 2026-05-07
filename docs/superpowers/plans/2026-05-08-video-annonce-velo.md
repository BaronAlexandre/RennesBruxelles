# Video Annonce Rennes→Bruxelles — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Generate `annonce_16x9.mp4` and `annonce_9x16.mp4`, a ~35s animated announcement of the Rennes→Bruxelles bike trip.

**Architecture:** Python builds the video as 5 moviepy clips (intro, windows accumulation+freeze, blackout, philosophical question, announcement) concatenated in sequence. Pillow renders individual frames; staticmap fetches OSM tiles for the route. The same pipeline runs twice — once per canvas dimension — to produce 16:9 and 9:16 variants.

**Tech Stack:** Python 3.10+, moviepy==1.0.3, Pillow>=10.0, staticmap==0.5.4, numpy, requests, pytest

---

## File Map

| File | Responsibility |
|------|----------------|
| `requirements.txt` | Pinned dependencies |
| `video/__init__.py` | Package marker |
| `video/constants.py` | Colors, timing, questions, coordinates, font path |
| `video/window_renderer.py` | Renders one Claude Code window as PIL Image |
| `video/map_generator.py` | Fetches OSM tiles, draws 6-waypoint route, returns PIL Image |
| `video/scenes.py` | Builds each of the 5 moviepy clips |
| `generate_video.py` | Entry point: assembles clips, exports both MP4s |
| `tests/__init__.py` | Package marker |
| `tests/test_window_renderer.py` | Unit tests for window rendering |
| `tests/test_map_generator.py` | Unit tests for map generation |
| `tests/test_scenes.py` | Unit tests for clip durations and frame shapes |
| `assets/` | User-provided intro footage (intro.mp4 or intro.png) |

---

### Task 1: Project setup

**Files:**
- Create: `requirements.txt`
- Create: `video/__init__.py`
- Create: `tests/__init__.py`
- Create: `assets/` (empty folder)

- [ ] **Step 1: Create requirements.txt**

```
moviepy==1.0.3
Pillow>=10.0.0
staticmap==0.5.4
numpy>=1.24.0
requests>=2.31.0
pytest>=7.4.0
imageio>=2.31.0
imageio-ffmpeg>=0.4.9
```

- [ ] **Step 2: Create package markers and assets folder**

```bash
mkdir -p assets tests video
echo "" > video/__init__.py
echo "" > tests/__init__.py
```

- [ ] **Step 3: Install dependencies**

Run: `pip install -r requirements.txt`
Expected: all packages install without error. If `imageio-ffmpeg` fails, also run `pip install ffmpeg-python`.

- [ ] **Step 4: Commit**

```bash
git add requirements.txt video/__init__.py tests/__init__.py
git commit -m "feat: project setup for video generation"
```

---

### Task 2: video/constants.py

**Files:**
- Create: `video/constants.py`

- [ ] **Step 1: Write constants.py**

```python
import os

FORMATS = {
    "16x9": (1920, 1080),
    "9x16": (1080, 1920),
}

WIN_W = 800
WIN_H = 500
WIN_OFFSET_X = 40
WIN_OFFSET_Y = 30

COLORS = {
    "bg":          "#1a1a1a",
    "border":      "#333333",
    "titlebar":    "#2d2d2d",
    "dot_red":     "#FF5F57",
    "dot_yellow":  "#FFBD2E",
    "dot_green":   "#28CA41",
    "text_white":  "#ffffff",
    "text_dim":    "#a0a0a0",
    "text_orange": "#E8521A",
    "canvas_bg":   "#000000",
}

_win_dir = os.environ.get("WINDIR", "C:\\Windows")
FONT_PATH = os.path.join(_win_dir, "Fonts", "consola.ttf")
FONT_PATH_FALLBACK = os.path.join(_win_dir, "Fonts", "cour.ttf")

# Delay (seconds) BEFORE each window appears; index 0 = delay before first window
WINDOW_DELAYS = [0.0, 3.0, 2.0, 1.5, 1.0, 0.7, 0.5, 0.35, 0.25, 0.15]
WINDOW_FREEZE_DURATION = 2.0
BLACKOUT_DURATION = 4.0

CHAR_DELAY = 0.04
PHILOSOPHICAL_QUESTION = "et maintenant que j'ai terminé toutes mes missions... qu'est-ce que je fais ?"
SPINNER_CHARS = ["|", "/", "-", "\\"]
THINK_DURATION = 5.0
FADE_DURATION = 1.0

ANNOUNCEMENT_LINES = [
    "Rennes → Bruxelles",
    "680 km  ·  5 jours",
    "14 — 18 mai 2026",
]
LINE_DELAY = 0.8
HANDLE = "@alex.san.dre"

ROUTE_WAYPOINTS = [
    (48.1173, -1.6778),
    (48.7444, -0.5733),
    (49.4432,  1.0993),
    (49.8941,  2.2957),
    (50.3578,  3.5237),
    (50.8503,  4.3517),
]

WINDOWS = [
    (
        "Comment optimiser une requête SQL avec 3 jointures et 500k rows ?",
        ["→ Ajoute des index sur les colonnes de JOIN", "→ Utilise EXPLAIN ANALYZE pour profiler", "→ Évite SELECT *, liste les colonnes explicitement"],
    ),
    (
        "Mon composant React se re-render en boucle, useEffect dépendance objet",
        ["→ Problème : référence objet recréée à chaque render", "→ Fix : useMemo sur l'objet ou useRef pour comparer", "→ Ou passe les propriétés scalaires séparément"],
    ),
    (
        "Dockerfile multi-stage pour FastAPI Python, prod-ready",
        ["→ Stage 1 builder : pip install dans /venv", "→ Stage 2 runtime : copie /venv, user non-root", "→ Expose 8000, CMD uvicorn app.main:app --host 0.0.0.0"],
    ),
    (
        "Regex pour valider un email sans librairie externe",
        [r"→ r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$'", "→ Couvre 99% des cas réels", "→ Ne valide pas l'existence du domaine"],
    ),
    (
        "Comment implémenter un debounce en TypeScript ?",
        ["→ function debounce<T extends unknown[]>(fn: (...a: T) => void, ms: number)", "→ let timer: ReturnType<typeof setTimeout>", "→ return (...args: T) => { clearTimeout(timer); timer = setTimeout(...) }"],
    ),
    (
        "JWT refresh token rotation — best practices sécurité",
        ["→ Invalide l'ancien refresh token à chaque usage", "→ Stocke les tokens en DB avec hash bcrypt", "→ Réutilisation détectée = révocation de toute la famille"],
    ),
    (
        "Ma CI GitHub Actions timeout après 6min, comment debugger ?",
        ["→ Ajoute timeout-minutes: 15 sur le job pour voir le log complet", "→ Active le cache pip/npm entre runs", "→ Action tmate pour SSH interactif en cas de blocage"],
    ),
    (
        "Diff entre Promise.all et Promise.allSettled ?",
        ["→ Promise.all : échoue dès le premier rejet (fail-fast)", "→ Promise.allSettled : attend toutes, retourne statut+valeur", "→ Utilise allSettled quand les échecs partiels sont acceptables"],
    ),
    (
        "PostgreSQL vs MongoDB pour stocker des événements time-series",
        ["→ Postgres + TimescaleDB : SQL, compression, agrégations natives", "→ MongoDB : flexible si le schéma évolue souvent", "→ Pour du time-series pur : Timescale > Mongo"],
    ),
    (
        "Graceful shutdown d'un serveur Node.js Express ?",
        ["→ process.on('SIGTERM', () => server.close(callback))", "→ Arrête d'accepter nouvelles connexions, attend les actives", "→ Force kill après timeout de 10s avec process.exit(1)"],
    ),
]
```

- [ ] **Step 2: Commit**

```bash
git add video/constants.py
git commit -m "feat: add video constants (colors, timing, content)"
```

---

### Task 3: video/window_renderer.py

**Files:**
- Create: `video/window_renderer.py`
- Create: `tests/test_window_renderer.py`

- [ ] **Step 1: Write failing test**

```python
# tests/test_window_renderer.py
from PIL import Image
from video.window_renderer import render_window

Q = "Comment optimiser une requête SQL ?"
R = ["→ Ajoute des index", "→ Utilise EXPLAIN"]

def test_render_window_dimensions():
    img = render_window(Q, R)
    assert img.size == (800, 500)

def test_render_window_is_rgb():
    img = render_window(Q, R)
    assert isinstance(img, Image.Image)
    assert img.mode == "RGB"

def test_render_window_bg_color():
    img = render_window(Q, R)
    # pixel just inside border should be bg color #1a1a1a = (26, 26, 26)
    assert img.getpixel((2, 42)) == (26, 26, 26)

def test_render_window_custom_size():
    img = render_window(Q, R, width=600, height=400)
    assert img.size == (600, 400)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_window_renderer.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'video.window_renderer'`

- [ ] **Step 3: Write window_renderer.py**

```python
# video/window_renderer.py
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
```

- [ ] **Step 4: Run tests**

Run: `pytest tests/test_window_renderer.py -v`
Expected: 4 tests PASS

- [ ] **Step 5: Commit**

```bash
git add video/window_renderer.py tests/test_window_renderer.py
git commit -m "feat: add Claude Code window renderer"
```

---

### Task 4: video/map_generator.py

**Files:**
- Create: `video/map_generator.py`
- Create: `tests/test_map_generator.py`

- [ ] **Step 1: Write failing test**

```python
# tests/test_map_generator.py
from PIL import Image
from video.map_generator import generate_route_map

def test_generate_route_map_dimensions():
    img = generate_route_map(800, 400)
    assert img.size == (800, 400)

def test_generate_route_map_is_rgb():
    img = generate_route_map(800, 400)
    assert isinstance(img, Image.Image)
    assert img.mode == "RGB"
```

- [ ] **Step 2: Run to verify failure**

Run: `pytest tests/test_map_generator.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'video.map_generator'`

- [ ] **Step 3: Write map_generator.py**

```python
# video/map_generator.py
from PIL import Image
from staticmap import StaticMap, CircleMarker, Line
from video.constants import ROUTE_WAYPOINTS, COLORS


def generate_route_map(width: int, height: int) -> Image.Image:
    m = StaticMap(width, height, url_template="https://tile.openstreetmap.org/{z}/{x}/{y}.png")

    # Route line: staticmap expects (lon, lat) pairs
    coords = [(lon, lat) for lat, lon in ROUTE_WAYPOINTS]
    m.add_line(Line(coords, COLORS["text_orange"], 4))

    # Waypoint markers
    for lat, lon in ROUTE_WAYPOINTS:
        m.add_marker(CircleMarker((lon, lat), "#ffffff", 12))
        m.add_marker(CircleMarker((lon, lat), COLORS["text_orange"], 7))

    img = m.render()
    return img.convert("RGB")
```

- [ ] **Step 4: Run tests** (requires internet for OSM tiles)

Run: `pytest tests/test_map_generator.py -v`
Expected: 2 tests PASS

- [ ] **Step 5: Commit**

```bash
git add video/map_generator.py tests/test_map_generator.py
git commit -m "feat: add OSM route map generator"
```

---

### Task 5: video/scenes.py — intro + windows

**Files:**
- Create: `video/scenes.py`
- Create: `tests/test_scenes.py`

- [ ] **Step 1: Write failing tests**

```python
# tests/test_scenes.py
import os
import pytest
from PIL import Image
from video.scenes import make_intro_clip, make_windows_clip
from video.constants import WINDOW_DELAYS, WINDOW_FREEZE_DURATION


def _dummy_asset(tmp_path):
    img = Image.new("RGB", (320, 240), "#ff0000")
    p = str(tmp_path / "intro.png")
    img.save(p)
    return p


def test_intro_clip_duration(tmp_path):
    clip = make_intro_clip(1920, 1080, asset_path=_dummy_asset(tmp_path))
    assert abs(clip.duration - 3.0) < 0.1


def test_intro_clip_frame_shape(tmp_path):
    clip = make_intro_clip(1920, 1080, asset_path=_dummy_asset(tmp_path))
    frame = clip.get_frame(0)
    assert frame.shape == (1080, 1920, 3)


def test_windows_clip_duration():
    clip = make_windows_clip(1920, 1080)
    expected = sum(WINDOW_DELAYS) + WINDOW_FREEZE_DURATION
    assert abs(clip.duration - expected) < 0.5


def test_windows_clip_frame_shape():
    clip = make_windows_clip(1920, 1080)
    frame = clip.get_frame(0)
    assert frame.shape == (1080, 1920, 3)
```

- [ ] **Step 2: Run to verify failure**

Run: `pytest tests/test_scenes.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'video.scenes'`

- [ ] **Step 3: Write scenes.py with imports, helpers, intro_clip, windows_clip**

```python
# video/scenes.py
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
```

- [ ] **Step 4: Run tests**

Run: `pytest tests/test_scenes.py -v`
Expected: 4 tests PASS

- [ ] **Step 5: Commit**

```bash
git add video/scenes.py tests/test_scenes.py
git commit -m "feat: add intro and window accumulation clips"
```

---

### Task 6: video/scenes.py — blackout + philosophical clip

**Files:**
- Modify: `video/scenes.py` (append functions)
- Modify: `tests/test_scenes.py` (append tests)

- [ ] **Step 1: Add failing tests**

Append to `tests/test_scenes.py`:

```python
from video.scenes import make_blackout_clip, make_philosophical_clip
from video.constants import BLACKOUT_DURATION, CHAR_DELAY, PHILOSOPHICAL_QUESTION, THINK_DURATION, FADE_DURATION


def test_blackout_clip_duration():
    clip = make_blackout_clip(1920, 1080)
    assert abs(clip.duration - BLACKOUT_DURATION) < 0.01


def test_blackout_clip_is_black():
    clip = make_blackout_clip(1920, 1080)
    assert clip.get_frame(0).max() == 0


def test_philosophical_clip_duration():
    expected = len(PHILOSOPHICAL_QUESTION) * CHAR_DELAY + 0.5 + THINK_DURATION + FADE_DURATION
    clip = make_philosophical_clip(1920, 1080)
    assert abs(clip.duration - expected) < 0.5


def test_philosophical_clip_frame_shape():
    clip = make_philosophical_clip(1920, 1080)
    assert clip.get_frame(0).shape == (1080, 1920, 3)
```

- [ ] **Step 2: Run to verify failure**

Run: `pytest tests/test_scenes.py::test_blackout_clip_duration tests/test_scenes.py::test_philosophical_clip_duration -v`
Expected: FAIL with `ImportError`

- [ ] **Step 3: Append blackout_clip and philosophical_clip to scenes.py**

```python
def make_blackout_clip(w: int, h: int) -> VideoClip:
    arr = np.zeros((h, w, 3), dtype=np.uint8)
    return ImageClip(arr).set_duration(BLACKOUT_DURATION).set_fps(FPS)


def make_philosophical_clip(w: int, h: int) -> VideoClip:
    type_dur = len(PHILOSOPHICAL_QUESTION) * CHAR_DELAY
    pause = 0.5
    total = type_dur + pause + THINK_DURATION + FADE_DURATION

    font_mono = _load_font(16)

    win_w = min(980, w - 60)
    win_h = 130
    win_x = (w - win_w) // 2
    win_y = (h - win_h) // 2

    def make_frame(t):
        canvas = _black(w, h)
        draw = ImageDraw.Draw(canvas)

        # Window
        draw.rectangle([win_x, win_y, win_x + win_w, win_y + win_h], fill=COLORS["bg"], outline=COLORS["border"])
        bar_h = 32
        draw.rectangle([win_x, win_y, win_x + win_w, win_y + bar_h], fill=COLORS["titlebar"])
        for i, dc in enumerate([COLORS["dot_red"], COLORS["dot_yellow"], COLORS["dot_green"]]):
            cx = win_x + 14 + i * 20
            cy = win_y + bar_h // 2
            draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=dc)

        content_y = win_y + bar_h + 12

        if t < type_dur + pause:
            n = min(int(t / CHAR_DELAY), len(PHILOSOPHICAL_QUESTION))
            draw.text((win_x + 14, content_y), "> " + PHILOSOPHICAL_QUESTION[:n], fill=COLORS["text_white"], font=font_mono)
        else:
            draw.text((win_x + 14, content_y), "> " + PHILOSOPHICAL_QUESTION, fill=COLORS["text_white"], font=font_mono)
            think_t = t - type_dur - pause
            if think_t < THINK_DURATION:
                spin = SPINNER_CHARS[int(think_t * 8) % len(SPINNER_CHARS)]
                draw.text((win_x + 14, content_y + 26), f"{spin} Thinking...", fill="#888888", font=font_mono)

        # Fade to black
        if t > type_dur + pause + THINK_DURATION:
            alpha = min(1.0, (t - (type_dur + pause + THINK_DURATION)) / FADE_DURATION)
            arr = _np(canvas).astype(float)
            return (arr * (1.0 - alpha)).astype(np.uint8)

        return _np(canvas)

    return VideoClip(make_frame, duration=total).set_fps(FPS)
```

- [ ] **Step 4: Run all tests**

Run: `pytest tests/test_scenes.py -v`
Expected: all tests PASS

- [ ] **Step 5: Commit**

```bash
git add video/scenes.py tests/test_scenes.py
git commit -m "feat: add blackout and philosophical question clips"
```

---

### Task 7: video/scenes.py — announcement clip

**Files:**
- Modify: `video/scenes.py` (append function)
- Modify: `tests/test_scenes.py` (append tests)

- [ ] **Step 1: Add failing tests**

Append to `tests/test_scenes.py`:

```python
from video.scenes import make_announcement_clip
from video.constants import LINE_DELAY, ANNOUNCEMENT_LINES


def test_announcement_clip_frame_shape():
    clip = make_announcement_clip(1920, 1080)
    assert clip.get_frame(0).shape == (1080, 1920, 3)


def test_announcement_clip_duration():
    clip = make_announcement_clip(1920, 1080)
    # text phase + map fade + hold >= 6s
    assert clip.duration >= 6.0
```

- [ ] **Step 2: Run to verify failure**

Run: `pytest tests/test_scenes.py::test_announcement_clip_frame_shape -v`
Expected: FAIL with `ImportError`

- [ ] **Step 3: Append announcement_clip to scenes.py**

```python
def make_announcement_clip(w: int, h: int) -> VideoClip:
    map_h = int(h * 0.50)
    map_img = generate_route_map(w, map_h).convert("RGB")
    map_np = _np(map_img).astype(float)

    text_phase = len(ANNOUNCEMENT_LINES) * LINE_DELAY + 0.6
    map_fade = 1.5
    hold = 2.5
    total = text_phase + map_fade + hold

    font_big = _load_font(64)
    font_med = _load_font(42)
    font_small = _load_font(22)

    text_start_y = int(h * 0.10)
    map_y = int(h * 0.40)
    cx = w // 2

    def make_frame(t):
        canvas = _black(w, h)
        draw = ImageDraw.Draw(canvas)

        # Announcement lines appear one by one
        for i, line in enumerate(ANNOUNCEMENT_LINES):
            if t >= i * LINE_DELAY:
                y = text_start_y + i * 82
                font = font_big if i == 0 else font_med
                draw.text((cx, y), line, fill=COLORS["text_white"], font=font, anchor="mm")

        # Map fades in after text phase
        if t >= text_phase:
            alpha = min(1.0, (t - text_phase) / map_fade)
            canvas_np = _np(canvas).astype(float)
            region = canvas_np[map_y:map_y + map_h, 0:w]
            canvas_np[map_y:map_y + map_h, 0:w] = region * (1 - alpha) + map_np * alpha
            canvas = Image.fromarray(canvas_np.astype(np.uint8))
            draw = ImageDraw.Draw(canvas)

        # Handle appears after map is fully visible
        if t >= text_phase + map_fade:
            draw.text((cx, h - 50), HANDLE, fill="#888888", font=font_small, anchor="mm")

        return _np(canvas)

    return VideoClip(make_frame, duration=total).set_fps(FPS)
```

- [ ] **Step 4: Run all tests**

Run: `pytest tests/test_scenes.py -v`
Expected: all tests PASS

- [ ] **Step 5: Commit**

```bash
git add video/scenes.py tests/test_scenes.py
git commit -m "feat: add announcement clip (text + OSM map + handle)"
```

---

### Task 8: generate_video.py — assembly and export

**Files:**
- Create: `generate_video.py`

- [ ] **Step 1: Write generate_video.py**

```python
# generate_video.py
import os
import sys
from moviepy.editor import concatenate_videoclips

from video.constants import FORMATS
from video.scenes import (
    make_intro_clip,
    make_windows_clip,
    make_blackout_clip,
    make_philosophical_clip,
    make_announcement_clip,
)

# Locate intro asset
ASSET = next(
    (p for p in ["assets/intro.mp4", "assets/intro.png", "assets/intro.jpg"] if os.path.exists(p)),
    None,
)
if ASSET is None:
    print("ERROR: place your intro capture at assets/intro.mp4 or assets/intro.png")
    sys.exit(1)

for fmt_name, (w, h) in FORMATS.items():
    print(f"\n=== {fmt_name}  {w}x{h} ===")

    clips = [
        make_intro_clip(w, h, asset_path=ASSET),
        make_windows_clip(w, h),
        make_blackout_clip(w, h),
        make_philosophical_clip(w, h),
        make_announcement_clip(w, h),
    ]

    final = concatenate_videoclips(clips, method="compose")
    out = f"annonce_{fmt_name}.mp4"
    print(f"Rendering {out}  (duration: {final.duration:.1f}s) ...")
    final.write_videofile(
        out,
        fps=30,
        codec="libx264",
        audio=False,
        preset="medium",
        ffmpeg_params=["-crf", "18"],
        logger=None,
    )
    print(f"Saved {out}")
    final.close()
    for c in clips:
        c.close()

print("\nDone. Files: annonce_16x9.mp4  annonce_9x16.mp4")
```

- [ ] **Step 2: Place your intro asset**

Copy your screen recording or screenshot to `assets/intro.mp4` (or `assets/intro.png`).

- [ ] **Step 3: Run the script**

Run: `python generate_video.py`
Expected: progress output, then two files created:
```
annonce_16x9.mp4
annonce_9x16.mp4
```

If you get `OSError: [Errno 22]` on the font, open `video/constants.py` and set `FONT_PATH` to an existing `.ttf` on your machine (e.g., `C:\Windows\Fonts\lucon.ttf`).

If `moviepy` can't find ffmpeg, run: `pip install imageio-ffmpeg` then `python -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())"` to confirm it's found.

- [ ] **Step 4: Spot-check the output**

Open `annonce_16x9.mp4`. Verify in order:
1. Intro footage plays ~3s
2. Claude Code windows appear, first slow then accelerating, all 10 stacked
3. 4s pure black
4. Philosophical question types out, spinner animates, fades to black
5. Announcement text appears line by line, route map fades in, `@alex.san.dre` appears
6. Total duration ~35s

- [ ] **Step 5: Commit**

```bash
git add generate_video.py
git commit -m "feat: add video assembly entry point — generates 16:9 and 9:16 MP4"
```
