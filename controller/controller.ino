#define VRX_PIN  A0  // Joystick X-axis pin
#define VRY_PIN  A1  // Joystick Y-axis pin

// Define Button Pins
#define SHIFT_PIN 3
#define Q_PIN 2
#define E_PIN 4
#define RIGHT_CLICK_PIN 5
#define LEFT_CLICK_PIN 6

void setup() {
  Serial.begin(115200); // Faster serial communication

  pinMode(SHIFT_PIN, INPUT_PULLUP);
  pinMode(Q_PIN, INPUT_PULLUP);
  pinMode(E_PIN, INPUT_PULLUP);
  pinMode(RIGHT_CLICK_PIN, INPUT_PULLUP);
  pinMode(LEFT_CLICK_PIN, INPUT_PULLUP);
}

void loop() {
  int xValue = analogRead(VRX_PIN);
  int yValue = analogRead(VRY_PIN);

  int moveX = map(xValue, 0, 1023, -5, 5);
  int moveY = map(yValue, 0, 1023, -5, 5);

  // Read Button States
  bool shiftPress = digitalRead(SHIFT_PIN) == LOW;
  bool qPress = digitalRead(Q_PIN) == LOW;
  bool ePress = digitalRead(E_PIN) == LOW;
  bool rightClickPress = digitalRead(RIGHT_CLICK_PIN) == LOW;
  bool leftClickPress = digitalRead(LEFT_CLICK_PIN) == LOW;

  Serial.print(moveX);
  Serial.print(",");
  Serial.print(moveY);
  Serial.print(",");
  Serial.print(shiftPress);
  Serial.print(",");
  Serial.print(qPress);
  Serial.print(",");
  Serial.print(ePress);
  Serial.print(",");
  Serial.print(rightClickPress);
  Serial.print(",");
  Serial.println(leftClickPress);
}
