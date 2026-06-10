Virtual simulation — how to simulate air pollution monitoring

Purpose
This guide explains how to simulate different air-quality scenarios, trigger alerts, update the dashboard, and save logs for reports or demos.

Files used
- `python_simulation/simulate_aqi.py` — basic random simulator that logs CSV.
- `python_simulation/simulate_presets.py` — helper to generate specific scenarios (normal, moderate, smoke, hazardous, temp/humidity change).
- `python_simulation/plot_dashboard.py` — generate interactive HTML charts from CSV.

Running presets
- Normal air quality (low PM2.5):

  ```powershell
  python python_simulation/simulate_presets.py --mode normal --samples 20 --interval 0.5
  ```

- Moderate pollution:

  ```powershell
  python python_simulation/simulate_presets.py --mode moderate --samples 20 --interval 0.5
  ```

- Smoke / gas leakage (sudden spike):

  ```powershell
  python python_simulation/simulate_presets.py --mode smoke --samples 10 --interval 0.5
  ```

- Hazardous sustained pollution:

  ```powershell
  python python_simulation/simulate_presets.py --mode hazardous --samples 30 --interval 0.5
  ```

- Temperature / humidity change (heat/humidity event):

  ```powershell
  python python_simulation/simulate_presets.py --mode temp_hum --samples 20 --interval 0.5
  ```

What each mode does
- `normal`: generates PM2.5 values in the range 3–12 µg/m³ and modest temp/humidity.
- `moderate`: PM2.5 between 12.1–35.4 µg/m³, occasional spikes.
- `smoke`: sharp spikes in PM2.5 and PM10 to simulate nearby smoke or gas leakage; produces alert messages.
- `hazardous`: sustained high PM2.5 values (>150 µg/m³) and repeated alerts.
- `temp_hum`: simulates rapid temperature and humidity changes (useful for thermal sensor QA).

Alert output
- Preset script prints alert messages to the console when the category is `Poor`, `Unhealthy`, or `Hazardous`.
- Alerts are also saved as a column (`category` and `aqi`) in `data/simulated_readings.csv` for later analysis.

Updating the dashboard
- After running a preset, regenerate the dashboard:

  ```powershell
  python python_simulation/plot_dashboard.py
  ```

- The interactive HTML files are saved to `outputs/` (e.g., `outputs/sensor_readings.html`). Open them in a browser to view live charts reflecting the latest CSV.

Saving sensor logs
- All generated rows append to `data/simulated_readings.csv` with columns: `timestamp,pm25,pm10,temp,hum,aqi,category`.
- Use `pandas` or Excel to filter time ranges, export subsets, or prepare graphs for reports.

Serial Monitor simulation
- To mimic Serial Monitor output, run `simulate_presets.py` and watch console prints. Save console output using PowerShell redirection:

  ```powershell
  python python_simulation/simulate_presets.py --mode smoke --samples 10 > outputs/serial_smoke.txt
  ```

Dashboard update demo flow
1. Run a preset (e.g., `smoke`) to generate high PM values and alerts.
2. Run `plot_dashboard.py` to refresh HTML dashboard.
3. Open `outputs/sensor_readings.html` in a browser and observe spikes and category changes.
4. Capture screenshots (see below).

Screenshots to capture (for reports and GitHub):
- Serial monitor console output showing values and alert lines. Save to `outputs/serial_<mode>.txt` and capture a screenshot `images/serial_<mode>.png`.
- Dashboard full view: `images/dashboard_full.png` (open `outputs/sensor_readings.html` and screenshot).
- Graph close-up showing spikes: `images/graph_spike.png`.
- CSV/log preview: open `data/simulated_readings.csv` and capture `images/csv_preview.png`.
- Alert examples: screenshot of console lines highlighting `ALERT:` and a cropped image `images/alert_console.png`.

Notes and tips
- Use short intervals when simulating to create visible spikes quickly (0.2–0.5s).
- For reproducible demos, set the random seed in `simulate_presets.py` by passing `--seed 123`.
- If you want a live dashboard hosted on the web, consider pushing CSV data periodically to ThingSpeak or a small Flask server; this guide focuses on offline demos and exported HTML.

Next steps I can take
- Run a preset here to produce sample CSV and dashboard files, then save screenshots into `images/` and `outputs/`.
- Alternatively, generate a short screencast script showing the steps above.

Which would you like me to run now?