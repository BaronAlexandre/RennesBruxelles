import math
import requests
import sys

USER_ID = "5602835891342"

JWT = (
    "eyJ4NXQjUzI1NiI6InlIQ2xZdUdwWlNvU2c3dkhrT1k4YzYyR2NGdGxSeV9neEpIYkJfNFpjamsi"
    "LCJraWQiOiJqd3QtMjAyNTAyMTEiLCJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJydGkiOiJi"
    "ZmEzOGJmYzU2MDQ4YzI1OWI2MjMyNWY4NTJiYjQwMjIwZmNhZmMyOWU4NmU4NjA4OWE1MjYzYzI4"
    "YzNjMTAxIiwidXNlcl9uYW1lIjoiNTYwMjgzNTg5MTM0MiIsInNjb3BlIjpbInVzZXIuKiJdLCJleH"
    "AiOjE3Nzc3NTc2OTksImlhdCI6MTc3Nzc1NTg5OSwianRpIjoiMGIxOTkwN2YtYmE2Ny00MGU0LTg2"
    "NWQtMGIzZDViMWY3MjViIiwiY2xpZW50X2lkIjoia29tb290LXdlYiIsInVzZXJuYW1lIjoiNTYwMjgz"
    "NTg5MTM0MiJ9.Kl_LNS9IT7I8J3FNZskv4qmTMhOcTvBEhOU6n-4AXCSrO-0sHFnelbRPnNudlMm6"
    "VPSxPlaiY7JQ89pNmuWWPD9FRgVbhgrdGx53rhvKwHMRm13cxmgcyPHYGhhNXXVKqsPqox7WfKNOZ-"
    "OJsrWgW2RERzRS-t5HxjQIWWVn_PtsXsrlQ6ClmPkY7a-JcbgSXKB-eFIG8Aw18X1Vb3-XqkFnuZ7"
    "u9ftKIGfZsotmllH61T-5wNBQ02mDu1nHbiUwy-4bJvxF81DlY-DEaLmfhg8TCRyQuaEx9mDqbtGGI"
    "SD3qBaYVhJtxKbv_vg-YqMOHltrkCxF5MoLqMeGDrtU8w"
)

COOKIES = {
    "koa_at":       f"{USER_ID}%7C{JWT}%7C1777757639",
    "koa_rt":       f"{USER_ID}%7C%2F{USER_ID}%2Fkomoot-web%2F318e1cc1-26a4-43a7-99aa-f5d94dfb0b3f%7C1809291899",
    "koa_re":       "1809291899",
    "koa_ae":       "1777757639",
    "kmt_sess":     "eyJsYW5nIjoiZW4iLCJtZXRyaWMiOnRydWUsInByb2ZpbGUiOnsidXNlcm5hbWUiOiI1NjAyODM1ODkxMzQyIiwibG9jYWxlIjoiZW5fRlIiLCJtZXRyaWMiOnRydWV9fQ==",
    "kmt_sess.sig": "GqvetiOyVCSuzDQjJIk2jURXlOg",
}

STAGES = [
    {"name": "J1 - Rennes Flers",          "start": (48.1173, -1.6778), "end": (48.7484, -0.5721)},
    {"name": "J2 - Flers Rouen",            "start": (48.7484, -0.5721), "end": (49.4432,  1.0993)},
    {"name": "J3 - Rouen Amiens",           "start": (49.4432,  1.0993), "end": (49.8942,  2.2957)},
    {"name": "J4 - Amiens Valenciennes",    "start": (49.8942,  2.2957), "end": (50.3576,  3.5238)},
    {"name": "J5 - Valenciennes Bruxelles", "start": (50.3576,  3.5238), "end": (50.8503,  4.3517)},
]


def haversine(a, b):
    R = 6371
    lat1, lon1 = math.radians(a[1]), math.radians(a[0])
    lat2, lon2 = math.radians(b[1]), math.radians(b[0])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    h = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    return 2 * R * math.asin(math.sqrt(h))


def find_midpoint(coords):
    total = sum(haversine(coords[i], coords[i+1]) for i in range(len(coords) - 1))
    target, cumul = total / 2, 0
    for i in range(len(coords) - 1):
        d = haversine(coords[i], coords[i+1])
        if cumul + d >= target:
            return coords[i]
        cumul += d
    return coords[-1]


def reverse_geocode(lng, lat):
    r = requests.get(
        "https://nominatim.openstreetmap.org/reverse",
        params={"lat": lat, "lon": lng, "format": "json", "zoom": 10},
        headers={"User-Agent": "RennesBruxellesVelo/1.0"},
    )
    r.raise_for_status()
    addr = r.json().get("address", {})
    return addr.get("city") or addr.get("town") or addr.get("village") or addr.get("hamlet") or "?"


def get_osrm_route(start, end):
    url = (
        f"http://router.project-osrm.org/route/v1/cycling/"
        f"{start[1]},{start[0]};{end[1]},{end[0]}"
    )
    r = requests.get(url, params={"overview": "full", "geometries": "geojson"})
    r.raise_for_status()
    coords = r.json()["routes"][0]["geometry"]["coordinates"]  # [[lng, lat], ...]
    return coords


def to_gpx(name, coords):
    # Format trk (track) — plus largement accepte que rte
    points = "\n".join(
        f'      <trkpt lat="{lat}" lon="{lng}"/>'
        for lng, lat in coords
    )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<gpx version="1.1" creator="RennesBruxelles">\n'
        "  <trk>\n"
        f"    <name>{name}</name>\n"
        "    <trkseg>\n"
        f"{points}\n"
        "    </trkseg>\n"
        "  </trk>\n"
        "</gpx>"
    )


def make_session():
    s = requests.Session()
    s.headers.update({
        "Authorization": f"Bearer {JWT}",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X) AppleWebKit/605.1.15",
    })
    s.cookies.update(COOKIES)
    return s


def upload_gpx(name, gpx_content):
    s = make_session()
    gpx_bytes = gpx_content.encode("utf-8")

    for url in [
        "https://external-api.komoot.de/v007/tours/",
        f"https://www.komoot.com/api/v007/tours/",
        f"https://api.komoot.de/v007/users/{USER_ID}/tours/",
    ]:
        r = s.post(
            url,
            params={"data_type": "gpx", "sport": "racebike"},
            data=gpx_bytes,
            headers={"Content-Type": "application/octet-stream"},
        )
        print(f"   [{r.status_code}] {url} — {r.text[:200]}")
        if r.status_code in (200, 201):
            break

    if r.status_code == 401:
        print("Token expire — recharge Komoot dans le navigateur et refais Copy as cURL.")
        sys.exit(1)
    if not r.ok:
        print(f"Erreur upload {r.status_code}: {r.text[:500]}")
        sys.exit(1)

    data = r.json()
    tour_id = data.get("id") or data.get("_embedded", {}).get("tours", [{}])[0].get("id")
    return tour_id


def main():
    print("Creation des 5 routes Komoot via GPX upload...\n")
    links = []

    for stage in STAGES:
        print(f"-> {stage['name']}...")
        coords = get_osrm_route(stage["start"], stage["end"])
        print(f"   {len(coords)} points OSRM")
        gpx = to_gpx(stage["name"], coords)
        tour_id = upload_gpx(stage["name"], gpx)
        url = f"https://www.komoot.com/tour/{tour_id}"
        links.append((stage["name"], url))
        print(f"   {url}")

    print("\n=== LIENS ===")
    for name, url in links:
        print(f"{name}: {url}")


if __name__ == "__main__":
    main()
