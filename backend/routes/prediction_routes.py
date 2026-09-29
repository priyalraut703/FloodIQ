from flask import Blueprint, request, jsonify
from backend.services.prediction_service import predict_flood_risk

prediction_bp = Blueprint("prediction", __name__)

@prediction_bp.route("/predict", methods=["POST"])
def predict():
    d = request.get_json(silent=True)
    if not isinstance(d, dict):
        return jsonify(error="Send a JSON object"), 400
    try:
        r = predict_flood_risk(float(d.get("rainfall", 80)), float(d.get("elevation", 310)),
                               float(d.get("drain_capacity", 0.6)), float(d.get("river_dist_km", 1.0)),
                               float(d.get("past_events", 0)))
    except (TypeError, ValueError):
        return jsonify(error="All inputs must be numbers"), 400
    return jsonify(r)
