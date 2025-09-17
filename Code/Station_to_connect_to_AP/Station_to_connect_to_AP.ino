#include <WiFi.h>

const char* ssid = "ESP32-AP";
const char* password = "12345678";

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.println("Connected to ESP32-AP!");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  // ESP32 #2 can now communicate with ESP32 #1
}
