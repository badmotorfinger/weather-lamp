print("=========== Loading sky_colour.py ===========")

try:
    print("Importing usocket...")
    import usocket
    print("Importing ujson...")
    import ujson as json
    print("Importing math...")
    import math
    print("All sky_colour imports successful")
except Exception as e:
    print("SKY_COLOUR IMPORT ERROR:", e)
    import sys
    if hasattr(sys, 'print_exception'):
        sys.print_exception(e)

print("Defining ConfigManager class...")
class ConfigManager:
    config = None

    @staticmethod
    def fetch_config():
        print ("fetch_config executing")
        url = "http://192.168.1.90/weather-forecast-config"
        response = ConfigManager.__http_get(url)
        if response:
            try:
                ConfigManager.config = json.loads(response)
                print("Configuration successfully loaded.")
            except ValueError as e:  # Use ValueError instead of JSONDecodeError
                print("Failed to parse configuration:", e)
                ConfigManager.config = None
        else:
            print("Failed to fetch configuration.")

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
        response = b""

        try:
            s.connect(addr)
            request = f"GET /{path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
            s.send(request.encode('utf-8'))
            while True:
                data = s.recv(128)
                if data:
                    response += data
                else:
                    break
        except Exception as e:
            print(f"Error during HTTP request: {e}")
        finally:
            if s:
                s.close()

        if response:
            headers, json_data = response.split(b"\r\n\r\n", 1)
            return json_data.decode('utf-8')
        else:
            return None

class SkyColour:
    @staticmethod
    def get_colour_for_temp(temp):
        # Temperature color gradient:
        # 10°C and below: pure blue (0, 0, 255)
        # 18°C: still blue shades
        # 25°C: warm orange-red (255, 100, 0)
        # 40°C and above: pure red (255, 0, 0)

        if temp <= 18:
            return (0, 0, 255)
        elif temp >= 40:
            return (255, 0, 0)
        elif temp < 25:
            # Interpolate from yellow-orange to warm orange-red (18-25°C)
            # No blue component to avoid purple
            ratio = (temp - 18) / 7.0
            r = 255
            g = int(200 - (ratio * 100))  # From 200 down to 100
            b = 0
            return (r, g, b)
        else:
            # Interpolate from warm orange-red to pure red (25-40°C)
            ratio = (temp - 25) / 15.0
            r = 255
            g = int(100 - (ratio * 100))
            b = 0
            return (r, g, b)

    @staticmethod
    def get_colour_for_skycondition(precip):
        # Precipitation color gradient:
        # 0-30%: No color (0, 0, 0)
        # 30%: Very light green (50, 255, 50)
        # 30-80%: Transition from light green to pure green
        # 80% and above: Pure green (0, 255, 0)

        precip_percent = precip * 100

        if precip_percent < 30:
            return (0, 0, 0)
        elif precip_percent >= 80:
            return (0, 255, 0)
        else:
            # Interpolate from light green to pure green (30-80%)
            ratio = (precip_percent - 30) / 50.0
            r = int(50 - (ratio * 50))
            g = 255
            b = int(50 - (ratio * 50))
            return (r, g, b)
