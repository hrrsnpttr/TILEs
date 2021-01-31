
#include "BluetoothSerial.h"

#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif

const int redPin =18;
const int  greenPin =19;
const int  bluePin =21;
bool rainbow = false;

BluetoothSerial SerialBT;

void setup() {
  //Initializing three separate PWM channels
  ledcSetup(0, 1000, 8); //Red Channel
  ledcSetup(1, 1000, 8); //Green Channel
  ledcSetup(2, 1000, 8); //Blue Channel

  //Attaching Pins to Respective Channels
  ledcAttachPin(redPin, 0);
  ledcAttachPin(greenPin, 1);
  ledcAttachPin(bluePin, 2);

  //Begin Bluetooth
  Serial.begin(115200);
  SerialBT.begin("ESP32LED_TILES"); //Bluetooth device name
  Serial.println("Bluetooth connection available");
  //Allows the ESP32 to read color inputs faster
  SerialBT.setTimeout(100);
}
void loop() {
  //Send commands back to the computer
  if (Serial.available()) {
    SerialBT.write(Serial.read());
  }
  //Read color values from the computer
  if (SerialBT.available()) {
    //Serial.write(SerialBT.read());
    String ts=SerialBT.readString();
    rainbow = false;
    if(ts.substring(0,1)=="a")
    {
      rainbow = true;
      
    }
    else
    {
      rainbow = false;
    int red = (ts.substring(0,3)).toInt();
    int green =(ts.substring(3,6)).toInt();
    int blue =(ts.substring(6)).toInt();
    setColor(red,green,blue);
    Serial.println(red);
    Serial.println(green);
    Serial.println(blue);
    }
  }
  if(rainbow)
  {
    rainbowFunction();
  }
  delay(25);
}

//Rainbow Function
void rainbowFunction(){
    setColor(255, 0, 0);
    int red = 255;
    int green =0;
    int blue =0;
    //Turn on green
  for(int x=0; x<255; x++)
    {
      green =x;
      setColor(red,green,blue);
      delay(10);
    }
     //Turn off red
  for(int x=255; x<=0; x--)
    {
      red=x;
      setColor(red,green,blue);
      delay(10);
    }
    //turn on blue
   for(int x=0; x<255; x++)
    {
      blue=x;
      setColor(red,green,blue);
      delay(10);
    }
    //turn off green
   for(int x=255; x<=0; x--)
    {
      green=x;
      setColor(red,green,blue);
      delay(10);
    }
    //turn on red
    for(int x=0; x<255; x++)
    {
      red=x;
      setColor(red,green,blue);
      delay(10);
    }
    //turn off blue
    for(int x=255; x<=0; x--)
    {
      blue=x;
      setColor(red,green,blue);
      delay(10);
    } 

  }

//Set Color Function for Common Anode RGB leds
void setColor(int red, int green, int blue)
{
 ledcWrite(0, 255-red);  
 ledcWrite(1, 255-green);  
 ledcWrite(2, 255-blue);  
 delay(15);
}
