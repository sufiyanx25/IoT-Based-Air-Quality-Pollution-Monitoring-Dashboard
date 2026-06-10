ESP32 firmware (real sensor)

Files:
- `esp32_aqi_real.ino` — Reads MQ135 (analog) and DHT22, classifies AQI, triggers LED/buzzer, posts to ThingSpeak optionally.

Wiring summary (see ../circuit_diagram/CONNECTIONS.md for details):
- MQ135 AO -> voltage divider -> `GPIO34` (ADC1)
- DHT22 DATA -> `GPIO4`, VCC -> 3.3V, pull-up 4.7k
- LED -> `GPIO2` -> 220Ω -> LED -> GND
- Buzzer -> transistor controlled by `GPIO16` (or direct if 3.3V-rated)

How to use:
1. Open `esp32_aqi_real.ino` in Arduino IDE.
2. Replace `WIFI_SSID`, `WIFI_PASS`, and `THINGSPEAK_API_KEY` if you want cloud posting.
3. Select the correct ESP32 board and COM port.
4. Upload and open Serial Monitor at 115200 baud.

Notes:
- Calibrate the MQ135 sensor following the datasheet; the conversion in this sketch is for demonstration only.
- Keep MQ sensors powered for at least 24 hours when doing calibration for best stability.
