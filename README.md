# IoT Air Quality & Pollution Monitoring Dashboard

Student project: ESP32-based air quality & pollution monitoring with simulation, dashboard, and reporting.

Overview
This repository contains everything needed to build, simulate, and demonstrate an IoT air-quality monitoring system suitable for a student portfolio.

Quick links
- Folder structure: [docs/FOLDER_STRUCTURE.md](docs/FOLDER_STRUCTURE.md)
- Environment setup: [07_ENVIRONMENT_SETUP.md](07_ENVIRONMENT_SETUP.md)
- Circuit connections: [circuit_diagram/CONNECTIONS.md](circuit_diagram/CONNECTIONS.md)

Problem statement
Air pollution and indoor air-quality issues affect health and productivity. This project measures particulate matter and environmental conditions, classifies air quality, triggers alerts, and visualizes data on a dashboard.

Components used
- ESP32 (Wi‑Fi microcontroller)
- MQ135 gas sensor (analog VOC/air-quality proxy)
- DHT22 (temperature & humidity)
- Active buzzer + LEDs for alerts
- Optional OLED/LCD for local display

Architecture
- Sensors → ESP32 (ADC/Digital) → Processing (AQI classification) → Output (LED/buzzer/local display) → Cloud (ThingSpeak / Blynk) → Dashboard

Features
- Real sensor firmware (ESP32): reads MQ135 + DHT22, classifies AQI, triggers alerts, optional cloud upload
- Virtual simulator (Python): generates realistic PM/temp/humidity data, saves CSV, and creates interactive charts
- Report generator: CSV, text, and PDF outputs for presentations
- Documentation: wiring, simulation, dashboard setup, and GitHub strategy

Setup
1. Install Python dependencies: `pip install -r requirements.txt`
2. Set up Arduino/ESP32 toolchain (see [07_ENVIRONMENT_SETUP.md](07_ENVIRONMENT_SETUP.md)).
3. Review wiring in [circuit_diagram/CONNECTIONS.md](circuit_diagram/CONNECTIONS.md).

Execution
- Run simulator (example):
```
python python_simulation/simulate_aqi.py --samples 50 --interval 0.5
```
- Generate dashboard:
```
python python_simulation/plot_dashboard.py
```
- Upload firmware: Open `arduino_code/esp32_aqi_real.ino` in Arduino IDE, configure Wi‑Fi and ThingSpeak keys, then upload.

Dashboard
- Follow [docs/DASHBOARD_SETUP.md](docs/DASHBOARD_SETUP.md) to configure ThingSpeak or Blynk and map fields for `aqi`, `temperature`, `humidity`, `pollution_status`, and `alert`.

Sample output
- Simulated CSV: `data/simulated_readings.csv`
- Reports: `reports/air_quality_report_<TIMESTAMP>.csv|.txt|.pdf`
- Interactive HTML dashboards: `outputs/sensor_readings.html`

Screenshots
- Place wiring photos and screenshots in `images/`:
	- `images/wiring_photo.jpg`
	- `images/serial_output.png`
	- `images/dashboard_full.png`
	- `images/graph_spike.png`

Future improvements
- Replace MQ-series with calibrated PM sensors (e.g., PMS7003) for accurate particulate measurements
- Add MQTT + persistent time-series DB (InfluxDB) for long-term storage
- Add hardware enclosure and mobile notifications

Learning outcomes
- Sensor interfacing and ADC protection
- Simple AQI classification and thresholding
- Building cloud dashboards and alerts
- Data simulation, logging, and report generation

Credits & License
See `LICENSE` (if present) and `CONTRIBUTING.md` for contribution guidelines.

---
Start with `python_simulation/` to generate sample data and `arduino_code/` when you have a board connected.

Live dashboard (interactive)
------------------------------
A live local dashboard is available using Dash (Python). It reads `data/simulated_readings.csv` and provides real‑time indicators, trends, and a recent readings table.

Run the Dash app:
```bash
pip install dash
python python_simulation/live_dashboard.py
```

Open http://127.0.0.1:8050 in your browser. The dashboard refreshes every 10 seconds.

Static enhanced dashboard
-------------------------
If you prefer a static single‑file HTML report (includes CSV export), run:
```bash
python python_simulation/enhanced_dashboard.py
```
Then open `outputs/sensor_dashboard.html`.
