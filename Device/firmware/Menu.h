#include "Bitmaps.h"
#include "uRTCLib.h"

#ifndef Menu_h
#define Menu_h

class Menu
{
  public:
    byte currentPos = 1;
    bool isActive = true;
    Menu(Config& config, GyverOLED<SSD1306_128x64, OLED_NO_BUFFER> &oledRef, uRTCLib &rtc) :config(config),  oled(oledRef), rtc(rtc)
    {
    }

    DrawCurrentWidget()
    {      
      switch (currentPos) 
      {
        case 1:
            rtc.refresh();
            oled.clear();
            oled.home();
            oled.setScale(3);
            //oled.println("Холтер");
            oled.print(rtc.hour());
            oled.print(':');
            oled.println(rtc.minute());
            //oled.print(':');
            //oled.println(rtc.second());

            oled.setScale(2);
            oled.println("Холтер v1.1");
            oled.setScale(1);
            oled.println("--------------------------");
            
            EEPROM.get(0, config);
            if(config.isECGStarted)
            {
                oled.setScale(1);
                oled.setCursor(0, 7);
                oled.print("Идёт запись ЭКГ");
            }
          break;
        case 2:
            oled.clear();
            oled.drawBitmap(1, 1, ecg_icon_128x64, 128, 64, BITMAP_NORMAL, BUF_ADD);
            oled.setScale(1);
            oled.setCursor(0, 7);
            oled.print("      Запись ЭКГ          ");
          break;
        case 3:
            oled.clear();
            oled.drawBitmap(1, 1, diary_icon_128x64, 128, 64, BITMAP_NORMAL, BUF_ADD);
            oled.setScale(1);
            oled.setCursor(0, 7);
            oled.print("    Дневник пациента      ");
      }

    }
    byte GetCurrentWidgetID()
    {
      return currentPos;
    }
    Right()
    {
      if(currentPos == widgetsCount)
      {
        currentPos = 1;
      }
      else
      {
        currentPos++;
      }
      DrawCurrentWidget();
    } 
    Left()
    {
      if(currentPos == 1)
      {
        currentPos = widgetsCount;
      }
      else
      {
        currentPos--;
      }
      DrawCurrentWidget();
    }

    Homepage()
    {
      
    } 
  private:
    Config& config;
    GyverOLED<SSD1306_128x64, OLED_NO_BUFFER> &oled;
    uRTCLib &rtc;
    byte widgetsCount = 3;

};
#endif