#include <Servo.h>

// Claw
Servo myservo;
int servoPin = 9;

// Serial port return
char inByte;

void setup() {
  // Set up 9600 baud serial port
  Serial.begin(9600);

  // Attach servo on pin 9 and send middle command
  myservo.attach(servoPin);
  myservo.writeMicroseconds(1500);
  delay(500);
}

void loop() {
  // Parse the serial port for close or open command
  if(Serial.available()){
    inByte = Serial.read();
    if (inByte == 0x68){
      myservo.writeMicroseconds(2000);
      delay(100);
    } else if (inByte == 0x14){
      myservo.writeMicroseconds(700);
      delay(10000);
    }
  }
}
