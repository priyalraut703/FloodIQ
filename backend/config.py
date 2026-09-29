import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-change-me")
    DEBUG = os.environ.get("FLASK_DEBUG") == "1"
    CITY = "Nagpur"
    CENTER_LAT, CENTER_LNG = 21.1458, 79.0882
    DEFAULT_RAIN_MM = 80            # 24h design-storm used when no forecast is available
    DATA_DIR = os.path.join(BASE_DIR, "data")
    MODEL_DIR = os.path.join(BASE_DIR, "backend", "models")
    WARDS_CSV = os.path.join(DATA_DIR, "wards_data.csv")
    HOTSPOTS_CSV = os.path.join(DATA_DIR, "hotspot_data.csv")
    MODEL_PATH = os.path.join(MODEL_DIR, "flood_model.pkl")
    SIMULATION_STEPS = [0, 30, 60, 90]
