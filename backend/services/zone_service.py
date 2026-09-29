from backend.services.data_service import wards_at
from backend.services.forecast_service import get_forecast
from backend.config import Config

LEVELS = {  # IMD-style colour codes
 "RED":    {"citizen": ["Move to higher ground/upper floors now", "Avoid underpasses, nallahs and Nag river banks", "Keep phone charged; call 112 for rescue"],
            "authority": ["Pre-position pumps, boats and SDRF/NDRF", "Close flooded underpasses; divert traffic", "Prepare relief shelters and evacuate low-lying pockets"]},
 "ORANGE": {"citizen": ["Avoid travel through waterlogged roads/underpasses", "Move vehicles and valuables to higher ground", "Store drinking water and medicines"],
            "authority": ["Deploy dewatering pumps at known hotspots", "Clear drain inlets and river-side blockages", "Keep control room on 24x7 watch"]},
 "YELLOW": {"citizen": ["Stay alert; avoid low-lying roads if rain intensifies", "Follow NMC and IMD updates"],
            "authority": ["Inspect drains at listed hotspots", "Keep pumps on standby"]},
 "GREEN":  {"citizen": ["No action needed. Normal precautions."], "authority": ["Routine monitoring"]},
}
HINDI = {"RED": "खतरा: तुरंत ऊँचे स्थान पर जाएँ, अंडरपास/नाले से दूर रहें, मदद के लिए 112 डायल करें।",
         "ORANGE": "सावधान: जलभराव वाले रास्तों से बचें, वाहन ऊँची जगह खड़े करें।",
         "YELLOW": "सतर्क रहें: बारिश तेज़ हो तो निचले इलाकों से बचें।", "GREEN": "कोई खतरा नहीं। सामान्य सावधानी रखें।"}

def severity(w):
    h, m = (w.risk_level == "HIGH").sum(), (w.risk_level == "MEDIUM").sum()
    return "RED" if h >= 3 else "ORANGE" if h >= 1 else "YELLOW" if m >= 1 else "GREEN"

def resolve_rain(rain=None):
    if rain is not None:
        return float(rain), "manual scenario", None
    f = get_forecast()
    if f:
        return f["next24_mm"], "live forecast (Open-Meteo)", f
    return float(Config.DEFAULT_RAIN_MM), "default scenario (forecast unavailable)", None

def zone_alerts(rain=None):
    mm, source, f = resolve_rain(rain)
    w = wards_at(mm)
    window = (f"Peak rain expected around {f['peak_time'][11:16]} IST ({f['peak_mm_per_hr']} mm/hr)" if f
              else "Next 6-12 hours (scenario)")
    zones = []
    for z, g in w.groupby("zone"):
        s = severity(g); hi = g[g.risk_level == "HIGH"]
        zones.append({"zone": z, "severity": s, "high": len(hi), "medium": int((g.risk_level == "MEDIUM").sum()),
            "wards": len(g), "population_at_risk": int(hi.population.sum()),
            "top_wards": g.sort_values("risk_level", key=lambda c: c.map({"HIGH": 0, "MEDIUM": 1, "LOW": 2}))["ward_name"].head(4).tolist(),
            "citizen_advice": LEVELS[s]["citizen"], "authority_actions": LEVELS[s]["authority"], "hindi": HINDI[s]})
    order = {"RED": 0, "ORANGE": 1, "YELLOW": 2, "GREEN": 3}
    zones.sort(key=lambda z: (order[z["severity"]], -z["population_at_risk"]))
    return {"rainfall_mm_24h": mm, "rain_source": source, "window": window, "zones": zones,
            "emergency": {"Police / Emergency": "112", "Fire": "101", "Ambulance": "108"}}

def citizen_view(area, rain=None):
    mm, source, _ = resolve_rain(rain)
    w = wards_at(mm)
    m = w[w.ward_name.str.lower().str.contains(area.lower(), regex=False)]
    if m.empty:
        return None
    r = m.iloc[0]; z = w[w.zone == r.zone]; s = severity(z)
    lvl = {"HIGH": "RED", "MEDIUM": "ORANGE", "LOW": "GREEN"}[r.risk_level]
    return {"area": r.ward_name, "zone": r.zone, "risk_level": r.risk_level, "alert": lvl,
            "zone_alert": s, "rainfall_mm_24h": mm, "rain_source": source, "advice": LEVELS[lvl]["citizen"],
            "hindi": HINDI[lvl], "history": r.event_note if isinstance(r.event_note, str) else "No documented flooding on record"}
