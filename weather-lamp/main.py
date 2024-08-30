from machine import Pin
import neopixel
import time

import wifi_setup
from weather_data import WeatherData
from sky_colour import ConfigManager

print("neopixel init")
pin = Pin(2, Pin.OUT)
np = neopixel.NeoPixel(pin, 4)

np[0] = (0, 0, 0)
np[1] = (0, 0, 0)
np[2] = (0, 0, 0)
np[3] = (255, 0, 0)
np.write()

while True:

    try:
        np[0] = (0, 0, 0)
        np[1] = (0, 0, 0)
        np[2] = (0, 0, 0)
        np[3] = (255, 0, 0)
        np.write()

        wifi_setup.init_wifi()
        ConfigManager.fetch_config()
        weather = WeatherData.get_weather()
        wifi_setup.disable_wifi()

        temp1 = weather[0]
        temp2 = weather[1]
        sky1 = weather[2]
        sky2 = weather[3]

        np[0] = temp1
        np[1] = sky1
        np[2] = sky2
        np[3] = temp2
        np.write()

    except:
        print("Failed to get weather")
        np[0] = np[1] = np[2] = np[3] = (255, 0, 0)
        np.write()

    time.sleep(300)
