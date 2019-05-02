#include <fstream>
#include <iostream>
#include "serial_port.h"

using namespace std;
int analogOut;
uint8_t nKByte = 0;

Serial_Port serial_port;

int main(int argc, const char **argv){
  serial_port.uart_name = "/dev/cu.usbmodem14101";
  serial_port.baudrate = 9600;
  serial_port.start();

  while (true){
    serial_port._read_port(nKByte);
    analogOut = nKByte;
    cout << analogOut << " " << nKByte << endl;
  }

}
