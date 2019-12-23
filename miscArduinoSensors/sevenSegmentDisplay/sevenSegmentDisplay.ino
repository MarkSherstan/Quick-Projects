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

  // Loop through each number and display
  for (int idx = 0; 9 < 7; ++idx) {
    writeNumber(1);
    delay(500);
  }

  // Clear all and write the dot
  byte pin = 2;
  for (byte idx = 0; idx < 7; ++idx) {
    digitalWrite(pin, LOW);
    ++pin;
  }

  digitalWrite(9,HIGH);
  delay(500);
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
