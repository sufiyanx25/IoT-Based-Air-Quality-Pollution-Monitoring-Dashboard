# 4️⃣ Hardware Components & Detailed Specifications

---

## 🎯 Overview: What Each Component Does

Before diving into details, here's a quick overview of the system:

```
SENSOR INPUTS (Read Air Quality)
    ↓
MICROCONTROLLER (Process Data)
    ↓
DISPLAY (Show Results)
    ↓
ALERTS (Buzzer, LEDs, WiFi)
    ↓
CLOUD (Send to Internet)
```

Let me explain each component in detail:

---

## 1️⃣ **ESP32 Development Board** (Brain of the System)

### 🎯 **Purpose**
The ESP32 is the **central microcontroller** that:
- Reads sensor data (temperature, humidity, air quality)
- Processes the data (calculates AQI, detects anomalies)
- Controls output devices (LEDs, buzzer, display)
- Communicates with the cloud (WiFi)
- Makes decisions (when to alert, when to update)

### 🔧 **Key Specifications**

```
PROCESSOR:
├─ Dual-core 32-bit Xtensa LX6
├─ Clock speed: 240 MHz
└─ Very fast for sensor processing

MEMORY:
├─ RAM: 520 KB SRAM
├─ Flash: 4-16 MB (depends on model)
└─ Enough to store sensor data locally

CONNECTIVITY (Built-in!):
├─ WiFi 802.11 b/g/n (up to 150 Mbps)
├─ Bluetooth 4.2
└─ Can send data to cloud without extra module

GPIO PINS:
├─ 34 total GPIO pins
├─ 12 ADC (Analog-to-Digital Converter) channels
│  └─ For reading analog sensors (MQ135, MQ7, DHT11)
├─ 2 DAC (Digital-to-Analog) outputs
└─ SPI, I2C, UART interfaces
   └─ For communicating with sensors

POWER:
├─ Operating voltage: 3.3V (with 5V input regulation)
├─ Current consumption: 80-160 mA (WiFi active)
└─ Can be powered via Micro USB or direct 5V input

PROGRAMMING:
├─ Compatible with Arduino IDE (easy!)
├─ Supports MicroPython
└─ Extensive library ecosystem
```

### 📊 **ESP32 Pinout for Our Project**

```
ESP32 30-PIN DEVELOPMENT BOARD

                    USB (Micro)
                        │
                   ┌────┴────┐
                   │          │
    ┌──────────────┤          ├──────────────┐
    │              │          │              │
    │  [GND]────────┤          ├─── [3.3V]   │
    │  [D34]────────┤ ESP32    ├─── [D35]    │
    │  [D35]────────┤ 30-pin   ├─── [D36]    │
    │  [D36]────────┤  Board   ├─── [D39]    │
    │  [D39]────────┤          ├─── [GND]    │
    │  [GND]────────┤          ├─── [D4]     │
    │  [D4]─────────┤          ├─── [D2]     │
    │  [D2]─────────┤          ├─── [D15]    │
    │  [D15]────────┤          ├─── [D13]    │
    │  [D13]────────┤          ├─── [D12]    │
    │  [D12]────────┤          ├─── [D14]    │
    │  [D14]────────┤          ├─── [D27]    │
    │  [D27]────────┤          ├─── [D26]    │
    │  [D26]────────┤          ├─── [D25]    │
    │  [D25]────────┤          ├─── [D33]    │
    │  [D33]────────┤          ├─── [D32]    │
    │  [D32]────────┤          ├─── [GND]    │
    │  [GND]────────┤          ├─── [5V]     │
    │               │          │              │
    │               └──────────┘              │
    │                                         │
    └─────────────────────────────────────────┘

PINS FOR OUR PROJECT:
├─ GPIO 32 (ADC): MQ135 AQI sensor
├─ GPIO 33 (ADC): MQ7 CO sensor
├─ GPIO 34 (ADC): PM2.5 sensor
├─ GPIO 21 (SDA): DHT11 I2C data
├─ GPIO 22 (SCL): DHT11 I2C clock
├─ GPIO 16 (RX2): CO₂ sensor (optional)
├─ GPIO 17 (TX2): CO₂ sensor (optional)
├─ GPIO 5: OLED display (SPI CLK)
├─ GPIO 18: OLED display (SPI MOSI)
├─ GPIO 19: OLED display (SPI MISO)
├─ GPIO 4: Buzzer alert
├─ GPIO 2: LED Green (Good air)
├─ GPIO 15: LED Yellow (Moderate)
├─ GPIO 27: LED Red (Unhealthy)
├─ GND: Ground (common return)
└─ 5V: Power input (via USB or external)
```

### 💡 **Why ESP32 Over Arduino?**

```
Arduino Uno                 vs    ESP32
────────────────────────────────────────────
8-bit processor             32-bit processor ✅
16 MHz speed                240 MHz speed ✅
32 KB RAM                   520 KB RAM ✅
Needs WiFi shield ($$$)     WiFi Built-in ✅
Limited sensors             34 GPIO pins ✅
Lower cost                  Higher value
```

### 🔄 **How It Connects in Our System**

```
┌─────────────────────────────────┐
│        SENSORS (Input)          │
│  ├─ MQ135 (ADC-32)              │
│  ├─ MQ7 (ADC-33)                │
│  ├─ DHT11 (GPIO-21)             │
│  └─ PM2.5 (ADC-34)              │
└────────────┬────────────────────┘
             │ Analog/Digital signals
             ↓
    ┌────────────────────┐
    │      ESP32         │
    │  (This component!)  │
    │  ├─ ADC converter   │
    │  ├─ Data processor  │
    │  ├─ Logic controller│
    │  └─ WiFi transmitter│
    └────────┬───────────┘
             │ Control signals
             ↓
┌─────────────────────────────────┐
│       OUTPUTS (Display/Alert)   │
│  ├─ OLED display (GPIO-5)       │
│  ├─ Buzzer (GPIO-4)             │
│  └─ LEDs (GPIO-2,15,27)         │
└─────────────────────────────────┘
```

### 📦 **Physical Specifications**

```
Dimensions: 54mm × 26mm × 13mm (very compact!)
Weight: 11g
Operating Temperature: -40°C to +85°C
Can be mounted on breadboard (30-pin)
```

### 🛒 **Cost & Availability**

```
ESP32 (30-pin development board):
├─ India: ₹500-700 (Amazon, Robocraze, Flipkart)
├─ Global: $8-15 (AliExpress, eBay)
├─ Bulk: ₹350-400 per unit (for 10+)
└─ Includes USB cable usually

Why not Arduino?
Arduino Uno: ₹400 + WiFi Shield ₹800 = ₹1200
ESP32: ₹600 (WiFi included)
→ ESP32 saves money AND is more powerful!
```

---

## 2️⃣ **MQ135 Air Quality Sensor**

### 🎯 **Purpose**
The MQ135 detects **overall air quality** by measuring:
- **CO₂** (carbon dioxide) - from breathing, combustion
- **CO** (carbon monoxide) - toxic gas from vehicles, fires
- **NH₃** (ammonia) - from decomposition, industrial
- **NOₓ** (nitrogen oxides) - from vehicles, factories
- **Smoke** - from fires, cigarettes
- **Alcohol vapors** - from spills, fermentation

### 🔧 **How It Works**

```
SENSOR MECHANISM:

┌────────────────────────────────────┐
│  MQ135 Sensor (looks like a screw) │
│                                    │
│  Heating Element (gets hot to ~200°C)
│         ↓
│  SnO₂ (Tin Oxide) Material
│  └─ SENSITIVE TO POLLUTANTS
│
│  When pollutants present:
│  ├─ Material absorbs gas molecules
│  ├─ Resistance DECREASES
│  ├─ Current flow INCREASES
│  └─ Arduino reads higher voltage
│
│  Without pollutants:
│  └─ High resistance, low voltage
│
└────────────────────────────────────┘

CHARACTERISTIC RESPONSE:

Voltage Output:
Clean air:     0.3-0.5V (low)  → AQI ~50 (GOOD)
Moderate:      1.0-2.0V        → AQI ~100 (MODERATE)
Poor:          3.0-4.0V        → AQI ~200 (UNHEALTHY)
Very Bad:      4.0-5.0V (high) → AQI ~300+ (HAZARDOUS)
```

### 📊 **Specifications**

```
SENSOR TYPE:        Semiconductor gas sensor
DETECTION RANGE:    10 ppm - 10,000 ppm (adjustable)
RESPONSE TIME:      < 10 seconds
OPERATING VOLTAGE:  5V DC
CURRENT:            ~150 mA (heater active)
PREHEATING TIME:    5-10 minutes (for accuracy)
LIFESPAN:           ~5-10 years
COST:               ₹400-600 per unit
```

### 🔌 **Pin Configuration**

```
MQ135 Module (Breakout Board):

      ┌─────────────┐
      │  MQ135      │
      │  Module     │
      └─────────────┘
           │
      ┌────┼────┐
      │    │    │
    [A0] [GND] [5V]

CONNECTIONS:
├─ A0 (Analog Out) → ESP32 GPIO 32 (ADC input)
│  └─ Sends voltage (0-5V) proportional to pollution
├─ GND → ESP32 GND (common ground)
└─ 5V → ESP32 5V (power input)
```

### 📈 **Sensor Response Curve**

```
Voltage vs AQI Relationship (Typical):

Voltage (V)
   5V  │         ╱╱╱╱╱╱╱╱
        │        ╱╱
   4V  │       ╱╱
        │      ╱╱
   3V  │     ╱╱
        │    ╱╱
   2V  │   ╱╱
        │  ╱╱
   1V  │ ╱╱
        │╱╱
   0V  ├─────────────────────
        0   50  100  150  200  AQI

Formula (Approximate):
AQI = (Voltage / 5) × 500
Example: 3V → (3/5) × 500 = 300 AQI ✓
```

### ⚠️ **Important Calibration Note**

```
MQ135 CALIBRATION:
The sensor is VERY SENSITIVE and requires calibration:

STEPS:
1. Let sensor warm up: 5-10 minutes
2. In CLEAN AIR (outdoor, away from traffic):
   └─ Record voltage reading (e.g., 0.4V)
   
3. Use this as BASELINE for calibration:
   ├─ Calibration Voltage = 0.4V
   ├─ Readings < 0.4V = Very clean
   ├─ Readings = 0.4V = Baseline
   └─ Readings > 0.4V = Polluted

CALIBRATION CODE:
float calibrationVoltage = 0.4;  // From clean air reading
float rawVoltage = analogRead(MQ135_PIN) / 4095.0 * 5.0;
float ratio = rawVoltage / calibrationVoltage;

// AQI calculation (simplified)
float AQI = (ratio - 1) * 500 + 50;
```

### 💡 **Why Include MQ135?**

✅ Detects multiple pollutants at once
✅ Affordable sensor
✅ Widely available
✅ Shows overall air quality trend
⚠️ Requires calibration
⚠️ Not super accurate (±5-10%)
→ **Good for student project, not lab-grade**

---

## 3️⃣ **MQ7 Carbon Monoxide Sensor** (Optional)

### 🎯 **Purpose**
The MQ7 detects **Carbon Monoxide (CO)** specifically:
- CO from vehicle exhaust (major pollution)
- CO from fires, faulty appliances
- Extremely toxic at high concentrations
- Can cause headaches, unconsciousness, death

### 🔧 **How It Works**

```
OPERATING PRINCIPLE:

MQ7 Heating Cycle:
├─ High temp (90°C): Detects CO and other gases
├─ Low temp (60°C): Removes interference compounds
└─ Cycle repeats every ~60 seconds

Result:
└─ More accurate CO measurement than MQ135

SENSITIVITY:
┌─────────────────────────────────┐
│  CO Concentration → Voltage     │
├─────────────────────────────────┤
│  < 10 ppm (SAFE)    → < 0.5V   │
│  10-50 ppm          → 1.0-2.0V │
│  50-100 ppm (ALERT) → 2.0-3.0V │
│  > 100 ppm (DANGER) → > 3.0V   │
└─────────────────────────────────┘
```

### 📊 **Specifications**

```
SENSOR TYPE:        Semiconductor with cycle heating
DETECTION RANGE:    10 ppm - 10,000 ppm
RESPONSE TIME:      < 10 seconds (after heating)
OPERATING VOLTAGE:  5V DC
HEATER CURRENT:     ~150 mA (cycling)
PREHEATING TIME:    1-2 minutes
LIFESPAN:           ~5-10 years
COST:               ₹400-600 per unit
```

### 🔌 **Pin Configuration**

```
MQ7 Module:

      ┌─────────────┐
      │   MQ7       │
      │   Module    │
      └─────────────┘
           │
      ┌────┼────┐
      │    │    │
    [A0] [GND] [5V]

CONNECTIONS:
├─ A0 (Analog Out) → ESP32 GPIO 33 (ADC input)
├─ GND → ESP32 GND
└─ 5V → ESP32 5V

NOTE: Can also use GPIO 27 for heating cycle control
(advanced temperature cycling for accuracy)
```

### ⚠️ **Why It's Optional**

```
With MQ135 (detects CO):
├─ Basic CO detection covered
├─ Budget constraint ($600)
└─ Limited pins on breadboard

With MQ135 + MQ7:
├─ Separate CO sensor (more accurate)
├─ Can distinguish CO from other gases
├─ Better for traffic pollution monitoring
└─ Budget: ₹800-1200 (additional)

RECOMMENDATION:
If budget allows: Include MQ7
If budget tight: MQ135 is sufficient
```

---

## 4️⃣ **DHT11/DHT22 Temperature & Humidity Sensor**

### 🎯 **Purpose**
DHT sensors measure:
- **Temperature** (-40°C to +80°C)
- **Humidity** (0-100% RH)

Why needed for air quality?
1. **Health correlation**: Heat + humidity + pollution = worse effects
2. **Thermal inversion**: Cold nights trap pollution near ground
3. **Sensor calibration**: Temperature affects sensor readings
4. **Environmental analysis**: Complete environmental picture

### 🔧 **How It Works**

```
SENSOR MECHANISM:

DHT11/DHT22 Package:
│
├─ Humidity Sensing: Polymer material changes resistance with moisture
│
├─ Temperature Sensing: Thermistor (NTC resistor)
│  └─ Resistance changes inversely with temperature
│
├─ Digital Output: Built-in microcontroller
│  └─ Converts readings to digital signal
│
└─ Protocol: One-wire serial communication
   └─ Sends both values in single message


TIMING DIAGRAM:
Microcontroller → Send START signal
                ↓ (25ms wait)
DHT11 → Send 40 bits of data
        ├─ 8 bits humidity integer
        ├─ 8 bits humidity decimal
        ├─ 8 bits temperature integer
        ├─ 8 bits temperature decimal
        └─ 8 bits checksum

Time: ~2.4 milliseconds total
```

### 📊 **Specifications Comparison**

```
                DHT11               DHT22
────────────────────────────────────────────────
Temperature    0°C to +50°C      -40°C to +80°C ✅
Range          ±2°C accuracy      ±0.5°C accuracy ✅

Humidity       20% to 80%         0% to 100% ✅
Range          ±5% accuracy       ±2% accuracy ✅

Response Time  ~5 seconds          ~2 seconds ✅
               (slower)            (faster)

Cost           ₹100-150           ₹200-300
               (cheaper)          (expensive)

Lifespan       ~1-2 years         ~3-5 years ✅

RECOMMENDATION:
Use DHT11 for: Budget projects, classroom use
Use DHT22 for: Professional deployment, long-term
For student: DHT11 is sufficient ✓
```

### 🔌 **Pin Configuration**

```
DHT11 / DHT22 Module (3-pin):

   ┌──────────┐
   │  DHT11   │
   │ (3-pin)  │
   └──────────┘
       │││
       │││
    [1][2][3]
     │  │  │
     │  │  └─ GND
     │  └──── Data (1-wire)
     └─────── 5V

CONNECTIONS (Common):
├─ Pin 1 (5V)   → ESP32 5V
├─ Pin 2 (Data) → ESP32 GPIO 21 (with 10kΩ pull-up resistor)
└─ Pin 3 (GND)  → ESP32 GND

Pull-up Resistor:
Why needed? One-wire protocol requires pull-up
├─ Connect 10kΩ resistor between Data pin and 5V
└─ Helps signal transitions cleanly
```

### 📈 **Reading Values**

```
DHT Sensor Output Example:

Temperature: 28.5°C
Humidity: 65%

FORMULA (approximately):
Actual Temp = Sensor Reading ± 2°C
Actual Humidity = Sensor Reading ± 5%

In code:
float temp = dht.readTemperature();   // Returns 28.5
float humidity = dht.readHumidity();  // Returns 65.0

Interpretation:
├─ Temp 15-25°C: Cool (better air dispersion)
├─ Temp 25-35°C: Warm (pollution stagnates)
├─ Humidity 30-60%: Optimal (avoid extremes)
├─ Humidity <30%: Dry (health issues)
└─ Humidity >70%: Very humid (mold, discomfort)
```

### 💡 **Why Include Temperature & Humidity?**

✅ Part of complete environmental monitoring
✅ Improves sensor calibration
✅ Shows thermal inversion (traps pollution)
✅ Correlates with health impacts
✅ Very affordable (₹100-300)
✅ Widely available and well-documented

---

## 5️⃣ **OLED Display** (Optional but Recommended)

### 🎯 **Purpose**
Shows real-time data locally on device:
- Air quality status
- Current readings
- Alerts and warnings
- No need for phone/computer

### 🔧 **How It Works**

```
OLED = Organic Light-Emitting Diode

Each pixel emits its own light:
┌─────────────────────────────┐
│ OLED Display (0.96" or 1.3")│
│                             │
│ Each pixel has:             │
│ ├─ Red component            │
│ ├─ Green component          │
│ └─ Blue component           │
│ → Can display any color!    │
│                             │
│ Resolution: 128×64 pixels   │
│ (Perfect for small data)    │
└─────────────────────────────┘

ADVANTAGES:
├─ Bright (visible in sunlight)
├─ Low power (better than LCD)
├─ Fast refresh (updates smoothly)
├─ Small size (compact)
└─ Good color reproduction
```

### 📊 **Display Example**

```
OLED Display Output:

┌────────────────────────────────┐
│   AIR QUALITY MONITOR         │
│   ─────────────────────────   │
│                               │
│   AQI: 98  MODERATE           │
│   ▓▓▓▓▓░░░░░░░░░░░░░░░░       │
│                               │
│   PM2.5: 45.3 μg/m³           │
│   CO: 2.1 ppm                 │
│   Temp: 28°C  Humidity: 65%   │
│                               │
│   Last: 14:32:18              │
│                               │
└────────────────────────────────┘
```

### 📊 **Specifications**

```
OLED MODULE:         0.96" I2C OLED
RESOLUTION:          128×64 pixels
COLOR:               Monochrome (White/Blue/Yellow)
INTERFACE:           I2C (2-wire: SCL, SDA)
OPERATING VOLTAGE:   3.3V (ESP32 compatible!)
CURRENT:             ~20 mA (low power)
RESPONSE TIME:       Instant
LIFESPAN:            10,000-100,000 hours
COST:                ₹400-600 per module
```

### 🔌 **Pin Configuration**

```
0.96" OLED Module (4-pin I2C):

   ┌──────────────┐
   │   OLED       │
   │  0.96" I2C   │
   └──────────────┘
      ││││
      ││││
  [G][D][C][+]
   │  │  │  │
   │  │  │  └─ 3.3V → ESP32 3.3V
   │  │  └──── SCL → ESP32 GPIO 22
   │  └─────── SDA → ESP32 GPIO 21
   └────────── GND → ESP32 GND

NOTE: GPIO 21 & 22 are same as DHT11!
How to connect both?
├─ Use I2C multiplexer (₹100)
├─ Or use different DHT11 pin
└─ Or power one at a time (time-multiplex)
```

### 💡 **Advantages & Disadvantages**

```
ADVANTAGES:
✅ See data without phone/computer
✅ Real-time feedback
✅ Useful for debugging
✅ Professional appearance
✅ Can show alerts immediately

DISADVANTAGES:
❌ Additional cost (₹400-600)
❌ Takes up pins (I2C interface)
❌ Small text can be hard to read
❌ Power consumption

RECOMMENDATION:
Optional but HIGHLY RECOMMENDED
Costs only ₹400-600 and greatly improves usability
```

### 🔧 **Display Libraries**

```cpp
// Arduino library for OLED:
#include <Adafruit_SSD1306.h>

// Initialize display
Adafruit_SSD1306 display(128, 64, &Wire, -1);

// Display text
display.clearDisplay();
display.setTextSize(1);
display.setCursor(0, 0);
display.println("AQI: 98");
display.display();
```

---

## 6️⃣ **Buzzer** (Alert Speaker)

### 🎯 **Purpose**
Provides **audible alert** when:
- Air quality exceeds dangerous levels
- Sensor malfunction detected
- System errors occur
- Can be heard even if display/phone not visible

### 🔧 **How It Works**

```
BUZZER MECHANISM:

Passive Buzzer (Needs frequency signal):
├─ Piezo element + oscillation circuit
├─ Apply AC voltage at specific frequency
└─ Element vibrates → Produces sound

Active Buzzer (Simpler):
├─ Built-in oscillation circuit
├─ Just apply DC voltage
├─ Automatically generates tone
└─ **RECOMMENDED for this project**

Sound Output:
Frequency: 2-4 kHz (audible to most people)
Volume: ~85-90 dB (loud enough to notice)
Cost: ₹20-50 (very cheap!)
```

### 📊 **Specifications**

```
BUZZER TYPE:         Active (with built-in circuit)
OPERATING VOLTAGE:   5V DC
CURRENT DRAW:        ~20 mA
FREQUENCY:           ~2.5 kHz
SOUND LEVEL:         85-90 dB SPL
DIMENSIONS:          9mm × 9mm (very small)
LIFESPAN:            10,000+ hours
COST:                ₹20-50 per unit
```

### 🔌 **Pin Configuration**

```
Active Buzzer (2-pin):

   ┌──────────┐
   │ Buzzer   │
   │ (Active) │
   └──────────┘
      ││
      ││
    [+][-]
     │  │
     │  └─ GND → ESP32 GND
     └───── Positive → ESP32 GPIO 4

CIRCUIT:
ESP32 GPIO 4 ─────[Buzzer+]
                    │
              [Buzzer-]
                    │
               ESP32 GND

CONTROL:
├─ digitalWrite(BUZZER_PIN, HIGH)  → Buzzer ON
├─ digitalWrite(BUZZER_PIN, LOW)   → Buzzer OFF
└─ Can use PWM for volume control
```

### 🔔 **Alert Patterns**

```
DIFFERENT PATTERNS FOR DIFFERENT ALERTS:

Good Air (AQI < 50):
└─ No beeping

Moderate (AQI 50-100):
└─ Slow bip...bip...bip (every 5 seconds)

Unhealthy (AQI 100-150):
└─ Faster bip-bip-bip (every 2 seconds)

Unhealthy for All (AQI 150-200):
└─ Fast BIP-BIP-BIP (every 1 second)

Hazardous (AQI > 200):
└─ CONTINUOUS BEEPING! 🚨

CODE EXAMPLE:
void alertBuzzer(int aqi) {
  if (aqi > 200) {
    digitalWrite(BUZZER_PIN, HIGH);  // ON
    delay(100);
    digitalWrite(BUZZER_PIN, LOW);   // OFF
    delay(100);
    // Repeat continuously
  } else if (aqi > 150) {
    digitalWrite(BUZZER_PIN, HIGH);
    delay(200);
    digitalWrite(BUZZER_PIN, LOW);
    delay(800);
  }
  // ... more patterns
}
```

### 💡 **Why Include Buzzer?**

✅ Immediate audible feedback
✅ Alerts even when looking away
✅ Very cheap (₹20-50)
✅ Low power consumption
✅ Improves user safety
✅ Professional feel

---

## 7️⃣ **LED Indicators** (Status Lights)

### 🎯 **Purpose**
Provides **visual status** at a glance:
- 🟢 Green: Air quality is GOOD
- 🟡 Yellow: Air quality is MODERATE
- 🔴 Red: Air quality is UNHEALTHY

### 🔧 **How It Works**

```
LED PHYSICS:

LED = Light-Emitting Diode
├─ Semiconductor that emits light when current flows
├─ Only works in one direction (anode to cathode)
├─ Needs current-limiting resistor (protection)
└─ Very long lifespan (10,000+ hours)

LED COLORS:
┌─────────────────────────────┐
│ Color   │ Voltage | Cost    │
├─────────────────────────────┤
│ Red     │ 2.0V    │ ₹5      │
│ Yellow  │ 2.0V    │ ₹5      │
│ Green   │ 2.2V    │ ₹5      │
│ Blue    │ 3.0V    │ ₹10     │
└─────────────────────────────┘

BRIGHTNESS CONTROL:
Can use PWM (Pulse Width Modulation) to:
├─ Fade LEDs in/out
├─ Show intensity (brighter = worse air)
└─ Create visual effects
```

### 📊 **Specifications**

```
LED TYPE:            Standard 5mm LEDs
OPERATING VOLTAGE:   2.0-2.2V (Red, Yellow, Green)
FORWARD CURRENT:     20 mA (typical)
LIMITING RESISTOR:   220Ω (470Ω also works)
LIFESPAN:            10,000-100,000 hours
COST:                ₹5-10 per LED

RESISTOR CALCULATION:
Needed current = 20 mA
ESP32 output = 3.3V

R = (Vin - Vled) / I
  = (3.3V - 2.0V) / 0.020A
  = 1.3V / 0.020A
  = 65Ω

Standard resistor: 220Ω (safe, dimmer)
                   470Ω (even dimmer)
                   100Ω (brighter)
```

### 🔌 **Pin Configuration**

```
Three LEDs Circuit:

GREEN LED:
  [220Ω Resistor] ─┐
                   ├─[Green LED]─ ESP32 GPIO 2
                   │
              ESP32 GND ────────────┘

YELLOW LED:
  [220Ω Resistor] ─┐
                   ├─[Yellow LED]─ ESP32 GPIO 15
                   │
              ESP32 GND ────────────┘

RED LED:
  [220Ω Resistor] ─┐
                   ├─[Red LED]─ ESP32 GPIO 27
                   │
              ESP32 GND ────────────┘

BREADBOARD LAYOUT:
┌──────────────────────────────────┐
│ Green LED  Yellow LED  Red LED   │
│    │          │          │       │
│    R          R          R       │
│    │          │          │       │
│   D2         D15        D27      │
│    └──────────┴──────────┘       │
│           ESP32 GND              │
└──────────────────────────────────┘
```

### 🎨 **LED Logic**

```
LED CONTROL BASED ON AQI:

if (AQI <= 50) {
  digitalWrite(GREEN, HIGH);
  digitalWrite(YELLOW, LOW);
  digitalWrite(RED, LOW);
  // Show GREEN only
}
else if (AQI <= 100) {
  digitalWrite(GREEN, LOW);
  digitalWrite(YELLOW, HIGH);
  digitalWrite(RED, LOW);
  // Show YELLOW only
}
else {
  digitalWrite(GREEN, LOW);
  digitalWrite(YELLOW, LOW);
  digitalWrite(RED, HIGH);
  // Show RED only
}

ADVANCED: LED BLINKING

Red alert (blink if unhealthy):
void blinkRed() {
  digitalWrite(RED, HIGH);   // ON
  delay(500);
  digitalWrite(RED, LOW);    // OFF
  delay(500);
  // Repeats, creates blinking effect
}

// More serious alert = faster blinking
```

### 💡 **Why Include LEDs?**

✅ Instant visual feedback
✅ No power overhead
✅ Very cheap (₹5-10 per LED)
✅ Reliable (simple on/off logic)
✅ Can see status from across room
✅ Professional appearance

---

## 8️⃣ **WiFi Module** (Only if Arduino Used)

### 🎯 **Purpose**
Enables **wireless internet connection** (for Arduino only)

### ⚠️ **IMPORTANT: Not Needed for ESP32!**

```
ESP32 has WiFi BUILT-IN ✅
├─ 802.11 b/g/n WiFi support
├─ Dual-band (2.4GHz)
├─ No external module needed
├─ Saves cost, space, power

Arduino Uno does NOT have WiFi ❌
├─ Needs separate WiFi shield
├─ Examples:
│  ├─ WiFi Shield (₹800)
│  ├─ ESP8266 module (₹300-500)
│  └─ GSM module (₹400)
```

### **Since We're Using ESP32:** ✅ WiFi is INCLUDED!

No need to buy extra WiFi module. The ESP32 board itself has WiFi capability built-in.

---

## 9️⃣ **Power Supply**

### 🎯 **Purpose**
Provides electrical power for the entire system

### 📊 **Power Requirements**

```
COMPONENT POWER CONSUMPTION:

ESP32 (Idle):        ~10-30 mA
ESP32 (WiFi Active): ~80-160 mA

DHT11:              ~10 mA
MQ135 Sensor:       ~150 mA (heater)
MQ7 Sensor:         ~150 mA (heater, cycling)
OLED Display:       ~20 mA
Buzzer:             ~20 mA
LEDs (3):           ~5 mA each = 15 mA total

TOTAL MAXIMUM:      ~600 mA (when all devices active)
TYPICAL USAGE:      ~300-400 mA (during normal operation)

SAFETY MARGIN:      1000 mA (1A) power supply recommended
```

### 🔌 **Power Supply Options**

```
OPTION 1: USB Power (Simplest)
├─ Micro USB cable
├─ Connected to laptop/PC
├─ Can provide ~500 mA (USB 2.0 limit)
├─ Or 900+ mA (USB 3.0/Battery charger)
└─ PROS: Free (likely have already), convenient
└─ CONS: Limited range, must stay tethered

OPTION 2: USB Power Bank
├─ Portable battery 5000 mAh+
├─ 5V output via USB
├─ Can power for 8-12 hours
└─ PROS: Wireless, portable, affordable (₹500-1000)
└─ CONS: Battery depletes, need charging

OPTION 3: AC to DC Power Supply
├─ 5V, 2A power adapter (wall plug)
├─ Micro USB connector
├─ Unlimited runtime (plugged into wall)
└─ PROS: Reliable, always on, long-term deployment
└─ CONS: Must be near outlet, ₹300-500

OPTION 4: Solar Powered
├─ 5V solar panel (5-10W)
├─ Charge battery during day
├─ Run system 24/7
└─ PROS: Eco-friendly, independent power
└─ CONS: Expensive (₹2000+), weather dependent
```

### 🔋 **Recommended Power Setup**

For student project:
```
Option 1: Start with USB cable (if near computer)
Option 2: Graduate to USB power bank (for testing)
Option 3: Use AC adapter for permanent installation

SHOPPING:
┌─────────────────────────────────────┐
│ 5V / 2A USB Power Adapter           │
│ ├─ Input: 100-240V AC              │
│ ├─ Output: 5V / 2A DC              │
│ ├─ Type: Micro USB                 │
│ ├─ Cost: ₹300-500                  │
│ └─ Availability: Amazon, Flipkart  │
└─────────────────────────────────────┘
```

### ⚡ **Power Distribution**

```
POWER WIRING DIAGRAM:

USB Power Supply (5V, 2A)
        │
   ┌────┴────┐
   │          │
  +5V        GND
   │          │
   ├─────────┐│
   │         ││
   │    ┌────┘│
   │    │     │
   ├───[+]    ├───[-]
   │    │     │    │
  5V   │     GND   │
   │   │     │     │
   ├─ ESP32 ──────┤
   │ +───────────+│
   │ │           ││
   ├─[Buzzer]   └┤
   │             ││
   ├─[LEDs]──────┘│
   │              ││
   ├─[DHT11]──────┘
   │              │
   └──[Sensors]───┘

KEY POINT: All components share GND (common return)
```

---

## 📋 **COMPLETE COMPONENT CHECKLIST**

### **Essential Components (For Basic System)**

```
✅ MUST HAVE:
├─ ESP32 Development Board (30-pin)     ₹600-700
├─ MQ135 Air Quality Sensor             ₹400-600
├─ DHT11 Temperature/Humidity           ₹100-150
├─ Breadboard (Full-size)               ₹100-150
├─ Jumper Wires (65-piece pack)         ₹80-100
├─ USB Cable (Micro USB)                ₹50-100
├─ Resistors:
│  ├─ 220Ω (for LEDs)                   ₹20
│  └─ 10kΩ (DHT11 pull-up)              ₹20
├─ LEDs (3 colors):
│  ├─ Green LED                         ₹5
│  ├─ Yellow LED                        ₹5
│  └─ Red LED                           ₹5
├─ Buzzer (Active)                      ₹30-50
└─ 5V Power Supply                      ₹300-500

SUBTOTAL ESSENTIAL:          ₹2,000-2,500

⭐ HIGHLY RECOMMENDED (Add if budget):
├─ MQ7 CO Sensor                        ₹400-600
├─ OLED 0.96" I2C Display              ₹400-600
└─ Sensor Breakout Boards               ₹200-300

SUBTOTAL RECOMMENDED:        ₹3,000-4,000

📊 TOTAL SYSTEM (Essential + Recommended):  ₹5,000-6,500
```

### **Supplier Links** (Example - India)

```
AMAZON INDIA:
├─ ESP32 → amazon.in (search "ESP32 board")
├─ MQ135 → amazon.in (search "MQ135 sensor")
├─ DHT11 → amazon.in (search "DHT11 module")
└─ Components Kit → Often available as bundles

ROBOCRAZE.COM:
├─ Complete IoT kits sometimes available
├─ Individual components
└─ Good documentation

FLIPKART:
├─ Electronics components
├─ Sometimes more competitive pricing

ALIEXPRESS.COM (International):
├─ Cheapest prices (but shipping takes 2-4 weeks)
├─ Good for bulk orders
└─ Requires patience
```

---

## 🔄 **System Block Diagram**

```
                    ┌─────────────────┐
                    │   POWER INPUT   │
                    │  (5V USB/AC)    │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  DISTRIBUTION   │
                    │  (Breadboard)   │
                    └────────┬────────┘
         ┌──────────────────┼──────────────────┐
         │                  │                  │
    ┌────▼────┐      ┌──────▼──────┐    ┌─────▼─────┐
    │  ESP32   │      │ SENSORS     │    │ OUTPUTS   │
    │  (Brain) │      │ (Input)     │    │           │
    │          │      │             │    │           │
    │ ├─ WiFi  │      ├─ MQ135      │    ├─ Buzzer   │
    │ ├─ GPIO  │      ├─ MQ7        │    ├─ LEDs     │
    │ ├─ ADC   │      ├─ DHT11      │    └─ OLED     │
    │ └─ Logic │      └─ PM2.5      │
    │          │
    └────┬─────┘
         │
         ├─ Process sensor data
         ├─ Calculate AQI
         ├─ Detect anomalies
         ├─ Control outputs
         └─ Send to WiFi

         ↓ Cloud ↓

    ┌──────────────┐
    │ ThingSpeak   │
    │ Dashboard    │
    │ (Internet)   │
    └──────────────┘
```

---

## ✅ **Summary Table: Each Component's Role**

```
┌──────────────┬────────────────┬──────────────┬──────────┬──────┐
│ Component    │ Role           │ Function     │ Cost     │ Need │
├──────────────┼────────────────┼──────────────┼──────────┼──────┤
│ ESP32        │ Brain          │ Process      │ ₹600     │ ✅   │
│              │                │ Control      │          │      │
├──────────────┼────────────────┼──────────────┼──────────┼──────┤
│ MQ135        │ Sensor Input   │ Detect       │ ₹500     │ ✅   │
│              │                │ pollutants   │          │      │
├──────────────┼────────────────┼──────────────┼──────────┼──────┤
│ MQ7          │ Sensor Input   │ Detect CO    │ ₹500     │ ⭐   │
│              │                │ specifically │          │      │
├──────────────┼────────────────┼──────────────┼──────────┼──────┤
│ DHT11        │ Sensor Input   │ Temperature  │ ₹120     │ ✅   │
│              │                │ Humidity     │          │      │
├──────────────┼────────────────┼──────────────┼──────────┼──────┤
│ OLED         │ Display Output │ Show data    │ ₹500     │ ⭐   │
│              │                │ locally      │          │      │
├──────────────┼────────────────┼──────────────┼──────────┼──────┤
│ Buzzer       │ Alert Output   │ Audible      │ ₹40      │ ✅   │
│              │                │ notification │          │      │
├──────────────┼────────────────┼──────────────┼──────────┼──────┤
│ LEDs (3)     │ Alert Output   │ Visual       │ ₹30      │ ✅   │
│              │                │ status       │          │      │
├──────────────┼────────────────┼──────────────┼──────────┼──────┤
│ Power Supply │ Power System   │ Provide      │ ₹400     │ ✅   │
│              │                │ electricity  │          │      │
├──────────────┼────────────────┼──────────────┼──────────┼──────┤
│ Breadboard   │ Connectivity   │ Connect      │ ₹120     │ ✅   │
│ + Jumpers    │                │ components   │          │      │
└──────────────┴────────────────┴──────────────┴──────────┴──────┘

✅ = Essential (Must have)
⭐ = Recommended (Add if budget allows)
```

---

## 🎓 **Key Learnings**

✅ **ESP32** = Complete system (processor + WiFi included)
✅ **Sensors** = Convert physical properties to electrical signals
✅ **Processing** = Microcontroller reads and analyzes data
✅ **Output** = Display, alerts, cloud notifications
✅ **Power** = All components need reliable 5V source
✅ **Budget** = ₹5,000-6,500 for complete system

---

## 🚀 **Next Steps**

Once you have components:
1. Unbox and identify each component
2. Verify all items received
3. Test each sensor individually
4. Then proceed to **Step 5: Circuit Diagram & Wiring**

**Ready for Step 5?** Let me know when you've reviewed the hardware components! 🎯
