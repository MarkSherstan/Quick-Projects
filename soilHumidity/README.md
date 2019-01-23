# Soil Humidity Classifier for Home Plants
Program for determining the soil humidity levels in various house hold plants.

Also using the project to test the basic functionality of PlatformIO instead of Arduino IDE.

## To Do
- [x] Fritzing wiring diagram
- [x] Initial test(s)
- [ ] Quantify humidity levels (~670 when fully submerged)
- [x] Make 3D printed case

## Usage
Build and upload with PlatformIO or copy and paste `\src\main.cpp` excluding the `#include <Arduino.h>` header into Arduino IDE and compile as normal.

The following lights indicate the corresponding humidity levels.
* Slow Flash --> Low
* No Flash --> Good
* Fast Flash --> High

## Specs and Data Sheets
Sensor purchased from Banggood and came with the following information:

* Supply voltage: 3.3V or 5V
* Operating current: less than 20mA
* Output voltage: 0-2.3V (2.3V is completely immersed in water voltage value),
* 5V power supply, the greater the humidity, the greater the output voltage.
* Sensor type: Analog Output

<!-- ## Wiring schematic
![]() -->
