print("=========== Loading weather_data.py ===========")

try:
    print("Importing usocket...")
    import usocket
    print("Importing ujson...")
    import ujson as json
    print("Importing time...")
    import time
    print("Importing SkyColour...")
    from sky_colour import SkyColour
    print("All weather_data imports successful")
except Exception as e:
    print("WEATHER_DATA IMPORT ERROR:", e)
    import sys
    if hasattr(sys, 'print_exception'):
        sys.print_exception(e)

print("Defining WeatherData class...")
class WeatherData:
    _cached_ip = {}

    @staticmethod
    def get_weather():
        try:
            # Get weather data with safety checks
            result = WeatherData.__get_weather_data()
            if not result or len(result) != 3:
                print("Invalid weather data response")
                return None
                
            oneToFourHours, fourToEightHours, updated_at = result
            
            # Check if we have valid data
            if not oneToFourHours or not fourToEightHours:
                print("Missing weather forecast data")
                return None
                
            # Convert to RGB colors
            try:
                temp1 = SkyColour.get_colour_for_temp(oneToFourHours["averageTemp"])
                temp2 = SkyColour.get_colour_for_temp(fourToEightHours["averageTemp"])
                sky1 = SkyColour.get_colour_for_skycondition(oneToFourHours["averagePrecip"])
                sky2 = SkyColour.get_colour_for_skycondition(fourToEightHours["averagePrecip"])
            except Exception as e:
                print(f"Error converting to colors: {e}")
                return None
                
            # Determine if LEDs should be enabled based on time
            leds_enabled = WeatherData._should_enable_leds(updated_at)
            
            # Return all values
            return (temp1, temp2, sky1, sky2, leds_enabled)
        except Exception as e:
            print(f"Error in get_weather: {e}")
            return None
    
    @staticmethod
    def _should_enable_leds(iso_date):
        if not iso_date:
            print("No date available, defaulting to enabled")
            return True  # Default to enabled if no date available
            
        try:
            # Parse ISO date (format: "2025-05-05T05:49:18.948Z")
            print(f"Parsing date: '{iso_date}'")
            
            # Add safety check for string format
            if not isinstance(iso_date, str) or len(iso_date) < 16:
                print(f"Invalid date format: {iso_date}")
                return True
                
            year = int(iso_date[0:4])
            month = int(iso_date[5:7])
            day = int(iso_date[8:10])
            hour = int(iso_date[11:13])
            minute = int(iso_date[14:16])
            
            # Add 9 hours to the UTC time
            hour = (hour + 9) % 24
            
            # Check if time is between 5 AM and 9 PM
            print(f"Current local time (UTC+9): {hour}:{minute}")
            enabled = 5 <= hour < 21
            print(f"LEDs enabled: {enabled}")
            return enabled
        except Exception as e:
            print(f"Error parsing date: '{iso_date}' - {e}")
            return True  # Default to enabled on error

    @staticmethod
    def __get_weather_data():
        print("Calling API to get weather")
        url = "http://192.168.1.90/weather-forecast"
        response = WeatherData.__http_get(url)
        if response:
            return WeatherData.__process_weather_data(response)
        else:
            print("No response received.")
            return None, None, None

    @staticmethod
    def __http_get(url):
        _, _, host, path = url.split("/", 3)

        # Check if IP address is already cached
        if host in WeatherData._cached_ip:
            addr = WeatherData._cached_ip[host]
            print(f"Using cached IP for {host}: {addr}")
        else:
            addr = None
            # Resolve hostname with retry mechanism
            for _ in range(3):
                try:
                    addr = usocket.getaddrinfo(host, 80)[0][-1]
                    # Cache the resolved IP address
                    WeatherData._cached_ip[host] = addr
                    print(f"Resolved and cached IP for {host}: {addr}")
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
            
            # Safely get required fields with detailed error reporting
            one_to_four = weather.get("oneToFourHours")
            if not one_to_four:
                print("oneToFourHours field missing or null")
                
            four_to_eight = weather.get("fourToEightHours")
            if not four_to_eight:
                print("fourToEightHours field missing or null")
                
            # Extract the updatedAt string, safely handling different formats
            updated_at = weather.get("updatedAt", None)
            print(f"Raw updatedAt: {updated_at}")
            
            # Clean up the updatedAt string if needed
            if updated_at:
                if isinstance(updated_at, str):
                    # Remove quotes if present
                    if updated_at.startswith('"') and updated_at.endswith('"'):
                        updated_at = updated_at[1:-1]
                else:
                    # Convert to string if it's another type
                    updated_at = str(updated_at)
            
            print(f"Processed timestamp: {updated_at}")
            return one_to_four, four_to_eight, updated_at
        except Exception as e:  # Use broader exception handling
            import sys
            print(f"Error processing weather data: {e}")
            print("Exception type:", type(e).__name__)
            # Print traceback info if available
            if hasattr(sys, 'print_exception'):
                sys.print_exception(e)
            return None, None, None
