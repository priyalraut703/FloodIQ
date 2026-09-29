import numpy as np
from backend.utils.data_loader import load_wards_data


def generate_alerts():
    """
    Generate flood alerts for high-risk wards.
    """

    wards_df = load_wards_data()

    high_risk = wards_df[wards_df["risk_level"] == "HIGH"].head(15)

    severities = ["CRITICAL", "HIGH", "MODERATE"]

    advisories = [
        ["Evacuate low-lying areas", "Close road underpasses", "Deploy rescue teams"],
        ["Avoid travel", "Move vehicles to higher ground", "Stock emergency supplies"],
        ["Monitor water levels", "Clear drain outlets", "Stay indoors"],
    ]

    alerts = []

    rng = np.random.RandomState(7)

    for i, (_, row) in enumerate(high_risk.iterrows()):

        severity_index = i % 3

        alerts.append({
            "alert_id": f"ALT{i+1:03d}",
            "ward_name": row["ward_name"],
            "severity": severities[severity_index],
            "expected_depth": round(float(rng.uniform(0.3, 1.2)), 1),
            "eta_hours": int(rng.randint(1, 6)),
            "population_at_risk": int(row["population"]),
            "advisories": advisories[severity_index],
            "rainfall": int(row["rainfall"]),
        })

    return alerts