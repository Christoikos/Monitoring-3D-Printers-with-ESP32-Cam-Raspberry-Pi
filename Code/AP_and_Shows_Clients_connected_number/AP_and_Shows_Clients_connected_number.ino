#include <WiFi.h>
#include "esp_wifi.h"

const char *ssid = "ESP32-AP2";
const char *password = "12345678";

// IP settings for the Access Point itself
IPAddress local_ip(192, 168, 5, 1);
IPAddress gateway(192, 168, 5, 1);
IPAddress subnet(255, 255, 255, 0);


void setup() {
  Serial.begin(115200);

   // Configure static IP for AP
  WiFi.softAPConfig(local_ip, gateway, subnet);

  //WiFi.mode(WIFI_AP);
  WiFi.softAP(ssid, password);

  Serial.println("ESP32 AP2 started");
  Serial.print("SSID: "); Serial.println(ssid);
  Serial.print("IP: "); Serial.println(WiFi.softAPIP());
}

void loop() {
  wifi_sta_list_t stationList;
  esp_wifi_ap_get_sta_list(&stationList);

  Serial.printf("Stations connected: %d\n", stationList.num);

  for (int i = 0; i < stationList.num; i++) {
    wifi_sta_info_t station = stationList.sta[i];

    Serial.print("Client MAC: ");
    for (int j = 0; j < 6; j++) {
      Serial.printf("%02X", station.mac[j]);
      if (j < 5) Serial.print(":");
    }
    Serial.println();
  }

  Serial.println("-----");
  delay(10000);
}
