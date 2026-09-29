import pandas as pd
from flask import Blueprint, jsonify
from backend.services.data_service import get_all_data

analytics_bp = Blueprint("analytics", __name__)

@analytics_bp.route("/analytics", methods=["GET"])
def get_analytics():

    wards_df, hotspots_df = get_all_data()

    # Risk distribution
    risk_counts = wards_df["risk_level"].value_counts().to_dict()

    # Top rainfall wards
    top_wards = wards_df.nlargest(
        10, "rainfall"
    )[["ward_name","rainfall","risk_level","population"]].to_dict(orient="records")

    # Readiness distribution
    readiness_bins = {"0-0.4":0,"0.4-0.6":0,"0.6-0.8":0,"0.8-1.0":0}

    for v in wards_df["readiness_score"]:
        if v < 0.4:
            readiness_bins["0-0.4"] += 1
        elif v < 0.6:
            readiness_bins["0.4-0.6"] += 1
        elif v < 0.8:
            readiness_bins["0.6-0.8"] += 1
        else:
            readiness_bins["0.8-1.0"] += 1

    # Approx. Nagpur monthly rainfall normals (mm); flood_events = documented major events only (Sep 2023, Jul 2025)
    months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

    monthly_trend = {
        "months": months,
        "rainfall": [14,21,22,12,21,172,384,285,195,68,20,12],
        "flood_events": [0,0,0,0,0,0,1,0,1,0,0,0]
    }

    return jsonify({
        "risk_distribution": risk_counts,
        "top_rainfall_wards": top_wards,
        "readiness_distribution": readiness_bins,
        "monthly_trend": monthly_trend,
        "zone_distribution": pd.crosstab(wards_df["zone"], wards_df["risk_level"]).reindex(columns=["HIGH","MEDIUM","LOW"], fill_value=0).astype(int).to_dict(orient="index"),
        "total_population_at_risk": int(
            wards_df[wards_df["risk_level"]=="HIGH"]["population"].sum()
        ),
        "avg_drain_capacity": round(float(wards_df["drain_capacity"].mean()),3)
    })