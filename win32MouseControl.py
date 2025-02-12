import win32api
import serial, time

# Open Serial Connection
ser = serial.Serial('COM3', 115200)
time.sleep(2)

while True:
    line = ser.readline().decode().strip()
    dx, dy = map(int, line.split(","))

    dx = 0 if abs(dx) <= 1 else dx
    dy = 0 if abs(dy) <= 1 else dy

    win32api.mouse_event(0x0001, dx, dy, 0, 0)  # Invert Y-axis if needed
