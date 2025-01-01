#include <GyverOLED.h>

#ifndef Menu_h
#define Menu_h

class Menu
{
  public:
    Menu(GyverOLED<SSD1306_128x64, OLED_NO_BUFFER> &oledRef) : oled(oledRef)
    {
    }

    GetCurrentWidget()
    {      
      switch (currentPos) 
      {
        case 1:
            oled.clear();
            oled.home();
            oled.print("Старт");
          break;
        case 2:
            oled.clear();
            oled.home();
            oled.print("ЭКГ");
          break;
        case 3:
            oled.clear();
            oled.home();
            oled.print("Дневник пациента");
      }

    }
    RunCurrentWidget()
    {
      switch (currentPos) 
      {
        case 2:
            oled.clear();
            oled.home();
            oled.print("Поиск SD карты...");
      }
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
      GetCurrentWidget();
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
      GetCurrentWidget();
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