# Nerf Controller Overwatch Mod
![nerfcontroller](https://github.com/user-attachments/assets/11d01093-5cc5-4ff6-840c-1b9a19ac65a0)

## Overview

This project repurposes an old Adventure Force toy gun to function as a controller for playing Overwatch, specifically for the character Cassidy. The project involves hardware modification using an Arduino Nano and software implementation via Arduino and Python scripts.

## Hardware Components

- **Adventure Force Sentry X2** (controller case)
- **Arduino Nano** (handles input processing)
- **MPU6050 IMU** (controls mouse movement based on where the user points)
- **Joystick Module** (controls player movement and ultimate ability)
- **Buttons** (handles the rest of Cassidy's abilities)

## Software Components

- **Arduino Script**: Reads input from the modified Nerf controller and prints relevant keyboard/mouse values to serial.
- **Python Script**: Reads serial data from the Arduino, interprets input values, and emulates keyboard/mouse actions to control Cassidy in Overwatch.

## Setup & Installation

### Upload the Arduino Code

- Upload the provided Arduino script to the Arduino Nano using the Arduino IDE.
- Ensure correct baud rate and serial communication settings.

### Install Python Dependencies

Install required Python libraries:

```sh
pip install pyserial
```

### Connect & Run

- Connect the Arduino to the PC via USB (make sure the controller is held still for one second for IMU calibration).
- Make sure to update the name of the USB port in `controller.py`.
- Run the Python script to start reading inputs and emulating controls.

```sh
python controller.py
```

## Limitations

- The Arduino Nano cannot function as an HID device, requiring serial communication with the Python script.
- Some latency may be present depending on serial communication and script execution speed.

