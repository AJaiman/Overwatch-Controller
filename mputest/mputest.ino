#include <Wire.h>
#include <MPU6050.h>

MPU6050 mpu;

float sensitivity = 10; // Adjust for more or less movement responsiveness
float dx = 0, dy = 0;

void setup() {
  Serial.begin(115200);

  // Initialize MPU6050
  while (!mpu.begin(MPU6050_SCALE_250DPS, MPU6050_RANGE_2G)) {
    Serial.println("Could not find a valid MPU6050 sensor, check wiring!");
    delay(500);
  }

  mpu.calibrateGyro(); // Calibrate gyroscope while at rest
  mpu.setThreshold(3); // Reduce noise by ignoring small movements
}

void loop() {
  Vector normGyro = mpu.readNormalizeGyro();

  // Convert angular velocity to relative screen movement
  dx = -1 * normGyro.ZAxis / sensitivity;  // Left/Right movement
  dy = normGyro.XAxis / sensitivity;  // Up/Down movement

  // Print dx and dy to Serial monitor for Python script
  Serial.print(dx);
  Serial.print(",");
  Serial.println(dy);

  delay(10); // Small delay to maintain responsiveness
}
