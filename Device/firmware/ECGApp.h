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
        oled.print("Поиск SD карты...");
        while (!SD.begin(SPI_HALF_SPEED, 7)) { Serial.println("1"); }
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
      if(millis() - ecgTimer >= period)
      {
        oled.setScale(1);
        oled.home();
        oled.println("[>] Завершить");
        oled.print("[v] Назад");

        int data = analogRead(A0);
        x0 = x;
        x += 1;
        y0 = y;
        //y = 63 - (data * 0.0625);
        y = 75 - (data * 0.0625);
        Serial.println(data);

        if (myFile) 
        {
          myFile.println(String(data));
        }
        else
        {
          Serial.println("1"); 
          myFile.close();
        }
      
        //oled.dot(x, y);
        oled.line(x0, y0, x, y);

        if(x>=128)
        {
          x = 0;
          oled.clear();
          myFile.close();
          myFile = SD.open("ECG.txt", FILE_WRITE);
        }

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
          oled.setScale(1);
          oled.setCursor(0, 6);
          oled.print("Повторный поиск SD");
          while (!SD.begin(SPI_HALF_SPEED, 7)) { Serial.println("1"); }
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
      else//update app
      {
        if(millis() - ecgTimer >= period)
        {
          myFile = SD.open("ECG.txt", FILE_WRITE);

          if (myFile) 
          {
            myFile.println(String(analogRead(A0)));
            myFile.close();
          }
          else
          {
            myFile.close();
          }

          ecgTimer = millis();
        }
      }
    }

  private:
    unsigned long ecgTimer = millis();
    bool isECGActive = false;
    byte period = 1000 / 100; //1000 / v [Hz] = 10 ms
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