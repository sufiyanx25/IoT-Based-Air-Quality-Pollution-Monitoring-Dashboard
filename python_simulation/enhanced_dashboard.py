import pandas as pd
import numpy as np
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.io as pio
from datetime import datetime
import html


def compute_aqi_pm25(conc):
    # US EPA breakpoints for PM2.5 (µg/m3)
    breakpoints = [
        (0.0, 12.0, 0, 50),
        (12.1, 35.4, 51, 100),
        (35.5, 55.4, 101, 150),
        (55.5, 150.4, 151, 200),
        (150.5, 250.4, 201, 300),
        (250.5, 350.4, 301, 400),
        (350.5, 500.4, 401, 500),
    ]
    for (Clow, Chigh, Ilow, Ihigh) in breakpoints:
        if Clow <= conc <= Chigh:
            aqi = ((Ihigh - Ilow) / (Chigh - Clow)) * (conc - Clow) + Ilow
            return int(round(aqi))
    return None


def aqi_category(aqi):
    if aqi is None:
        return "Unknown", "#9E9E9E"
    if aqi <= 50:
        return "Good", "#2ECC71"
    if aqi <= 100:
        return "Moderate", "#F1C40F"
    if aqi <= 200:
        return "Unhealthy", "#E67E22"
    if aqi <= 300:
        return "Very Unhealthy", "#E74C3C"
    return "Hazardous", "#6C3483"


def build_dashboard(csv_path="data/simulated_readings.csv", out_html="outputs/sensor_dashboard.html"):
    df = pd.read_csv(csv_path, parse_dates=["timestamp"]) if pd.io.common.file_exists(csv_path) else pd.DataFrame()
    if df.empty:
        # create a small placeholder
        now = datetime.utcnow()
        df = pd.DataFrame({
            "timestamp": [now],
            "pm25": [12.0],
            "pm10": [20.0],
            "gas": [150],
            "temperature": [25.0],
            "humidity": [45.0],
            "node_id": ["sim-node-1"],
            "lat": [0.0],
            "lon": [0.0],
        })

    # ensure columns exist
    for c in ["pm25", "pm10", "gas", "temperature", "humidity"]:
        if c not in df.columns:
            df[c] = np.nan

    # compute AQI for PM2.5
    df["aqi"] = df["pm25"].apply(lambda x: compute_aqi_pm25(float(x)) if not np.isnan(x) else None)
    df["aqi_cat"], df["aqi_color"] = zip(*df["aqi"].apply(lambda v: aqi_category(v)))

    latest = df.sort_values("timestamp").iloc[-1]

    # Indicators
    ind_aqi = go.Indicator(
        mode="number+gauge", value=latest["aqi"] if pd.notna(latest["aqi"]) else 0,
        title={"text": "AQI (PM2.5)"},
        gauge={"axis": {"range": [0, 500]}, "bar": {"color": latest["aqi_color"]}},
    )

    ind_pm25 = go.Indicator(mode="number", value=latest["pm25"], title={"text": "PM2.5 (µg/m³)"})
    ind_pm10 = go.Indicator(mode="number", value=latest["pm10"], title={"text": "PM10 (µg/m³)"})
    ind_temp = go.Indicator(mode="number", value=latest["temperature"], title={"text": "Temperature (°C)"})
    ind_hum = go.Indicator(mode="number", value=latest["humidity"], title={"text": "Humidity (%)"})

    # Time series
    ts_pm25 = go.Scatter(x=df["timestamp"], y=df["pm25"], mode="lines+markers", name="PM2.5")
    ts_pm10 = go.Scatter(x=df["timestamp"], y=df["pm10"], mode="lines+markers", name="PM10")
    ts_gas = go.Scatter(x=df["timestamp"], y=df["gas"], mode="lines+markers", name="Gas Index")

    # Data table (last 20 rows)
    table = go.Table(
        header=dict(values=["Timestamp", "Node", "PM2.5", "PM10", "AQI", "Category", "Temp", "Hum"], fill_color="#222" , font=dict(color='white')),
        cells=dict(values=[
            df["timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S"),
            df.get("node_id", [""] * len(df)),
            df["pm25"],
            df["pm10"],
            df["aqi"],
            df["aqi_cat"],
            df["temperature"],
            df["humidity"],
        ], fill_color="#fafafa")
    )

    # Layout: indicators row + time series + table
    fig = make_subplots(rows=4, cols=3, specs=[[{"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"}],
                                              [{"colspan": 3, "type": "xy"}, None, None],
                                              [{"colspan": 3, "type": "xy"}, None, None],
                                              [{"colspan": 3, "type": "table"}, None, None]],
                         subplot_titles=("AQI", "PM2.5", "PM10", "PM & Gas Trends", "Gas Index (trend)", "Recent readings"))

    fig.add_trace(ind_aqi, row=1, col=1)
    fig.add_trace(ind_pm25, row=1, col=2)
    fig.add_trace(ind_pm10, row=1, col=3)

    # add temperature/humidity as small separate traces in the second row as markers on right axis
    fig.add_trace(ts_pm25, row=2, col=1)
    fig.add_trace(ts_pm10, row=2, col=1)
    fig.update_yaxes(title_text="µg/m³", row=2, col=1)

    fig.add_trace(ts_gas, row=3, col=1)
    fig.update_yaxes(title_text="Gas Index", row=3, col=1)

    fig.add_trace(table, row=4, col=1)

    fig.update_layout(height=1100, showlegend=True, title_text="Air Quality Dashboard — Simulated Readings")

    # create CSV content for export
    csv_text = df.to_csv(index=False)
    safe_csv = html.escape(csv_text)

    # assemble full HTML with export button and a small map link
    dashboard_html = pio.to_html(fig, full_html=False, include_plotlyjs='cdn')

    full_html = f"""
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <meta http-equiv="refresh" content="300"> <!-- refresh every 5 minutes -->
  <title>Air Quality Dashboard</title>
  <style>
    body{{font-family: Arial, sans-serif; margin: 12px; background:#f7f9fc}}
    .topbar{{display:flex;justify-content:space-between;align-items:center}}
    .brand{{font-weight:700;font-size:20px}}
    .controls{{display:flex;gap:8px}}
    .btn{{padding:8px 12px;background:#2D9CDB;color:white;border-radius:4px;text-decoration:none}}
    .muted{{color:#666;font-size:13px}}
  </style>
</head>
<body>
  <div class="topbar">
    <div class="brand">IoT Air Quality Dashboard</div>
    <div class="controls">
      <a class="btn" href="#" id="exportCsv">Export CSV</a>
      <a class="btn" href="outputs/sensor_readings.html" target="_blank">Open Chart</a>
    </div>
  </div>
  <p class="muted">Last updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%SZ')}</p>
  {dashboard_html}

  <script>
    const csvData = `{safe_csv}`;
    document.getElementById('exportCsv').addEventListener('click', function(e) {{
      e.preventDefault();
      const blob = new Blob([csvData], {{ type: 'text/csv;charset=utf-8;' }});
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url; a.download = 'simulated_readings.csv'; document.body.appendChild(a); a.click(); a.remove(); URL.revokeObjectURL(url);
    }});
  </script>
</body>
</html>
"""

    # write out
    with open(out_html, 'w', encoding='utf-8') as f:
        f.write(full_html)
    print(f"Dashboard written to {out_html}")


if __name__ == '__main__':
    build_dashboard()
