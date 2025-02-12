import serial
import time
import ctypes

# --- Setup for using SendInput ---
# Constants for input type and mouse flags:
INPUT_MOUSE = 0
MOUSEEVENTF_MOVE = 0x0001

# Define pointer type for extra info
PUL = ctypes.POINTER(ctypes.c_ulong)

# Define the MOUSEINPUT structure
class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", ctypes.c_long),
        ("dy", ctypes.c_long),
        ("mouseData", ctypes.c_ulong),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", PUL)
    ]

# Define the _INPUT union. (We only use mouse input here.)
class _INPUT(ctypes.Union):
    _fields_ = [
        ("mi", MOUSEINPUT),
        # (Other members for keyboard and hardware input are omitted)
    ]

# Define the INPUT structure
class INPUT(ctypes.Structure):
    _anonymous_ = ("u",)
    _fields_ = [
        ("type", ctypes.c_ulong),
        ("u", _INPUT)
    ]

def send_mouse_input(dx, dy):
    """Simulate relative mouse movement using SendInput."""
    extra = ctypes.c_ulong(0)
    mi = MOUSEINPUT(dx, dy, 0, MOUSEEVENTF_MOVE, 0, ctypes.pointer(extra))
    inp = INPUT(INPUT_MOUSE, _INPUT(mi=mi))
    ctypes.windll.user32.SendInput(1, ctypes.pointer(inp), ctypes.sizeof(inp))

# --- Serial port setup ---
ser = serial.Serial('COM3', 115200)
time.sleep(2)  # Allow time for connection

while True:
    try:
        line = ser.readline().decode().strip()
        dx, dy = map(int, line.split(","))
    except Exception:
        continue

    # Apply a deadzone: if absolute movement is <=1, set it to zero
    dx = 0 if abs(dx) <= 1 else dx
    dy = 0 if abs(dy) <= 1 else dy

    if dx != 0 or dy != 0:
        send_mouse_input(dx, dy)
