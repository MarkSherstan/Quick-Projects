int analogValue;


void setup() {
  // Setup serial port
  Serial.begin(9600);
}


void loop() {
  // Read the analog pin
  analogValue = analogRead(A0);

  // Write bytes via serial
  writeBytes(&analogValue);
}


void writeBytes(int* data1){
  // Cast to a byte pointer
  byte* byteData1 = (byte*)(data1);

  // Byte array with header for transmission
  byte buf[4] = {0x9F, 0x6E, byteData1[0], byteData1[1]};

  // Write the byte
  Serial.write(buf, 4);
}
