Circuit wiring guide — ESP32 build

Overview
This document explains wiring for common components used in the project. Use the example pin assignments below; you can change GPIOs but keep ADC pins and I2C pins consistent with ESP32 rules.

Recommended example pin mapping (ESP32 Dev Module)
- MQ135 (analog): ADC1_CH6 -> GPIO34
- DHT11/DHT22 (digital): GPIO4
- Buzzer (control via transistor): GPIO16
- LED (status): GPIO2
- OLED (I2C): SDA=GPIO21, SCL=GPIO22

Important safety notes
- Common ground: connect all module grounds to the ESP32 ground.
- Level shifting: MQ modules often run at 5V. Never feed >3.3V directly into ESP32 ADC pins — use a voltage divider or amplifier with 3.3V-safe output.
- Use a regulated 5V/3.3V power supply with sufficient current for sensor heaters (MQ series consume heater current).

1) ESP32 → MQ135 (analog gas sensor, module with analog output)
- MQ135 module pins: `VCC`, `GND`, `AO` (analog out), sometimes `DO`.
- Wiring:
  - `VCC` -> 5V (VIN on USB-powered ESP32 or separate 5V supply)
  - `GND` -> GND
  - `AO` -> Voltage divider -> `GPIO34` (ADC1 input)
- Voltage divider (example): Rtop = 10 kΩ, Rbot = 20 kΩ between AO and GND to scale 0–5V to ≈0–3.33V.
  - Connect AO to Rtop; other end of Rtop to ADC pin; ADC pin to Rbot; other end of Rbot to GND. (Or simpler: AO -> divider -> ADC pin, where ADC pin sees ≤3.3V.)
- Notes:
  - Use ADC1 pins (GPIO32–39) for reliable readings while Wi‑Fi is active.
  - Calibrate sensor in fresh air and compute Rs/Ro as per MQ datasheet; readings require warm-up (~24–48 hours for first calibration).

2) ESP32 → DHT11 / DHT22 (temperature & humidity)
- Wiring (single-wire protocol):
  - `VCC` -> 3.3V (DHT22 works on 3.3V; DHT11 often works too but check spec)
  - `GND` -> GND
  - `DATA` -> `GPIO4`
  - Add pull-up resistor: 4.7 kΩ — 10 kΩ between `DATA` and 3.3V.
- Notes:
  - Place a small 0.1 µF decoupling capacitor between VCC and GND near the sensor for stability.
  - DHT timing is sensitive; use a well-tested DHT library and allow 1–2s between reads.

3) ESP32 → Buzzer (active/passive)
- If using a low-current active buzzer that accepts 3.3V: you can drive it directly from GPIO through a resistor, but using a transistor is safer.
- Recommended (transistor) wiring:
  - Buzzer positive `+` -> 5V (or 3.3V if buzzer rated for it)
  - Buzzer negative `-` -> Collector of NPN transistor (e.g., 2N2222)
  - Emitter -> GND
  - ESP32 `GPIO16` -> 1 kΩ resistor -> transistor base
  - Add base-emitter resistor 10 kΩ (optional) to ensure transistor off
  - Add a diode across the buzzer if it's an inductive device (place diode cathode to +V, anode to collector)
- If buzzer is active and 3.3V-rated, you may instead connect: `GPIO16` -> 220 Ω -> buzzer positive, buzzer negative -> GND. Only do this for very low-current buzzers.

4) ESP32 → LED (status indicator)
- Wiring (single LED):
  - `GPIO2` -> 220 Ω resistor -> LED anode
  - LED cathode -> GND
- For multiple LEDs or 5V LEDs, use transistors or MOSFETs and a common 5V supply.

5) Optional: ESP32 → OLED (SSD1306 I2C 128x64) or I2C LCD backpack
- Wiring (I2C):
  - `VCC` -> 3.3V
  - `GND` -> GND
  - `SDA` -> `GPIO21` (default ESP32 I2C SDA)
  - `SCL` -> `GPIO22` (default ESP32 I2C SCL)
- Notes:
  - Most SSD1306 modules are 3.3V-safe; verify the module VCC tolerance before using 5V.
  - If using multiple I2C devices, ensure each device has a unique address or an address jumper is set.

General tips and troubleshooting
- Always tie sensor GNDs to ESP32 GND.
- Use ADC1 pins (GPIO32–39) for analog sensors when Wi‑Fi is active; ADC2 pins are shared with Wi‑Fi and can give unreliable results.
- If an MQ sensor is powered at 5V, route its analog output through a divider or use an op-amp to shift to 3.3V.
- Add small capacitors (0.1 µF) across power rails near sensors to stabilize readings.
- Start with simple serial-print sketches (like `esp32_aqi_sim.ino`) to verify each sensor before integrating into the full system.

Example quick-check wiring table (summary)
- MQ135: `5V` -> `VCC`, `GND` -> `GND`, `AO` -> `Voltage divider` -> `GPIO34` (ADC1)
- DHT22: `3.3V` -> `VCC`, `GND` -> `GND`, `DATA` -> `GPIO4` + `10k` pull-up to 3.3V
- Buzzer (via transistor): `+` -> `5V`, `-` -> `Collector`, `Emitter` -> `GND`, `GPIO16` -> `1k` -> `Base`
- LED: `GPIO2` -> `220Ω` -> LED -> `GND`
- OLED (I2C): `3.3V`, `GND`, `SDA`->`GPIO21`, `SCL`->`GPIO22`

Files to add to repo
- `circuit_diagram/CONNECTIONS.md` (this file)
- Optionally a `circuit_diagram/export/` folder to store PNG/SVG schematic exports from Fritzing or KiCad.

If you want, I can now:
- Generate a Fritzing-style breadboard wiring diagram as an SVG (text description + suggested positions), or
- Produce a formal KiCad schematic file (requires more inputs).

Which diagram format do you prefer?