#define VRX_PIN  A0  // Joystick X-axis pin
#define VRY_PIN  A1  // Joystick Y-axis pin

void setup() {
  Serial.begin(115200); // Faster serial communication
}

void loop() {
  int xValue = analogRead(VRX_PIN);
  int yValue = analogRead(VRY_PIN);

  int moveX = map(xValue, 0, 1023, -5, 5);
  int moveY = map(yValue, 0, 1023, -5, 5);

  Serial.print(moveX);
  Serial.print(",");
  Serial.println(moveY);
}
