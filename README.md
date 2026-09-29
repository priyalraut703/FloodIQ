🌊 FloodIQ Nagpur

Flood-prone area prediction and zone-wise early warnings for Nagpur, Maharashtra.

FloodIQ combines rainfall, terrain, and historical flood records to predict which parts of Nagpur are likely to flood, then turns that prediction into colour-coded, zone-wise warnings that both citizens and authorities can act on.

Status: hackathon prototype. Flood events and NMC zone names come from public reports. Several inputs (coordinates, elevation, drainage, population) are approximate placeholders. See Data & honesty notes.

📌 Problem Statement

Predict flood-prone locations using rainfall, terrain and historical data, and issue timely, zone-wise warnings to citizens and authorities. The solution should present risk information in an actionable and easy-to-understand manner.

How this project answers it
Requirement	How FloodIQ addresses it
Predict flood-prone locations	Risk model over 32 Nagpur localities using rainfall, elevation, drain capacity, distance to river and past flood events
Rainfall	Live 24 h forecast from Open-Meteo, or a manual "what-if" rainfall value (slider / input)
Terrain	Elevation and distance to the Nag/Pili river are model features
Historical data	Documented floods (Sept 2023 Nag river flood, July 2025 waterlogging) used as a history feature and as validation
Timely warnings	Warnings are recomputed from rainfall on every request and show the expected peak-rain time window
Zone-wise	Localities grouped into the 10 NMC zones, each with its own severity level
Citizens and authorities	Separate Citizen view (plain-language advice, Hindi + English) and Authority view (actions, population at risk)
Actionable and easy to understand	IMD-style RED / ORANGE / YELLOW / GREEN colours, short to-do lists, emergency numbers, maps and charts
✨ Features
Zone Warnings page with two tabs:
Authority view: every NMC zone ranked by severity, with high/medium locality counts, people at risk, localities to watch, and recommended actions.
Citizen view: pick your area and get a large risk card, what to do, Hindi advice, and that area's flood history.
Live rainfall input: pulls the next-24 h forecast for Nagpur and finds the peak-rain hour. If the forecast is unavailable, the app falls back to a manual/default scenario and says so on screen.
Interactive dashboard: hotspot and locality map with clustering, a rainfall slider (10 to 250 mm) that recomputes risk live, risk distribution chart, top-risk localities.
Flood prediction tool: enter rainfall, elevation, drain capacity, river distance and past events to get a predicted risk level with model confidence.
Simulation: animated flood-spread view over high-risk localities at 0/30/60/90 minutes (illustrative).
Analytics: risk distribution, zone-wise risk counts, top-rainfall localities, readiness scores, monthly rainfall pattern.
Resources: suggested pumps, teams and boats per at-risk locality.
Alerts: advisory cards for high-risk localities.
Light/dark theme, responsive layout.
🧠 How It Works
Rainfallforecast or manual
Risk enginebackend/risk.py
Terrainelevation, river distance,drainage
Historydocumented past floods
Per-locality riskHIGH / MEDIUM / LOW
Group by NMC zone
Zone severityRED / ORANGE / YELLOW /GREEN
Authority viewactions + people at risk
Citizen viewadvice + Hindi + emergencynumbers
1. Risk score

A single function, backend/risk.py, is the one source of truth used by the data builder, model training and every API.

score = 0.35 × rainfall factor      (24 h rain / 150 mm, capped)
      + 0.20 × low-elevation factor (lower ground = higher risk)
      + 0.20 × (1 − drain capacity)
      + 0.15 × river-proximity factor
      + 0.10 × flood-history factor (documented past events, up to 3)
Score	Risk level
> 0.55	HIGH
> 0.42	MEDIUM
otherwise	LOW
2. Machine-learning model

A Random Forest classifier (scikit-learn, 150 trees) is trained on 4,000 sampled scenarios over the five features: rainfall, elevation, drain_capacity, river_dist_km, past_events. It powers the /api/predict endpoint and returns a risk level and confidence. Held-out accuracy against the rule-based labels is about 92%.

The model learns the risk formula, so that 92% shows it reproduces the formula, not that it predicts real floods. The real check is the historical validation below.

3. Zone severity (IMD-style colours)
Colour	Rule (per NMC zone)	Meaning
🔴 RED	3 or more HIGH-risk localities	Immediate action
🟠 ORANGE	1 to 2 HIGH-risk localities	Be prepared
🟡 YELLOW	No HIGH but at least 1 MEDIUM	Stay alert
🟢 GREEN	Everything LOW	Normal

Each level carries a tailored citizen advice list, an authority action list and a Hindi message.

4. Timely warnings

/api/zone-alerts resolves the rainfall in this order: manual value (if given), then live Open-Meteo forecast (next 24 h total plus peak hour), then default scenario (80 mm). The response always reports which source was used and a time window, for example "Peak rain expected around 17:00 IST (12.4 mm/hr)".

5. Validation against real events

The Sept 2023 Nagpur flood (about 109 mm rain, Nag river overflow) is the reference case. At 110 mm/day, the model rates 12 of 16 documented flood spots as HIGH without forcing them, and at 15 mm/day no zone reaches RED or ORANGE. This is enforced by automated tests (tests/).

🛠️ Tech Stack
Layer	Technology
Backend	Python 3.10+, Flask, Gunicorn
ML / data	scikit-learn (Random Forest), pandas, NumPy, joblib
Frontend	HTML, CSS, vanilla JavaScript, Jinja2 templates
Maps and charts	Leaflet + MarkerCluster, OpenStreetMap tiles (no API key), Chart.js
Rainfall data	Open-Meteo forecast API (free, no key)
Testing	pytest
Deployment	Render (render.yaml, Procfile)
📁 Project Structure
Flood-Management/
├── backend/
│   ├── app.py                  # Flask app: pages + API routes
│   ├── config.py               # City centre, paths, defaults
│   ├── risk.py                 # ★ Shared risk formula (single source of truth)
│   ├── models/
│   │   ├── train_model.py      # Trains the Random Forest
│   │   └── flood_model.pkl     # Trained model (auto-retrained if missing)
│   ├── routes/                 # Blueprints: predict, analytics, simulation
│   ├── services/
│   │   ├── zone_service.py     # ★ Zone-wise warnings + citizen view
│   │   ├── forecast_service.py # ★ Open-Meteo rainfall forecast
│   │   ├── data_service.py     # Loads wards, recomputes risk for any rainfall
│   │   ├── prediction_service.py
│   │   └── alert_service.py
│   └── utils/
│       ├── build_data.py       # Builds the Nagpur dataset
│       ├── data_loader.py
│       └── model_loader.py     # Lazy, cached model loading
├── data/
│   ├── wards_data.csv          # 32 Nagpur localities
│   └── hotspot_data.csv        # 16 documented flood hotspots
├── frontend/
│   ├── templates/              # base, dashboard, prediction, simulation,
│   │                           # analytics, resources, alerts, warnings, settings
│   └── static/                 # css, js, images
├── tests/test_predictions.py   # 22 tests
├── requirements.txt
├── render.yaml  Procfile       # Deployment config
└── README.md
🚀 Getting Started
Prerequisites
Python 3.10 or newer (python --version)
Internet connection (map tiles, charts and forecast load from the web)
Install and run
bash
git clone https://github.com/Therock1037X/Flood-Management.git
cd Flood-Management

# optional but recommended
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
python -m backend.app

Open http://localhost:5000. Zone warnings are at http://localhost:5000/warnings.

Use python -m backend.app, not python backend/app.py, otherwise imports fail.

To use a different port: PORT=5001 python -m backend.app (Windows: set PORT=5001 first).

Quick demo
Open Zone Warnings, enter 110 mm and press Apply. Dharampeth and Dhantoli go RED (a Sept 2023-like event).
Enter 15 mm. Most zones drop to YELLOW/GREEN.
Switch to Citizen view, pick Ambazari, and read the advice and flood history.
On the Dashboard, drag the rainfall slider and watch the map and risk chart update.
Useful commands
bash
pytest                                  # run all tests
python -m backend.utils.build_data      # regenerate the dataset
python -m backend.models.train_model    # retrain the model
🔌 API Reference
Method	Endpoint	Description
GET	/api/zone-alerts?rain=<mm>	Zone-wise warnings. rain optional; otherwise uses live forecast
GET	/api/citizen?area=<name>&rain=<mm>	Plain-language risk and advice for one locality
GET	/api/forecast	Next-24 h rainfall for Nagpur (503 if unavailable)
GET	/api/wards?rainfall=<mm>	All localities with risk recomputed for that rainfall, plus summary stats
GET	/api/hotspots?risk=ALL|HIGH|MEDIUM|LOW	Documented flood hotspots
POST	/api/predict	Predict risk from inputs (below)
GET	/api/analytics	Charts data: risk and zone distribution, top rainfall, readiness
GET	/api/simulation	Time-stepped flood-spread points
GET	/api/resources	Suggested pumps/teams/boats per at-risk locality
GET	/api/alerts	Advisory cards for high-risk localities

Example

bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"rainfall":110,"elevation":306,"drain_capacity":0.4,"river_dist_km":0.3,"past_events":1}'
# {"confidence":0.973,"risk_level":"HIGH"}

Invalid input returns 400 with an error message.

🗂️ Data & Honesty Notes
Item	Status
NMC zone names (10 zones)	✅ Real
Flood events: Sept 2023 Nag river flood, July 2025 waterlogging	✅ Real, from news and public reports
Named waterlogging spots (Ambazari, Sitabuldi, Manish Nagar, Lakadganj, etc.)	✅ Real localities
Coordinates, distance to river	⚠️ Approximate
Zone assigned to each locality	⚠️ Approximate, verify against the NMC ward map
Elevation, drain capacity, population, readiness	⚠️ Illustrative placeholders
Monthly rainfall chart	⚠️ Approximate climatological values
Simulation	⚠️ Illustrative, not a hydrological model

To make this production-grade, replace the placeholders with NMC ward boundaries and population, an SRTM/Copernicus elevation model, the NMC drainage survey, and a longer flood-incident history. The schema in data/wards_data.csv and backend/utils/build_data.py is designed for this swap.

🧪 Testing

pytest runs 22 tests covering:

Historical validation (most documented flood spots are HIGH at 2023-like rainfall)
Light rain produces no HIGH/RED conditions; heavy rain produces a RED zone
Input validation on /api/predict
Every page returns 200
Every JSON API returns strict valid JSON (no NaN)
☁️ Deployment (Render)
Push the repo to GitHub.
On render.com choose New → Web Service and connect the repo.
Build command: pip install -r requirements.txt
Start command: gunicorn backend.app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 60
Set env var PYTHON_VERSION=3.11.9.

render.yaml and Procfile already contain this config. Free instances sleep after about 15 minutes of inactivity, so open the link once before a demo.

⚠️ Limitations
The model is trained on a rule-based score, so it is a decision-support tool, not an official forecast.
Rainfall is city-wide; there is no per-locality rainfall or radar data yet.
No live river-level, lake-level or drain-blockage sensing.
Warnings are displayed only in the app. No SMS/WhatsApp/Telegram delivery yet.
Hindi and English only. No Marathi text yet.
Warnings are not an official IMD or NMC advisory. In an emergency, call 112 (police), 101 (fire) or 108 (ambulance).
🗺️ Roadmap
 Replace placeholder data with NMC ward boundaries, DEM elevation and drainage survey
 Add more historical events (2019, 2020 and other years) and train on real flood incidents
 Alert delivery via Telegram / SMS / WhatsApp
 Marathi language support
 Add the NMC control-room number and shelter locations
 Live lake and river level integration (Ambazari, Futala, Nag river)
 Ward-level rainfall from radar or gauge data
👥 Team

Add your team name, members and college here.

🙏 Acknowledgements
Flood event details: public reports on the 2023 Nagpur flood and July 2025 waterlogging coverage
Open-Meteo for the free forecast API
OpenStreetMap contributors, Leaflet, Chart.js