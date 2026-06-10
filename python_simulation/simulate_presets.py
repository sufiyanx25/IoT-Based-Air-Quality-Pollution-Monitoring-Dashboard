"""
simulate_presets.py
- Generate preset scenarios for the AQI simulator
- Modes: normal, moderate, smoke, hazardous, temp_hum
- Appends rows to data/simulated_readings.csv and prints alerts

Usage:
    python simulate_presets.py --mode smoke --samples 10 --interval 0.5 --seed 42
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


def write_row(row):
    exists = os.path.isfile(CSV_PATH)
    with open(CSV_PATH, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['timestamp','pm25','pm10','temp','hum','aqi','category'])
        if not exists:
            writer.writeheader()
        writer.writerow(row)


def classify(pm25):
    if pm25 <= 12.0:
        return 'Good', 50
    if pm25 <= 35.4:
        return 'Moderate', 100
    if pm25 <= 55.4:
        return 'Poor', 150
    if pm25 <= 150.4:
        return 'Unhealthy', 200
    return 'Hazardous', 300


def gen_normal():
    pm25 = round(random.uniform(3.0, 12.0),1)
    pm10 = round(pm25 + random.uniform(1.0,6.0),1)
    temp = round(random.uniform(20.0,25.0),1)
    hum = round(random.uniform(30.0,50.0),1)
    return pm25, pm10, temp, hum


def gen_moderate():
    pm25 = round(random.uniform(15.0,35.0),1)
    pm10 = round(pm25 + random.uniform(5.0,40.0),1)
    temp = round(random.uniform(20.0,30.0),1)
    hum = round(random.uniform(30.0,60.0),1)
    return pm25, pm10, temp, hum


def gen_smoke():
    # sudden spikes
    pm25 = round(random.uniform(80.0,250.0),1)
    pm10 = round(pm25 + random.uniform(20.0,150.0),1)
    temp = round(random.uniform(22.0,35.0),1)
    hum = round(random.uniform(20.0,50.0),1)
    return pm25, pm10, temp, hum


def gen_hazardous():
    pm25 = round(random.uniform(160.0,400.0),1)
    pm10 = round(pm25 + random.uniform(30.0,200.0),1)
    temp = round(random.uniform(25.0,40.0),1)
    hum = round(random.uniform(10.0,40.0),1)
    return pm25, pm10, temp, hum


def gen_temp_hum():
    pm25 = round(random.uniform(5.0,80.0),1)
    pm10 = round(pm25 + random.uniform(1.0,60.0),1)
    temp = round(random.uniform(5.0,45.0),1)
    hum = round(random.uniform(10.0,95.0),1)
    return pm25, pm10, temp, hum


def run(mode, samples=10, interval=1.0, seed=None):
    if seed is not None:
        random.seed(seed)

    gen_map = {
        'normal': gen_normal,
        'moderate': gen_moderate,
        'smoke': gen_smoke,
        'hazardous': gen_hazardous,
        'temp_hum': gen_temp_hum
    }
    if mode not in gen_map:
        raise ValueError('Unknown mode')

    gen = gen_map[mode]
    print(f"Running mode={mode}, samples={samples}, interval={interval}")
    for i in range(samples):
        pm25, pm10, temp, hum = gen()
        category, aqi = classify(pm25)
        row = {
            'timestamp': datetime.utcnow().isoformat(),
            'pm25': pm25,
            'pm10': pm10,
            'temp': temp,
            'hum': hum,
            'aqi': aqi,
            'category': category
        }
        write_row(row)
        print(f"{row['timestamp']} PM2.5={pm25} PM10={pm10} Temp={temp} Hum={hum} AQI={aqi} ({category})")
        if category in ('Poor','Unhealthy','Hazardous'):
            print('ALERT:', category)
        time.sleep(interval)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=['normal','moderate','smoke','hazardous','temp_hum'], default='normal')
    parser.add_argument('--samples', type=int, default=20)
    parser.add_argument('--interval', type=float, default=0.5)
    parser.add_argument('--seed', type=int, default=None)
    args = parser.parse_args()
    run(args.mode, samples=args.samples, interval=args.interval, seed=args.seed)
