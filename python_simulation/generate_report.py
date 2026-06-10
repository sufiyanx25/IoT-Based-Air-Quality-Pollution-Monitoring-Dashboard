"""
generate_report.py
- Reads simulated sensor CSV (`data/simulated_readings.csv`)
- Produces a cleaned report CSV and a text summary in `reports/`
- Optionally creates a PDF if `reportlab` is installed

Usage:
    python python_simulation/generate_report.py --last 100

"""
import os
import pandas as pd
from datetime import datetime
import argparse

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_CSV = os.path.join(PROJECT_ROOT, 'data', 'simulated_readings.csv')
REPORTS_DIR = os.path.join(PROJECT_ROOT, 'reports')
os.makedirs(REPORTS_DIR, exist_ok=True)


def ensure_sample_data():
    """Create small sample CSV if none exists."""
    if os.path.isfile(DATA_CSV):
        return
    print('No simulated CSV found — creating sample data')
    import random
    import csv
    from datetime import datetime, timedelta
    os.makedirs(os.path.dirname(DATA_CSV), exist_ok=True)
    now = datetime.utcnow()
    with open(DATA_CSV, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['timestamp','pm25','pm10','temp','hum','aqi','category'])
        writer.writeheader()
        for i in range(30):
            t = (now - timedelta(seconds=(30-i)*10)).isoformat()
            pm25 = round(random.uniform(5,80),1)
            pm10 = round(pm25 + random.uniform(1,50),1)
            temp = round(random.uniform(18,32),1)
            hum = round(random.uniform(30,70),1)
            if pm25 <= 12.0:
                cat, aqi = 'Good', 50
            elif pm25 <= 35.4:
                cat, aqi = 'Moderate', 100
            elif pm25 <= 55.4:
                cat, aqi = 'Poor', 150
            elif pm25 <= 150.4:
                cat, aqi = 'Unhealthy', 200
            else:
                cat, aqi = 'Hazardous', 300
            writer.writerow({
                'timestamp': t,
                'pm25': pm25,
                'pm10': pm10,
                'temp': temp,
                'hum': hum,
                'aqi': aqi,
                'category': cat
            })
    print('Sample data created at', DATA_CSV)


def build_report(last_n=None):
    ensure_sample_data()
    df = pd.read_csv(DATA_CSV, parse_dates=['timestamp'])
    if last_n is not None:
        df = df.tail(last_n)

    # Build report frame
    report_df = pd.DataFrame()
    report_df['timestamp'] = df['timestamp']
    # Air quality value: use `aqi` column if present, otherwise use pm25-derived
    if 'aqi' in df.columns:
        report_df['air_quality_value'] = df['aqi']
    else:
        # fallback: convert pm25 to simple AQI
        def pm25_to_aqi(x):
            x = float(x)
            if x <= 12.0: return 50
            if x <= 35.4: return 100
            if x <= 55.4: return 150
            if x <= 150.4: return 200
            return 300
        report_df['air_quality_value'] = df['pm25'].apply(pm25_to_aqi)

    report_df['temperature_C'] = df['temp']
    report_df['humidity_pct'] = df['hum']
    report_df['pollution_category'] = df['category']
    # alert status: 1 when category in Poor/Unhealthy/Hazardous
    report_df['alert_status'] = report_df['pollution_category'].isin(['Poor','Unhealthy','Hazardous']).astype(int)

    # Filenames
    ts = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    csv_out = os.path.join(REPORTS_DIR, f'air_quality_report_{ts}.csv')
    txt_out = os.path.join(REPORTS_DIR, f'air_quality_report_{ts}.txt')
    pdf_out = os.path.join(REPORTS_DIR, f'air_quality_report_{ts}.pdf')

    # Save CSV
    report_df.to_csv(csv_out, index=False)
    print('Saved report CSV to', csv_out)

    # Save text summary
    summary_lines = []
    summary_lines.append('Air Quality Report')
    summary_lines.append('Generated: ' + datetime.utcnow().isoformat())
    summary_lines.append('Rows: ' + str(len(report_df)))
    summary_lines.append('')
    summary_lines.append(report_df.to_string(index=False))
    with open(txt_out, 'w') as f:
        f.write('\n'.join(summary_lines))
    print('Saved text report to', txt_out)

    # Optional PDF using reportlab if available
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
        from reportlab.lib.units import mm

        c = canvas.Canvas(pdf_out, pagesize=A4)
        width, height = A4
        margin = 15 * mm
        y = height - margin
        c.setFont('Helvetica-Bold', 14)
        c.drawString(margin, y, 'Air Quality Report')
        c.setFont('Helvetica', 9)
        y -= 12
        c.drawString(margin, y, 'Generated: ' + datetime.utcnow().isoformat())
        y -= 18

        # Write table header
        cols = ['timestamp','air_quality_value','temperature_C','humidity_pct','pollution_category','alert_status']
        col_w = (width - 2*margin) / len(cols)
        c.setFont('Helvetica-Bold', 8)
        x = margin
        for col in cols:
            c.drawString(x, y, col)
            x += col_w
        y -= 10
        c.setFont('Helvetica', 8)
        # rows
        for _, row in report_df.iterrows():
            x = margin
            for col in cols:
                text = str(row[col])
                c.drawString(x, y, text[:30])
                x += col_w
            y -= 10
            if y < margin + 30:
                c.showPage()
                y = height - margin
        c.save()
        print('Saved PDF report to', pdf_out)
    except Exception as e:
        print('PDF generation skipped (reportlab missing or error):', e)

    return csv_out, txt_out


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--last', type=int, default=100, help='How many last rows to include')
    args = parser.parse_args()
    build_report(last_n=args.last)
