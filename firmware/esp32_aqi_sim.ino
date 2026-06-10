#include <WiFi.h>
#include <HTTPClient.h>

// --- CONFIG ---
const char* WIFI_SSID = "YOUR_WIFI_SSID";
const char* WIFI_PASS = "YOUR_WIFI_PASSWORD";
const char* THINGSPEAK_API_KEY = "YOUR_THINGSPEAK_WRITE_KEY"; // optional

const char* THINGSPEAK_HOST = "http://api.thingspeak.com";

// --- UTILS ---
float randomFloat(float lo, float hi) {
  return lo + ((float)esp_random() / UINT32_MAX) * (hi - lo);
}

int computeSimpleAQI(float pm25) {
  // Very simplified mapping for demo only
  if (pm25 <= 12.0) return 50;        // Good
  if (pm25 <= 35.4) return 100;      // Moderate
  if (pm25 <= 55.4) return 150;      // Unhealthy for sensitive
  if (pm25 <= 150.4) return 200;     // Unhealthy
  return 300;                         // Very unhealthy
}

void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("ESP32 AQI Simulator starting...");

  WiFi.begin(WIFI_SSID, WIFI_PASS);
  Serial.print("Connecting to WiFi");
  int tries = 0;
  while (WiFi.status() != WL_CONNECTED && tries < 20) {
    delay(500);
    Serial.print('.');
    tries++;
  }
  Serial.println();
  if (WiFi.status() == WL_CONNECTED) {
    Serial.print("Connected. IP=");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("WiFi not connected — proceeding in offline mode.");
  }
}

void loop() {
  // Simulate sensor readings
  float pm25 = randomFloat(5.0, 200.0);    // ug/m3
  float pm10 = randomFloat(10.0, 250.0);
  float temp = randomFloat(18.0, 38.0);
  float hum = randomFloat(20.0, 85.0);
  int aqi = computeSimpleAQI(pm25);

  // Print to serial
  Serial.printf("PM2.5=%.1f ug/m3, PM10=%.1f, Temp=%.1f C, Hum=%.1f%%, AQI=%d\n",
                pm25, pm10, temp, hum, aqi);

  // Send to ThingSpeak if configured
  if (WiFi.status() == WL_CONNECTED && strlen(THINGSPEAK_API_KEY) > 0) {
    HTTPClient http;
    String url = String("") + THINGSPEAK_HOST + "/update?api_key=" + THINGSPEAK_API_KEY;
    url += "&field1=" + String(pm25, 1);
    url += "&field2=" + String(pm10, 1);
    url += "&field3=" + String(temp, 1);
    url += "&field4=" + String(hum, 1);
    url += "&field5=" + String(aqi);

    http.begin(url);
    int httpCode = http.GET();
    if (httpCode > 0) {
      Serial.printf("ThingSpeak update status: %d\n", httpCode);
    } else {
      Serial.printf("ThingSpeak update failed: %s\n", http.errorToString(httpCode).c_str());
    }
    http.end();
  }

  delay(15000); // ThingSpeak free channel rate limit (15s)
}
