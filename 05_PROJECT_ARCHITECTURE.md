# 5️⃣ Project Architecture: Air Quality Monitoring System

---

## 🏗️ System Architecture Overview

The Air Quality Monitoring system follows a **3-tier architecture**:

```
┌─────────────────────────────────────────────────────┐
│              3-TIER ARCHITECTURE                    │
├─────────────────────────────────────────────────────┤
│                                                     │
│  TIER 1: INPUT LAYER (Sensors)                      │
│  └─ Capture physical air quality parameters         │
│                                                     │
│  TIER 2: PROCESSING LAYER (ESP32 Logic)            │
│  └─ Convert readings to meaningful data             │
│                                                     │
│  TIER 3: OUTPUT LAYER (Displays & Alerts)          │
│  └─ Communicate results to users & cloud           │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 📥 **TIER 1: INPUT LAYER - SENSOR DATA ACQUISITION**

### **Sensors & What They Measure**

```
SENSOR INPUTS (What we measure):

┌─────────────────────────────────────────────────────┐
│  AIR QUALITY SENSORS                                │
├─────────────────────────────────────────────────────┤
│                                                     │
│  MQ135 Sensor                                       │
│  ├─ Reads: Air quality index (AQI baseline)        │
│  ├─ Output: Analog voltage (0-5V)                  │
│  ├─ Maps to: 0-500 AQI range                       │
│  └─ Frequency: Every 1 second                      │
│                                                     │
│  MQ7 Sensor (Optional)                             │
│  ├─ Reads: Carbon Monoxide (CO) specifically       │
│  ├─ Output: Analog voltage (0-5V)                  │
│  ├─ Maps to: 0-100 ppm CO concentration           │
│  └─ Frequency: Every 1 second                      │
│                                                     │
│  DHT11 Sensor                                       │
│  ├─ Reads: Temperature & Humidity                  │
│  ├─ Output: Digital signal (1-wire protocol)       │
│  ├─ Temp: -40 to +80°C                             │
│  ├─ Humidity: 0-100% RH                            │
│  └─ Frequency: Every 2 seconds (slower)            │
│                                                     │
│  PM2.5 Sensor (Optional)                           │
│  ├─ Reads: Particulate matter concentration        │
│  ├─ Output: Analog voltage (0-5V)                  │
│  ├─ Maps to: 0-500 μg/m³                           │
│  └─ Frequency: Every 1 second                      │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### **Raw Data Collection Process**

```
SENSOR → ADC CONVERSION → DIGITAL VALUE:

Step 1: Physical Property (Air pollutants)
        │
        ├─ Pollutant molecules hit sensor
        ├─ Cause change in resistance/voltage
        └─ Sensor outputs analog signal (0-5V)

Step 2: Analog Signal (0-5V from sensor)
        │
        ├─ Comes directly from sensor pins
        ├─ Continuous values (infinite precision theoretically)
        └─ Cannot be read directly by digital microcontroller

Step 3: Analog-to-Digital Conversion (ADC)
        │
        ├─ ESP32 ADC: 12-bit resolution
        ├─ Converts 0-5V to 0-4095 digital values
        │  (each unit = 5V / 4095 = 1.22 mV)
        └─ Resolution: ±1.22 mV precision

Step 4: Digital Value (0-4095)
        │
        ├─ Safe to store in microcontroller
        ├─ Can be processed, compared, transmitted
        └─ Represents sensor reading

EXAMPLE:
Sensor voltage: 2.5V
ADC value = (2.5V / 5V) × 4095 = 2047
Integer stored in memory: 2047 ✓
```

### **Sensor Data Structure**

```cpp
// Data structure for sensor readings

struct SensorReading {
  // Raw ADC values
  int mq135_raw;      // 0-4095
  int mq7_raw;        // 0-4095
  int dht11_temp;     // Temperature in °C
  int dht11_humidity; // Humidity in %RH
  
  // Converted values (meaningful units)
  float aqi_level;    // 0-500
  float co_ppm;       // 0-100 ppm
  float temp;         // °C
  float humidity;     // %
  
  // Timestamp
  unsigned long timestamp; // milliseconds
};

// Create reading every second
SensorReading current_reading;
```

### **Data Flow: From Sensor to Digital Value**

```
POLLUTANT IN AIR
        ↓
    MQ135 SENSOR
    (Semiconductor changes resistance)
        ↓
    ANALOG VOLTAGE OUTPUT
    (0-5V from sensor pin)
        ↓
    ESP32 ADC CONVERTER
    (Analog to Digital)
        ↓
    DIGITAL VALUE
    (0-4095, 12-bit)
        ↓
    STORED IN VARIABLE
    (mq135_raw = 2047)
        ↓
    READY FOR PROCESSING
```

---

## ⚙️ **TIER 2: PROCESSING LAYER - DATA ANALYSIS & AQI CALCULATION**

### **Processing Pipeline**

```
RAW SENSOR DATA
        ↓
    ┌───────────────────────────┐
    │ STAGE 1: DATA VALIDATION  │
    │ (Check if readings valid) │
    └────────┬──────────────────┘
             ↓
    ┌───────────────────────────┐
    │ STAGE 2: NOISE FILTERING  │
    │ (Smooth out spikes)       │
    └────────┬──────────────────┘
             ↓
    ┌───────────────────────────┐
    │ STAGE 3: UNIT CONVERSION  │
    │ (ADC → ppm/μg/m³)         │
    └────────┬──────────────────┘
             ↓
    ┌───────────────────────────┐
    │ STAGE 4: AQI CALCULATION  │
    │ (EPA formula)             │
    └────────┬──────────────────┘
             ↓
    ┌───────────────────────────┐
    │ STAGE 5: THRESHOLD CHECK  │
    │ (Compare with limits)     │
    └────────┬──────────────────┘
             ↓
    ┌───────────────────────────┐
    │ STAGE 6: CATEGORIZATION   │
    │ (Good/Moderate/Bad?)      │
    └────────┬──────────────────┘
             ↓
    ┌───────────────────────────┐
    │ STAGE 7: ALERT LOGIC      │
    │ (Trigger if needed)       │
    └────────┬──────────────────┘
             ↓
    ┌───────────────────────────┐
    │ STAGE 8: LOGGING          │
    │ (Store for history)       │
    └────────┬──────────────────┘
             ↓
    PROCESSED DATA (Ready for output)
```

### **Stage 1: Data Validation**

```cpp
// Check if sensor readings are within valid range

bool isValidReading(int adc_value) {
  // ADC should be 0-4095 (12-bit)
  if (adc_value < 0 || adc_value > 4095) {
    return false; // Invalid
  }
  
  // Check for sensor errors
  if (adc_value == 0 || adc_value == 4095) {
    return false; // Likely sensor disconnected
  }
  
  return true; // Valid reading
}

// Remove completely invalid readings
if (!isValidReading(mq135_raw)) {
  // Skip this reading, use last known good value
  mq135_raw = last_valid_mq135;
}
```

### **Stage 2: Noise Filtering (Moving Average)**

```cpp
// Sensor readings can be noisy, smooth them out

#define FILTER_SIZE 10
int adc_buffer[FILTER_SIZE];
int buffer_index = 0;

int getFilteredValue(int raw_adc) {
  // Add new reading to circular buffer
  adc_buffer[buffer_index] = raw_adc;
  buffer_index = (buffer_index + 1) % FILTER_SIZE;
  
  // Calculate average of last 10 readings
  int sum = 0;
  for (int i = 0; i < FILTER_SIZE; i++) {
    sum += adc_buffer[i];
  }
  
  return sum / FILTER_SIZE; // Smoothed value
}

// Example: Before and after filtering
// Raw: 2050, 2055, 2048, 2100 (noisy)
// Filtered: 2060, 2061, 2062 (smooth trend)
```

### **Stage 3: Unit Conversion (ADC → Real Units)**

```cpp
// Convert raw ADC values to meaningful units

// CONVERSION FORMULA:
// Actual Value = (ADC_Value / ADC_Max) × Max_Range

// MQ135: Convert ADC to AQI (0-500)
float adc_to_aqi(int adc_value) {
  // Calibration: voltage at clean air = 0.4V (ADC ~825)
  int calibration_adc = 825; // When in clean air
  
  // Calculate ratio
  float ratio = (float)adc_value / calibration_adc;
  
  // AQI calculation (empirical formula)
  float aqi = (ratio - 1.0) * 500.0 + 50.0;
  
  // Clamp to valid range
  if (aqi < 0) aqi = 0;
  if (aqi > 500) aqi = 500;
  
  return aqi;
}

// MQ7: Convert ADC to CO ppm (0-100)
float adc_to_co_ppm(int adc_value) {
  // Simple linear mapping
  float co_ppm = (float)adc_value / 4095.0 * 100.0;
  return co_ppm;
}

// EXAMPLE CONVERSION:
// ADC 2047 → AQI 245 ✓
// ADC 1024 → CO 25 ppm ✓
```

### **Stage 4: AQI Calculation (EPA Standard)**

```cpp
// Calculate official Air Quality Index

float calculateAQI(float pm25, float co, float co2, float no2) {
  // AQI = maximum of individual pollutant AQIs
  
  // PM2.5 AQI calculation
  float pm25_aqi;
  if (pm25 <= 12) {
    pm25_aqi = (pm25 / 12.0) * 50.0;
  } else if (pm25 <= 35.4) {
    pm25_aqi = ((pm25 - 12.1) / (35.4 - 12.1)) * (100.0 - 50.0) + 50.0;
  } else if (pm25 <= 55.4) {
    pm25_aqi = ((pm25 - 35.5) / (55.4 - 35.5)) * (150.0 - 100.0) + 100.0;
  } else {
    pm25_aqi = 200.0; // Hazardous
  }
  
  // CO AQI calculation
  float co_aqi;
  if (co <= 4.4) {
    co_aqi = (co / 4.4) * 50.0;
  } else if (co <= 9.4) {
    co_aqi = ((co - 4.5) / (9.4 - 4.5)) * (100.0 - 50.0) + 50.0;
  } else if (co <= 12.4) {
    co_aqi = ((co - 9.5) / (12.4 - 9.5)) * (150.0 - 100.0) + 100.0;
  } else {
    co_aqi = 200.0; // Hazardous
  }
  
  // Take maximum (worst pollutant determines AQI)
  float aqi = max(pm25_aqi, co_aqi);
  
  return aqi;
}

// RESULT: Overall AQI value (0-500+)
```

### **Stage 5: Threshold Comparison**

```cpp
// Compare calculated values against safety limits

#define PM25_THRESHOLD 55    // μg/m³
#define CO_THRESHOLD 70      // ppm
#define CO2_THRESHOLD 1000   // ppm
#define AQI_THRESHOLD 150    // AQI value

struct ThresholdCheck {
  bool pm25_exceeded;
  bool co_exceeded;
  bool co2_exceeded;
  bool aqi_exceeded;
  int alert_level;  // 0=none, 1=warning, 2=critical
};

ThresholdCheck checkThresholds(float pm25, float co, float co2, float aqi) {
  ThresholdCheck result = {false, false, false, false, 0};
  
  // Check each pollutant
  if (pm25 > PM25_THRESHOLD) {
    result.pm25_exceeded = true;
    result.alert_level = 2; // Critical
  }
  
  if (co > CO_THRESHOLD) {
    result.co_exceeded = true;
    result.alert_level = 2; // Critical
  }
  
  if (co2 > CO2_THRESHOLD) {
    result.co2_exceeded = true;
    result.alert_level = 1; // Warning
  }
  
  if (aqi > AQI_THRESHOLD) {
    result.aqi_exceeded = true;
    result.alert_level = 2; // Critical
  }
  
  return result;
}
```

### **Stage 6: Categorization**

```cpp
// Classify air quality into categories

enum AirQualityCategory {
  GOOD,              // AQI 0-50
  MODERATE,          // AQI 51-100
  UNHEALTHY_SENS,    // AQI 101-150
  UNHEALTHY,         // AQI 151-200
  VERY_UNHEALTHY,    // AQI 201-300
  HAZARDOUS          // AQI 301+
};

AirQualityCategory categorizeAQI(float aqi) {
  if (aqi <= 50) return GOOD;
  else if (aqi <= 100) return MODERATE;
  else if (aqi <= 150) return UNHEALTHY_SENS;
  else if (aqi <= 200) return UNHEALTHY;
  else if (aqi <= 300) return VERY_UNHEALTHY;
  else return HAZARDOUS;
}

// Get readable string
const char* getCategory(AirQualityCategory cat) {
  switch(cat) {
    case GOOD: return "GOOD ✓";
    case MODERATE: return "MODERATE ⚠️";
    case UNHEALTHY_SENS: return "UNHEALTHY (Sensitive Groups)";
    case UNHEALTHY: return "UNHEALTHY 🔴";
    case VERY_UNHEALTHY: return "VERY UNHEALTHY 🔴🔴";
    case HAZARDOUS: return "HAZARDOUS ☠️";
    default: return "UNKNOWN";
  }
}
```

### **Stage 7: Alert Logic**

```cpp
// Decide what alerts to trigger

void triggerAlerts(ThresholdCheck checks, float aqi) {
  
  // NO ALERT (Green)
  if (!checks.aqi_exceeded && aqi <= 100) {
    digitalWrite(LED_GREEN, HIGH);
    digitalWrite(LED_YELLOW, LOW);
    digitalWrite(LED_RED, LOW);
    digitalWrite(BUZZER, LOW);
    return;
  }
  
  // MODERATE WARNING (Yellow)
  if (aqi <= 150) {
    digitalWrite(LED_GREEN, LOW);
    digitalWrite(LED_YELLOW, HIGH);
    digitalWrite(LED_RED, LOW);
    // Slow buzzer beep
    slowBuzzer();
    return;
  }
  
  // UNHEALTHY ALERT (Red)
  if (aqi <= 200) {
    digitalWrite(LED_GREEN, LOW);
    digitalWrite(LED_YELLOW, LOW);
    digitalWrite(LED_RED, HIGH);
    // Fast buzzer beep
    fastBuzzer();
    // Send cloud alert
    sendCloudAlert("High AQI: " + String(aqi));
    return;
  }
  
  // HAZARDOUS EMERGENCY (Critical)
  if (aqi > 200) {
    digitalWrite(LED_GREEN, LOW);
    digitalWrite(LED_YELLOW, LOW);
    digitalWrite(LED_RED, HIGH);
    // CONTINUOUS ALARM
    digitalWrite(BUZZER, HIGH);
    // Send multiple alerts
    sendCloudAlert("HAZARDOUS AQI: " + String(aqi));
    sendSMS("Air quality critical! Stay indoors.");
  }
}

void slowBuzzer() {
  digitalWrite(BUZZER, HIGH);
  delay(100);
  digitalWrite(BUZZER, LOW);
  delay(4900);
}

void fastBuzzer() {
  digitalWrite(BUZZER, HIGH);
  delay(200);
  digitalWrite(BUZZER, LOW);
  delay(800);
}
```

### **Stage 8: Data Logging**

```cpp
// Store readings for historical analysis

#define MAX_LOGS 1440 // Store 24 hours (one per minute)

struct DataLog {
  unsigned long timestamp;
  float aqi;
  float pm25;
  float temperature;
  float humidity;
  AirQualityCategory category;
};

DataLog logs[MAX_LOGS];
int log_index = 0;

void logData(float aqi, float pm25, float temp, float humidity) {
  // Create log entry
  logs[log_index].timestamp = millis();
  logs[log_index].aqi = aqi;
  logs[log_index].pm25 = pm25;
  logs[log_index].temperature = temp;
  logs[log_index].humidity = humidity;
  logs[log_index].category = categorizeAQI(aqi);
  
  // Move to next position (circular buffer)
  log_index = (log_index + 1) % MAX_LOGS;
  
  // Once per hour, send logs to cloud
  if (log_index % 60 == 0) {
    sendToThingSpeak();
  }
}

void generateCSVReport() {
  // Create CSV format for download
  Serial.println("timestamp,aqi,pm25,temp,humidity,category");
  for (int i = 0; i < MAX_LOGS; i++) {
    Serial.print(logs[i].timestamp);
    Serial.print(",");
    Serial.print(logs[i].aqi);
    Serial.print(",");
    Serial.print(logs[i].pm25);
    Serial.print(",");
    Serial.print(logs[i].temperature);
    Serial.print(",");
    Serial.print(logs[i].humidity);
    Serial.print(",");
    Serial.println(getCategory(logs[i].category));
  }
}
```

---

## 📤 **TIER 3: OUTPUT LAYER - DISPLAY & COMMUNICATION**

### **Output Channels**

```
PROCESSED DATA
        ↓
    ┌───────────────────────────────────┐
    │ TIER 3: OUTPUT & COMMUNICATION    │
    └───────────────────────────────────┘
        │           │           │
        ├─ Local    ├─ Alerts  ├─ Cloud
        │ Display   │          │
        ↓           ↓          ↓
    ┌──────────┐ ┌──────────┐ ┌───────────┐
    │ OLED/LCD │ │ Buzzer   │ │ ThingSpeak│
    │ Display  │ │ LEDs     │ │ WiFi      │
    │          │ │ Serial   │ │ MQTT      │
    └──────────┘ └──────────┘ └───────────┘
```

### **Output 1: Local Display (OLED)**

```
OLED DISPLAY LAYOUT:

┌──────────────────────────────────────────┐
│  AIR QUALITY MONITOR                     │
│  Time: 14:32:18                          │
├──────────────────────────────────────────┤
│                                          │
│  AQI Status: MODERATE                    │
│  ▓▓▓▓▓░░░░░░░░░░░░ 87                   │
│                                          │
│  PM2.5: 35 μg/m³   ✓ Normal              │
│  CO:    2.1 ppm    ✓ Normal              │
│  CO₂:   420 ppm    ✓ Normal              │
│                                          │
│  Temperature: 28.5°C                     │
│  Humidity:    65%                        │
│                                          │
├──────────────────────────────────────────┤
│  Status: All systems normal ✓            │
└──────────────────────────────────────────┘

CODE:
void displayOLED(float aqi, float pm25, float temp, float humidity) {
  display.clearDisplay();
  display.setTextSize(1);
  display.setCursor(0, 0);
  
  display.println("AIR QUALITY MONITOR");
  display.println("Time: " + getTime());
  
  display.println("");
  display.println("AQI: " + String(aqi));
  display.println("PM2.5: " + String(pm25));
  display.println("Temp: " + String(temp));
  display.println("Humidity: " + String(humidity));
  
  display.display();
}
```

### **Output 2: Alert System (Buzzer & LEDs)**

```
ALERT DECISION TREE:

AQI < 50 (GOOD)
├─ Green LED: ON
├─ Yellow LED: OFF
├─ Red LED: OFF
├─ Buzzer: OFF
└─ Status: "Air quality is good ✓"

AQI 50-100 (MODERATE)
├─ Green LED: OFF
├─ Yellow LED: ON
├─ Red LED: OFF
├─ Buzzer: OFF (silent warning)
└─ Status: "Moderate air quality"

AQI 100-150 (UNHEALTHY FOR SENSITIVE)
├─ Green LED: OFF
├─ Yellow LED: OFF
├─ Red LED: ON
├─ Buzzer: Slow beep (every 5 sec)
└─ Status: "Alert: Limit outdoor activities"

AQI 150-200 (UNHEALTHY)
├─ Green LED: OFF
├─ Yellow LED: OFF
├─ Red LED: BLINK
├─ Buzzer: Fast beep (every 2 sec)
└─ Status: "WARNING: Avoid outdoor activities"

AQI > 200 (HAZARDOUS)
├─ Green LED: OFF
├─ Yellow LED: OFF
├─ Red LED: BLINK FAST
├─ Buzzer: CONTINUOUS
└─ Status: "EMERGENCY: Stay indoors!"

CODE:
void updateAlerts(float aqi) {
  AirQualityCategory category = categorizeAQI(aqi);
  
  switch(category) {
    case GOOD:
      setLEDs(HIGH, LOW, LOW);
      noSound();
      break;
    case MODERATE:
      setLEDs(LOW, HIGH, LOW);
      noSound();
      break;
    case UNHEALTHY_SENS:
    case UNHEALTHY:
      setLEDs(LOW, LOW, HIGH);
      slowBeep();
      break;
    case VERY_UNHEALTHY:
    case HAZARDOUS:
      setLEDs(LOW, LOW, HIGH);
      fastBeep();
      break;
  }
}
```

### **Output 3: Serial Monitor (Debugging)**

```
SERIAL OUTPUT (USB for debugging):

--- Air Quality Monitor ---
2026-06-10 14:32:18

Sensor Readings:
├─ MQ135 ADC: 2047
├─ MQ7 ADC: 1024
├─ DHT11 Temp: 28.5°C
└─ DHT11 Humidity: 65%

Processed Values:
├─ AQI: 87 (MODERATE)
├─ PM2.5: 35 μg/m³
├─ CO: 2.1 ppm
└─ CO₂: 420 ppm

Threshold Check:
├─ AQI exceeded: NO ✓
├─ PM2.5 exceeded: NO ✓
├─ CO exceeded: NO ✓
└─ Status: All normal

Alert Status:
├─ LED: Yellow ON
├─ Buzzer: OFF
└─ Cloud Alert: Not sent

Last WiFi Update: 2 minutes ago
--- End ---
```

### **Output 4: Cloud Dashboard (ThingSpeak)**

```
THINGSPEAK DASHBOARD DISPLAY:

Current Readings (Real-time):
┌──────────────────────────────────────────┐
│ Channel: Air Quality Monitor             │
│ Updated: Just now                        │
├──────────────────────────────────────────┤
│                                          │
│ Field 1: PM2.5 = 35 μg/m³                │
│ Field 2: CO = 2.1 ppm                    │
│ Field 3: CO₂ = 420 ppm                   │
│ Field 4: Temperature = 28.5°C            │
│ Field 5: Humidity = 65%                  │
│ Field 6: AQI = 87                        │
│                                          │
├──────────────────────────────────────────┤
│ Last 24 Hours Trend:                     │
│                                          │
│ PM2.5 Trend:                             │
│  ┌──────────────────────────────────┐   │
│  │    ╱╲     ╱╲                     │   │
│  │   ╱  ╲   ╱  ╲   ╱╲              │   │
│  │  ╱    ╲ ╱    ╲ ╱  ╲             │   │
│  │_╱______╱______╱____╲_            │   │
│  │ 00:00  12:00  24:00             │   │
│  └──────────────────────────────────┘   │
│                                          │
│ AQI Trend: STABLE (avg 85)               │
│                                          │
└──────────────────────────────────────────┘

CODE (ESP32 sends data):
void sendToThingSpeak() {
  String url = "http://api.thingspeak.com/update?";
  url += "api_key=YOUR_API_KEY";
  url += "&field1=" + String(pm25);
  url += "&field2=" + String(co);
  url += "&field3=" + String(co2);
  url += "&field4=" + String(temperature);
  url += "&field5=" + String(humidity);
  url += "&field6=" + String(aqi);
  
  HTTPClient http;
  http.begin(url);
  int httpCode = http.GET();
  http.end();
}
```

### **Output 5: CSV Report (Data Download)**

```
CSV Format (Excel-compatible):

timestamp,aqi,pm25,co,co2,temperature,humidity,category
2026-06-10 00:00:00,45,22,0.8,398,24.5,62,GOOD
2026-06-10 01:00:00,52,28,1.2,402,24.2,64,MODERATE
2026-06-10 02:00:00,68,35,1.8,410,24.0,66,MODERATE
2026-06-10 03:00:00,95,45,2.5,420,25.0,70,MODERATE
2026-06-10 04:00:00,145,58,4.2,438,26.5,75,UNHEALTHY_SENS
2026-06-10 05:00:00,200,72,6.8,458,27.5,78,UNHEALTHY
...

CODE (Generate CSV):
void generateReport() {
  String csv = "timestamp,aqi,pm25,co,co2,temperature,humidity,category\n";
  
  for (int i = 0; i < MAX_LOGS; i++) {
    csv += logs[i].timestamp;
    csv += "," + String(logs[i].aqi);
    csv += "," + String(logs[i].pm25);
    csv += "," + String(logs[i].co);
    csv += "," + String(logs[i].co2);
    csv += "," + String(logs[i].temperature);
    csv += "," + String(logs[i].humidity);
    csv += "," + getCategory(logs[i].category);
    csv += "\n";
  }
  
  // Save to SPIFFS or send via HTTP
  saveFile("report.csv", csv);
}
```

---

## 🔄 **COMPLETE DATA FLOW DIAGRAM**

### **From Sensor to Output (End-to-End)**

```
┌─────────────────────────────────────────────────────────────┐
│                    COMPLETE DATA FLOW                       │
└─────────────────────────────────────────────────────────────┘

1. PHYSICAL MEASUREMENT
   │
   Pollutant molecules in air
   │
   └─→ MQ135 detects increase in concentration
       └─→ Resistance of SnO₂ decreases
           └─→ Output voltage increases

2. ELECTRICAL SIGNAL
   │
   Sensor output: 3.2V (analog signal)
   │
   └─→ Sent through wire to ESP32 GPIO 32

3. ANALOG-TO-DIGITAL CONVERSION
   │
   3.2V analog input
   │
   └─→ ESP32 ADC converter
       └─→ 12-bit conversion: (3.2 / 5) × 4095 = 2621
           └─→ Digital value: 2621

4. STORAGE IN MEMORY
   │
   Integer 2621 stored in variable "mq135_raw"
   │
   └─→ Ready for processing

5. VALIDATION
   │
   Check if 0 < 2621 < 4095?  YES ✓
   │
   └─→ Reading is valid

6. NOISE FILTERING
   │
   Apply moving average filter
   Last 10 readings: [2621, 2618, 2625, 2619, 2620, ...]
   │
   └─→ Average: 2620 (smoother)

7. UNIT CONVERSION
   │
   2620 ADC → Real units
   ratio = 2620 / 825 = 3.18
   AQI = (3.18 - 1) × 500 + 50 = 1140 (too high, cap at 500)
   │
   └─→ Final AQI: 500 (HAZARDOUS)

8. THRESHOLD COMPARISON
   │
   Is AQI (500) > THRESHOLD (150)?  YES ⚠️
   │
   └─→ Threshold exceeded!

9. CATEGORIZATION
   │
   AQI 500 falls into:  HAZARDOUS
   │
   └─→ Category determined

10. ALERT LOGIC
    │
    HAZARDOUS category triggers:
    │
    ├─→ LED RED: Turn ON
    ├─→ Buzzer: CONTINUOUS
    ├─→ Cloud Alert: Send via WiFi
    └─→ Serial: Print warning

11. LOCAL DISPLAY (OLED)
    │
    Update display with:
    ├─ "AQI: 500 HAZARDOUS ☠️"
    ├─ Red light indicator
    └─ "STAY INDOORS!"

12. CLOUD TRANSMISSION (WiFi)
    │
    Connect to WiFi network
    │
    └─→ Send HTTP request to ThingSpeak
        with data:
        api_key=YOUR_KEY&field1=500&field6=500

13. CLOUD STORAGE
    │
    ThingSpeak receives data
    │
    └─→ Stores timestamp + value
        Creates historical record
        Updates dashboard

14. DATA LOGGING (Local Storage)
    │
    Store reading in circular buffer:
    logs[minute].aqi = 500
    logs[minute].timestamp = 1623334338
    │
    └─→ Available for CSV export

RESULT: One complete sensor reading → multiple outputs
        (Display, Alert, Cloud, Log) in ~2 seconds!
```

---

## 🏗️ **SYSTEM ARCHITECTURE DIAGRAM (Text-based)**

```
┌──────────────────────────────────────────────────────────────┐
│                 IOT AIR QUALITY SYSTEM                       │
│                                                              │
│  ┌────────────────┐  ┌────────────────┐  ┌──────────────┐   │
│  │   SENSORS      │  │   SENSORS      │  │  SENSORS     │   │
│  │ (Physical)     │  │ (Physical)     │  │ (Physical)   │   │
│  │                │  │                │  │              │   │
│  │ MQ135 AQI      │  │ DHT11 Temp/Hum │  │ MQ7 CO       │   │
│  └────────┬───────┘  └────────┬───────┘  └──────┬───────┘   │
│           │                   │                 │            │
│           └───────────────────┼─────────────────┘            │
│                               │                              │
│                   ┌───────────▼────────────┐                 │
│                   │   ANALOG SIGNALS       │                 │
│                   │   (0-5V voltages)      │                 │
│                   └───────────┬────────────┘                 │
│                               │                              │
│                   ┌───────────▼────────────┐                 │
│                   │  MICROCONTROLLER       │                 │
│                   │   (ESP32 Main Board)   │                 │
│                   │                        │                 │
│                   │  ┌──────────────────┐  │                 │
│                   │  │ ADC Converter    │  │                 │
│                   │  │ (Analog→Digital) │  │                 │
│                   │  └────────┬─────────┘  │                 │
│                   │           │            │                 │
│                   │  ┌────────▼─────────┐  │                 │
│                   │  │ Processing Layer │  │                 │
│                   │  │                  │  │                 │
│                   │  │ ├─ Validation    │  │                 │
│                   │  │ ├─ Filtering     │  │                 │
│                   │  │ ├─ Conversion    │  │                 │
│                   │  │ ├─ AQI Calc      │  │                 │
│                   │  │ ├─ Threshold     │  │                 │
│                   │  │ ├─ Category      │  │                 │
│                   │  │ ├─ Alert Logic   │  │                 │
│                   │  │ └─ Logging       │  │                 │
│                   │  └────────┬─────────┘  │                 │
│                   │           │            │                 │
│                   │  ┌────────▼─────────┐  │                 │
│                   │  │ WiFi Module      │  │                 │
│                   │  │ (Built-in)       │  │                 │
│                   │  └────────┬─────────┘  │                 │
│                   │                        │                 │
│                   └────────┬─────────┬──────┴──────┐          │
│                            │         │             │          │
│          ┌─────────────────┼─────────┼─────────────┐          │
│          │                 │         │             │          │
│    ┌─────▼──────┐  ┌──────▼────┐  ┌▼────────┐  ┌─▼─────┐   │
│    │ OLED       │  │ WiFi      │  │ Buzzer  │  │ LEDs  │   │
│    │ Display    │  │ ThingSpeak│  │ Alert   │  │ Status│   │
│    │ (Real-time)│  │ (Cloud)   │  │         │  │Lights │   │
│    └────────────┘  └───────────┘  └─────────┘  └───────┘   │
│          │                │             │           │        │
│          └────────────────┼─────────────┼───────────┘        │
│                           │             │                    │
│        ┌──────────────────┴─────────────┴──────────┐          │
│        │         USER SEES RESULTS                 │          │
│        │                                          │          │
│        │ ✓ Current AQI displayed                   │          │
│        │ ✓ Visual alerts (colors)                  │          │
│        │ ✓ Audio alerts (buzzer)                   │          │
│        │ ✓ Can check phone for cloud data          │          │
│        │ ✓ Download CSV reports                    │          │
│        └──────────────────────────────────────────┘          │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## 📊 **Processing Pipeline Summary**

```
SENSOR RAW DATA
    ↓ (Analog 0-5V)
ADC CONVERTER
    ↓ (Digital 0-4095)
DATA VALIDATION
    ↓ (Check valid range)
NOISE FILTERING
    ↓ (Moving average)
UNIT CONVERSION
    ↓ (ADC → ppm/μg/m³)
AQI CALCULATION
    ↓ (EPA formula)
THRESHOLD CHECK
    ↓ (Compare limits)
CATEGORIZATION
    ↓ (Good/Moderate/Bad)
ALERT LOGIC
    ↓ (Buzzer/LEDs)
DATA LOGGING
    ↓ (Store history)
CLOUD TRANSMISSION
    ↓ (WiFi to ThingSpeak)
DISPLAY UPDATE
    ↓ (OLED/Serial)
USER SEES RESULT ✓
```

---

## 🔐 **Data Structure (In Memory)**

```cpp
// Complete data structure representing system state

struct SystemState {
  // Raw sensor values
  struct {
    int mq135_adc;      // 0-4095
    int mq7_adc;        // 0-4095
    float temp_c;       // -40 to +80
    float humidity_pct;  // 0-100
  } raw_sensors;
  
  // Processed values
  struct {
    float aqi;          // 0-500+
    float co_ppm;       // ppm
    float pm25_ugm3;    // μg/m³
    float co2_ppm;      // ppm
  } processed_values;
  
  // Status information
  struct {
    AirQualityCategory category;
    bool aqi_alert;
    bool co_alert;
    bool temp_warning;
    unsigned long last_update_ms;
  } status;
  
  // Alert outputs
  struct {
    bool green_led;
    bool yellow_led;
    bool red_led;
    bool buzzer_active;
    int buzzer_frequency_hz;
  } outputs;
  
  // Cloud communication
  struct {
    bool connected;
    unsigned long last_sync_ms;
    int failed_attempts;
  } wifi_status;
  
} system_state;
```

---

## ✅ **Tier Summary**

```
┌─────────────────────────────────────────────────────┐
│ TIER 1: INPUT                                       │
│ └─ Sensors measure air quality                      │
│    Result: Raw ADC values (0-4095)                  │
├─────────────────────────────────────────────────────┤
│ TIER 2: PROCESSING                                  │
│ └─ ESP32 converts and analyzes data                 │
│    Result: AQI, alerts, categorization              │
├─────────────────────────────────────────────────────┤
│ TIER 3: OUTPUT                                      │
│ └─ Display and transmit results                     │
│    Result: User feedback + cloud record             │
└─────────────────────────────────────────────────────┘
```

---

**Ready for Step 6?** 🚀

Please provide your next requirement! (e.g., Circuit Diagram, Microcontroller Code, etc.)
