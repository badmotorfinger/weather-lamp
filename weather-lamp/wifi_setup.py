import network
import time

print("Init WiFi network")
sta_if = network.WLAN(network.STA_IF)
ap_if = network.WLAN(network.AP_IF)


def init_wifi():
    print("Setting AP to false")
    ap_if.active(False)
    time.sleep(1)
    print("Setting IF to true")
    sta_if.active(True)
    time.sleep(1)
    print("Connecting to WiFi...")
    # Put WiFi details in here
    sta_if.connect('Access Point Name', 'Access Point Password')

    while not sta_if.isconnected():
        print("Connecting...")
        time.sleep_ms(2000)

    print("Connected")


def disable_wifi():
    sta_if.active(False)
