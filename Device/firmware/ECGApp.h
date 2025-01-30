#ifndef ECGApp_h
#define ECGApp_h

class ECGApp 
{
  public:
    ECGApp(Config& config, button& leftKey, button& rightKey, button& goKey, 
              GyverOLED<SSD1306_128x64, OLED_NO_BUFFER>& oled, 
              File& myFile, 
              Menu& menu)
        :config(config), leftKey(leftKey), rightKey(rightKey), goKey(goKey),
          oled(oled), myFile(myFile), menu(menu) {}

    void ECGAppActive()
    {
      //init app
      if(!isECGActive)
      {
        oled.clear();
        oled.home();
        oled.println("Поиск SD карты...");
        oled.println("[>]Не сохранять на SD");
        while (!SD.begin(SPI_HALF_SPEED, 10)) 
        {
          if(rightKey.click()){break;}
        }
        oled.clear();
    
        myFile = SD.open("ECG.txt", FILE_WRITE);
        if (myFile) 
        {
          //IF ECG started (chek config!) 
          myFile.print(String(1000 / period));
          myFile.println(" Hz");
          myFile.println("---");
          myFile.close();
        }
        else { Serial.println("error opening 1 txt"); }
    
        myFile = SD.open("ECG.txt", FILE_WRITE);
        isECGActive = true;
        //change config
        EEPROM.get(0, config);
        config.isECGStarted = true;
        EEPROM.put(0, config);
      }

      //update app
      if(millis() - oledTimer >= 50)
      {
        oled.setScale(1);
        oled.home();
        oled.println("[>] Завершить");
        oled.print("[v] Назад");
      
        //oled.dot(x, y);
        x0 = x;
        x += 1;
        y0 = y;
        //y = 63 - (data * 0.0625);
        y = 75 - (data * 0.0625);
        oled.line(x0, y0, x, y);

        if(x>=128)
        {
          x = 0;
          oled.clear();
          myFile.close();
          myFile = SD.open("ECG.txt", FILE_WRITE);
        }
        oledTimer = millis();
        
      }
      if(millis() - sdTimer >= 3000)
      {
        myFile.close();
        myFile = SD.open("ECG.txt", FILE_WRITE);
        sdTimer = millis();
      }
      if(millis() - ecgTimer >= period)
      {
        //put data
        data = analogRead(A0);
        myFile.println(String(data));
        ecgTimer = millis();
      }

      //key input
      if(leftKey.click())
        {
          //a
        }
        if(rightKey.click())
        {
          //Stop recording
          EEPROM.get(0, config);
          config.isECGStarted = false;
          isECGActive = false;
          EEPROM.put(0, config);
          oled.setScale(1);
          oled.home();
          oled.print("Запись остановлена");
          menu.isActive = true;
          menu.DrawCurrentWidget();
        }
        if(goKey.click()) //exit active mode, open menu
        {
          menu.isActive = true;
          menu.DrawCurrentWidget();
        }
    }

    void ECGAppBackground()
    {
      //init app
      if(!isECGActive)
      {
        EEPROM.get(0, config);
        if(config.isECGStarted)//if ECG is "unactive" but it started (config) 
        {
          bool findSD = true;
          oled.setScale(1);
          oled.setCursor(0, 6);
          oled.print("Поиск SD. [v]-отмена");
          while (!SD.begin(SPI_HALF_SPEED, 10)) 
          {
            if(goKey.click())
            {
              oled.setCursor(0, 6);
              oled.print("SD карта НЕ обнаружена      ");
              oled.setCursor(0, 7);
              oled.print("Запись ЭКГ остановлена");
              //Stop recording
              EEPROM.get(0, config);
              config.isECGStarted = false;
              isECGActive = false;
              EEPROM.put(0, config);
              isECGActive = false;
              findSD = false;
              break;
            }
          }
          if(findSD)
          {
            oled.setCursor(0, 6);
            oled.print("SD карта обнаружена");
            myFile = SD.open("ECG.txt", FILE_WRITE);
            if (myFile) 
            {
              Serial.println("0");
              myFile.close();
            }
            else { Serial.println("1"); }
        
            myFile = SD.open("ECG.txt", FILE_WRITE);
            isECGActive = true;
          }
        }
      }
      else//update app
      {
        if(millis() - sdTimer >= 3000)
        {
          myFile.close();
          myFile = SD.open("ECG.txt", FILE_WRITE);
          sdTimer = millis();
        }
        if(millis() - ecgTimer >= period)
        {
          //myFile = SD.open("ECG.txt", FILE_WRITE);
          myFile.println(String(analogRead(A0)));
          ecgTimer = millis();
        }

      }
    }

  private:
    int data = 0;//ECG signal
    unsigned long ecgTimer = millis();
    unsigned long sdTimer = millis();
    unsigned long oledTimer = millis();
    bool isECGActive = false;
    byte period = 1000 / 40; //1000 / v [Hz] = x ms
    byte x0 = 0;
    byte y0 = 0;
    byte x = 0;
    byte y = 0;

    Config& config;
    button& leftKey;
    button& rightKey;
    button& goKey;
    GyverOLED<SSD1306_128x64, OLED_NO_BUFFER>& oled;
    File& myFile;
    Menu& menu;

};
#endif