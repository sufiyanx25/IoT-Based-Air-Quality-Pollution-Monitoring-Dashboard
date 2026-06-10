Python simulation

Files:
- `simulate_aqi.py` — generate simulated sensor readings, classify AQI, log CSV.
- `plot_dashboard.py` — read CSV and create interactive Plotly dashboards saved to `outputs/`.

Quick start
1. Create and activate a virtual environment:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

2. Install dependencies (from project root):

```powershell
pip install -r requirements.txt
pip install plotly pandas
# optional: pip install kaleido (for PNG export)
```

3. Run simulation:

```powershell
python python_simulation/simulate_aqi.py --samples 50 --interval 0.5
```

4. Create dashboard:

```powershell
python python_simulation/plot_dashboard.py
```

CSV output: `data/simulated_readings.csv`
Interactive HTML: `outputs/sensor_readings.html`
