// Declare variables
int rawSensorVal;
String incomingString;

void setup(){
  // Initialize serial port
  Serial.begin(115200);
  Serial.setTimeout(3);
}

void loop(){
  // Read analog pin
  rawSensorVal = analogRead(A0);

  // Check if MATLAB has sent a character
  if (Serial.available() > 0) {
    incomingString = Serial.readString();

    // If character is correct send MATLAB the analog value
    if (incomingString == "a\n") {
      Serial.println(rawSensorVal);
    }
  }
}
