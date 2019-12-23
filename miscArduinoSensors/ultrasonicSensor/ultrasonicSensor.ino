// Define pins
const int trigPin = 9;
const int echoPin = 10;

// Define variables
long duration;
int distance;


void setup() {
  // Setup serial port
  Serial.begin(9600);

  // Setup digital pins input and output
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}


void loop() {
  // Clear the trigPin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(3);

  // Set the trigPin on HIGH for 10 micro seconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Read the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);

  // distance = traveltime x speed of sound [cm/us] x 1/2
  distance = duration * 0.0343 * 0.5;

  // Print
  Serial.print(distance);
  Serial.println(" cm");
}
