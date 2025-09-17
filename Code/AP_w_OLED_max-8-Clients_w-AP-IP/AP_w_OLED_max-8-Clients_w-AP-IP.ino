#include <WiFi.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include "esp_netif.h"

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1

// I2C pins for ESP32-CAM
#define I2C_SDA 15
#define I2C_SCL 13

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

// ======== AP Settings ========
const char* ap_ssid = "ESP32-AP3";  // <--- Change only this  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
const char* ap_password = "12345678";

// ======== Dynamic Static IP from SSID ========
IPAddress local_ip;
IPAddress gateway;
IPAddress subnet(255, 255, 255, 0);

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

// ======== Parse AP number from SSID and assign subnet ========
void configureStaticIP() {
  int apNumber = 0;
  String ssidStr = String(ap_ssid);

  // Look for "AP" and get number after it
  int idx = ssidStr.indexOf("AP");
  if (idx != -1) {
    apNumber = ssidStr.substring(idx + 2).toInt();
  }

  if (apNumber <= 0) {
    apNumber = 10;  // fallback subnet if parsing fails
  }

  int subnetId = 10 + apNumber;  // AP1 → 11, AP2 → 12, ...
  local_ip = IPAddress(192, 168, subnetId, 1);
  gateway = IPAddress(192, 168, subnetId, 1);

  Serial.print("Derived subnet for ");
  Serial.print(ap_ssid);
  Serial.print(": 192.168.");
  Serial.println(subnetId);
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

  // Configure subnet from AP name
  configureStaticIP();

  // Configure AP with static IP
  WiFi.mode(WIFI_AP);
  WiFi.softAPConfig(local_ip, gateway, subnet);
  WiFi.softAP(ap_ssid, ap_password, 1, 0, 8);   // last param = max connections (default 4, max 8)
  WiFi.softAPsetHostname(ap_ssid);

  /*
  // Disable DHCP (new API)
  esp_netif_t* netif = esp_netif_get_handle_from_ifkey("WIFI_AP_DEF");
  if (netif != NULL) {
    esp_netif_dhcps_stop(netif);
  }
  */

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

  // Instead of MACs, just show client IDs
  if (numClients > 0) {
    display.println("====================");
    display.println("IDs:");
    for (int i = 1; i <= numClients; i++) {
      display.print(String(i) + "|");
    }
  }

  display.display();
  delay(200);  // refresh every 200ms
}
