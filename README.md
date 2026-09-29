# 🌊 FloodIQ

### AI-Powered Flood Risk Prediction & Emergency Response Control Panel

> **Predict the risk. Identify the hotspot. Trigger the response.**

FloodIQ is an AI-powered flood risk prediction and emergency response system designed to help authorities identify **flood-prone zones before conditions become critical**.

Instead of presenting flood data as a traditional analytics dashboard, FloodIQ works as a **real-time flood response control panel** that combines rainfall, terrain, historical flood patterns, and location-based factors to estimate flood risk and turn those predictions into **zone-wise, actionable warnings**.

---

## 🚨 The Problem

Flood management systems often face a critical gap between **prediction and action**.

Authorities may have access to rainfall measurements, weather forecasts, terrain information, and historical flood records, but these data points are often fragmented across different sources.

This creates three challenges:

* **Where** is the flood risk increasing?
* **How severe** could it become?
* **What action should be taken right now?**

Citizens also need warnings that are simple and location-specific rather than raw technical data.

FloodIQ addresses this gap by converting multiple environmental signals into a **single operational view for flood response**.

---

# 💡 Our Solution

FloodIQ combines multiple flood-related factors and uses a machine learning model to generate a **localized flood-risk prediction**.

### Input

🌧️ Rainfall
⛰️ Terrain / Elevation
🌊 Historical flood patterns
📍 Location-based features
🚧 Vulnerability indicators

↓

### AI Risk Engine

**Machine Learning Model**

↓

### Output

**Zone-wise Flood Risk**

🟢 Low
🟡 Moderate
🟠 High
🔴 Critical

↓

### Response Layer

🚨 Active alerts
📍 Affected zones
👥 Citizen warnings
🚑 Recommended response actions

---

# 🖥️ Flood Response Control Panel

FloodIQ is designed around a simple principle:

> **The system should not only tell authorities what is happening. It should help them decide what to do next.**

The control panel focuses on four key areas.

### 1. 🗺️ Live Risk Map

The central map provides a geographic view of flood risk.

Each zone/locality is represented using a risk level:

| Level       | Meaning              |
| ----------- | -------------------- |
| 🟢 Low      | Normal monitoring    |
| 🟡 Moderate | Increased monitoring |
| 🟠 High     | Prepare response     |
| 🔴 Critical | Immediate attention  |

Authorities can select a zone to inspect its risk factors.

---

### 2. 🚨 Active Alerts

The system highlights areas where the predicted risk has crossed predefined thresholds.

Example:

```text
🔴 CRITICAL ALERT

Zone: Zone 7
Risk Probability: 82%
Rainfall: 87 mm/hr

Expected Impact:
Potential waterlogging within 1–2 hours

Recommended Response:
→ Deploy emergency response team
→ Issue citizen warning
→ Monitor drainage points
```

---

### 3. ⚡ Response Actions

Instead of stopping at prediction, FloodIQ connects risk with operational recommendations.

Depending on severity, the system can suggest:

* Issue citizen alerts
* Deploy emergency teams
* Monitor vulnerable locations
* Prepare evacuation routes
* Inspect drainage hotspots
* Increase monitoring frequency

---

### 4. 📊 Risk Analysis

Detailed analytics remain available without overwhelming the main control panel.

For every zone, authorities can inspect:

* Rainfall contribution
* Terrain/elevation
* Historical flood occurrence
* Risk probability
* Risk trend
* Model confidence
* Contributing factors

---

# 🧠 How FloodIQ Works

```text
               DATA SOURCES
                    │
       ┌────────────┼────────────┐
       ↓            ↓            ↓
   Rainfall      Terrain      Historical
      Data         Data       Flood Data
       │            │            │
       └────────────┼────────────┘
                    ↓
             DATA PROCESSING
                    ↓
           FEATURE ENGINEERING
                    ↓
          MACHINE LEARNING MODEL
                    ↓
             RISK PREDICTION
                    ↓
          ┌─────────┴─────────┐
          ↓                   ↓
      RISK MAP           ALERT ENGINE
          │                   │
          └─────────┬─────────┘
                    ↓
            RESPONSE ACTIONS
                    ↓
       AUTHORITIES + CITIZENS
```

---

# 🤖 Machine Learning

FloodIQ uses a supervised machine learning approach to estimate flood risk from environmental and historical features.

### Example Features

```text
Rainfall intensity
Cumulative rainfall
Elevation
Slope
Historical flood frequency
Location vulnerability
Distance from drainage/water bodies
```

The model produces a risk probability which is then mapped into operational risk categories.

### Risk Classification

```text
0 – 25%     → LOW
25 – 50%    → MODERATE
50 – 75%    → HIGH
75 – 100%   → CRITICAL
```

> Thresholds can be calibrated according to the target city's historical flood characteristics and operational requirements.

---

# 📍 Nagpur Pilot

FloodIQ is initially designed around **Nagpur, Maharashtra**, making the prototype relevant to a real urban environment.

The system models flood risk at a localized level instead of treating the entire city as one uniform region.

The prototype covers:

* Multiple Nagpur localities
* 10 administrative zones
* Zone-wise risk classification
* Local rainfall conditions
* Historical flood information
* Map-based visualization

This architecture can later be extended to other cities by replacing or expanding the underlying geographic and historical datasets.

---

# 🌧️ Data Sources

FloodIQ can integrate data from multiple sources depending on availability:

### Weather

Real-time and forecast rainfall data can be obtained through weather APIs such as Open-Meteo.

### Terrain

Elevation and terrain information can be derived from digital elevation models.

### Historical Flood Data

Historical flood/waterlogging records can be used to identify recurring vulnerable locations.

### Geographic Data

Locality, zone, road, drainage, and water-body information can be incorporated to improve spatial risk estimation.

---

# 🏗️ Tech Stack

### Frontend

* HTML
* CSS
* JavaScript
* Leaflet.js
* Chart.js

### Backend

* Python
* Flask

### Machine Learning

* Scikit-learn
* Random Forest

### Data

* CSV / structured datasets
* Weather API
* Geographic data

### Maps

* Leaflet
* OpenStreetMap

---

# 📂 Project Structure

```text
FloodIQ/
│
├── app.py
│
├── model/
│   ├── flood_model.pkl
│   └── preprocessing.pkl
│
├── data/
│   ├── rainfall.csv
│   ├── flood_history.csv
│   └── locations.csv
│
├── templates/
│   ├── index.html
│   └── control_panel.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   └── js/
│       └── app.js
│
├── notebooks/
│   └── model_training.ipynb
│
├── requirements.txt
└── README.md
```

---

# ⚙️ Installation

### 1. Clone the repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd FloodIQ
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python app.py
```

The application will be available locally at:

```text
http://127.0.0.1:5000
```

---

# 🎯 Key Features

### Prediction

* AI-based flood risk estimation
* Localized risk prediction
* Probability-based risk scoring

### Monitoring

* Interactive city map
* Zone-wise risk visualization
* Rainfall monitoring
* Risk trend monitoring

### Emergency Response

* Active incident alerts
* Severity classification
* Recommended response actions
* Citizen warning workflow

### Explainability

FloodIQ does not simply output:

> **"Zone is Critical."**

It can explain:

> **"Risk increased because of high rainfall, low elevation and historical flood frequency."**

This makes the prediction more useful for operational decision-making.

---

# 🔄 Example Control Flow

```text
Heavy rainfall detected
          ↓
Rainfall + terrain + historical data analysed
          ↓
ML model calculates flood probability
          ↓
Risk crosses critical threshold
          ↓
Zone marked 🔴 CRITICAL
          ↓
Alert generated
          ↓
Response recommendations displayed
          ↓
Authority takes action
```

---

# 👥 Who Can Use FloodIQ?

### 🏛️ Disaster Management Authorities

To monitor vulnerable zones and prioritize emergency response.

### 🚑 Emergency Response Teams

To identify areas requiring immediate deployment.

### 🏙️ Municipal Authorities

To monitor drainage and waterlogging-prone locations.

### 👨‍👩‍👧 Citizens

To receive understandable, location-specific warnings.

---

# 🌍 Scalability

FloodIQ is designed as a city-agnostic architecture.

```text
              FloodIQ Engine
                    │
       ┌────────────┼────────────┐
       ↓            ↓            ↓
    Nagpur       City B       City C
       │            │            │
   Local Data    Local Data    Local Data
```

The same prediction and response pipeline can be adapted to another city by integrating:

* Local rainfall data
* Local terrain
* Historical flood records
* Administrative zones
* Drainage infrastructure
* Local vulnerability data

---

# 🔮 Future Scope

### Real-Time IoT Integration

Integrate water-level sensors and drainage sensors for live ground-level measurements.

### Satellite-Based Monitoring

Use satellite imagery to detect water spread and improve flood mapping.

### Hyperlocal Alerts

Send location-specific warnings to citizens based on their locality.

### Dynamic Evacuation Routing

Generate safer routes based on current flood conditions.

### Multi-Agent Emergency Coordination

Use AI agents to coordinate alerts, emergency teams, shelters and resource allocation.

### Continuous Model Learning

Retrain the model using newly observed flood events to improve future predictions.

---

# 🛡️ Important Note

FloodIQ is a **prototype for disaster-risk analysis and emergency response support**.

Predictions are dependent on the quality, coverage, and timeliness of the u
