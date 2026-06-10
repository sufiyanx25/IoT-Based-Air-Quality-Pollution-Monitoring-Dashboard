Phase 1 — Environment setup

Objective
- Prepare a development environment to build and upload ESP32 firmware, and to run the dashboard simulation locally.

Prerequisites
- Windows PC (you already use PowerShell)
- USB cable for ESP32
- Internet access to download tools and libraries

1) Arduino IDE (quick, recommended)
- Download and install the latest Arduino IDE for Windows from the Arduino website.
- Open Arduino IDE → File → Preferences → Additional Boards Manager URLs and add:

  https://dl.espressif.com/dl/package_esp32_index.json

- Open Tools → Board → Boards Manager, search "esp32" and install "esp32 by Espressif Systems".
- Select board: Tools → Board → "ESP32 Dev Module" (or your specific board).
- Select port: Tools → Port → COMx

2) Drivers (Windows)
- If your board uses CP210x: install Silicon Labs CP210x USB to UART drivers.
- If your board uses CH340: install CH340 drivers.
- After installing, reconnect board and confirm a COM port appears.

3) VS Code + PlatformIO (alternative / advanced)
- Install Visual Studio Code.
- Install the PlatformIO IDE extension from the Extensions view.
- PlatformIO supports project management, libraries, and serial monitor integrated with VS Code.

4) Required Arduino libraries
- In Arduino IDE: Sketch → Include Library → Manage Libraries
  - "DHT sensor library" by Adafruit (if using DHT)
  - "Adafruit Unified Sensor" (dependency)
  - "ThingSpeak" (if using ThingSpeak)
  - "ArduinoJson" (optional for JSON handling)
- In PlatformIO, add libs via `platformio.ini` or the library manager.

5) Verify board connectivity with Blink
- Open a simple Blink sketch for ESP32 and upload. Example snippet below (use in Arduino IDE):

  ```cpp
  void setup() {
    pinMode(2, OUTPUT);
  }
  void loop() {
    digitalWrite(2, HIGH);
    delay(500);
    digitalWrite(2, LOW);
    delay(500);
  }
  ```

- Confirm on the board the onboard LED blinks (pin may vary by board; try 2 or LED_BUILTIN).

6) Serial monitor test
- In Arduino IDE select baud 115200 and open Serial Monitor.
- Upload a sketch that prints a message to Serial to confirm communication.

7) ThingSpeak / Blynk setup (optional now)
- ThingSpeak: create an account, create a channel, note the Write API Key.
- Blynk: create project in Blynk app, obtain Auth Token.

8) Notes and troubleshooting
- If uploads fail, check:
  - Correct COM port selected
  - Correct board selected
  - Drivers installed
  - USB cable supports data (some are power-only)
- If using PlatformIO, run `pio update` to refresh libraries.

Next: upload the starter ESP32 sketch in `firmware/esp32_aqi_sim.ino` and test serial output and ThingSpeak updates (if you configured API key).