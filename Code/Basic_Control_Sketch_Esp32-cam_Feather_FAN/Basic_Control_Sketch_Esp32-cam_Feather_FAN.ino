#include <Wire.h>
#include <Adafruit_MotorShield.h>

Adafruit_MotorShield AFMS(0x60);  // Use detected address
/*

AFMS is a variable that stands for Adafruit Motor Shield, 
specifically created using the Adafruit_MotorShield class from the Adafruit Motor Shield library.

*/

Adafruit_DCMotor *motor = nullptr;

/*
In this context, nullptr means no object was returned—essentially, 
the function failed to give you a valid pointer to a motor.
E.G.:
Adafruit_DCMotor *motor = AFMS.getMotor(1);
if (motor == nullptr) {
  Serial.println("Motor not found!");
}

*/

void setup() {
  Wire.begin(15, 14);  // SDA = GPIO15, SCL = GPIO14
  Serial.begin(115200);

  if (!AFMS.begin()) {
    Serial.println("Motor Shield not found");
    while (1);
  }

  motor = AFMS.getMotor(1);  // M1
  if (motor) {
    motor->setSpeed(255);  // Max speed
    motor->run(FORWARD);
    Serial.println("Motor should be running");
  } else {
    Serial.println("Motor M1 not initialized");
  }
}

void loop() {
  // Nothing
}
