"""
simulate_aqi.py
- Generates virtual PM2.5/PM10/temperature/humidity readings
- Classifies air quality using PM2.5 thresholds
- Logs readings to CSV in ../data/
- Prints alerts to console when poor/hazardous

Usage:
    python simulate_aqi.py --samples 100 --interval 1

"""
import argparse
import csv
import os
import random
import time
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
CSV_PATH = os.path.join(DATA_DIR, 'simulated_readings.csv')

os.makedirs(DATA_DIR, exist_ok=True)


def generate_reading():
    """Return a dict with simulated readings."""
    pm25 = round(random.uniform(3.0, 200.0), 1)
    pm10 = round(pm25 + random.uniform(1.0, 80.0), 1)
    temp = round(random.uniform(15.0, 40.0), 1)
    hum = round(random.uniform(20.0, 90.0), 1)
    timestamp = datetime.utcnow().isoformat()
    return {
        'timestamp': timestamp,
        'pm25': pm25,
        'pm10': pm10,
        'temp': temp,
        'hum': hum
    }


def classify_aqi(pm25):
    if pm25 <= 12.0:
        return 'Good', 50
    if pm25 <= 35.4:
        return 'Moderate', 100
    if pm25 <= 55.4:
        return 'Poor', 150
    if pm25 <= 150.4:
        return 'Unhealthy', 200
    return 'Hazardous', 300


def append_csv(row):
    file_exists = os.path.isfile(CSV_PATH)
    with open(CSV_PATH, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['timestamp', 'pm25', 'pm10', 'temp', 'hum', 'aqi', 'category'])
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def main(samples=10, interval=1):
    print(f"Simulating {samples} samples, interval={interval}s, saving to {CSV_PATH}")
    for i in range(samples):
        r = generate_reading()
        category, aqi = classify_aqi(r['pm25'])
        r['aqi'] = aqi
        r['category'] = category
        append_csv(r)
        print(f"{r['timestamp']} PM2.5={r['pm25']} PM10={r['pm10']} Temp={r['temp']}C Hum={r['hum']}% AQI={aqi} ({category})")
        if category in ('Poor', 'Unhealthy', 'Hazardous'):
            print('ALERT:', category, '- consider ventilation or warnings')
        time.sleep(interval)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--samples', type=int, default=20)
    parser.add_argument('--interval', type=float, default=1.0)
    args = parser.parse_args()
    main(samples=args.samples, interval=args.interval)
