#include "Bitmaps.h"

#ifndef Menu_h
#define Menu_h

class Menu
{
  public:
    bool isActive = true;
    Menu(GyverOLED<SSD1306_128x64, OLED_NO_BUFFER> &oledRef) : oled(oledRef)
    {
    }

    DrawCurrentWidget()
    {      
      switch (currentPos) 
      {
        case 1:
            oled.clear();
            oled.home();
            oled.setScale(5);
            oled.print("21:05");
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
    GyverOLED<SSD1306_128x64, OLED_NO_BUFFER> &oled;
    byte widgetsCount = 3;
    byte currentPos = 1;

};
#endif