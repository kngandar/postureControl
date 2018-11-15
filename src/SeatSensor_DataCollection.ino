/*
 Seat sensor data collection sketch
*/

#include "HX711.h"

#define DOUT 2
#define CLK 3
#define DOUT2 4
#define CLK2 5
#define DOUT3 6
#define CLK3 7
#define DOUT4 8
#define CLK4 9

// Initialize load cell sensor objects
HX711 frontR(DOUT, CLK);
HX711 frontL(DOUT2, CLK2);
HX711 backR(DOUT3, CLK3);
HX711 backL(DOUT4, CLK4);

// Calibration factors
float cf_frontR = 280000;
float cf_frontL = 774000;
float cf_backR = 840000;
float cf_backL = 881000;

void setup() {
  Serial.begin(9600);
  Serial.println("HX711 data collection sketch");
  Serial.println("Remove all weight from scale");
  Serial.println("After readings begin, place known weight on scale");

  // Resets scale to 0
  frontR.set_scale();
  frontR.tare();
  frontL.set_scale();
  frontL.tare();
  backR.set_scale();
  backR.tare();
  backL.set_scale();
  backL.tare();

  // Set calibration factor
  frontR.set_scale(cf_frontR);
  frontL.set_scale(cf_frontL);
  backR.set_scale(cf_backR);
  backL.set_scale(cf_backL);
}

void loop() {
  // Print sensor values
  Serial.print("Reading front right: ");
  Serial.print(frontR.get_units(), 1);
  Serial.print(" kg"); 
  Serial.print(" calibration_factor: ");
  Serial.print(cf_frontR);
  Serial.println();

  Serial.print("Reading front left: ");
  Serial.print(frontL.get_units(), 1);
  Serial.print(" kg"); 
  Serial.print(" calibration_factor: ");
  Serial.print(cf_frontL);
  Serial.println();

  Serial.print("Reading back right: ");
  Serial.print(backR.get_units(), 1);
  Serial.print(" kg"); 
  Serial.print(" calibration_factor: ");
  Serial.print(cf_backR);
  Serial.println();

  Serial.print("Reading back left: ");
  Serial.print(backL.get_units(), 1);
  Serial.print(" kg"); 
  Serial.print(" calibration_factor: ");
  Serial.print(cf_backL);
  Serial.println();

  // Displays data after every 250ms
  delay(250);

  // Quit the program if enter 'q' or 'Q'
  if(Serial.available())
  {
    char temp = Serial.read();
    if (temp == 'q' || temp == 'Q')
      return;
  }
}
