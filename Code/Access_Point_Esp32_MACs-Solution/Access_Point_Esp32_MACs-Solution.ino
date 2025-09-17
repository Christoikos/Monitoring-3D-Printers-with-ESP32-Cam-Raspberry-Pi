#include <WiFi.h>
#include <WiFiClient.h>
#include <WiFiAP.h>

// Access Point credentials
const char* ssid = "ESP32-AP";
const char* password = "12345678"; // Minimum 8 characters

// IP settings for the Access Point itself
IPAddress local_ip(192, 168, 4, 1);
IPAddress gateway(192, 168, 4, 1);
IPAddress subnet(255, 255, 255, 0);

void setup() {
  Serial.begin(115200);
  delay(1000);

  // Configure static IP for AP
  WiFi.softAPConfig(local_ip, gateway, subnet);

  // Start the Access Point
  WiFi.softAP(ssid, password);

  Serial.println("ESP32 AP started.");
  Serial.print("AP IP address: ");
  Serial.println(WiFi.softAPIP());
}

void loop() {
  // Nothing here. Just maintaining the AP
}
