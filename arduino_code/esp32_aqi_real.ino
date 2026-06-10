/*
  ESP32 Air Quality Monitor (beginner-friendly)
  - Reads MQ135 analog output (via voltage divider) and DHT22 (temp & humidity)
  - Classifies air quality (Good/Moderate/Poor/Hazardous)
  - Triggers LED and buzzer alerts
  - Prints values to Serial
  - Optionally posts to ThingSpeak (set THINGSPEAK_API_KEY)

  Notes:
  - MQ135 modules require calibration and warm-up. The conversion below is a simplified linear mapping for demo purposes.
  - Use ADC1 pins (GPIO32-39) for analog reads when Wi-Fi is active.
  - Protect ESP32 ADC input with a voltage divider so the ADC never sees >3.3V.

  Replace WIFI_SSID, WIFI_PASS, and THINGSPEAK_API_KEY before uploading.
*/

#include <WiFi.h>
#include <HTTPClient.h>
#include "DHT.h"

// -------- CONFIG --------
// WiFi (optional, used for ThingSpeak posting)
const char* WIFI_SSID = "YOUR_WIFI_SSID";
const char* WIFI_PASS = "YOUR_WIFI_PASSWORD";
const char* THINGSPEAK_API_KEY = ""; // optional - set to your channel write API key

// Pins
const int MQ_PIN = 34;        // ADC1_CH6 (GPIO34) - after voltage divider
const int DHT_PIN = 4;        // Digital pin for DHT22
const int DHT_TYPE = DHT22;   // Change to DHT11 if using DHT11
const int LED_PIN = 2;        // Onboard LED / status
const int BUZZER_PIN = 16;    // Buzzer control (use transistor if buzzer needs >3.3V)

DHT dht(DHT_PIN, DHT_TYPE);

// -------- UTILS --------
// Simple mapping from analog value to "ppm-like" reading for demo only.
float mqAnalogToPPM(int raw) {
  // raw range: 0 - 4095 (12-bit ADC on ESP32)
  // Map to 0 - 500 ppm (very approximate)
  float ppm = ((float)raw / 4095.0) * 500.0;
  return ppm;
}

// Convert PM2.5-like value to a simple AQI classification (demo)
String classifyAQI(float pm25) {
  if (pm25 <= 12.0) return "Good";
  if (pm25 <= 35.4) return "Moderate";
  if (pm25 <= 55.4) return "Poor";
  return "Hazardous";
}

int computeSimpleAQI(float pm25) {
  // Very simplified numeric AQI mapping for demo purposes
  if (pm25 <= 12.0) return 50;
  if (pm25 <= 35.4) return 100;
  if (pm25 <= 55.4) return 150;
  if (pm25 <= 150.4) return 200;
  return 300;
}

void alertActions(String category) {
  if (category == "Good" || category == "Moderate") {
    digitalWrite(LED_PIN, LOW);
    digitalWrite(BUZZER_PIN, LOW);
  } else if (category == "Poor") {
    digitalWrite(LED_PIN, HIGH); // steady LED
    digitalWrite(BUZZER_PIN, LOW);
  } else { // Hazardous
    // Blink LED and beep buzzer
    digitalWrite(LED_PIN, !digitalRead(LED_PIN));
    tone(BUZZER_PIN, 2000, 200); // frequency 2kHz for 200 ms
  }
}

void sendToThingSpeak(float pm25, float temp, float hum, int aqi) {
  if (WiFi.status() != WL_CONNECTED || strlen(THINGSPEAK_API_KEY) == 0) return;

  HTTPClient http;
  String url = String("http://api.thingspeak.com/update?api_key=") + THINGSPEAK_API_KEY;
  url += "&field1=" + String(pm25, 1);
  url += "&field2=" + String(temp, 1);
  url += "&field3=" + String(hum, 1);
  url += "&field4=" + String(aqi);

  http.begin(url);
  int httpCode = http.GET();
  if (httpCode > 0) {
    Serial.printf("ThingSpeak update: %d\n", httpCode);
  } else {
    Serial.printf("ThingSpeak failed: %s\n", http.errorToString(httpCode).c_str());
  }
  http.end();
}

void setup() {
  Serial.begin(115200);
  delay(500);
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  dht.begin();

  // Connect WiFi (optional)
  if (strlen(WIFI_SSID) > 0) {
    WiFi.begin(WIFI_SSID, WIFI_PASS);
    Serial.print("Connecting to WiFi");
    int tries = 0;
    while (WiFi.status() != WL_CONNECTED && tries < 20) {
      delay(500);
      Serial.print('.');
      tries++;
    }
    Serial.println();
    if (WiFi.status() == WL_CONNECTED) Serial.println("WiFi connected");
    else Serial.println("WiFi not connected - continuing offline");
  }
}

void loop() {
  // Read MQ135 (analog) - ensure voltage divider is used so ADC <=3.3V
  int raw = analogRead(MQ_PIN);
  float ppm = mqAnalogToPPM(raw);

  // Read DHT (temp & humidity)
  float hum = dht.readHumidity();
  float temp = dht.readTemperature();
  if (isnan(hum) || isnan(temp)) {
    Serial.println("Failed to read from DHT sensor!");
    delay(2000);
    return;
  }

  int aqi = computeSimpleAQI(ppm);
  String category = classifyAQI(ppm);

  // Print to Serial
  Serial.printf("MQ135 raw=%d -> approx_ppm=%.1f, Temp=%.1fC, Hum=%.1f%%, AQI=%d (%s)\n",
                raw, ppm, temp, hum, aqi, category.c_str());

  // Alerts
  alertActions(category);

  // Send to ThingSpeak (optional)
  sendToThingSpeak(ppm, temp, hum, aqi);

  delay(15000); // Wait 15s between uploads (ThingSpeak limit)
}
