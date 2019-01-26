# Soil Humidity Classifier for Home Plants
Program for determining the soil humidity levels in various house hold plants.

Also using the project to test the basic functionality of PlatformIO instead of Arduino IDE.

## Usage
Build and upload with PlatformIO or copy and paste `\src\main.cpp` excluding the `#include <Arduino.h>` header into Arduino IDE and compile as normal.

The 7 segment display values correspond to the relative humidity. For example 1 indicates 0-10% relative humidity, 2 indicates 10-20% relative humidity, etc... For greater than 90% relative humidity the decimal point will flash.

## Specs and Data Sheets
Sensor purchased from Banggood and came with the following information:

* Supply voltage: 3.3V or 5V
* Operating current: less than 20mA
* Output voltage: 0-2.3V (2.3V is completely immersed in water voltage value),
* 5V power supply, the greater the humidity, the greater the output voltage.
* Sensor type: Analog Output

## Case
The top of the case was modified from [this](https://www.thingiverse.com/thing:994827) model on Thingiverse. CAD files can be found in the `case` directory.  

## Wiring schematic
![](https://github.com/MarkSherstan/Quick-Projects/blob/master/soilHumidity/wiringDiagram.png)
