#include <EEPROM.h>
#include <GyverOLED.h>
#include "SPI.h"
#include "SD.h"
#include "DeviceConfigs.h"
#include "Menu.h"
#include "button.h"
#include "ECGApp.h"
#include "Bitmaps.h"

#define leftKeyPin 2
#define rightKeyPin 3
#define goKeyPin 4

button leftKey(leftKeyPin);
button rightKey(rightKeyPin);
button goKey(goKeyPin);
Config config;
GyverOLED<SSD1306_128x64, OLED_NO_BUFFER> oled;
File myFile;   
Menu menu(config, oled);
ECGApp ecgApp(config, leftKey, rightKey, goKey, oled, myFile, menu);

void setup()
{
  pinMode(SS, OUTPUT);
  Serial.begin(9600);

  //EEPROM.get(0, config);
  //EEPROM.put(0, config);
  //Oled preview
  oled.init();
  oled.clear();

  oled.drawBitmap(1, 1, loading_128x64, 128, 64, BITMAP_INVERT, BUF_ADD);

  oled.setScale(1);
  oled.setCursor(0, 7);
  oled.print("      загрузка...         ");
  delay(1000);
  menu.DrawCurrentWidget();
}

void loop()
{
  //menu mode
  if(menu.isActive)
  {
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
}