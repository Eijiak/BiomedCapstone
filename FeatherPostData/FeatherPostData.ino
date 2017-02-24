#include <ESP8266WiFi.h>
#include <WiFiClient.h> 
#include <ESP8266WebServer.h>
#include <EEPROM.h>

// SSID and Password
const char *ssid = "ESP Hotspot";
const char *password = "capstone";

// Pin definitions
const int LED_PIN = 0; // Onboard red LED
const int ANALOG_PIN = A0; // The only analog pin on the board (TEST)

// Defined variables
uint8_t analogData;
int storedData[2000];
int counter = 0;
String message = "";
long previousMillis = 0;        // will store last time LED was updated
long interval = 5;           // interval at which to sample (milliseconds) -> 1 sample / 5ms = 200Hz

ESP8266WebServer server(80);

// IP address:  http://192.168.4.1

void setup() {
  delay(1000);
  memset(storedData, 0, sizeof(storedData)); // Make all values of array 0
  
  Serial.begin(115200);
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
  if (currentMillis - previousMillis > interval && counter < 2000){
    previousMillis = currentMillis;
    storedData[counter] = analogRead(ANALOG_PIN);
    Serial.println(storedData[counter]);
    counter ++;
  }
  
  server.handleClient();
  
}

void defaultResponse() {
  message = "";
  int i = 0;
  while (storedData[i] != 0) { // Send all data that is available
    if(storedData[i] < 100){
      message += "0";
    }
    message += storedData[i];
    storedData[i] = 0;
    i++;
  }
  counter = 0; // Reset counter 
  Serial.println(message);
  server.send(200, "text/html", message);
}

void showLove() {
  server.send(200, "text/html", "Love you");
}
