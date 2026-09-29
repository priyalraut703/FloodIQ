import pandas as pd
from backend.config import Config


def load_wards_data():
    """
    Load wards dataset.
    """
    return pd.read_csv(Config.WARDS_CSV)


def load_hotspots_data():
    """
    Load hotspot dataset.
    """
    return pd.read_csv(Config.HOTSPOTS_CSV)


def load_all_data():
    """
    Load both datasets at once.
    """
    wards = load_wards_data()
    hotspots = load_hotspots_data()

    return wards, hotspots