from flask import Blueprint, jsonify
from backend.services.data_service import get_all_data

simulation_bp = Blueprint("simulation", __name__)


@simulation_bp.route("/simulation", methods=["GET"])
def simulate_flood():

    wards_df, _ = get_all_data()

    high_risk_wards = wards_df[wards_df["risk_level"] == "HIGH"].head(20)

    steps = []

    for time in [0, 30, 60, 90]:

        points = []

        for _, row in high_risk_wards.iterrows():

            intensity = min(1.0, time / 90 * 0.8 + 0.2)

            points.append({
                "lat": float(row["latitude"]),
                "lng": float(row["longitude"]),
                "ward_name": row["ward_name"],
                "radius": time * 15 + 100,
                "intensity": round(intensity, 2),
                "water_depth": round(intensity * 1.2, 2)
            })

        steps.append({
            "time_min": time,
            "points": points
        })

    return jsonify({
        "steps": steps
    })