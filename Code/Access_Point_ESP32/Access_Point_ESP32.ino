#include <WiFi.h>

const char* ssid = "ESP32-AP";
const char* password = "12345678";

void setup() {
  Serial.begin(115200);

  WiFi.softAP(ssid, password);
  Serial.println("ESP32 Soft AP Started");
  Serial.print("IP address: ");
  Serial.println(WiFi.softAPIP());
}

void loop() {
  // You could handle incoming data here or add a web server
}
