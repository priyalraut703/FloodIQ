import os
from flask import Flask, render_template, jsonify, request
from backend.config import Config, BASE_DIR
from backend.routes.prediction_routes import prediction_bp
from backend.routes.analytics_routes import analytics_bp
from backend.routes.simulation_routes import simulation_bp
from backend.services import data_service as ds, zone_service as zs
from backend.services.alert_service import generate_alerts
from backend.services.forecast_service import get_forecast

app = Flask(__name__, template_folder=os.path.join(BASE_DIR, "frontend", "templates"),
            static_folder=os.path.join(BASE_DIR, "frontend", "static"))
app.config.from_object(Config)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0   # never serve stale JS/CSS
import time
ASSET_V = int(time.time())

@app.context_processor
def inject_asset_version():
    return {"asset_v": ASSET_V}
for bp in (prediction_bp, analytics_bp, simulation_bp):
    app.register_blueprint(bp, url_prefix="/api")

if not (os.path.exists(Config.WARDS_CSV) and os.path.exists(Config.HOTSPOTS_CSV)):
    from backend.utils.build_data import build; build()

def stats(w=None):
    _, h = ds.get_all_data()
    return ds.summary(w if w is not None else ds.wards_at(), h)

def page(tpl, key, with_stats=True):
    return render_template(tpl, active=key, **({"stats": stats()} if with_stats else {}))

@app.route("/")
def dashboard(): return page("index.html", "dashboard")
@app.route("/prediction")
def prediction(): return page("prediction.html", "prediction")
@app.route("/simulation")
def simulation(): return page("simulation.html", "simulation", False)
@app.route("/analytics")
def analytics(): return page("analytics.html", "analytics")
@app.route("/resources")
def resources(): return page("resources.html", "resources", False)
@app.route("/alerts")
def alerts(): return page("alerts.html", "alerts", False)
@app.route("/warnings")
def warnings(): return page("warnings.html", "warnings", False)
@app.route("/settings")
def settings(): return page("settings.html", "settings", False)

@app.route("/api/wards")
def api_wards():
    w = ds.wards_at(request.args.get("rainfall", type=float))
    return jsonify({"wards": w.fillna("").to_dict(orient="records"), "stats": stats(w)})

@app.route("/api/hotspots")
def api_hotspots():
    _, h = ds.get_all_data()
    r = request.args.get("risk", "ALL")
    if r != "ALL": h = h[h.flood_risk_level == r]
    return jsonify({"hotspots": h.to_dict(orient="records"), "count": len(h)})

@app.route("/api/resources")
def api_resources():
    out = []
    for _, r in ds.wards_at().iterrows():
        if r.risk_level == "LOW": continue
        p, t, b = (3, 2, 1) if r.risk_level == "HIGH" else (2, 1, 0)
        out.append({"ward_id": r.ward_id, "ward_name": r.ward_name, "zone": r.zone, "risk_level": r.risk_level,
                    "pumps": p, "teams": t, "boats": b, "population": int(r.population),
                    "readiness_score": float(r.readiness_score)})
    return jsonify({"resources": out})

@app.route("/api/alerts")
def api_alerts():
    a = generate_alerts(); return jsonify({"alerts": a, "total": len(a)})

@app.route("/api/forecast")
def api_forecast():
    f = get_forecast(); return jsonify(f or {"error": "forecast unavailable"}), (200 if f else 503)

@app.route("/api/zone-alerts")
def api_zone_alerts():
    return jsonify(zs.zone_alerts(request.args.get("rain", type=float)))

@app.route("/api/citizen")
def api_citizen():
    r = zs.citizen_view(request.args.get("area", ""), request.args.get("rain", type=float))
    return (jsonify(r), 200) if r else (jsonify(error="Area not found"), 404)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=Config.DEBUG)
