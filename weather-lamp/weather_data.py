import usocket
import ujson as json
from sky_colour import SkyColour

class WeatherData:
    @staticmethod
    def get_weather():
        oneToFourHours, fourToEightHours = WeatherData.__get_weather_data()

        if oneToFourHours and fourToEightHours:
            temp1 = SkyColour.get_colour_for_temp(oneToFourHours["averageTemp"])
            temp2 = SkyColour.get_colour_for_temp(fourToEightHours["averageTemp"])
            sky1 = SkyColour.get_colour_for_skycondition(oneToFourHours["averagePrecip"])
            sky2 = SkyColour.get_colour_for_skycondition(fourToEightHours["averagePrecip"])
            return (temp1, temp2, sky1, sky2)
        else:
            print("Incomplete weather data received.")
            return None

    @staticmethod
    def __get_weather_data():
        print("Calling API to get weather")
        url = "http://nodered.home.lan/weather-forecast"
        response = WeatherData.__http_get(url)
        if response:
            return WeatherData.__process_weather_data(response)
        else:
            print("No response received.")
            return None, None

    @staticmethod
    def __http_get(url):
        _, _, host, path = url.split("/", 3)
        addr = None
        # Resolve hostname with retry mechanism
        for _ in range(3):
            try:
                addr = usocket.getaddrinfo(host, 80)[0][-1]
                break
            except OSError as e:
                print(f"Error resolving hostname: {e}")

        if not addr:
            print("Failed to resolve hostname after multiple attempts.")
            return None

        # Connect to server and retrieve data
        s = usocket.socket()
        try:
            s.connect(addr)
            request = f"GET /{path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
            s.send(request.encode('utf-8'))
            response = b""
            while True:
                data = s.recv(128)
                if data:
                    response += data
                else:
                    break
        except Exception as e:
            print(f"Error during HTTP request: {e}")
        finally:
            s.close()

        if response:
            headers, json_data = response.split(b"\r\n\r\n", 1)
            return json_data.decode('utf-8')
        else:
            return None

    @staticmethod
    def __process_weather_data(json_data):
        try:
            weather = json.loads(json_data)
            print(weather)
            return weather["oneToFourHours"], weather["fourToEightHours"]
        except ValueError as e:  # Handling JSON errors with ValueError in ujson
            print(f"Error processing weather data: {e}")
            return None, None
