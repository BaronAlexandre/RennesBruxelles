import math, requests, pathlib, sys

STAGES = [
    {"name": "J1 - Rennes-Flers",             "start": (48.1173, -1.6778), "end": (48.7484, -0.5721)},
    {"name": "J2 - Flers-Rouen",              "start": (48.7484, -0.5721), "end": (49.4432,  1.0993)},
    {"name": "J3 - Rouen-Amiens",             "start": (49.4432,  1.0993), "end": (49.8942,  2.2957)},
    {"name": "J4 - Amiens-Valenciennes",      "start": (49.8942,  2.2957), "end": (50.3576,  3.5238)},
    {"name": "J5 - Valenciennes-Bruxelles",   "start": (50.3576,  3.5238), "end": (50.8503,  4.3517)},
]

OUT = pathlib.Path("gpx")
OUT.mkdir(exist_ok=True)


def get_osrm_route(start, end):
    url = (
        f"http://router.project-osrm.org/route/v1/cycling/"
        f"{start[1]},{start[0]};{end[1]},{end[0]}"
    )
    r = requests.get(url, params={"overview": "full", "geometries": "geojson"}, timeout=20)
    r.raise_for_status()
    return r.json()["routes"][0]["geometry"]["coordinates"]  # [[lng, lat], ...]


def haversine(a, b):
    R = 6371
    lat1, lon1 = math.radians(a[0]), math.radians(a[1])
    lat2, lon2 = math.radians(b[0]), math.radians(b[1])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    h = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))


def to_gpx_course(name, coords):
    points = "\n".join(
        f'    <rtept lat="{lat}" lon="{lng}"><ele>0</ele></rtept>'
        for lng, lat in coords
    )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<gpx version="1.1" creator="RennesBruxelles"\n'
        '     xmlns="http://www.topografix.com/GPX/1/1"\n'
        '     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n'
        '     xsi:schemaLocation="http://www.topografix.com/GPX/1/1 '
        'http://www.topografix.com/GPX/1/1/gpx.xsd">\n'
        "  <rte>\n"
        f"    <name>{name}</name>\n"
        f"{points}\n"
        "  </rte>\n"
        "</gpx>"
    )


print("Generation des GPX courses pour Garmin...\n")

for s in STAGES:
    print(f"-> {s['name']}...")
    coords = get_osrm_route(s["start"], s["end"])
    pts = [(c[1], c[0]) for c in coords]
    km = sum(haversine(pts[i], pts[i + 1]) for i in range(len(pts) - 1))
    gpx = to_gpx_course(s["name"], coords)
    fname = OUT / f"{s['name'].replace(' ', '_')}.gpx"
    fname.write_text(gpx, encoding="utf-8")
    print(f"   {round(km)} km -> {fname}")

print("\nOK - 5 fichiers dans gpx/")
print("\nChargement sur Garmin Edge Explorer :")
print("  Option A - USB direct (le plus simple) :")
print("    1. Branche le Garmin en USB")
print("    2. Copie les .gpx dans Garmin/NewFiles/")
print("    3. Deconnecte - les courses apparaissent dans Navigation > Parcours")
print("  Option B - Garmin Connect web :")
print("    1. connect.garmin.com -> Entrainement -> Parcours")
print("    2. Importe chaque fichier GPX")
print("    3. Sync via l'appli Garmin Connect sur le telephone")
