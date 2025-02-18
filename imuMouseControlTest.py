import serial
import time
import ctypes
import pyautogui

# Get screen size
screen_width, screen_height = pyautogui.size()

# Start mouse in the center of the screen
ctypes.windll.user32.SetCursorPos(screen_width // 2, screen_height // 2)

# Open serial connection (adjust COM port as needed)
ser = serial.Serial('COM3', 115200, timeout=1)
time.sleep(2)  # Allow time for Arduino to initialize

while True:
    try:
        line = ser.readline().decode('utf-8').strip()
        if line:
            dx, dy = map(float, line.split(","))  # Read and parse dx, dy

            # Move the mouse relative to its current position
            ctypes.windll.user32.mouse_event(0x0001, int(dx), -int(dy), 0, 0)

    except Exception as e:
        print(f"Error: {e}")
        break
