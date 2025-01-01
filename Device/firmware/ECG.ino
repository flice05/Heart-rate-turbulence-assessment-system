#include <GyverOLED.h>
#include "SPI.h"
#include "SD.h"
#include "Menu.h"
#include "button.h"

#define leftKeyPin 2
#define rightKeyPin 3
#define goKeyPin 4

button leftKey(leftKeyPin);
button rightKey(rightKeyPin);
button goKey(goKeyPin);

GyverOLED<SSD1306_128x64, OLED_NO_BUFFER> oled;
File myFile;   
Menu menu(oled);

byte period = 1000 / 100; //1000 / v [Hz]
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

  //just test some features bcz i dont change loop
  while(1)
  {
    if(leftKey.click())
    {
      menu.Left();
    }
    if(rightKey.click())
    {
      menu.Right();
    }
    if(goKey.click())
    {
      menu.RunCurrentWidget();
      break;
    }

  }

  pinMode(8, INPUT); // Setup for leads off detection LO +
  pinMode(9, INPUT); // Setup for leads off detection LO -
  pinMode(SS, OUTPUT);

  while (!SD.begin(SPI_HALF_SPEED, 7)) { Serial.println("initialization failed"); }
  delay(3000);
 
   myFile = SD.open("a.txt", FILE_WRITE);
   if (myFile) {
      Serial.println("*start*");
      myFile.print(String(1000 / period));
      myFile.println(" Hz");
      myFile.println("-------------------");
      myFile.close();
   }

   else { Serial.println("error opening 1 txt"); }
 
   myFile = SD.open("a.txt", FILE_WRITE);
}

void loop()
{
  int data = analogRead(A0);
  x0 = x;
  x += 1;
  y0 = y;
  y = 63 - (data * 0.0625);
  Serial.println(data);

  if (myFile) {
    myFile.println(String(data));
  }
  else
  {
    Serial.println("error opening 2 txt"); 
    myFile.close();
  }
 
  //oled.dot(x, y);
  oled.line(x0, y0, x, y);

  if(x>=128)
  {
    x = 0;
    oled.clear();
    myFile.close();
    myFile = SD.open("a.txt", FILE_WRITE);
  }
  
  delay(period);
}