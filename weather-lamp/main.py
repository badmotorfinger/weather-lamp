from machine import Pin
import neopixel
import time

import wifi_setup
from weather_data import WeatherData

print("neopixel init")
pin = Pin(2, Pin.OUT)
np = neopixel.NeoPixel(pin, 4)

while True:
    wifi_setup.init_wifi()
    weather = WeatherData.get_weather()
    wifi_setup.disable_wifi()

    temp1 = weather[0]
    temp2 = weather[1]
    sky1 = weather[2]
    sky2 = weather[3]
    timeSinceLastUpdate = 0

    np[0] = temp1
    np[1] = sky1
    np[2] = sky2
    np[3] = temp2

    np.write()

    time.sleep(3600)
