#include <EEPROM.h>
#include <GyverOLED.h>
#include "SPI.h"
#include "SD.h"
#include "DeviceConfigs.h"
#include "Menu.h"
#include "button.h"
#include "ECGApp.h"
#include "Bitmaps.h"
#include "uRTCLib.h"

#define leftKeyPin 6
#define rightKeyPin 9
#define goKeyPin 8
#define powerKeyPin 5
//#define chipSelect 4

char daysOfTheWeek[7][12] = {"Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"};

button leftKey(leftKeyPin);
button rightKey(rightKeyPin);
button goKey(goKeyPin);
button powerKey(powerKeyPin);
Config config;
uRTCLib rtc(0x68);
GyverOLED<SSD1306_128x64, OLED_NO_BUFFER> oled;
File myFile;   
Menu menu(config, oled, rtc);
ECGApp ecgApp(config, leftKey, rightKey, goKey, oled, myFile, menu);

bool deviceOn = true;
unsigned long menuTimer = millis();

void setup()
{
  URTCLIB_WIRE.begin();
  //rtc.set(0, 18, 22, 4, 19, 3, 2025);
  while(!powerKey.click()){}
  
  //pinMode(SS, OUTPUT);
  Serial.begin(9600);

  //EEPROM.get(0, config);
  //EEPROM.put(0, config);
  //Oled preview
  oled.init();
  oled.clear();

  oled.drawBitmap(1, 1, loading_128x64, 128, 64, BITMAP_NORMAL, BUF_ADD);

  oled.setScale(1);
  //oled.setCursor(0, 7);
  //oled.print("      загрузка...         ");
  delay(2900);
  menu.DrawCurrentWidget();
}

void loop()
{
  //"power"
  if(deviceOn)
  {
    //menu mode
    if(menu.isActive)
    {
      if(menu.GetCurrentWidgetID() == 1 && millis() - menuTimer > 30000)
      {
        menu.DrawCurrentWidget();
        menuTimer = millis();
      }
      
      if(leftKey.click())
      {
        menu.Left();
      }
      if(rightKey.click())
      {
        menu.Right();
      }
      if(goKey.click())//exit menu
      {
        //Serial.println("a");
        menu.isActive = false;
        oled.clear();
      }

      //then update all mini apps (background mode)
      ecgApp.ECGAppBackground();
    }
    else
    {
      //run current mini app (active mode)
      switch(menu.GetCurrentWidgetID())
      {
        case 1:
          menu.isActive = true;
          menu.DrawCurrentWidget();
          break;
        case 2:
          //Run ECG app in active mode
          ecgApp.ECGAppActive();
          break;
        case 3:
          menu.isActive = true;
          menu.DrawCurrentWidget();
          break;
      }
    }

    //device off
    if(powerKey.click())
    {
      menu.isActive = true;
      menu.currentPos = 1;
      oled.clear();
      deviceOn = false;
    }
  }
  //if device off
  else
  {
    //update all mini apps (background mode)
    ecgApp.ECGAppBackground();

    //turn device on
    if(powerKey.click())
    {
      menu.isActive = false;
      deviceOn = true;
    }
  }
}