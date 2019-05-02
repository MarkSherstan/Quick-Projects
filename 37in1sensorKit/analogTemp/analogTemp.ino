// Operating voltage	5V
// Temperature measurement range	-55°C to 125°C [-67°F to 257°F]
// Measurement Accuracy	±0.5°C
// Use steinhart-hart coeficients for thermistor

// Define variables
float R1 = 10000;
float logR2, R2, T;
float c1 = 0.001125309, c2 = 0.000234711, c3 = 0.0000000856635;
int thermistorPin = A0;
int sensorVal;

void setup() {
  // Setup serial port
  Serial.begin(9600);
}

void loop() {
  // Read analog pin and calculate resistance on thermistor
  sensorVal = analogRead(thermistorPin);
  R2 = R1 * (1023.0 / (float)sensorVal - 1.0);

  // Calculate the temperature in Kelvin and convert
  logR2 = log(R2);
  T = (1.0 / (c1 + c2*logR2 + c3*logR2*logR2*logR2));
  T = T - 273.15;

  // Display the results
  Serial.print("Temperature: ");
  Serial.print(T);
  Serial.println(" C");
}
