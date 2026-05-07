from PIL import Image
from video.map_generator import generate_route_map


def test_generate_route_map_dimensions():
    img = generate_route_map(800, 400)
    assert img.size == (800, 400)


def test_generate_route_map_is_rgb():
    img = generate_route_map(800, 400)
    assert isinstance(img, Image.Image)
    assert img.mode == "RGB"
