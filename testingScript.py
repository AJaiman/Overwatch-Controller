import serial
import ctypes
import time

# Update SERIAL_PORT to your Arduino port (e.g., "COM3" on Windows or "/dev/ttyUSB0" on Linux)
SERIAL_PORT = "COM3"
BAUD_RATE = 115200

# Open the serial connection and allow it to initialize
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
time.sleep(2)

def move_mouse_relative(dx, dy):
    """
    Move the mouse by a relative amount using the Windows API.
    The flag 0x0001 indicates relative mouse movement.
    """
    ctypes.windll.user32.mouse_event(0x0001, dx, dy, 0, 0)

while True:
    try:
        line = ser.readline().decode('utf-8').strip()
        if line:
            parts = line.split(',')
            if len(parts) == 2:
                try:
                    dx = int(parts[0])
                    dy = int(parts[1])
                    move_mouse_relative(dx, dy)
                except ValueError:
                    print("Received non-integer values:", parts)
    except KeyboardInterrupt:
        print("Exiting...")
        break
    except Exception as e:
        print("Error:", e)
