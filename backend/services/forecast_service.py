import json, urllib.request
from backend.config import Config

URL = ("https://api.open-meteo.com/v1/forecast?latitude={}&longitude={}"
       "&hourly=precipitation&forecast_days=2&timezone=Asia%2FKolkata")

def get_forecast(timeout=4):
    """Next-24h rainfall for Nagpur from Open-Meteo. Returns None if unavailable (caller falls back)."""
    try:
        with urllib.request.urlopen(URL.format(Config.CENTER_LAT, Config.CENTER_LNG), timeout=timeout) as r:
            h = json.load(r)["hourly"]
        t, p = h["time"][:24], [x or 0 for x in h["precipitation"][:24]]
        i = max(range(len(p)), key=p.__getitem__)
        return {"source": "open-meteo", "next24_mm": round(sum(p), 1), "peak_mm_per_hr": p[i],
                "peak_time": t[i], "hourly": [{"time": a, "mm": b} for a, b in zip(t, p)]}
    except Exception:
        return None
