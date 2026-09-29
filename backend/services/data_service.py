import numpy as np
from backend.risk import risk_score, label
from backend.utils.data_loader import load_all_data

def wards_at(rain_mm=None):
    """Wards with risk recomputed for a given 24h rainfall (mm)."""
    w, _ = load_all_data()
    if rain_mm is not None:
        w = w.copy(); w["rainfall"] = rain_mm
        w["risk_level"] = [label(risk_score(r.rainfall, r.elevation, r.drain_capacity, r.river_dist_km, r.past_events))
                           for r in w.itertuples()]
    return w

def get_all_data():
    return load_all_data()

def summary(w, hotspots):
    hi = w[w.risk_level == "HIGH"]
    return {"total_wards": len(w), "high_risk": len(hi), "medium_risk": int((w.risk_level == "MEDIUM").sum()),
            "low_risk": int((w.risk_level == "LOW").sum()), "affected_population": int(hi.population.sum()),
            "avg_rainfall": int(w.rainfall.mean()), "total_hotspots": len(hotspots)}
