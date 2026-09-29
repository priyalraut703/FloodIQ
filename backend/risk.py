"""Single source of truth for flood risk (data builder, model training, API all use this)."""
import numpy as np

FEATURES = ["rainfall", "elevation", "drain_capacity", "river_dist_km", "past_events"]

def risk_score(rain, elev, drain, river_km, past):
    rain_n = np.minimum(np.asarray(rain, float) / 150.0, 1.2)
    low = np.clip((330 - np.asarray(elev, float)) / 40.0, 0, 1)
    riv = np.clip(1 - np.asarray(river_km, float) / 3.0, 0, 1)
    hist = np.minimum(np.asarray(past, float), 3) / 3.0
    return 0.35 * rain_n + 0.20 * low + 0.20 * (1 - np.asarray(drain, float)) + 0.15 * riv + 0.10 * hist

def label(score):
    return "HIGH" if score > 0.55 else "MEDIUM" if score > 0.42 else "LOW"
