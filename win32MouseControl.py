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
    extra = ctypes.c_ulong(0)
    mi = MOUSEINPUT(dx, dy, 0, MOUSEEVENTF_MOVE, 0, ctypes.pointer(extra))
    inp = INPUT(INPUT_MOUSE, _INPUT(mi=mi))
    ctypes.windll.user32.SendInput(1, ctypes.pointer(inp), ctypes.sizeof(inp))

def mouse_click(button, state):
    extra = ctypes.c_ulong(0)
    flag = MOUSEEVENTF_LEFTDOWN if button == "left" and state else MOUSEEVENTF_LEFTUP
    if button == "right":
        flag = MOUSEEVENTF_RIGHTDOWN if state else MOUSEEVENTF_RIGHTUP

    mi = MOUSEINPUT(0, 0, 0, flag, 0, ctypes.pointer(extra))
    inp = INPUT(INPUT_MOUSE, _INPUT(mi=mi))
    ctypes.windll.user32.SendInput(1, ctypes.pointer(inp), ctypes.sizeof(inp))

def key_press(vk_code, state):
    extra = ctypes.c_ulong(0)
    flag = KEYEVENTF_KEYDOWN if state else KEYEVENTF_KEYUP
    ki = KEYBDINPUT(vk_code, 0, flag, 0, ctypes.pointer(extra))
    inp = INPUT(INPUT_KEYBOARD, _INPUT(ki=ki))
    ctypes.windll.user32.SendInput(1, ctypes.pointer(inp), ctypes.sizeof(inp))

VK_SHIFT = 0x10
VK_Q = 0x51
VK_E = 0x45

ser = serial.Serial('COM3', 115200)
time.sleep(2)

previous_states = {"shift": False, "q": False, "e": False, "right_click": False, "left_click": False}

while True:
    try:
        line = ser.readline().decode().strip()
        data = list(map(int, line.split(",")))

        dx, dy, shiftPress, qPress, ePress, rightClickPress, leftClickPress = data

        dx = 0 if abs(dx) <= 1 else dx
        dy = 0 if abs(dy) <= 1 else dy

        if dx != 0 or dy != 0:
            send_mouse_input(dx, dy)

        button_map = {
            "shift": (VK_SHIFT, shiftPress),
            "q": (VK_Q, qPress),
            "e": (VK_E, ePress),
            "right_click": ("right", rightClickPress),
            "left_click": ("left", leftClickPress)
        }

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
    except Exception as e:
        print("Error:", e)
        continue
