#include <Servo.h>

// Claw
Servo myservo;
int servoPin = 9;
int pos;

// Open clamp button
int buttonPin = 7;

// Serial port return
char inByte;

void setup() {
  // Set up 9600 baud serial port
  Serial.begin(9600);

  // Attach button on button pin
  pinMode(buttonPin, INPUT);

  // Attach servo on pin 9 and send middle command
  myservo.attach(servoPin);
  myservo.writeMicroseconds(1500);
  delay(100);
}

void loop() {
  // Parse the serial port for close command
  if(Serial.available()){
    inByte = Serial.read();
    if (inByte == 0x68){
      myservo.writeMicroseconds(2000);
      delay(100);
    }
  }

  // Parse the button for open command
  if (digitalRead(buttonPin) == LOW) {
    myservo.writeMicroseconds(700);
    delay(100);
  }
}
