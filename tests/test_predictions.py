import pandas as pd, pytest
from backend.app import app
from backend.risk import risk_score, label
from backend.services.zone_service import zone_alerts, citizen_view
from backend.utils.data_loader import load_wards_data

@pytest.fixture
def client(): return app.test_client()

def test_documented_floods_recalled_at_2023_intensity():
    """~110 mm/day (Sep 2023 Nag river flood): most documented flood spots must be HIGH."""
    w = load_wards_data(); d = w[w.past_events > 0]
    hi = sum(label(risk_score(110, r.elevation, r.drain_capacity, r.river_dist_km, r.past_events)) == "HIGH" for r in d.itertuples())
    assert hi / len(d) >= 0.7

def test_light_rain_no_high_risk():
    assert all(z["high"] == 0 for z in zone_alerts(15)["zones"])

def test_heavy_rain_has_red_zone():
    assert any(z["severity"] == "RED" for z in zone_alerts(110)["zones"])

def test_citizen_unknown_area():
    assert citizen_view("nowhere") is None

def test_predict_validation(client):
    assert client.post("/api/predict", json={"rainfall": "abc"}).status_code == 400
    assert client.post("/api/predict", data="x").status_code == 400
    assert client.post("/api/predict", json={"rainfall": 110, "elevation": 306, "drain_capacity": .4, "river_dist_km": .3, "past_events": 1}).json["risk_level"] == "HIGH"

@pytest.mark.parametrize("u", ["/", "/prediction", "/simulation", "/analytics", "/resources", "/alerts", "/warnings", "/settings", "/api/zone-alerts?rain=90"])
def test_pages(client, u): assert client.get(u).status_code == 200

@pytest.mark.parametrize("u", ["/api/wards", "/api/hotspots", "/api/resources", "/api/alerts", "/api/simulation", "/api/analytics", "/api/zone-alerts?rain=110", "/api/citizen?area=ambazari"])
def test_json_is_strict(client, u):
    import json
    def bad(x): raise ValueError("NaN/Infinity in JSON: " + x)
    json.loads(client.get(u).get_data(as_text=True), parse_constant=bad)
