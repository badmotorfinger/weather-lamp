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

The lamp updates once per hour to avoid paying a monthly fee to use the weather API which this lamp relies on.

### Parts list

* The 3D printed lamp or any other lamp you want to use
* ESP8266
* 4 x NeoPixel's (multi-colour, programable LED lights)
* A free weather subscription to https://darksky.net/dev
* An account on either Azure or AWS to host a function/lambda app to process the JSON data coming from the DarkSky weather API. Alternatively you can host your own API at home.

Unfortunately, I will not be detailing any steps to assemble this project since it was purely a learning excercise for me. What I will say is that the ESP8266 is 
running Micropython which does all of the magic of calling the API and setting the colour of the LED lights. The rest you'll have to figure out :)

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

