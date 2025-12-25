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
        if ConfigManager.config is None:
            print("Configuration is not loaded.")
            return (255, 255, 255)  # Default color or handle the error differently

        temp_ranges = ConfigManager.config.get('temp_ranges', [])
        temp = math.floor(temp)
        for range in temp_ranges:
            if range['min'] <= temp <= range['max']:
                return tuple(range['color'])
        return (255, 255, 255)  # Default color if no range matches

    @staticmethod
    def get_colour_for_skycondition(precip):
        precip = math.floor(precip * 100)
        precip_ranges = ConfigManager.config.get('precip_ranges', [])
        for range in precip_ranges:
            if range['min'] <= precip <= range['max']:
                return tuple(range['color'])
        return (255, 255, 255)  # Default color if no range matches
