// Constant values
#define analogPin   0
#define VCC         4.98
#define R_DIV       10000.0

// Variables
int fsrADC;
float fsrV, fsrR, fsrG, force;

void setup(){
  // Serial coms
  Serial.begin(9600);
}

void loop(){
  // Read analog pin
  fsrADC = analogRead(analogPin);

  // Use ADC reading to calculate voltage
  fsrV = fsrADC * VCC / 1023.0;

  // Use voltage and static resistor value to calculate FSR resistance
  fsrR = ((VCC - fsrV) * R_DIV) / fsrV;

  // Guesstimate force based on slopes in figure 3 of FSR datasheet (conductance)
  fsrG = 1.0 / fsrR;

  // Break parabolic curve down into two linear slopes
  if (fsrR <= 600)
    force = (fsrG - 0.00075) / 0.00000032639;
  else
    force =  fsrG / 0.000000642857;

  // Display results and delay
  Serial.println(force, 1);
  delay(50);
}
