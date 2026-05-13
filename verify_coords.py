#!/usr/bin/env python
# Verify the waypoint coordinates match the journey
waypoints = [
    (48.1173, -1.6778),  # Should be Rennes
    (48.7444, -0.5733),  # Should be Flers
    (49.4432,  1.0993),  # Should be Rouen
    (49.8941,  2.2957),  # Should be Amiens
    (50.3578,  3.5237),  # Should be Valenciennes
    (50.8503,  4.3517),  # Should be Bruxelles
]

cities_approx = {
    "Rennes": (48.1113, -1.6800),
    "Flers": (48.7441, -0.5747),
    "Rouen": (49.4432, 1.0993),
    "Amiens": (49.8941, 2.2957),
    "Valenciennes": (50.3587, 3.5239),
    "Bruxelles": (50.8503, 4.3517),
}

print("Waypoint verification:")
cities = ["Rennes", "Flers", "Rouen", "Amiens", "Valenciennes", "Bruxelles"]
for i, (city, wp) in enumerate(zip(cities, waypoints)):
    approx = cities_approx[city]
    diff_lat = abs(wp[0] - approx[0])
    diff_lon = abs(wp[1] - approx[1])
    status = "OK" if diff_lat < 0.01 and diff_lon < 0.01 else "CHECK"
    print(f"{i+1}. {city:15} | wp: ({wp[0]:8.4f}, {wp[1]:8.4f}) | approx: ({approx[0]:8.4f}, {approx[1]:8.4f}) | {status}")
