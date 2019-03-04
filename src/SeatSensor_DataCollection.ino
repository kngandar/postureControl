/*
 Seat sensor data collection sketch
*/

#include "HX711.h"

//Chair Seat
#define DOUT 2
#define CLK 3
#define DOUT2 4
#define CLK2 5
#define DOUT3 6
#define CLK3 7
#define DOUT4 8
#define CLK4 9

//Chair Back
#define DOUT5 10
#define CLK5 11
#define DOUT6 12
#define CLK6 13
#define DOUT7 16
#define CLK7 17
#define DOUT8 18
#define CLK8 19

// Initialize load cell sensor objects
HX711 backR(DOUT, CLK);
HX711 frontR(DOUT2, CLK2);
HX711 frontL(DOUT3, CLK3);
HX711 backL(DOUT4, CLK4);

HX711 lowerR(DOUT5, CLK5);
HX711 lowerL(DOUT6, CLK6);
HX711 upperL(DOUT7, CLK7);
HX711 upperR(DOUT8, CLK8);

// Calibration factors
float cf_backR = 550000;
float cf_frontR = 650000;
float cf_frontL = 480000;
float cf_backL = 650000;

float cf_lowerR = -22500;
float cf_lowerL = -21000;
float cf_upperL = -7500;
float cf_upperR = -7500;

char msg;

void setup() {
  Serial.begin(9600);

  // Resets scale to 0
  frontR.set_scale();
  frontR.tare();
  frontL.set_scale();
  frontL.tare();
  backR.set_scale();
  backR.tare();
  backL.set_scale();
  backL.tare();

  upperR.set_scale();
  upperR.tare();
  upperL.set_scale();
  upperL.tare();
  lowerR.set_scale();
  lowerR.tare();
  lowerL.set_scale();
  lowerL.tare();
  
  // Set calibration factor
  frontR.set_scale(cf_frontR);
  frontL.set_scale(cf_frontL);
  backR.set_scale(cf_backR);
  backL.set_scale(cf_backL);
  
  upperR.set_scale(cf_upperR);
  upperL.set_scale(cf_upperL);
  lowerR.set_scale(cf_lowerR);
  lowerL.set_scale(cf_lowerL);
}

void loop() {
  // Print sensor values

  if(Serial.available())
  {

    msg = Serial.read();
      
	//front right
	Serial.print(frontR.get_units(),1);
	Serial.print(", ");

	//front left
	Serial.print(frontL.get_units(),1);
	Serial.print(", ");

	//back right
	Serial.print(backR.get_units(), 1);
	Serial.print(", ");

	//back left
	Serial.print(backL.get_units(), 1);
	Serial.print(", ");

	//upper left
	Serial.print(upperL.get_units(), 1);
	Serial.print(", ");

	//upper right
	Serial.print(upperR.get_units(), 1);
	Serial.print(", ");

	//lower left
	Serial.print(lowerL.get_units(), 1);
	Serial.print(", ");

	//lower right
	Serial.println(lowerR.get_units(), 1);

  }

 