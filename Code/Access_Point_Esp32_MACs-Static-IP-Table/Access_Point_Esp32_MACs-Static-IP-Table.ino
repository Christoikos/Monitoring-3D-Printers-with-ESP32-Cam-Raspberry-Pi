#include <WiFi.h>
#include <esp_wifi.h>

// Set AP credentials
const char* ssid = "ESP32_AP";
const char* password = "12345678";

// Max clients
#define MAX_CLIENTS 26

// IP base
IPAddress apIP(192, 168, 4, 1);
IPAddress netMsk(255, 255, 255, 0);

// MAC-to-IP Table
struct StaticClient {
  uint8_t mac[6];
  IPAddress ip;
};

// Define your 26 static clients here
StaticClient staticClients[MAX_CLIENTS] = {
  {{0x14, 0x2B, 0x2F, 0xDE, 0x17, 0x14}, IPAddress(192,168,4,5)},
  {{0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0x02}, IPAddress(192,168,4,12)},
  {{0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0x03}, IPAddress(192,168,4,13)},
  // ... add up to 26
};

// Utility to compare MAC addresses
bool compareMAC(const uint8_t* mac1, const uint8_t* mac2) {
  for (int i = 0; i < 6; i++) {
    if (mac1[i] != mac2[i]) return false;
  }
  return true;
}

// Handle new client connection
void WiFiEvent(WiFiEvent_t event, WiFiEventInfo_t info) {
  if (event == SYSTEM_EVENT_AP_STACONNECTED) {
    Serial.print("New station connected: ");
    char macStr[18];
    sprintf(macStr, "%02X:%02X:%02X:%02X:%02X:%02X",
            info.sta_connected.mac[0], info.sta_connected.mac[1], info.sta_connected.mac[2],
            info.sta_connected.mac[3], info.sta_connected.mac[4], info.sta_connected.mac[5]);
    Serial.println(macStr);

    // Search static IP table
    for (int i = 0; i < MAX_CLIENTS; i++) {
      if (compareMAC(info.sta_connected.mac, staticClients[i].mac)) {
        Serial.print("-> Assigned Static IP: ");
        Serial.println(staticClients[i].ip);
        // Optional: send this info over UDP or HTTP to the client
        return;
      }
    }

    Serial.println("-> No static IP assigned (will get dynamic)");
  }
}

void setup() {
  Serial.begin(115200);

  WiFi.mode(WIFI_AP);
  WiFi.softAP(ssid, password);
  WiFi.softAPConfig(apIP, apIP, netMsk);

  Serial.print("Access Point Started with IP: ");
  Serial.println(WiFi.softAPIP());

  WiFi.onEvent(WiFiEvent);
}

void loop() {
  // You can add broadcast of IP-MAC mappings or heartbeat here
}
