#include <Arduino.h>

// Declare Variables
int ledPins[] = {11,12,13};
int analogOut;
int idx;



void setup() {
  Serial.begin(9600);

  // Set up LED's and set all to off
  for (idx = 0; idx <= 7; idx++) {
    pinMode(ledPins[idx],OUTPUT);
    digitalWrite(ledPins[idx], LOW);
  }

}



void loop() {
  // Read analog sensor and print
  analogOut = analogRead(A0);
  Serial.print(analogOut);

  // Display LED based on humidity level
  if (analogOut < 200){
    digitalWrite(ledPins[0], HIGH);
    Serial.println("\tLow");
  } else if (analogOut >= 200 && analogOut < 400){
    digitalWrite(ledPins[1], HIGH);
    Serial.println("\tMid");
  } else {
    digitalWrite(ledPins[2], HIGH);
    Serial.println("\tHigh");
  }

}
