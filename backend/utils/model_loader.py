import os, joblib
from functools import lru_cache
from backend.config import Config

@lru_cache(maxsize=1)
def load_model():
    """Lazy + cached; trains automatically if the pickle is missing or incompatible."""
    try:
        d = joblib.load(Config.MODEL_PATH)
    except Exception:
        from backend.models.train_model import train_model
        return train_model()
    return d["model"], d["encoder"]
