import requests, pathlib, json, math, re, time

USER_ID = "5602835891342"
JWT = (
    "eyJ4NXQjUzI1NiI6InlIQ2xZdUdwWlNvU2c3dkhrT1k4YzYyR2NGdGxSeV9neEpIYkJfNFpjamsi"
    "LCJraWQiOiJqd3QtMjAyNTAyMTEiLCJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJydGkiOiJi"
    "ZmEzOGJmYzU2MDQ4YzI1OWI2MjMyNWY4NTJiYjQwMjIwZmNhZmMyOWU4NmU4NjA4OWE1MjYzYzI4"
    "YzNjMTAxIiwidXNlcl9uYW1lIjoiNTYwMjgzNTg5MTM0MiIsInNjb3BlIjpbInVzZXIuKiJdLCJleH"
    "AiOjE3Nzg2ODc5ODAsImlhdCI6MTc3ODY4NjE4MCwianRpIjoiN2MyOWIwYmUtMzRiMi00NWRiLTg3"
    "ZDUtMjZiNjZmMzg4MWRkIiwiY2xpZW50X2lkIjoia29tb290LXdlYiIsInVzZXJuYW1lIjoiNTYwMjgz"
    "NTg5MTM0MiJ9.YckKrtW7B0PxmLqn3euXdJuWEehxNmb19b9qwdzabD3vYsfESj0Q87MwNJHSjzrm"
    "YWY3MynPmTvSH6ysX_q-ZwvoaZx1VfIIep5IvggaF8s15ge5M4yGdbhdA96FCXE5BKFHi6cTqIEQ5"
    "lMivaRrgNAMaxm8yywczT650O5sNKBZPdE33lb-52HBJqa0wmGpqAhHOq60gn0q7WpTIwkYVF8IwHB"
    "kY_IvXSkIKq4DdC4FBgOT0ePS1jIZtab5ILeTObYfmoYS_Fj00zQpzUnMSF7Cq9UFWNjQ7AD5RB4v"
    "K5WJTCYfQ2pQ4lil-EQSoJ517Vwh012bhrc9FoUpErOlqw"
)

OLD_IDS = [2952117232, 2952117325, 2952117377, 2952117451, 2952117489]

# Distances cibles en km
STAGES = [
    {"name": "J1 - Rennes-Flers",           "start": (48.1173, -1.6778), "end": (48.7484, -0.5721), "target": 140, "brouter_direct": 127},
    {"name": "J2 - Flers-Rouen",            "start": (48.7484, -0.5721), "end": (49.4432,  1.0993), "target": 200, "brouter_direct": 167},
    {"name": "J3 - Rouen-Amiens",           "start": (49.4432,  1.0993), "end": (49.8942,  2.2957), "target": 120, "brouter_direct": 112},
    {"name": "J4 - Amiens-Valenciennes",    "start": (49.8942,  2.2957), "end": (50.3576,  3.5238), "target": 130, "brouter_direct": 113},
    {"name": "J5 - Valenciennes-Bruxelles", "start": (50.3576,  3.5238), "end": (50.8503,  4.3517), "target": 110, "brouter_direct":  92},
]

GPX_DIR = pathlib.Path("gpx")
GPX_DIR.mkdir(exist_ok=True)

s_komoot = requests.Session()
s_komoot.headers.update({
    "Authorization": f"Bearer {JWT}",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
})


def haversine(a, b):
    R = 6371
    lat1, lon1 = math.radians(a[0]), math.radians(a[1])
    lat2, lon2 = math.radians(b[0]), math.radians(b[1])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    h = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    return 2*R*math.asin(math.sqrt(h))


def perpendicular_waypoint(start, end, current_km, target_km):
    """
    Calcule un waypoint perpendiculaire au milieu du trajet pour atteindre target_km.
    Renvoie (lat, lng) du waypoint intermédiaire.
    """
    lat1, lng1 = start
    lat2, lng2 = end
    mid_lat = (lat1 + lat2) / 2
    mid_lng = (lng1 + lng2) / 2
    cos_lat = math.cos(math.radians(mid_lat))

    dlat_km = (lat2 - lat1) * 111.0
    dlng_km = (lng2 - lng1) * 111.0 * cos_lat
    s = math.sqrt(dlat_km**2 + dlng_km**2)

    eff = current_km / s
    half_t = target_km / (2 * eff)
    if half_t <= s / 2:
        return mid_lat, mid_lng

    p = math.sqrt(half_t**2 - (s / 2)**2)

    # Perpendiculaire gauche (sens antihoraire)
    perp_lat_km = -dlng_km
    perp_lng_km = dlat_km
    scale = p / s

    wp_lat = mid_lat + (perp_lat_km * scale) / 111.0
    wp_lng = mid_lng + (perp_lng_km * scale) / (111.0 * cos_lat)
    return wp_lat, wp_lng


def get_brouter_gpx(waypoints, name):
    """
    waypoints: liste de (lat, lng)
    """
    lonlats = "|".join(f"{lng},{lat}" for lat, lng in waypoints)
    r = requests.get(
        "https://brouter.de/brouter",
        params={"lonlats": lonlats, "profile": "fastbike", "alternativeidx": "0", "format": "gpx"},
        headers={"User-Agent": "RennesBruxellesVelo/1.0"},
        timeout=30,
    )
    r.raise_for_status()
    gpx = r.text
    gpx = re.sub(r"<name>.*?</name>", f"<name>{name}</name>", gpx, count=1)
    return gpx


def get_gpx_distance(gpx_text):
    m = re.search(r"track-length\s*=\s*(\d+)", gpx_text)
    return round(int(m.group(1)) / 1000) if m else "?"


# 1. Supprimer anciens tours
print("Suppression des anciens tours...")
for tid in OLD_IDS:
    r = s_komoot.delete(f"https://api.komoot.de/v007/tours/{tid}/")
    print(f"  {tid} -> {r.status_code}")
    if r.status_code == 401:
        print("JWT expire.")
        exit(1)

# 2. Générer + uploader
print("\nGeneration des routes avec waypoints cibles...\n")
new_links = []

for stage in STAGES:
    name  = stage["name"]
    start = stage["start"]
    end   = stage["end"]
    target = stage["target"]
    current = stage["brouter_direct"]

    wp = perpendicular_waypoint(start, end, current, target)
    print(f"-> {name}  (cible {target} km)")
    print(f"   waypoint intermediaire: lat={wp[0]:.4f} lng={wp[1]:.4f}")

    gpx = get_brouter_gpx([start, wp, end], name)
    km  = get_gpx_distance(gpx)
    print(f"   distance Brouter: {km} km  (cible: {target} km)")

    gpx_file = GPX_DIR / f"{name.replace(' ', '_')}.gpx"
    gpx_file.write_text(gpx, encoding="utf-8")

    r = s_komoot.post(
        "https://api.komoot.de/v007/tours/",
        params={"data_type": "gpx", "sport": "racebike"},
        data=gpx.encode("utf-8"),
        headers={"Content-Type": "application/octet-stream"},
    )
    if not r.ok:
        print(f"   Komoot FAIL {r.status_code}: {r.text[:100]}")
        continue

    d = r.json()
    tid = d["id"]
    s_komoot.patch(f"https://api.komoot.de/v007/tours/{tid}/",
                   data=json.dumps({"status": "public"}),
                   headers={"Content-Type": "application/json"})
    url = f"https://www.komoot.com/tour/{tid}"
    new_links.append((name, tid, km, url))
    print(f"   Komoot: {url}\n")
    time.sleep(0.5)

print("=== LIENS KOMOOT ===")
for name, tid, km, url in new_links:
    print(f"{name} (~{km} km): {url}")
