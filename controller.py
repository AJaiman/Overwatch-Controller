import serial
import time
import ctypes

# --- Setup for using SendInput ---
INPUT_KEYBOARD = 1
INPUT_MOUSE = 0
KEYEVENTF_KEYDOWN = 0x0000
KEYEVENTF_KEYUP = 0x0002
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010

# Define pointer type for extra info
PUL = ctypes.POINTER(ctypes.c_ulong)

class MOUSEINPUT(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class KEYBDINPUT(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class _INPUT(ctypes.Union):
    _fields_ = [("mi", MOUSEINPUT),
                ("ki", KEYBDINPUT)]

class INPUT(ctypes.Structure):
    _anonymous_ = ("u",)
    _fields_ = [("type", ctypes.c_ulong),
                ("u", _INPUT)]

def send_mouse_input(dx, dy):
    """Send relative mouse movement using SendInput."""
    extra = ctypes.c_ulong(0)
    mi = MOUSEINPUT(dx, dy, 0, MOUSEEVENTF_MOVE, 0, ctypes.pointer(extra))
    inp = INPUT(INPUT_MOUSE, _INPUT(mi=mi))
    ctypes.windll.user32.SendInput(1, ctypes.pointer(inp), ctypes.sizeof(inp))

def mouse_click(button, state):
    """Send a mouse click event (left or right) based on the button and state."""
    extra = ctypes.c_ulong(0)
    if button == "left":
        flag = MOUSEEVENTF_LEFTDOWN if state else MOUSEEVENTF_LEFTUP
    elif button == "right":
        flag = MOUSEEVENTF_RIGHTDOWN if state else MOUSEEVENTF_RIGHTUP
    else:
        return
    mi = MOUSEINPUT(0, 0, 0, flag, 0, ctypes.pointer(extra))
    inp = INPUT(INPUT_MOUSE, _INPUT(mi=mi))
    ctypes.windll.user32.SendInput(1, ctypes.pointer(inp), ctypes.sizeof(inp))

def key_press(vk_code, state):
    """Send a key press or release event based on the virtual key code."""
    extra = ctypes.c_ulong(0)
    flag = KEYEVENTF_KEYDOWN if state else KEYEVENTF_KEYUP
    ki = KEYBDINPUT(vk_code, 0, flag, 0, ctypes.pointer(extra))
    inp = INPUT(INPUT_KEYBOARD, _INPUT(ki=ki))
    ctypes.windll.user32.SendInput(1, ctypes.pointer(inp), ctypes.sizeof(inp))

# Virtual Key Codes for letters and shift
VK_SHIFT = 0x10
VK_Q = 0x51
VK_E = 0x45
VK_W = 0x57
VK_A = 0x41
VK_S = 0x53
VK_D = 0x44
VK_R = 0x52

# --- Serial Setup ---
SERIAL_PORT = "COM3"  # Update this as needed (e.g., "COM3" on Windows or "/dev/ttyUSB0" on Linux)
BAUD_RATE = 115200

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
time.sleep(2)  # Allow time for the connection to initialize

# Dictionary to track previous states of keys/buttons
previous_states = {
    "w": False,
    "a": False,
    "s": False,
    "d": False,
    "shift": False,
    "q": False,
    "e": False,
    "right_click": False,
    "left_click": False,
    "r": False
}

while True:
    try:
        line = ser.readline().decode('utf-8').strip()
        if not line:
            continue

        # Expecting an 11-value comma-separated string:
        # w, a, s, d, shift, q, e, right_click, left_click, dx, dy
        parts = line.split(',')
        if len(parts) != 12:
            print("Unexpected data length:", parts)
            continue

        try:
            # Convert all values to integers
            data = list(map(int, parts))
        except ValueError:
            print("Received non-integer values:", parts)
            continue

        # Unpack values
        wPress, aPress, sPress, dPress, shiftPress, qPress, ePress, rightClickPress, leftClickPress, rPress, dx, dy = data

        # Map buttons and joystick directions to their virtual key codes or click labels
        button_map = {
            "shift": (VK_SHIFT, shiftPress),
            "q": (VK_Q, qPress),
            "e": (VK_E, ePress),
            "w": (VK_W, wPress),
            "a": (VK_A, aPress),
            "s": (VK_S, sPress),
            "d": (VK_D, dPress),
            "r": (VK_R, rPress),
            "right_click": ("right", rightClickPress),
            "left_click": ("left", leftClickPress)
        }

        # Process each key/button and send events on state changes
        for button, (vk_code, state) in button_map.items():
            if state and not previous_states[button]:
                if "click" in button:
                    mouse_click(vk_code, True)
                else:
                    key_press(vk_code, True)
            elif not state and previous_states[button]:
                if "click" in button:
                    mouse_click(vk_code, False)
                else:
                    key_press(vk_code, False)
            previous_states[button] = state

        # Process relative mouse movement using the dx, dy values
        send_mouse_input(dx, dy)

    except KeyboardInterrupt:
        print("Exiting...")
        break
    except Exception as e:
        print("Error:", e)
        continue
