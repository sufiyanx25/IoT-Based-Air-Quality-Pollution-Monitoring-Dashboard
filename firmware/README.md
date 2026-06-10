ESP32 firmware — quick start

Files:
- `esp32_aqi_sim.ino` — starter firmware that simulates sensor data and (optionally) posts to ThingSpeak.

Steps to run
1. Open `esp32_aqi_sim.ino` in Arduino IDE (or import into PlatformIO).
2. Replace `WIFI_SSID`, `WIFI_PASS`, and `THINGSPEAK_API_KEY` with your credentials.
3. Select the correct ESP32 board and COM port.
4. Upload the sketch.
5. Open Serial Monitor at 115200 baud to see simulated readings.

Notes
- This is a simulation sketch to allow development of the dashboard and testing without physical sensors.
- When ready, replace the simulated readings with real sensor reads (analog or digital) and adapt field mapping accordingly.
