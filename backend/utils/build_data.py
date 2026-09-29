"""Builds Nagpur ward/hotspot CSVs. Run: python -m backend.utils.build_data
Localities, NMC zones and flood events are taken from public reports (Sep 2023 Nag river flood,
Jul 2025 waterlogging). Coordinates, elevation, drainage and population are APPROXIMATE/illustrative
- replace with NMC ward data, a DEM (SRTM/Copernicus) and NMC drain survey when available."""
import numpy as np, pandas as pd
from backend.config import Config
from backend.risk import risk_score, label

# name, NMC zone, lat, lng, distance to Nag/Pili river (km, approx), documented events, event note
L = [
 ("Ambazari","Dharampeth",21.1290,79.0450,0.3,1,"Sep 2023 flood; lake overflow"),
 ("Sitabuldi","Dhantoli",21.1458,79.0882,0.5,2,"Sep 2023 flood; Jul 2025 underpass"),
 ("Mor Bhavan","Dhantoli",21.1430,79.0850,0.4,1,"Sep 2023 flood"),
 ("Variety Chowk","Dhantoli",21.1440,79.0870,0.4,1,"Sep 2023 flood"),
 ("Panchsheel Square","Dharampeth",21.1380,79.0700,0.2,1,"Sep 2023 Nag river"),
 ("Manish Nagar","Hanuman Nagar",21.0960,79.0640,0.8,1,"Jul 2025 underpass"),
 ("Narendra Nagar","Hanuman Nagar",21.1030,79.0870,0.9,1,"Jul 2025 underpass"),
 ("Somalwada","Dharampeth",21.1000,79.0650,0.9,1,"Jul 2025 underpass"),
 ("Lakadganj","Lakadganj",21.1310,79.1180,0.7,1,"Jul 2025 underpass"),
 ("New Narsala","Ashi Nagar",21.1750,79.1250,1.5,1,"Jul 2025 waist-deep water"),
 ("Bajaj Nagar","Dharampeth",21.1250,79.0600,0.6,1,"Jul 2025 waterlogging"),
 ("Shankar Nagar","Dharampeth",21.1330,79.0650,0.5,1,"Jul 2025 waterlogging"),
 ("Khamla","Laxmi Nagar",21.1150,79.0700,1.0,1,"Jul 2025 waterlogging"),
 ("Pratap Nagar","Laxmi Nagar",21.1170,79.0680,1.0,1,"Jul 2025 waterlogging"),
 ("Medical Square","Lakadganj",21.1180,79.1010,0.9,1,"Jul 2025 waterlogging"),
 ("Manewada","Hanuman Nagar",21.0900,79.1130,1.4,1,"Jul 2025 waterlogging"),
 ("Dhantoli","Dhantoli",21.1330,79.0800,0.9,0,""),("Civil Lines","Dhantoli",21.1560,79.0800,1.8,0,""),
 ("Sadar","Dhantoli",21.1650,79.0930,2.0,0,""),("Mangalwari","Mangalwari",21.1620,79.0620,1.6,0,""),
 ("Itwari","Gandhibagh",21.1500,79.1130,0.6,0,""),("Gandhibagh","Gandhibagh",21.1490,79.1050,0.7,0,""),
 ("Mahal","Gandhibagh",21.1450,79.1000,0.6,0,""),("Sakkardara","Laxmi Nagar",21.1160,79.1250,1.8,0,""),
 ("Nandanvan","Satranjipura",21.1250,79.1200,1.2,0,""),("Wardhaman Nagar","Satranjipura",21.1330,79.1300,1.5,0,""),
 ("Trimurti Nagar","Laxmi Nagar",21.1050,79.0500,1.6,0,""),("Hingna Road","Nehru Nagar",21.1000,79.0000,2.6,0,""),
 ("Wadi","Nehru Nagar",21.1800,79.0300,2.8,0,""),("Besa","Nehru Nagar",21.0800,79.1100,2.4,0,""),
 ("Kamptee Road","Ashi Nagar",21.1700,79.1350,1.9,0,""),("Pardi","Ashi Nagar",21.1500,79.1600,2.7,0,""),
]

def build():
    rng = np.random.RandomState(11)
    rows = []
    for i, (n, z, la, ln, rk, ev, note) in enumerate(L):
        elev = round(305 + rk * 8 + rng.normal(0, 3), 1)
        drain = round(float(rng.uniform(0.3, 0.85)), 2)
        rows.append(dict(ward_id=f"N{i+1:03d}", ward_name=n, zone=z, latitude=la, longitude=ln,
            rainfall=Config.DEFAULT_RAIN_MM, elevation=elev, drain_capacity=drain,
            population=int(rng.randint(15000, 90000)), drain_network=int(rng.randint(5, 40)),
            emergency_resources=int(rng.randint(1, 8)), readiness_score=round(float(rng.uniform(0.3, 0.9)), 2),
            river_dist_km=rk, past_events=ev, event_note=note))
    w = pd.DataFrame(rows)
    w["risk_level"] = [label(risk_score(r.rainfall, r.elevation, r.drain_capacity, r.river_dist_km, r.past_events)) for r in w.itertuples()]
    h = w[w.past_events > 0]
    hs = pd.DataFrame({"hotspot_id": [f"HS{i+1:03d}" for i in range(len(h))], "latitude": h.latitude.values,
        "longitude": h.longitude.values, "rainfall": h.rainfall.values, "elevation": h.elevation.values,
        "drain_capacity": h.drain_capacity.values, "flood_risk_level": h.risk_level.values,
        "associated_ward": h.ward_id.values, "event": h.event_note.values})
    import os; os.makedirs(Config.DATA_DIR, exist_ok=True)
    w.to_csv(Config.WARDS_CSV, index=False); hs.to_csv(Config.HOTSPOTS_CSV, index=False)
    return w, hs

if __name__ == "__main__":
    w, h = build(); print(len(w), "localities |", len(h), "documented hotspots")
