#include <Arduino.h>

// Declare Variables
int ledPin = 13;
int analogOut;



void setup() {
  Serial.begin(9600);

  // Set up LED's and turn off
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);
}



void loop() {
  // Read analog sensor and print results
  analogOut = analogRead(A0);
  Serial.print(analogOut);

  // Display LED based on humidity level
  if (analogOut < 200){
    Serial.println("\tLow");
    delay(500);
    digitalWrite(ledPin, HIGH);
    delay(500);
    digitalWrite(ledPin, LOW);

  } else if (analogOut >= 200 && analogOut < 400){
    Serial.println("\tMid");
    digitalWrite(ledPin, HIGH);

  } else {
    Serial.println("\tHigh");
    delay(100);
    digitalWrite(ledPin, HIGH);
    delay(100);
    digitalWrite(ledPin, LOW);
  }


}
