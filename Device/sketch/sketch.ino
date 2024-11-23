#include <GyverOLED.h>
GyverOLED<SSD1306_128x64, OLED_NO_BUFFER> oled;

int x0 = 0;
int y0 = 0;
int x = 0;
int y = 0;

void setup()
{
  Serial.begin(9600);
  oled.init();
  oled.clear();
  oled.print("start");
  pinMode(8, INPUT); // Setup for leads off detection LO +
  pinMode(9, INPUT); // Setup for leads off detection LO -
}

void loop()
{
  x0 = x;
  x += 1;
  y0 = y;
  y = 63 - (analogRead(A0) * 0.0625);
  Serial.println(analogRead(A0));
  //oled.dot(x, y);
  oled.line(x0, y0, x, y);

  if(x>=128)
  {
    x = 0;
    oled.clear();
  }
  
  delay(2);
}
