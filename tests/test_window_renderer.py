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
    # pixel in content area should be Claude Code bg #0d1117 = (13, 17, 23)
    assert img.getpixel((2, 42)) == (13, 17, 23)

def test_render_window_custom_size():
    img = render_window(Q, R, width=600, height=400)
    assert img.size == (600, 400)
