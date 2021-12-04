// !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
// Ensure "no newline ending" is selected
// !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

#include <Servo.h>

// Pinout
#define servoPin  9

// Call servo class and set vars
Servo myservo;

void setup() {
  // Serial setup
  Serial.begin(9600);
  Serial.setTimeout(3);

  // Servo setup
  myservo.attach(servoPin);
  myservo.writeMicroseconds(1520);
}

void loop() {
  // Only write data to the servo if there is something in the serial port
  if (Serial.available() > 0) {
    int val = Serial.parseInt();
    Serial.println(val);
    myservo.writeMicroseconds(val);
  }
}
