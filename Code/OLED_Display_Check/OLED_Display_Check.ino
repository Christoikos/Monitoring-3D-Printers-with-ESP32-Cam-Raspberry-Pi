#include <Wire.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1  // No reset pin
#define SDA_PIN 15
#define SCL_PIN 13

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

bool initOLED() {
  Wire.begin(SDA_PIN, SCL_PIN);

  // Scan for I2C devices
  Serial.println("Scanning I2C devices...");
  byte error, address;
  int nDevices = 0;
  for(address = 1; address < 127; address++ ) {
    Wire.beginTransmission(address);
    error = Wire.endTransmission();
    if (error == 0) {
      Serial.print("I2C device found at address 0x");
      Serial.println(address, HEX);
      nDevices++;
    }
  }
  if(nDevices == 0) {
    Serial.println("No I2C devices found");
    return false;
  }

  // Initialize OLED display
  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println(F("SSD1306 allocation failed"));
    return false;
  }

  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0,0);
  display.println("OLED initialized!");
  display.display();
  return true;
}

void setup() {
  Serial.begin(115200);

  if(initOLED()) {
    display.println("Ready");
    display.display();
  } else {
    Serial.println("OLED not detected");
  }

  // Your camera and Wi-Fi setup follows here...
}

void loop() {
  // Example usage: update Wi-Fi status on OLED
  display.clearDisplay();
  display.setCursor(0,0);
  display.println("Wi-Fi: connected"); // Or your dynamic status
  display.display();
  delay(1000);
}
