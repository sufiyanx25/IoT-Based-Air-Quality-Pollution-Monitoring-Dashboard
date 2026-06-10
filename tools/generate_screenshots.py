"""
Generate PNG screenshots for project checklist and save to images/.
Creates:
- project_folder.png
- circuit_diagram.png
- wokwi_simulation.png (placeholder)
- serial_output.png
- alert_output.png
- alert_hardware.png (simulated)
- dashboard_chart.png
- csv_preview.png
- github_repo.png

Run from project root.
"""
import os
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import plotly.express as px

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
IMG_DIR = os.path.join(ROOT, 'images')
DATA_CSV = os.path.join(ROOT, 'data', 'simulated_readings.csv')
CONN_MD = os.path.join(ROOT, 'circuit_diagram', 'CONNECTIONS.md')
README = os.path.join(ROOT, 'README.md')
OUT_DIR = os.path.join(ROOT, 'outputs')
os.makedirs(IMG_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)

# Helper to create text image
def text_to_image(text, out_path, size=(1280,720), fontsize=14, bg=(255,255,255)):
    img = Image.new('RGB', size, color=bg)
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype('arial.ttf', fontsize)
    except Exception:
        font = ImageFont.load_default()
    margin = 10
    x, y = margin, margin
    for line in text.splitlines():
        draw.text((x,y), line, fill=(0,0,0), font=font)
        y += fontsize + 4
        if y > size[1] - margin:
            break
    img.save(out_path)
    print('Wrote', out_path)

# 1) project_folder.png
listing = []
for root, dirs, files in os.walk(ROOT):
    # list top-level only
    break
for name in sorted(dirs) + sorted(files):
    listing.append(name)
text = 'Project root listing:\n' + '\n'.join(listing)
text_to_image(text, os.path.join(IMG_DIR, 'project_folder.png'))

# 2) circuit_diagram.png (render md)
if os.path.isfile(CONN_MD):
    with open(CONN_MD, 'r', encoding='utf-8') as f:
        md = f.read()
else:
    md = 'Circuit connections file not found.'
text_to_image(md, os.path.join(IMG_DIR, 'circuit_diagram.png'))

# 3) wokwi_simulation.png placeholder
text_to_image('Wokwi / Tinkercad simulation (placeholder)\nRun simulation online and capture this screen.', os.path.join(IMG_DIR, 'wokwi_simulation.png'))

# 4) serial_output.png (last 12 rows)
if os.path.isfile(DATA_CSV):
    df = pd.read_csv(DATA_CSV)
    last = df.tail(12).to_string(index=False)
else:
    last = 'No CSV data available.'
text_to_image('Serial monitor sample:\n' + last, os.path.join(IMG_DIR, 'serial_output.png'))

# 5) alert_output.png (rows with Poor/Unhealthy/Hazardous)
if os.path.isfile(DATA_CSV):
    df = pd.read_csv(DATA_CSV)
    alerts = df[df['category'].isin(['Poor','Unhealthy','Hazardous'])].tail(12)
    if not alerts.empty:
        alert_text = alerts.to_string(index=False)
    else:
        alert_text = 'No alert rows in CSV.'
else:
    alert_text = 'No CSV data available.'
text_to_image('Alert output sample:\n' + alert_text, os.path.join(IMG_DIR, 'alert_output.png'))

# 6) alert_hardware.png (simulated LED ON)
img = Image.new('RGB', (640,360), color=(255,255,255))
draw = ImageDraw.Draw(img)
# draw LED circle
draw.ellipse((280,120,360,200), fill=(255,0,0), outline=(0,0,0))
try:
    font = ImageFont.truetype('arial.ttf', 16)
except Exception:
    font = ImageFont.load_default()
draw.text((10,10), 'Simulated hardware alert: LED is ON (red). Buzzer active (simulated).', fill=(0,0,0), font=font)
img.save(os.path.join(IMG_DIR, 'alert_hardware.png'))
print('Wrote', os.path.join(IMG_DIR, 'alert_hardware.png'))

# 7) dashboard_chart.png - create a simple plot from CSV
if os.path.isfile(DATA_CSV):
    df = pd.read_csv(DATA_CSV, parse_dates=['timestamp'])
    fig = px.line(df.tail(200), x='timestamp', y='pm25', title='PM2.5 (simulated)')
    png_out = os.path.join(IMG_DIR, 'dashboard_chart.png')
    fig.write_image(png_out)
    print('Wrote', png_out)
else:
    text_to_image('No CSV - dashboard chart not created.', os.path.join(IMG_DIR, 'dashboard_chart.png'))

# 8) csv_preview.png (first 12 rows)
if os.path.isfile(DATA_CSV):
    df = pd.read_csv(DATA_CSV)
    preview = df.head(12).to_string(index=False)
else:
    preview = 'No CSV data available.'
text_to_image('CSV preview:\n' + preview, os.path.join(IMG_DIR, 'csv_preview.png'))

# 9) github_repo.png - render README head
if os.path.isfile(README):
    with open(README, 'r', encoding='utf-8') as f:
        head = ''.join(f.readlines()[:200])
else:
    head = 'README not found.'
text_to_image('GitHub repo preview:\n' + head, os.path.join(IMG_DIR, 'github_repo.png'))

print('All images generated in', IMG_DIR)
