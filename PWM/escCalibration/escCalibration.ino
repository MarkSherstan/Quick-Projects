#include <Servo.h>

#define MAX_SIGNAL 2000
#define MIN_SIGNAL 1000

#define MOTOR_PIN_1 9
#define MOTOR_PIN_2 10
#define MOTOR_PIN_3 11
#define MOTOR_PIN_4 12

int DELAY = 1000;

Servo motor1;
Servo motor2;
Servo motor3;
Servo motor4;

void setup() {
  Serial.begin(9600);

  delay(1000);
  Serial.println("Press any key to start the ESC's");

  // Wait for input
  while (!Serial.available());
  Serial.read();

  // Initialize PWM pins and display message
  motor1.attach(MOTOR_PIN_1);
  motor2.attach(MOTOR_PIN_2);
  motor3.attach(MOTOR_PIN_3);
  motor4.attach(MOTOR_PIN_4);

  Serial.print("Writing maximum output: ");Serial.print(MAX_SIGNAL);Serial.println(" us");
  Serial.println("Turn on power source, wait 3 seconds and then press any key.");

  // Send max output
  motor1.writeMicroseconds(MAX_SIGNAL);
  motor2.writeMicroseconds(MAX_SIGNAL);
  motor3.writeMicroseconds(MAX_SIGNAL);
  motor4.writeMicroseconds(MAX_SIGNAL);

  // Wait for input
  while (!Serial.available());
  Serial.read();

  // Send min output and display message
  Serial.println("\n");
  Serial.print("Sending minimum output: ");Serial.print(MIN_SIGNAL);Serial.println(" us");

  motor1.writeMicroseconds(MIN_SIGNAL);
  motor2.writeMicroseconds(MIN_SIGNAL);
  motor3.writeMicroseconds(MIN_SIGNAL);
  motor4.writeMicroseconds(MIN_SIGNAL);

  // Instructions to test functionality
  Serial.println("\n");
  Serial.println("The ESC is calibrated");
  Serial.println("----");
  Serial.println("Type a values between 1000 and 2000 and press enter");
  Serial.println("and the motor will start rotating.");
  Serial.println("Send 1000 to stop the motor and 2000 for full throttle");

}

void loop() {

  if (Serial.available() > 0){
    int DELAY = Serial.parseInt();

    if (DELAY > 999) {
      motor1.writeMicroseconds(DELAY);
      motor2.writeMicroseconds(DELAY);
      motor3.writeMicroseconds(DELAY);
      motor4.writeMicroseconds(DELAY);
      float SPEED = (DELAY-1000)/10;
      Serial.print("\n");
      Serial.println("Motor speed:"); Serial.print("  "); Serial.print(SPEED); Serial.print("%");
    }

  }

}
