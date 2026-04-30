/*  Banner Drag Test.
  This program processes all raw analog inputs from (3) sensors as part of a remote controlled (RC) aircraft banner towing test.
  The goal of the test is to experimentally determine the aerodynamic drag created by a banner of varying dimensions, being towed by a small RC aircraft.
  The test will consist of the banner in question being towed from a mast erected from a truck (2010 Toyota Tacoma) moving up to 50mph groundspeed. 
  In order to simulate typical flight conditions, the banner will be towed from a height such that it is outside the truck's aerodynamic wake region and thus is exposed minimal aerodynamic effects
  that it would not experience during typical flight.
  During this test, the aerodynamic effects of the RC aircraft will be assumed to have a negligibly small impact on the banner and will not be simulated during the test.

  Force (F) will be gathered by a load cell to determine the raw drag force from the banner
  Airspeed (v) will be gathered by an anemometer to account for differences in ground speed and actual airspeed (wind)
  Air humidity, temperature, and pressure will be gathered by an environmental combo sensor for air density (p) calculations

  F = 1/2pCAv^2
  X = CA
  
  @author: Joey Ungerleider
  @version: 1-27-2026
*/

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

//include the Wire library to access the i2c interface
#include <Wire.h>
#include "SparkFunCCS811.h"
#include "SparkFunBME280.h"
#define CCS811_ADDR 0x5B //Default I2C Address

BME280 bmeSensor;

const int LCpin = A1;
const int AMpin = A0;

float LCvolt;
float AMvolt;

float force;
float airspeed;

int counter;
float LCsum;
float LCavg;
float AMsum;
float AMavg;

const int movAvgMark1 = 500;
unsigned long startTime;

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

void setup() {

  // serial port setup with arduino
  // input setup with load cell, anemometer, and environmental sensor
  
  Serial.begin(9600);
  startTime = millis(); // get start time
  Wire.begin();
  Serial.println("1");

  if (bmeSensor.beginI2C() == false) //Begin communication over I2C
  {
    Serial.println("Could not access the BME sensor. Please check wiring.");
    while (1); //Freeze
  }

  Serial.println("2");
  // delay 1s so the BME board can boot up
  delay(1000);


  Serial.println("3");
  // print out header for data going out
  Serial.println();
  Serial.println("time[s],force[lbf],airspeed[ft/s],humidity[RH%],pressure[psi],altitude[ft],temp[F]");
  
}

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

void loop() {

  // read data from all ports every X[ms]
  float runTime = millis() / 1000.0; // [s] 
  delay(1);
  counter++;

  //// LOAD CELL ////
      // input to MCU: 3-5[V]
      // should scale linearly with force applied
      // find scaling factor (slope) by calibration with known weights
      // output to serial port: force [lbf]

      LCvolt = analogRead(LCpin) * (5.0 / 1023.0);
      LCsum += LCvolt;

  //// ANEMOMETER ////
      // input to MCU: FM analog signal (will need amplification from 0-20mV to 0-5V)
      // detect peaks by searching above certain voltage amplitude threshold
      // frequency of peaks should scale linearly(?) with fan speed, and thus airspeed
      // find scaling factor (slope) by calibration with known airspeed or other anemometer
      // output to serial port: airspeed [ft/s]

      AMvolt = analogRead(AMpin) * (5.0 / 1023.0);
      AMsum += AMvolt;

  // ENV. SENSOR
      // Sparkfun enviro. breakout board: https://www.sparkfun.com/sparkfun-environmental-combo-breakout-ens160-bme280-qwiic.html#content-features
      // input to MCU: 
      // Use board libraries to process data
      // output to serial port: air temperature [F], relative humidity [RH%], pressure [psi]

      float humidity = bmeSensor.readFloatHumidity();
      float pressure = bmeSensor.readFloatPressure();
      float altitude = bmeSensor.readFloatAltitudeFeet();
      float temp = bmeSensor.readTempF();

      // MOVING AVERAGE //
      if (counter == movAvgMark1)
      {
        LCavg = LCsum/counter;
        force = (2.2)*LCavg - (3.3); // ADD CALIBRATION VALUES HERE

        AMavg = AMsum/counter;
        airspeed = (90)*AMavg - (58.5);   // ADD CALIBRATION VALUES HERE

        Serial.print(runTime,2);
        Serial.print(",");
        
        Serial.print(force,2);
        Serial.print(",");
        
        Serial.print(airspeed,2);
        Serial.print(",");

        Serial.print(humidity, 0);
        Serial.print(",");
      
        Serial.print(pressure * 0.00014504, 2); // convert Pa to psi
        Serial.print(",");
      
        Serial.print(altitude, 1);
        Serial.print(",");
      
        Serial.println(temp, 2);

        LCsum = 0;
        LCavg = 0;
        AMsum = 0;
        AMavg = 0;
        counter = 0;
      }
}
