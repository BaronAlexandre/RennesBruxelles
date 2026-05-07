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
