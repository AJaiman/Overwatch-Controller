#include <Wire.h>
#include <MPU6050.h>

MPU6050 mpu;

// Sensitivity scaling factors (adjust these to tune movement)
const float SENSITIVITY_YAW = 50.0;   // Scale factor for yaw (dx)
const float SENSITIVITY_ROLL = 50.0;  // Scale factor for roll (dy)

float yaw = 0, roll = 0;
float prevYaw = 0, prevRoll = 0;
unsigned long timer = 0;
float timeStep = 0.01;

void setup() {
  Serial.begin(115200);

  // Initialize MPU6050
  while (!mpu.begin(MPU6050_SCALE_2000DPS, MPU6050_RANGE_2G)) {
    Serial.println("Could not find a valid MPU6050 sensor, check wiring!");
    delay(500);
  }

  // Calibrate gyroscope at rest
  mpu.calibrateGyro();
  mpu.setThreshold(3);
}

void loop() {
  timer = millis();
  
  // Save previous integrated angles
  prevYaw = yaw;
  prevRoll = roll;
  
  // Read gyroscope angular velocities
  Vector norm = mpu.readNormalizeGyro();
  
  // Integrate angular velocities to update positions
  yaw  += norm.ZAxis * timeStep;
  roll += norm.XAxis * timeStep;
  
  // Compute change in position (relative movement)
  float deltaYaw = yaw - prevYaw;   // change in yaw
  float deltaRoll = roll - prevRoll; // change in roll
  
  // Scale to get relative movement in pixels
  int dx = (int)(deltaYaw * SENSITIVITY_YAW);
  int dy = (int)(deltaRoll * SENSITIVITY_ROLL);
  
  // Print relative movement values as "dx,dy"
  Serial.print(dx*-1);
  Serial.print(",");
  Serial.println(dy*-1);
  
  // Ensure consistent loop timing
  delay((timeStep * 1000) - (millis() - timer));
}
