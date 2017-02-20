#include <ESP8266WiFi.h>
#include <Time.h>

//////////////////////
// WiFi Definitions //
//////////////////////
const char WiFiAPPSK[] = "sparkfun";

/////////////////////
// Pin Definitions //
/////////////////////
const int LED_PIN = 0; // Onboard red LED
const int ANALOG_PIN = A0; // The only analog pin on the board (TEST)
const int DIGITAL_PIN = 12; // Digital pin to be read
String req = "";

WiFiServer server(80);

void setup() 
{
  initHardware(); // See function below
  setupWiFi(); // See function below
  server.begin();
}

void loop() 
{
  // Check if a client has connected
  WiFiClient client = server.available();
  if (!client) {
    Serial.println(String(millis()));
    return;
  }
  Serial.println(String(millis()));
  Serial.println("client: "); 
  // Read the first line of the request
  req = client.readStringUntil('\r');
//  Serial.println(req); // GET (/led/1, /led/0, /read) HTTP/1.1 
  client.flush();

  Serial.println(String(millis()));
  Serial.println("flush: "); 
  // Match the request
//  int val = -2; // We'll use 'val' to keep track of both the
                // request type (read/set) and value if set.
  /*
  if (req.indexOf("/led/0") != -1)
    val = 0; // Will write LED low
  else if (req.indexOf("/led/1") != -1)
    val = 1; // Will write LED high
  else if (req.indexOf("/read") != -1)
    val = -2; // Will print pin reads
  // Otherwise request will be invalid. We'll say as much in HTML
  */
  
  // Set LED according to the request
//  if (val >= 0){
//    if (val == 0) {
//      digitalWrite(LED_PIN, HIGH);
//    }
//    else {
//      digitalWrite(LED_PIN, LOW);
//    }
//  }
    

//  client.flush();

  // Prepare the response. Start with the common header:
  String s = "HTTP/1.1 200 OK\r\n";
  s += "Content-Type: text/html\r\n\r\n";
  s += String(analogRead(ANALOG_PIN));
  /*
  s += "<!DOCTYPE HTML>\r\n<html>\r\n";
  // If we're setting the LED, print out a message saying we did
  if (val >= 0)
  {
    s += "LED is now ";
    s += (val)?"on":"off";
  }
  else if (val == -2)
  { // If we're reading pins, print out those values:
      s += "Analog Pin = ";
      s += String(analogRead(ANALOG_PIN));
      s += "<br>"; // Go to the next line.
      s += "Digital Pin 12 = ";
      s += String(digitalRead(DIGITAL_PIN));
  }
  else
  {
    s += "Invalid Request.<br> Try /led/1, /led/0, or /read.";
  }
  s += "</html>\n";
  */
  
  // Send the response to the client
  client.print(s);
  Serial.println(String(millis()));
  Serial.println("End client");
//  delay(1);
//  Serial.println("Client disonnected");
  
  // The client will actually be disconnected 
  // when the function returns and 'client' object is detroyed
}

void setupWiFi()
{
  WiFi.mode(WIFI_AP);

  // Do a little work to get a unique-ish name. Append the
  // last two bytes of the MAC (HEX'd) to "Thing-":
  uint8_t mac[WL_MAC_ADDR_LENGTH];
  WiFi.softAPmacAddress(mac);
  String macID = String(mac[WL_MAC_ADDR_LENGTH - 2], HEX) +
                 String(mac[WL_MAC_ADDR_LENGTH - 1], HEX);
  macID.toUpperCase();
  String AP_NameString = "ESP8266 Huzzah " + macID;

  char AP_NameChar[AP_NameString.length() + 1];
  memset(AP_NameChar, 0, AP_NameString.length() + 1);

  for (int i=0; i<AP_NameString.length(); i++)
    AP_NameChar[i] = AP_NameString.charAt(i);

  WiFi.softAP(AP_NameChar, WiFiAPPSK);
}


void initHardware()
{
  Serial.begin(115200);
  pinMode(DIGITAL_PIN, INPUT_PULLUP);
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);
  // Don't need to set ANALOG_PIN as input, 
  // that's all it can be.
}




