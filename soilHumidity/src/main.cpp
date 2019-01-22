#include <Arduino.h>

// Declare Variables
int ledPins[] = {11,12,13};
int analogOut0, analogOut1, analogAvg;
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
  // Read analog sensor and print results
  analogOut0 = analogRead(A0);
  analogOut1 = analogRead(A1);
  analogAvg = (analogOut0 + analogOut1) / 2;
  Serial.print(analogOut0); Serial.print("  ");
  Serial.print(analogOut1); Serial.print("  ");
  Serial.print(analogAvg);

  // Display LED based on humidity level
  if (analogAvg < 200){
    digitalWrite(ledPins[0], HIGH);
    digitalWrite(ledPins[1], LOW);
    digitalWrite(ledPins[2], LOW);

    Serial.println("\tLow");

  } else if (analogAvg >= 200 && analogAvg < 400){
    digitalWrite(ledPins[0], LOW);
    digitalWrite(ledPins[1], HIGH);
    digitalWrite(ledPins[2], LOW);

    Serial.println("\tMid");

  } else {
    digitalWrite(ledPins[0], HIGH);
    digitalWrite(ledPins[1], LOW);
    digitalWrite(ledPins[2], HIGH);

    Serial.println("\tHigh");
  }

}
