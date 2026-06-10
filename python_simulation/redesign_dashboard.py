import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.io as pio
from datetime import datetime, timezone
import html
import os


def compute_aqi_pm25(conc):
    breakpoints = [
        (0.0, 12.0, 0, 50),
        (12.1, 35.4, 51, 100),
        (35.5, 55.4, 101, 150),
        (55.5, 150.4, 151, 200),
        (150.5, 250.4, 201, 300),
        (250.5, 350.4, 301, 400),
        (350.5, 500.4, 401, 500),
    ]
    try:
        conc = float(conc)
    except Exception:
        return None
    for Clow, Chigh, Ilow, Ihigh in breakpoints:
        if Clow <= conc <= Chigh:
            return int(round(((Ihigh - Ilow) / (Chigh - Clow)) * (conc - Clow) + Ilow))
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


def build(sensor_csv='data/simulated_readings.csv', out_html='outputs/sensor_readings.html'):
    ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    csv_path = os.path.join(ROOT, sensor_csv) if not os.path.isabs(sensor_csv) else sensor_csv
    out_path = os.path.join(ROOT, out_html) if not os.path.isabs(out_html) else out_html

    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path, parse_dates=['timestamp'])
    else:
        now = datetime.now(timezone.utc)
        df = pd.DataFrame([{
            'timestamp': now,
            'node_id': 'sim-node-1',
            'pm25': 12.0,
            'pm10': 20.0,
            'temperature': 25.0,
            'humidity': 45.0,
            'gas': 120,
        }])

    # Compute AQI and latest metrics
    df = df.sort_values('timestamp')
    df['pm25'] = pd.to_numeric(df.get('pm25', pd.Series(np.nan)), errors='coerce')
    df['pm10'] = pd.to_numeric(df.get('pm10', pd.Series(np.nan)), errors='coerce')
    df['temperature'] = pd.to_numeric(df.get('temperature', pd.Series(np.nan)), errors='coerce')
    df['humidity'] = pd.to_numeric(df.get('humidity', pd.Series(np.nan)), errors='coerce')
    df['gas'] = pd.to_numeric(df.get('gas', pd.Series(np.nan)), errors='coerce')

    df['aqi'] = df['pm25'].apply(lambda v: compute_aqi_pm25(v) if not np.isnan(v) else None)
    df['aqi_cat'], df['aqi_color'] = zip(*df['aqi'].apply(lambda v: aqi_category(v)))

    latest = df.iloc[-1]
    last_update = pd.to_datetime(latest['timestamp']).to_pydatetime().astimezone(timezone.utc)

    # Build Plotly figures
    fig_pm = go.Figure()
    fig_pm.add_trace(go.Scatter(x=df['timestamp'], y=df['pm25'], mode='lines', name='PM2.5', line=dict(shape='spline', color='#00E5FF', width=3)))
    fig_pm.add_trace(go.Scatter(x=df['timestamp'], y=df['pm10'], mode='lines', name='PM10', line=dict(shape='spline', color='#FF8A65', width=2)))
    fig_pm.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    fig_pm.update_xaxes(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
    fig_pm.update_yaxes(showgrid=True, gridcolor='rgba(255,255,255,0.05)', title='µg/m³')

    fig_gas = go.Figure()
    fig_gas.add_trace(go.Scatter(x=df['timestamp'], y=df['gas'], mode='lines', name='Gas Index', line=dict(shape='spline', color='#9FA8DA', width=2)))
    fig_gas.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    fig_gas.update_xaxes(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
    fig_gas.update_yaxes(showgrid=True, gridcolor='rgba(255,255,255,0.05)')

    # Convert to HTML fragments
    pm_html = pio.to_html(fig_pm, full_html=False, include_plotlyjs='cdn')
    gas_html = pio.to_html(fig_gas, full_html=False, include_plotlyjs=False)

    # Prepare CSV export safe
    csv_text = df.to_csv(index=False)
    safe_csv = html.escape(csv_text)

    # AQI status cards
    aqi_breaks = [
        ('Good', '#2ECC71'),
        ('Moderate', '#F1C40F'),
        ('Unhealthy', '#E67E22'),
        ('Hazardous', '#6C3483')
    ]

    # Build full HTML
    html_content = f"""
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>IoT Air Quality & Pollution Monitoring Dashboard</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
  <style>
    :root{{--bg:#0b1220;--card:#0f1724;--muted:#97a3b4;--accent:#2D9CDB}}
    body{{margin:0;font-family:Inter,Roboto,Arial,sans-serif;background:linear-gradient(180deg,var(--bg),#07101a);color:#e6eef8}}
    .container{{max-width:1200px;margin:20px auto;padding:16px}}
    .top{{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:12px}}
    h1{{margin:0;font-size:20px;font-weight:700}}
    .last-upd{{color:var(--muted);font-size:13px}}
    .aqi-cards{{display:flex;gap:10px;margin-top:12px;flex-wrap:wrap}}
    .aqi-card{{padding:12px 14px;border-radius:8px;background:var(--card);min-width:120px;text-align:center}}
    .aqi-dot{{width:12px;height:12px;border-radius:50%;display:inline-block;margin-right:8px;vertical-align:middle}}
    .metrics{{display:flex;gap:10px;margin-top:16px;flex-wrap:wrap}}
    .metric{{background:var(--card);padding:12px;border-radius:8px;min-width:140px;flex:1;box-shadow:0 3px 10px rgba(2,6,23,0.6)}}
    .metric .label{{color:var(--muted);font-size:12px}}
    .metric .value{{font-size:20px;font-weight:700}}
    .charts{{display:grid;grid-template-columns:1fr;gap:12px;margin-top:16px}}
    @media(min-width:900px){{.charts{{grid-template-columns:2fr 1fr}}}}
    .card{{background:var(--card);padding:12px;border-radius:10px}}
    .export{{background:transparent;border:1px solid rgba(255,255,255,0.06);color:var(--muted);padding:8px 10px;border-radius:6px;text-decoration:none}}
    .status-dot{{width:12px;height:12px;border-radius:50%;display:inline-block;margin-right:8px}}
  </style>
</head>
<body>
  <div class="container">
    <div class="top">
      <div>
        <h1>IoT Air Quality & Pollution Monitoring Dashboard</h1>
        <div class="last-upd">Last updated: {last_update.strftime('%Y-%m-%d %H:%M:%SZ')}</div>
      </div>
      <div style="display:flex;gap:8px;align-items:center">
        <div style="display:flex;align-items:center"><span class="status-dot" style="background:{latest['aqi_color']}"></span><strong style="color:{latest['aqi_color']}">{latest['aqi_cat']}</strong></div>
        <a class="export" href="#" id="exportCsv">Export CSV</a>
      </div>
    </div>

    <div class="aqi-cards">
"""

    for name, color in aqi_breaks:
        html_content += f"    <div class=\"aqi-card\"><div style='font-size:12px;color:var(--muted)'>{name}</div><div style='margin-top:6px;font-weight:700'><span class=\"aqi-dot\" style=\"background:{color}\"></span></div></div>\n"

    html_content += """
    </div>

    <div class="metrics">
      <div class="metric">
        <div class="label">PM2.5</div>
        <div class="value">{pm25_val}</div>
      </div>
      <div class="metric">
        <div class="label">PM10</div>
        <div class="value">{pm10_val}</div>
      </div>
      <div class="metric">
        <div class="label">Temperature</div>
        <div class="value">{temp_val}</div>
      </div>
      <div class="metric">
        <div class="label">Humidity</div>
        <div class="value">{hum_val}</div>
      </div>
    </div>

    <div class="charts">
      <div class="card">{pm_html}</div>
      <div class="card">{gas_html}</div>
    </div>
  </div>

  <script>
    const csvData = `{safe_csv}`;
    document.getElementById('exportCsv').addEventListener('click', function(e){
      e.preventDefault();
      const blob = new Blob([csvData], { type: 'text/csv;charset=utf-8;' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a'); a.href = url; a.download = 'simulated_readings.csv'; document.body.appendChild(a); a.click(); a.remove(); URL.revokeObjectURL(url);
    });
  </script>
</body>
</html>
"""

    # replace placeholders safely
    pm25_val = f"{latest['pm25']:.1f}" if not np.isnan(latest['pm25']) else '—'
    pm10_val = f"{latest['pm10']:.1f}" if not np.isnan(latest['pm10']) else '—'
    temp_val = f"{latest['temperature']:.1f}" if not np.isnan(latest['temperature']) else '—'
    hum_val = f"{latest['humidity']:.1f}" if not np.isnan(latest['humidity']) else '—'

    html_content = html_content.replace('{pm25_val}', pm25_val).replace('{pm10_val}', pm10_val).replace('{temp_val}', temp_val).replace('{hum_val}', hum_val).replace('{pm_html}', pm_html).replace('{gas_html}', gas_html).replace('{safe_csv}', safe_csv)

    # write file
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"Wrote {out_path}")


if __name__ == '__main__':
    build()
