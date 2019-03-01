#include <Servo.h> 

Servo myservo;

int val;

void setup() { 
  Serial.begin(9600);
  Serial.setTimeout(3);
  
  myservo.attach(9);
  myservo.writeMicroseconds(1520); 
} 

void loop() {
  if (Serial.available() > 0) {
    val = Serial.parseInt();
    Serial.println(val);
    myservo.writeMicroseconds(val);
  }
}
