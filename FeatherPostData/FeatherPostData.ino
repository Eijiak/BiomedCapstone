#include <ESP8266WiFi.h>
#include <WiFiClient.h> 
#include <ESP8266WebServer.h>
#include <EEPROM.h>
#include <Wire.h>
#include <Adafruit_ADS1015.h> 

// ADC
Adafruit_ADS1015 ads1015;

// SSID and Password
const char *ssid = "ESP Hotspot";
const char *password = "capstone";

// Pin definitions
const int LED_PIN = 0; // Onboard red LED
const int ANALOG_PIN = A0; // The only analog pin on the board (TEST)

// Defined variables
int16_t a0Data[2100];
int16_t a1Data[2100];
int16_t a2Data[2100];
int16_t a3Data[2100];
int counter = 0;
String message = "";
long previousMillis = 0;        // will store last time LED was updated
long interval = 5;           // interval at which to sample (milliseconds) -> 1 sample / 5ms = 200Hz

ESP8266WebServer server(80);

// IP address:  http://192.168.4.1

void setup() {
  delay(1000);
  clearData();
  
  Serial.begin(115200);
  ads1015.begin();
  WiFi.softAP(ssid, password); // Can remove password parameter for an open AP
  IPAddress thisIP = WiFi.softAPIP();
  Serial.print("The AP IP address: ");
  Serial.println(thisIP);
 
  server.on("/", defaultResponse);
  server.on("/love",showLove);
  server.begin();
 
  Serial.println("HTTP server started");
}

void loop() {
  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis > interval && counter < 2000){ // Makes sure the ESP is sampling at desired frequency
    previousMillis = currentMillis;
    int16_t one = 0;
    int16_t notone = 1024;
    // Get raw data
    a0Data[counter] = ads1015.readADC_SingleEnded(0); // A0: Electrode output 0
    a1Data[counter] = ads1015.readADC_SingleEnded(1); // A1: Electrode output 1
    a2Data[counter] = ads1015.readADC_SingleEnded(2); // A2: x-axis
    a3Data[counter] = ads1015.readADC_SingleEnded(3); // A3: y-axis //analogRead(ANALOG_PIN);

    // Data check
    a0Data[counter] = dataCheck(a0Data[counter]);
    a1Data[counter] = dataCheck(a1Data[counter]);
    a2Data[counter] = dataCheck(a2Data[counter]);
    a3Data[counter] = dataCheck(a3Data[counter]);
    
//    Serial.println(millis());
    Serial.print(a0Data[counter]);
    Serial.print(", ");
    Serial.print(a1Data[counter]);
    Serial.print(", ");
    Serial.print(a2Data[counter]);
    Serial.print(", ");
    Serial.print(a3Data[counter]);
    Serial.println();
    counter ++;
  }
  
  server.handleClient();
  if (counter >= 2000) { clearData(); } // Reset counter if data has not been sent
}

void defaultResponse() {
  message = "";
  int i = 0;
  // A0 Data
  while (a0Data[i] != 0) { // Send all data that is available
    if(a0Data[i] < 100){
      message += "0";
      if(a0Data[i] < 10){ message += "0"; }
    }
    message += a0Data[i];
    a0Data[i] = 0;
    i++;
  }
  message += ",";
  i=0;

  // A1 Data
  while (a1Data[i] != 0){
    if(a1Data[i] < 100){
      message += "0";
      if(a1Data[i] < 10){ message += "0"; }
    }
    message += a1Data[i];
    a1Data[i] = 0;
    i++;
  }
  message += ",";
  i=0;

  // A2 Data
  while (a2Data[i] != 0) { // Send all data that is available
    if(a2Data[i] < 100){
      message += "0";
      if(a2Data[i] < 10){ message += "0"; }
    }
    message += a2Data[i];
    a2Data[i] = 0;
    i++;
  }
  message += ",";
  i=0;

  // A3 Data
  while (a3Data[i] != 0) { // Send all data that is available
    if(a3Data[i] < 100){
      message += "0";
      if(a3Data[i] < 10){ message += "0"; }
    }
    message += a3Data[i];
    a3Data[i] = 0;
    i++;
  }  
  counter = 0; // Reset counter 
  Serial.println(message);
  server.send(200, "text/html", message); // 200 is HTTP Status code for OK
}

void showLove() {
  server.send(200, "text/html", "Love you");
}

void clearData() {
  memset(a3Data, 0, sizeof(a3Data)); 
  memset(a2Data, 0, sizeof(a2Data));
  memset(a1Data, 0, sizeof(a1Data)); 
  memset(a0Data, 0, sizeof(a0Data));
  counter = 0;
}

int16_t dataCheck(int16_t dataPoint) {
  if(dataPoint <= 0){dataPoint = 1;}
  if(dataPoint > 1023){dataPoint = 1023;} // For 10 bit resolution  
  
  return dataPoint;

}




