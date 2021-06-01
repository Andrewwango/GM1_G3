#include "HX711.h"

// HX711 circuit wiring
const int LOADCELL_DOUT_PIN = 3;
const int LOADCELL_SCK_PIN = 2;
const int LOADCELL_DOUT_PIN2 = 5;
const int LOADCELL_SCK_PIN2 = 4;
const int BUTTON_PIN = 6;
const int BUTTON_TIMEOUT_MILLIS = 5000; // 5 seconds

int pressed = LOW;
unsigned long last_pressed = 0;

HX711 scale;
HX711 scale2;

void setup() {
  Serial.begin(57600);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
  scale2.begin(LOADCELL_DOUT_PIN2, LOADCELL_SCK_PIN2);
}

void loop() {

  if (scale.is_ready() && scale2.is_ready()) {
    long reading = (scale.read() - 127150)/1891 - 229;
    long reading2 = (scale2.read() - 580750)/1017 + 447;
    long combined = reading + reading2;
    if (combined < 0) {
      combined = 0;
    }
    Serial.print(reading);
    Serial.print(",");
    Serial.print(reading2);
    Serial.print(",");
    Serial.println(combined);
  } else {
    
  }

  int buttonPress = digitalRead(6);
  if ((buttonPress == LOW) && (pressed == LOW)){
    Serial.println("-1");
    pressed = HIGH;
    last_pressed = millis();
  }
  if (millis() - last_pressed > BUTTON_TIMEOUT_MILLIS){
    pressed = LOW;
  }

  delay(100);
  
}
