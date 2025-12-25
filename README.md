## weather-lamp

A lamp which changes colour based on the forecast weather for your area.

![Screenshot](https://raw.githubusercontent.com/badmotorfinger/weather-lamp/master/lamp-img.jpg)

### Colour scheme for the top half of the lamp

The top half of the lamp contains two LED's. The top-most LED changes colour depending on an average temperature calculated over the next 1 - 4 hours. 

The bottom LED in top half of the lamp changes colour depending on the chance of rain between the next 1 - 4 hours. This value is not based on an average but rather the highest percentage chance over the next 4 hour period.

### Colour scheme for the bottom half of the lamp

Same as above but based on a time period which is 4 hours after. In other words, the top half of the lamp is for the next 1 - 4 hours and the bottom half of the lamp
is for the next 4 - 8 hours.

### Update interval

The lamp updates every 5 minutes. The Node-RED backend fetches fresh data from OpenWeatherMap every 10 minutes to stay within the free tier API limits (1000 calls/day).

### Parts list

* The 3D printed lamp or any other lamp you want to use
* ESP8266
* 4 x NeoPixel's (multi-colour, programmable LED lights)
* A free API key from https://openweathermap.org/api
* Node-RED installed on a local server (e.g., Raspberry Pi or home server)

## Setup Instructions

### 1. Hardware Setup

* Connect 4 NeoPixel LEDs to GPIO pin 4 on the ESP8266
* Power the ESP8266 and NeoPixels appropriately

### 2. ESP8266 Setup

1. Install MicroPython on your ESP8266
2. Upload all files from the `weather-lamp/` directory to the ESP8266
3. Edit `wifi_setup.py` (line 42) and update with your WiFi credentials:
   ```python
   sta_if.connect("YOUR_SSID", "YOUR_PASSWORD")
   ```
4. Update the Node-RED server IP address if not using `192.168.1.90`:
   - Edit `weather_data.py` line 94
   - Edit `sky_colour.py` line 24

### 3. Node-RED Setup

1. Install Node-RED on your local server
2. Import the flow from `nodered-flow-import.json`:
   - Open Node-RED web interface
   - Menu → Import → Paste the contents of `nodered-flow-import.json`
3. **Update the OpenWeatherMap API key**:
   - Double-click the "http request" node
   - Replace `PUT YOUR API KEY HERE` with your actual OpenWeatherMap API key
   - Update the latitude and longitude coordinates for your location (currently set to -33.426594, 151.342504)
4. Deploy the flow

### 4. Features

* **Automatic updates**: The lamp checks weather every 5 minutes
* **Nighttime mode**: LEDs automatically turn off between 9 PM and 5 AM (UTC+9 timezone)
* **Cached data**: Node-RED caches weather data and fetches from OpenWeatherMap every 10 minutes
* **Offline resilience**: If the API call fails, the lamp uses the last cached response

### 5. LED Positions

**Top half** (1-4 hours forecast):
* **LED 0**: Temperature for next 1-4 hours
* **LED 1**: Precipitation chance for next 1-4 hours

**Bottom half** (4-8 hours forecast):
* **LED 2**: Precipitation chance for next 4-8 hours
* **LED 3**: Temperature for next 4-8 hours

### 6. Color Configuration

**Temperature colors** (Celsius):
* Blue (0,0,255): ≤14°C - Cold
* Light blue/yellow (255,204,100): 17-20°C - Mild
* Orange (255,120,100): 21-25°C - Warm
* Red-orange (255,51,51): 29-33°C - Hot
* Red (255,0,0): ≥34°C - Very hot

**Precipitation colors** (% chance):
* Off (0,0,0): 0-39% - No rain expected
* Light green (204,255,204): 40-60% - Possible rain
* Medium green (153,255,153): 61-80% - Likely rain
* Bright green (0,255,0): 91-100% - Rain certain

Colors can be customized by editing the Node-RED function node "Return Weather Config Data".

## Debugging

Enter these commands in the Mu REPL to debug

`import main`

Or

```
from weather_data import WeatherData
weather_data = WeatherData()
print(weather_data.get_weather())
```

Enjoy!

