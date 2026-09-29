import numpy as np
from backend.utils.model_loader import load_model

def predict_flood_risk(rainfall, elevation, drain_capacity, river_dist_km=1.0, past_events=0):
    model, enc = load_model()
    X = np.array([[rainfall, elevation, drain_capacity, river_dist_km, past_events]])
    return {"risk_level": str(enc.inverse_transform(model.predict(X))[0]),
            "confidence": round(float(model.predict_proba(X).max()), 3)}
