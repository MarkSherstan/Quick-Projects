void setup()
{
    // Setup serial port
    Serial.begin(9600);
}

void loop()
{
    // Read the analog pin
    int analogValue = analogRead(A0);

    // Write bytes via serial
    writeBytes(&analogValue);
}

void writeBytes(int* data)
{
    // Cast to a byte pointer
    byte* byteData = (byte*)(data);

    // Byte array with header for transmission
    byte buf[4] = {0x9F, 0x6E, byteData[0], byteData[1]};

    // Write the byte
    Serial.write(buf, 4);
}
