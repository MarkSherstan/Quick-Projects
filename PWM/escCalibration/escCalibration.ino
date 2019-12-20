#include <Servo.h>

// Max and min of of ESC
#define MAX_SIGNAL 2000
#define MIN_SIGNAL 1000

// Pinout
#define MOTOR_PIN_1 9
#define MOTOR_PIN_2 10
#define MOTOR_PIN_3 11
#define MOTOR_PIN_4 12

// Var def
int PULSE = 1000;
float SPEED;

// Set up the ESC servo classes
Servo motor1;
Servo motor2;
Servo motor3;
Servo motor4;


void setup() {
  // Start serial port and display some messages
  Serial.begin(9600); delay(1000);
  Serial.println("##########################################");
  Serial.println("REMOVE PROPELLERS!!!");
  Serial.println("##########################################");
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
  Serial.print("Sending minimum output: "); Serial.print(MIN_SIGNAL); Serial.println(" us");

  motor1.writeMicroseconds(MIN_SIGNAL);
  motor2.writeMicroseconds(MIN_SIGNAL);
  motor3.writeMicroseconds(MIN_SIGNAL);
  motor4.writeMicroseconds(MIN_SIGNAL);

  // Instructions to test functionality
  Serial.println("\n");
  Serial.println("The ESC(s) are calibrated");
  Serial.println("----");
  Serial.print("Type a value between "); Serial.print(MIN_SIGNAL); Serial.print("(min) and "); Serial.print(MAX_SIGNAL); Serial.println("(max) and press enter.");
}


void loop() {
  // Check the serial port
  if (Serial.available() > 0){
    PULSE = Serial.parseInt();

    // If there is data in the serial port write it to the ESC's and display a message
    if (PULSE > 999) {
      motor1.writeMicroseconds(PULSE);
      motor2.writeMicroseconds(PULSE);
      motor3.writeMicroseconds(PULSE);
      motor4.writeMicroseconds(PULSE);

      SPEED = (PULSE - MIN_SIGNAL) / 10;
      Serial.println("\nMotor speed: "); Serial.print(SPEED); Serial.print("%");
    }
  }
}
