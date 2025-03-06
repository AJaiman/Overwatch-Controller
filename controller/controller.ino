#include <Wire.h>
#include <MPU6050.h>

MPU6050 mpu;

// --- MPU6050 (Mouse Control) Variables ---
const float SENSITIVITY_YAW = 50.0;   // Scale factor for yaw (dx)
const float SENSITIVITY_ROLL = 50.0;  // Scale factor for roll (dy)
float yaw = 0, roll = 0;
float prevYaw = 0, prevRoll = 0;
unsigned long timer = 0;
float timeStep = 0.01;

// --- Joystick & Button Definitions ---
#define VRX_PIN  A0  // Joystick X-axis pin
#define VRY_PIN  A1  // Joystick Y-axis pin

#define SHIFT_PIN 3
#define Q_PIN 2
#define E_PIN 4
#define RIGHT_CLICK_PIN 5
#define LEFT_CLICK_PIN 6
#define R_PIN 7

bool w = false;
bool a = false;
bool s = false;
bool d = false;

void setup() {
  Serial.begin(115200);

  // Initialize MPU6050
  while (!mpu.begin(MPU6050_SCALE_2000DPS, MPU6050_RANGE_2G)) {
    Serial.println("Could not find a valid MPU6050 sensor, check wiring!");
    delay(500);
  }
  mpu.calibrateGyro();
  mpu.setThreshold(3);

  // Initialize button pins with internal pull-ups
  pinMode(SHIFT_PIN, INPUT_PULLUP);
  pinMode(Q_PIN, INPUT_PULLUP);
  pinMode(E_PIN, INPUT_PULLUP);
  pinMode(RIGHT_CLICK_PIN, INPUT_PULLUP);
  pinMode(LEFT_CLICK_PIN, INPUT_PULLUP);
  pinMode(R_PIN, INPUT_PULLUP);
}

void loop() {
  timer = millis();

  // ----- MPU6050 Processing for Relative Mouse Movement -----
  prevYaw = yaw;
  prevRoll = roll;

  // Read gyroscope angular velocities
  Vector norm = mpu.readNormalizeGyro();

  // Integrate angular velocities to update angles
  yaw  += norm.ZAxis * timeStep;
  roll += norm.XAxis * timeStep;

  // Compute change (delta) in angles
  float deltaYaw = yaw - prevYaw;
  float deltaRoll = roll - prevRoll;

  // Convert changes to relative pixel movement and invert signs
  int dx = (int)(deltaYaw * SENSITIVITY_YAW) * -1;
  int dy = (int)(deltaRoll * SENSITIVITY_ROLL) * -1;

  // ----- Joystick & Button Processing -----
  int xValue = analogRead(VRX_PIN);
  int yValue = analogRead(VRY_PIN);

  int moveX = map(xValue, 0, 1023, -5, 5);
  int moveY = map(yValue, 0, 1023, -5, 5);

  // Set directional booleans based on joystick threshold
  d = (moveX > 2);
  a = (moveX < -2);
  s = (moveY > 2);
  w = (moveY < -2);

  // Read button states (active LOW)
  bool shiftPress = (digitalRead(SHIFT_PIN) == LOW);
  bool qPress = (digitalRead(Q_PIN) == LOW);
  bool ePress = (digitalRead(E_PIN) == LOW);
  bool rightClickPress = (digitalRead(RIGHT_CLICK_PIN) == LOW);
  bool leftClickPress = (digitalRead(LEFT_CLICK_PIN) == LOW);
  bool rPress = (digitalRead(R_PIN) == LOW);

  // ----- Combined Serial Output -----
  // Print joystick and button states first (w,a,s,d, shift, q, e, rightClick, leftClick)
  Serial.print(w);
  Serial.print(",");
  Serial.print(a);
  Serial.print(",");
  Serial.print(s);
  Serial.print(",");
  Serial.print(d);
  Serial.print(",");
  Serial.print(shiftPress);
  Serial.print(",");
  Serial.print(qPress);
  Serial.print(",");
  Serial.print(ePress);
  Serial.print(",");
  Serial.print(rightClickPress);
  Serial.print(",");
  Serial.print(leftClickPress);
  Serial.print(",");
  Serial.print(rPress);

  
  // Append the relative mouse movement (dx, dy) at the end
  Serial.print(",");
  Serial.print(dx);
  Serial.print(",");
  Serial.println(dy);

  // Ensure consistent loop timing
  int delayTime = (timeStep * 1000) - (millis() - timer);
  if(delayTime > 0) {
    delay(delayTime);
  }
}
