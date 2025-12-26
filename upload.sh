#!/bin/bash

AMPY="/home/vince/sourcecode/repos-arduino/weather-lamp/venv/bin/ampy"
PORT="/dev/ttyUSB0"
FILES_DIR="weather-lamp"

echo "Uploading files to ESP32 on ${PORT}..."

${AMPY} --port ${PORT} put ${FILES_DIR}/boot.py
echo "✓ Uploaded boot.py"

${AMPY} --port ${PORT} put ${FILES_DIR}/led_driver.py
echo "✓ Uploaded led_driver.py"

${AMPY} --port ${PORT} put ${FILES_DIR}/main.py
echo "✓ Uploaded main.py"

${AMPY} --port ${PORT} put ${FILES_DIR}/sky_colour.py
echo "✓ Uploaded sky_colour.py"

${AMPY} --port ${PORT} put ${FILES_DIR}/weather_data.py
echo "✓ Uploaded weather_data.py"

${AMPY} --port ${PORT} put ${FILES_DIR}/webrepl_cfg.py
echo "✓ Uploaded webrepl_cfg.py"

${AMPY} --port ${PORT} put ${FILES_DIR}/wifi_setup.py
echo "✓ Uploaded wifi_setup.py"

echo "All files uploaded successfully!"
echo "Resetting ESP32..."

python3 << EOF
import serial
import time
try:
    ser = serial.Serial('${PORT}', 115200, timeout=1)
    time.sleep(0.1)
    ser.write(b'\x04')  # Send Ctrl+D (soft reset)
    time.sleep(0.5)
    ser.close()
    print("✓ ESP32 reset complete!")
except Exception as e:
    print(f"Reset error: {e}")
    print("You may need to press the reset button manually")
EOF
echo ""
echo "To view debug output, run:"
echo "  screen ${PORT} 115200"
echo "(Press Ctrl+A then K to exit screen)"
