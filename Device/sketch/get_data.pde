import processing.serial.*;

Serial COMPort;  // Create object from Serial class
boolean ok = true;
String[] lines = new String[0];

void setup() 
{
  frameRate(2000);
  String portName = Serial.list()[0];
  COMPort = new Serial(this, portName, 9600);
}

void draw() 
{
  if (COMPort.available() > 0) {  // If data is available,
    String read = COMPort.readString();  // read and store it to string read
    println(read);
    ok = (read != null);
    lines = append(lines, read);// append new read to string lines
  } else {
    if(ok)
    {
      saveStrings("data.txt", lines);//save string to file
    }
  }
}
