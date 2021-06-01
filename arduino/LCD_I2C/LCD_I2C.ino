#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27,20,4);  // set the LCD address to 0x27 for a 16 chars and 2 line display

void print1(){
  lcd.setCursor(0, 0);
  lcd.print("Last meal: 10:30");
  lcd.setCursor(0, 1);
  lcd.print("200kcal      GM1");
}
void print2(){
  lcd.setCursor(0, 0);
  lcd.print("Current meal:   ");
  lcd.setCursor(0, 1);
  lcd.print("200kcal     150g");
}
void print3(){
  lcd.setCursor(0, 0);
  lcd.print("200kcal eaten so");
  lcd.setCursor(0, 1);
  lcd.print("far! Keep going!");
}
void print4(){
  lcd.setCursor(0, 0);
  lcd.print("500kcal eaten...");
  lcd.setCursor(0, 1);
  lcd.print("Congratulations!");
}
void print5(){
  lcd.setCursor(0, 0);
  lcd.print("Meal started");
  lcd.setCursor(0, 1);
  lcd.print("Time:      09:01");
}

void setup(){
  lcd.init();                      // initialize the lcd 
  lcd.backlight();
  print1();
}


void loop()
{
  print1();
  delay(1000);
  print2();
  delay(1000);
  print3();
  delay(1000);
  print4();
  delay(1000);  
  print5();
  delay(1000);
}
