// Pinout to match wiringDiagram.png
#include <Arduino.h>

// Functions
void writeNumber(int number);

// Declare Variables
int analogOut;
double relativeHumidity;
byte digits[10][7] = { { 1,1,1,1,1,1,0 },   // = 0
                       { 0,1,1,0,0,0,0 },   // = 1
                       { 1,1,0,1,1,0,1 },   // = 2
                       { 1,1,1,1,0,0,1 },   // = 3
                       { 0,1,1,0,0,1,1 },   // = 4
                       { 1,0,1,1,0,1,1 },   // = 5
                       { 1,0,1,1,1,1,1 },   // = 6
                       { 1,1,1,0,0,0,0 },   // = 7
                       { 1,1,1,1,1,1,1 },   // = 8
                       { 1,1,1,0,0,1,1 } }; // = 9


void setup() {
  // Start the serial port
  Serial.begin(9600);

  // Initialize pins 2 through 9
  for (int ii = 2; ii < 10; ii++){
    pinMode(ii, OUTPUT);
  }
}


void loop() {
  // Read analog sensor and print results
  analogOut = analogRead(A0);
  relativeHumidity = analogOut / 700.0;
  Serial.println(relativeHumidity*100.0,1);
  digitalWrite(9,LOW);

  // Check what number to display
  if (relativeHumidity == 0) {
    writeNumber(0);
  } else if (relativeHumidity != 0.0 && relativeHumidity < 0.1) {
    writeNumber(1);
  } else if (relativeHumidity >= 0.1 && relativeHumidity < 0.2) {
    writeNumber(2);
  } else if (relativeHumidity >= 0.2 && relativeHumidity < 0.3) {
    writeNumber(3);
  } else if (relativeHumidity >= 0.3 && relativeHumidity < 0.4) {
    writeNumber(4);
  } else if (relativeHumidity >= 0.4 && relativeHumidity < 0.5) {
    writeNumber(5);
  } else if (relativeHumidity >= 0.5 && relativeHumidity < 0.6) {
    writeNumber(6);
  } else if (relativeHumidity >= 0.6 && relativeHumidity < 0.7) {
    writeNumber(7);
  } else if (relativeHumidity >= 0.7 && relativeHumidity < 0.8) {
    writeNumber(8);
  } else if (relativeHumidity >= 0.8 && relativeHumidity < 0.9) {
    writeNumber(9);
  } else {
    byte pin = 2;
    for (byte idx = 0; idx < 7; ++idx) {
      digitalWrite(pin, LOW);
      ++pin;
    }
    digitalWrite(9,HIGH);
    delay(100);
  }
}


// Write number to 7 segment display
void writeNumber(int number) {
  byte pin = 2;
  for (byte idx = 0; idx < 7; ++idx) {
    digitalWrite(pin, digits[number][idx]);
    ++pin;
  }
  delay(100);
}
