print("=========== STARTING MAIN.PY ===========")

try:
    print("Importing machine.Pin...")
    from machine import Pin
    print("Importing neopixel...")
    import neopixel
    print("Importing time...")
    import time
    print("Importing wifi_setup...")
    import wifi_setup
    print("Importing WeatherData...")
    from weather_data import WeatherData
    print("Importing ConfigManager...")
    from sky_colour import ConfigManager
    
    print("All imports successful")
except Exception as e:
    print("IMPORT ERROR:", e)
    import sys
    if hasattr(sys, 'print_exception'):
        sys.print_exception(e)

print("Initializing NeoPixel...")
try:
    pin = Pin(4, Pin.OUT)
    print("Pin created")
    np = neopixel.NeoPixel(pin, 4)
    print("NeoPixel object created")
    
    # Initial startup pattern - all purple
    print("Setting initial colors...")
    for i in range(4):
        np[i] = (255, 0, 255)
    np.write()
    print("LEDs initialized with purple")
    
    # Turn on first LED to show we're starting
    np[0] = (0, 255, 0)
    np.write()
    print("First LED set to green")
except Exception as e:
    print("LED INIT ERROR:", e)
    import sys
    if hasattr(sys, 'print_exception'):
        sys.print_exception(e)

print("Starting main loop...")

# Simple debug LED function
def set_debug_led(r, g, b):
    try:
        for i in range(4):
            np[i] = (r, g, b)
        np.write()
        print(f"Set all LEDs to ({r}, {g}, {b})")
    except Exception as e:
        print(f"Error setting debug LEDs: {e}")

# Basic test of LEDs
print("Testing LEDs...")
try:
    # Red
    set_debug_led(255, 0, 0)
    time.sleep(0.5)
    
    # Green
    set_debug_led(0, 255, 0)
    time.sleep(0.5)
    
    # Blue
    set_debug_led(0, 0, 255)
    time.sleep(0.5)
    
    # Off
    set_debug_led(0, 0, 0)
    time.sleep(0.5)
    
    print("LED test complete")
except Exception as e:
    print("LED test failed:", e)

print("Entering main loop...")
loop_count = 0

while True:
    try:
        loop_count += 1
        print(f"\n=============== LOOP {loop_count} ===============")
        
        # Show we're connecting - purple
        print("Setting connecting indicator LED...")
        np[0] = (255, 0, 255)
        np.write()
        
        print("Connecting to WiFi...")
        wifi_setup.init_wifi()
        print("WiFi connected")
        
        # Show we're fetching config - blue
        print("Setting config indicator LED...")
        np[1] = (0, 0, 255)
        np.write()
        
        print("Fetching configuration...")
        ConfigManager.fetch_config()
        print("Configuration fetched")
        
        # Show we're getting weather - yellow
        print("Setting weather indicator LED...")
        np[2] = (255, 255, 0)
        np.write()
        
        print("Getting weather data...")
        weather = WeatherData.get_weather()
        print(f"Weather data result: {weather}")
        
        # Show we're disconnecting - red
        print("Setting disconnect indicator LED...")
        np[3] = (255, 0, 0)
        np.write()
        
        print("Disabling WiFi...")
        wifi_setup.disable_wifi()
        print("WiFi disabled")
        
        # Process weather data if available
        print("Processing weather result...")
        if weather:
            try:
                weather_len = len(weather)
                print(f"Weather data type: {type(weather)}, length: {weather_len}")
            except:
                weather_len = 0
                print(f"Weather data type: {type(weather)}, length: cannot determine")

            if weather_len == 5:
                print("Valid weather data received")
                try:
                    temp1 = weather[0]
                    temp2 = weather[1]
                    sky1 = weather[2]
                    sky2 = weather[3]
                    leds_enabled = weather[4]
                    
                    print(f"Weather data values:")
                    print(f"- temp1: {temp1}")
                    print(f"- temp2: {temp2}")
                    print(f"- sky1: {sky1}")
                    print(f"- sky2: {sky2}")
                    print(f"- leds_enabled: {leds_enabled}")
                    
                    if leds_enabled:
                        print("Setting weather colors to LEDs...")
                        np[0] = temp1
                        np[1] = sky1
                        np[2] = sky2
                        np[3] = temp2
                        print("Weather colors set")
                    else:
                        print("Nighttime mode - turning off LEDs...")
                        for i in range(4):
                            np[i] = (0, 0, 0)
                        print("LEDs turned off")
                except Exception as e:
                    print("Error setting LED colors:", e)
                    import sys
                    if hasattr(sys, 'print_exception'):
                        sys.print_exception(e)
                    print("Setting error indicator (orange)")
                    for i in range(4):
                        np[i] = (255, 128, 0)  # Orange for color setting error
            else:
                print("Invalid weather data structure")
                print("Setting error indicator (red)")
                for i in range(4):
                    np[i] = (255, 0, 0)  # All red on error
        else:
            print("No weather data received")
            print("Setting error indicator (red)")
            for i in range(4):
                np[i] = (255, 0, 0)  # All red on error
        
        print("Writing final LED state...")
        np.write()
        print("Sleeping for 5 minutes...")
        time.sleep(300)
        
    except Exception as e:
        print("CRITICAL ERROR in main loop:", e)
        import sys
        if hasattr(sys, 'print_exception'):
            sys.print_exception(e)
        # Error pattern - all cyan
        print("Setting critical error indicator (cyan)")
        for i in range(4):
            np[i] = (0, 255, 255)
        try:
            np.write()
        except Exception as write_error:
            print("Even np.write() failed:", write_error)
        print("Sleeping for 30 seconds before retry...")
        time.sleep(30)