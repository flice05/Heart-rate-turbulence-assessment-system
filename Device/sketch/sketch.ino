#include <GyverOLED.h>
GyverOLED<SSD1306_128x64, OLED_NO_BUFFER> oled;

int x0 = 0;
int y0 = 0;
int x = 0;
int y = 0;

#include "SPI.h"
#include "SD.h"

File myFile;
const int chipSelect = 4;    
byte period = 1000 / 100; //1000 / v [Hz]

void setup()
{
  Serial.begin(9600);
  oled.init();
  oled.clear();
  oled.print("start");
  pinMode(8, INPUT); // Setup for leads off detection LO +
  pinMode(9, INPUT); // Setup for leads off detection LO -
  pinMode(SS, OUTPUT);

   // если карта не исправна, есть ошибка в подключении модуля - выводим сообщение
  while (!SD.begin(SPI_HALF_SPEED, chipSelect)) { Serial.println("initialization failed"); }
  delay(3000);
 
   // открываем файл, в котором будем сохранять информацию
   myFile = SD.open("a.txt", FILE_WRITE);
   if (myFile) {
      Serial.println("*start*");
      myFile.print(String(1000 / period));
      myFile.println(" Hz");
      myFile.println("-------------------");
      myFile.close();
   }
   // иначе выводим ошибку об открытии файла
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
  // иначе выводим ошибку об открытии файла
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
