#include <Wire.h>
#include <SPI.h>
#include <Adafruit_LSM9DS1.h>
#include <Adafruit_Sensor.h>
#include <errno.h>

#define BINARY_INPUT

// i2c
Adafruit_LSM9DS1 lsm = Adafruit_LSM9DS1();

// Globals and constants
#define CS1 10
#define CS2 8

uint16_t load_dac1(uint16_t val, uint8_t cselect);
uint16_t load_dac2(uint16_t val, uint8_t cselect);

void setup()
{
  Serial.begin(115200);
  // Set up SPI Bus
  pinMode(CS1, OUTPUT);
  pinMode(CS2, OUTPUT);
  SPI.begin();
  SPI.beginTransaction(SPISettings(4000000, MSBFIRST, SPI_MODE0));
  digitalWrite(CS1, HIGH); // de-assert chipselect
  digitalWrite(CS2, HIGH); // de-assert chipselect
  delay(100);
  // Initialize all DACs to 0V
  load_dac1(2048, CS1);
  load_dac1(2048, CS2);
  load_dac2(2048, CS2);
  //  if (!lsm.begin())
  //  {
  //    Serial.println("Oops ... unable to initialize the LSM9DS1. Check your wiring!");
  //    while (1);
  //  }
  //  Serial.println("Found LSM9DS1 9DOF");
  lsm.begin();
  lsm.setupMag(lsm.LSM9DS1_MAGGAIN_4GAUSS);
}

void loop()
{
#ifndef BINARY_INPUT // Binary input not defined, reading voltage
  // Read serial
  while (Serial.available() < 1)
    ;
  uint8_t axis = Serial.parseInt(); // Which axis to fire
  while (Serial.available() < 1)
    ;
  short cmd = Serial.parseInt(); // Voltage in mV
                                 //  Serial.print(axis);
                                 //  Serial.print(" ");
                                 //  Serial.println(cmd);
  // Clear serial
  while (Serial.available() > 0)
    Serial.read();
  unsigned short val;
  // Format Voltage to 12 bit number
  if (cmd == 0) // 0 level
    val = 2048;
  else
  {
    cmd += 4910;                       // 0 offset (2*Vref)
    val = (cmd / (2 * 4910.0)) * 4096; // convert voltage to DAC number ( Voltage / range(4*Vref) * 2^12 )
  }
#else           // BINARY_INPUT
  // Wait for serial
  while (Serial.available() < 1)
    ;
  uint16_t cmd = Serial.parseInt();
  uint8_t axis = cmd >> 12;    // top 4 bits contain which axis to fire
  uint16_t val = cmd & 0x0fff; // bottom 12 bits contain which value to set
  // Clear serial
  while (Serial.available() > 0)
    Serial.read();
#endif          // BINARY_INPUT
  switch (axis) // Load required DAC with the required value
  {
  case 0:
    load_dac1(val, CS1);
    break;
  case 1:
    load_dac1(val, CS2);
    break;
  case 2:
    load_dac2(val, CS2);
    break;
  default:
    break;
  }
  //  if (errno)
  //  {
  //    Serial.println("Error occurred");
  //    errno = 0 ;
  //  }
  delay(10); // let the DAC output settle
  // make 10 magnetometer measurements
  for (int i = 0; i < 10; i++)
  {
    lsm.read();
    sensors_event_t a, m, g, temp;

    lsm.getEvent(&a, &m, &g, &temp);
    // uint16_t x, y, z;
    // Adafruit uses the number 6842 for scaling:
    // float_Bx = short_Bx / 6842 in 4 gauss range where short_Bx is in 2's complement rep
    // which stems from the fact that 0.14 mG/LSB is guaranteed.
    // Which is underestimated at 0.146 mG/LSB, which then gives
    // convert float measurements to short
//    x = lsm.magData.x*6842 + 32768;
//    y = lsm.magData.y*6842 + 32768;
//    z = lsm.magData.z*6842 + 32768;
//    byte out[12];
//    out[0] = ((uint8_t)x);
//    out[1] = ((uint8_t)(x >> 8));
//    out[2] = ((uint8_t)y);
//    out[3] = ((uint8_t)(y >> 8));
//    out[4] = ((uint8_t)z);
//    out[5] = ((uint8_t)(z >> 8));
//    out[6] = 0x48;
//    out[7] = 0x48;
//    out[8] = 0x48;
//    out[9] = 0x48;
//    out[10] = 0x48;
//    out[11] = 0x48;
//    Serial.write(out, 12);
      Serial.print(m.magnetic.x*10);Serial.print(" ");
      Serial.print(m.magnetic.y*10);Serial.print(" ");
      Serial.print(m.magnetic.z*10);Serial.print("\n");
//    Serial.print(lsm.magData.x/10);
//    Serial.print(",");
//    Serial.print(lsm.magData.y/10);
//    Serial.print(",");
//    Serial.println(lsm.magData.z/10);
    Serial.flush();
    delay(50); // wait before re-measuring
  }
}

uint16_t load_dac1(uint16_t val, uint8_t cselect)
{
  // Write the value to dac A
  val &= 0x0fff; // 12 bit values only
  val |= 0x4000; // Cmd: 0b0100|D11-D0
  digitalWrite(cselect, LOW);
  SPI.transfer16(val);
  digitalWrite(cselect, HIGH);
  __asm__("nop\n\t");
  __asm__("nop\n\t");
  digitalWrite(cselect, LOW);
  uint16_t result = SPI.transfer16(0x0000); // Send a NOP to retrieve the previous command
  digitalWrite(cselect, HIGH);
  if (result != val)
    errno = 30;
  return result;
}

uint16_t load_dac2(uint16_t val, uint8_t cselect)
{
  // Write the value to dac A
  val &= 0x0fff; // 12 bit values only
  val |= 0x5000; // Cmd: 0b0100|D11-D0
  digitalWrite(cselect, LOW);
  SPI.transfer16(val);
  digitalWrite(cselect, HIGH);
  __asm__("nop\n\t");
  __asm__("nop\n\t");
  digitalWrite(cselect, LOW);
  uint16_t result = SPI.transfer16(0x0000); // Send a NOP to retrieve the previous command
  digitalWrite(cselect, HIGH);
  if (result != val)
    errno = 30;
  return result;
}
