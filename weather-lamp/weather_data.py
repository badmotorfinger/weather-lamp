import json

from sky_colour import SkyColour


class WeatherData:

    @staticmethod
    def get_weather():
        rawWeatherData = WeatherData.__get_weather_data()
        # print(rawWeatherData)
        weatherDataStartIndex = rawWeatherData.index("{")
        jsonResponse = rawWeatherData[weatherDataStartIndex:]
        weather = json.loads(jsonResponse)
        # print(weather)
        oneToFourHours = weather["oneToFourHours"]
        fourToEightHours = weather["fourToEightHours"]
        # oneToFourHours = json.loads('{"averageCloudCover": 0.50, "averageTemp":40.6014, "averagePrecip": 0.17}')
        # fourToEightHours = json.loads('{"averageCloudCover": 0.50, "averageTemp": 40.6014, "averagePrecip": 0.17}')

        temp1 = SkyColour.get_colour_for_temp(oneToFourHours["averageTemp"])
        temp2 = SkyColour.get_colour_for_temp(fourToEightHours["averageTemp"])
        sky1 = SkyColour.get_colour_for_skycondition(oneToFourHours["averageCloudCover"],
                                                     oneToFourHours["averagePrecip"])
        sky2 = SkyColour.get_colour_for_skycondition(fourToEightHours["averageCloudCover"],
                                                     fourToEightHours["averagePrecip"])

        return (temp1, temp2, sky1, sky2)

    @staticmethod
    def __get_weather_data():
        import usocket as _socket
        import ussl as ssl

        print("Calling API to get weather")
        url = "https://weather-at-home.azurewebsites.net/api/GetWeather"

        _, _, host, path = url.split("/", 3)
        addr = _socket.getaddrinfo(host, 443)[0][-1]
        s = _socket.socket()
        print("Connecting to " + url)
        s.connect(addr)
        s = ssl.wrap_socket(s)

        s.write(
            bytes(
                "GET /%s HTTP/1.0\r\nspecial-key:OogZC#PFD$OxYgfXWZigj6Zh7a4gvRk0\r\nAccept: */*\r\n User-Agent: WeatherLamp\r\nHost: %s\r\n\r\n"
                % (path, host),
                "utf8",
            )
        )

        json = ""

        print("Web request finished. Reading stream...")
        while True:
            data = s.read(128)

            if data:
                json = json + str(data, "utf-8")
            else:
                break
        s.close()
        print("Web socket closed")
        print(json)
        return json
