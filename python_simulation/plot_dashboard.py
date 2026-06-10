"""
plot_dashboard.py
- Reads CSV produced by simulate_aqi.py
- Generates interactive Plotly dashboard saved to outputs/ (HTML)
- Also exports a static PNG for reports (requires kaleido)

Usage:
    python plot_dashboard.py
"""
import os
import pandas as pd
import plotly.express as px

BASE_DIR = os.path.dirname(__file__)
CSV_PATH = os.path.join(BASE_DIR, '..', 'data', 'simulated_readings.csv')
OUT_DIR = os.path.join(BASE_DIR, '..', 'outputs')
os.makedirs(OUT_DIR, exist_ok=True)


def load_data():
    if not os.path.isfile(CSV_PATH):
        raise FileNotFoundError(f"CSV not found: {CSV_PATH}. Run simulate_aqi.py first.")
    df = pd.read_csv(CSV_PATH, parse_dates=['timestamp'])
    return df


def make_plots(df):
    # PM2.5 time series with category coloring
    fig_pm25 = px.line(df, x='timestamp', y='pm25', title='PM2.5 over time')
    fig_pm25.write_html(os.path.join(OUT_DIR, 'pm25.html'))

    # Combined subplot style (use express for simplicity)
    fig = px.line(df, x='timestamp', y=['pm25','pm10','temp','hum'], title='Sensor readings')
    fig.update_layout(legend_title_text='Metric')
    html_path = os.path.join(OUT_DIR, 'sensor_readings.html')
    fig.write_html(html_path)
    print('Saved interactive dashboards to', html_path)

    # Save static PNGs (requires kaleido package)
    try:
        fig.write_image(os.path.join(OUT_DIR, 'sensor_readings.png'))
        print('Saved static PNG to outputs/')
    except Exception as e:
        print('Could not save PNG (kaleido missing):', e)


if __name__ == '__main__':
    df = load_data()
    make_plots(df)
