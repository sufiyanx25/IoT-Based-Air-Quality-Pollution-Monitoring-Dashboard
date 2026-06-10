Dashboard setup — ThingSpeak and Blynk

Overview
This guide shows two easy cloud/dashboard options: ThingSpeak (web-channel + graphs + React alerts) and Blynk (mobile-first dashboard + notifications). Both are suitable for student projects; ThingSpeak is quick for time-series logging, while Blynk is better for interactive mobile control and push notifications.

A. ThingSpeak (recommended for quick web dashboards)

1) Create an account
- Visit https://thingspeak.com and sign up for a free account.
- Verify your email to enable channels.

2) Create a channel (project)
- After login, go to "Channels" → "New Channel".
- Give a descriptive name (e.g., "ESP32_AQI_Monitor").
- In the Fields section add these fields and names:
  - Field 1: `aqi` (AQI / air quality numeric value)
  - Field 2: `temperature` (°C)
  - Field 3: `humidity` (%)
  - Field 4: `pollution_status` (string or numeric code)
  - Field 5: `alert` (0/1 or descriptive)
- Save the channel and note the Write API Key (Write API Key → Copy) — you will use this in your ESP32 firmware.

3) Posting data (HTTP example)
- Simple HTTP GET format:

  http://api.thingspeak.com/update?api_key=WRITE_KEY&field1=50&field2=25.4&field3=45.2&field4=2&field5=1

- Replace `WRITE_KEY` and fields with your sensor values. ThingSpeak enforces a ~15s rate limit for free channels.

4) Graph setup
- Open your channel page → "Private View" (or Public View).
- ThingSpeak automatically shows time-series graphs for each field. Click a field to customize the chart time window (last 8 hours, 30 days, etc.).
- For combined graphs use the Channel Visualizations or export data for Plotly/Matplotlib offline plots.

5) Alert setup (React / React+SMS/Email)
- ThingSpeak React app lets you trigger actions when a condition is met.
- In ThingSpeak Apps → React → Create a React:
  - Condition: choose a field (e.g., `field1` for AQI) and threshold (e.g., AQI > 150)
  - Action: send an email, trigger a webhook, or call another service (IFTTT/Slack).
- Configure action details (recipient email or webhook URL).
- Save and enable the React. React runs server-side on ThingSpeak and will evaluate new channel updates.

6) Screenshot checklist (what to capture)
- Channel overview page showing recent values and graphs.
- Channel settings page showing field names and API key (mask key in public docs).
- React alert configuration showing condition and action.
- Serial Monitor output (local) showing values being sent.
- Wiring photo of the prototype (in `images/` folder).

B. Blynk (mobile-first, interactive dashboards)

1) Accounts & app
- Install the Blynk IoT mobile app (iOS/Android).
- Sign up and log in. For Blynk IoT (cloud) create a new Device/Project in the app; you will receive an Auth Token (or device credentials) for HTTP/API access.

2) Create project / device
- In the app, create a new Project and choose device type (ESP32).
- Note the Auth Token (or credentials) — you will use it in your device code.
- Add widgets to the mobile canvas:
  - Value Display or Gauge (for `aqi`)
  - Gauge or Value (for `temperature`)
  - Value (for `humidity`)
  - Label or Value for `pollution_status`
  - Notification or Email widget for `alert`
  - Chart widget to graph historical values (uses virtual pins)

3) Fields & Virtual Pins
- Blynk uses virtual pins (V0, V1, ...). Decide mapping:
  - V0 → `aqi`
  - V1 → `temperature`
  - V2 → `humidity`
  - V3 → `pollution_status`
  - V4 → `alert`
- In your ESP32 firmware, send updates using the Blynk library or HTTP REST API to update virtual pins.

4) Sending data (HTTP example)
- Blynk HTTP update format (Blynk Cloud or new Blynk IoT differs):

  https://blynk.cloud/external/api/update?token=YOUR_TOKEN&v0=50&v1=25.4&v2=45.2

- For legacy Blynk servers the endpoint is `http://blynk-cloud.com/AUTH_TOKEN/update/V0?value=50`. Check current Blynk docs for exact URLs.

5) Chart setup
- Add a Chart widget to the project, select the virtual pin (e.g., V0 for AQI), and set window (e.g., last 100 points).
- Charts in the mobile app show recent history; for full reports export CSV via the Blynk Cloud or store logs on your own server.

6) Alert widget setup
- Add a Notification widget to the canvas and use server-side triggers (Blynk supports Automation/If This Then That in the cloud UI) or send notifications directly from the device using the Blynk.notify() function when alert conditions occur.
- You can also add an Email widget and/or SMS integration if available for your Blynk plan.

7) Screenshot checklist (what to capture)
- Mobile project canvas showing widgets and virtual pin mappings.
- Widget settings for Chart showing selected virtual pin and time window.
- Notification widget settings or Automation rules screen showing the alert rule.
- Example push notification received on the phone.

C. Field mapping & recommended types
- AQI / air quality value: numeric (field1 / V0) — both ThingSpeak and Blynk graphs support numeric visualization.
- Temperature: numeric (°C) (field2 / V1)
- Humidity: numeric (%) (field3 / V2)
- Pollution status: short text or numeric code (field4 / V3) — if sending text to ThingSpeak, you may need to encode label mapping (e.g., 0=Good,1=Moderate,2=Poor,3=Hazardous).
- Alert status: boolean or numeric (0/1) (field5 / V4) — use this to drive React alerts or notifications.

D. Best practices
- Respect rate limits (ThingSpeak ~15s). Buffer or average fast samples before sending.
- Include timestamps in your local logs; cloud channels automatically add server timestamps.
- Mask API keys in screenshots and README; store keys in a separate `secrets.md` (excluded from Git) or use environment variables for server code.
- For repeatable demos, use the Python simulator to produce consistent CSVs to show dashboard behavior.

E. Quick example: ESP32 HTTP POST to ThingSpeak (Arduino snippet)

```
// Replace WRITE_KEY with your ThingSpeak write key
String url = String("http://api.thingspeak.com/update?api_key=") + WRITE_KEY + "&field1=" + String(aqi) + "&field2=" + String(temp);
http.begin(url);
int code = http.GET();
http.end();
```

F. Quick example: ESP32 HTTP update to Blynk (external API)

```
// Replace TOKEN with your Blynk token
String url = String("https://blynk.cloud/external/api/update?token=") + TOKEN + "&v0=" + String(aqi);
http.begin(url);
int code = http.GET();
http.end();
```

G. Dashboard screenshot instructions (Windows)
- Use Snipping Tool or Win+Shift+S (Snip & Sketch) to take screenshots.
- Capture these images:
  - Full dashboard/channel view showing graphs and latest values.
  - Widget settings showing pin/field mapping and alert thresholds.
  - Notification received (mobile) or email alert example.
  - Serial Monitor and wiring photo.
- Save images in `images/` with descriptive names: `dashboard_channel.png`, `widget_alert.png`, `serial_output.png`, `wiring_photo.jpg`.

H. Next steps (suggested)
- I can create a sample ThingSpeak channel for you (I will not post real data) and provide a prefilled HTTP example for your `esp32_aqi_real.ino`, or
- Implement Blynk virtual pin updates in the firmware and a sample mobile widget layout export.

Which cloud/dashboard should I implement first: ThingSpeak or Blynk?