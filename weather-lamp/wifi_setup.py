print("=========== Loading wifi_setup.py ===========")

try:
    print("Importing network...")
    import network
    print("Importing time...")
    import time
    print("All wifi_setup imports successful")
except Exception as e:
    print("WIFI_SETUP IMPORT ERROR:", e)
    import sys
    if hasattr(sys, 'print_exception'):
        sys.print_exception(e)

print("Initializing WiFi interfaces...")
try:
    sta_if = network.WLAN(network.STA_IF)
    print("Station interface created")
    ap_if = network.WLAN(network.AP_IF)
    print("Access point interface created")
except Exception as e:
    print("WIFI INTERFACE INIT ERROR:", e)
    import sys
    if hasattr(sys, 'print_exception'):
        sys.print_exception(e)


def init_wifi():
    max_retries = 10  # Number of retries before giving up
    retries = 0

    print("Disabling AP interface...")
    sta_if.active(False)
    sta_if.active(True)
    sta_if.disconnect()
    ap_if.active(False)

    print("Activating station interface...")
    sta_if.active(True)

    print("Attempting to connect to Wi-Fi...")
    sta_if.connect("Saturday Night Lotion", "$$xxxp37y6152b$$")

    while not sta_if.isconnected() and retries < max_retries:
        retries += 1
        print(f"Waiting for connection... (Attempt {retries}/{max_retries})")
        time.sleep(10)  # Give more time for connection

    if sta_if.isconnected():
        print("Wi-Fi connected successfully!")
        print("Network configuration:", sta_if.ifconfig())
    else:
        print("Failed to connect after", retries, "attempts.")

def disable_wifi():
    sta_if.active(False)
