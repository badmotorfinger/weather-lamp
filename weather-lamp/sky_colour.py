import usocket
import ujson as json
import math

class ConfigManager:
    config = None

    @staticmethod
    def fetch_config():
        url = "http://nodered.home.lan/weather-forecast-config"
        response = ConfigManager.http_get(url)
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
    def http_get(url):
        try:
            import usocket
            _, _, host, path = url.split("/", 3)
            addr_info = usocket.getaddrinfo(host, 80)
            addr = addr_info[0][-1]
            s = usocket.socket()
            s.connect(addr)
            s.send(bytes(f"GET /{path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n", "utf8"))
            response = b""
            while True:
                data = s.recv(128)
                if not data:
                    break
                response += data
            s.close()
            headers, body = response.split(b"\r\n\r\n", 1)
            return body.decode()
        except Exception as e:
            print(f"HTTP request failed: {e}")
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
        return (0, 0, 0)  # Default color if no range matches

# Example usage
ConfigManager.fetch_config()
color = SkyColour.get_colour_for_temp(18)
print(color)
