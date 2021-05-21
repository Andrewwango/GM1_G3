#include "HX711.h"

// HX711 circuit wiring
const int LOADCELL_DOUT_PIN = 2;
const int LOADCELL_SCK_PIN = 3;
const int LOADCELL_DOUT_PIN2 = 4;
const int LOADCELL_SCK_PIN2 = 5;

int RAW_TARE1;
int RAW_TARE2;
int SCALE_GRAMS1;
int SCALE_GRAMS2;

HX711 scale;
HX711 scale2;

void setup() {
  Serial.begin(57600);
  scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
  scale2.begin(LOADCELL_DOUT_PIN2, LOADCELL_SCK_PIN2);

  RAW_TARE1 = 0;
  RAW_TARE2 = 0;
  SCALE_GRAMS1 = 1;
  SCALE_GRAMS2 = 1;
}

void loop() {

  if (scale.is_ready() && scale2.is_ready()) {
    long reading = (scale.read() - 535600)/1164 + 45;
    long reading2 = (scale2.read() + 311700)/2047 - 90;
    //Serial.print(reading);
    //Serial.print(",");
    //Serial.print(reading2);
    //Serial.print(",");
    Serial.println(reading + reading2);
  } else {
    
  }

  delay(100);
  
}
