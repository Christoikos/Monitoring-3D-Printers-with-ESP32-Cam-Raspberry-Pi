#include <WiFi.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include "esp_wifi.h"
#include "esp_netif.h"

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1

// I2C pins for ESP32-CAM
#define I2C_SDA 15
#define I2C_SCL 13

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

// ======== AP Settings ========
const char* ap_ssid = "ESP32-AP2";  // <--- Change per AP
const char* ap_password = "12345678";

// ======== Static IP Settings ========
IPAddress local_ip(192, 168, 12, 1);  // <--- Change per AP
IPAddress gateway(192, 168, 12, 1);
IPAddress subnet(255, 255, 255, 0);

// ========= Mapping Table =========
// subnet, lastOctet, Label
struct ClientMap {
  uint8_t subnet;
  uint8_t lastOctet;
  const char* label;
};

ClientMap clientMap[] = {
  // ===== AP1 → 192.168.11.X =====
  { 11, 5, "A1" },
  { 11, 6, "A2" },
  { 11, 7, "A3" },
  { 11, 8, "A4" },
  // ===== AP2 → 192.168.12.X =====
  { 12, 5, "D1" },
  { 12, 6, "D2" },
  { 12, 7, "D3" },
  { 12, 8, "D4" },
  // ===== AP3 → 192.168.13.X =====
  { 13, 5, "D5" },
  { 13, 6, "D6" },
  { 13, 7, "D7" },
  { 13, 8, "D8" },
  // ===== AP4 → 192.168.14.X =====
  { 14, 5, "D9" },
  { 14, 6, "D10" },
  { 14, 7, "D11" },
  { 14, 8, "D12" },
  // ===== AP5 → 192.168.15.X =====
  { 15, 5, "B1" },
  { 15, 6, "B2" },
  { 15, 7, "B3" },
  { 15, 8, "B4" },
  { 15, 9, "B5" },
  { 15, 10, "B6" },
};

const int mapSize = sizeof(clientMap) / sizeof(clientMap[0]);

// ========= Helper Function =========
String lookupLabel(IPAddress ip) {
  uint8_t subnet = ip[2];
  uint8_t last = ip[3];

  for (int i = 0; i < mapSize; i++) {
    if (clientMap[i].subnet == subnet && clientMap[i].lastOctet == last) {
      return String(clientMap[i].label);
    }
  }
  return "";  // Not found
}

// ========= I2C Scanner =========
void scanI2C() {
  Serial.println("Scanning I2C bus...");
  byte error, address;
  int nDevices = 0;
  for (address = 1; address < 127; address++) {
    Wire.beginTransmission(address);
    error = Wire.endTransmission();
    if (error == 0) {
      Serial.print("I2C device found at 0x");
      if (address < 16) Serial.print("0");
      Serial.println(address, HEX);
      nDevices++;
    }
  }
  if (nDevices == 0) Serial.println("No I2C devices found\n");
  else Serial.println("Scan complete\n");
}

void setup() {
  Serial.begin(115200);

  // Init I2C
  Wire.begin(I2C_SDA, I2C_SCL);
  scanI2C();

  // Init OLED
  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println("SSD1306 allocation failed");
    for (;;)
      ;
  }
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);

  // Configure AP with static IP
  WiFi.softAPConfig(local_ip, gateway, subnet);
  WiFi.softAP(ap_ssid, ap_password);

  Serial.println("ESP32 AP started");
  Serial.print("SSID: ");
  Serial.println(ap_ssid);
  Serial.print("IP: ");
  Serial.println(WiFi.softAPIP());

  display.setCursor(0, 0);
  display.println("AP Mode Started");
  display.display();
  delay(2000);
}

void loop() {
  display.clearDisplay();
  display.setCursor(0, 0);

  // Show AP SSID
  display.println("AP: " + String(ap_ssid));

  // Show AP IP
  display.println("====================");
  display.println("IP: " + WiFi.softAPIP().toString());

  // Show number of clients
  int numClients = WiFi.softAPgetStationNum();
  display.println("====================");
  display.println("Clients: " + String(numClients));

  // Show client IDs based on IPs
  if (numClients > 0) {
    display.println("====================");
    display.println("IDs:");

    wifi_sta_list_t stationList;
    esp_netif_sta_list_t netifList;

    esp_wifi_ap_get_sta_list(&stationList);
    esp_netif_get_sta_list(&stationList, &netifList);

    int unknownCounter = 1;
    for (int i = 0; i < netifList.num; i++) {
      IPAddress ip = IPAddress(netifList.sta[i].ip.addr);
      String label = lookupLabel(ip);

      if (label != "") {
        display.print(label + "|");
      } else {
        display.print("&" + String(unknownCounter) + "|");
        unknownCounter++;
      }
    }
  }

  display.display();
  delay(1000);  // refresh every second
}
