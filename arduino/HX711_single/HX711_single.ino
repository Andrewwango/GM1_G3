#include "HX711.h"

// HX711 circuit wiring
const int LOADCELL_DOUT_PIN = 3;
const int LOADCELL_SCK_PIN = 2;

const int BUTTON_PIN = 6;
const int BUTTON_TIMEOUT_MILLIS = 5000; // 5 seconds

int pressed = LOW;
unsigned long last_pressed = 0;

HX711 scale;

void setup() {
  Serial.begin(57600);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
}

void loop() {

  if (scale.is_ready()) {
    long reading = (scale.read() - 550550)/702 - 0;
    if (reading < 0) {
      reading = 0;
    }
    Serial.println(reading);
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
