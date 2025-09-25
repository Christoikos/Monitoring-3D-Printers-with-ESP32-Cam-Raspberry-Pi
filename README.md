# ESP32-CAM & Raspberry Pi Monitoring Project

This project connects multiple **ESP32-CAM modules** (organized into groups, each with its own ESP32 acting as an Access Point) to a **Raspberry Pi control center**.  

The Raspberry Pi is **not an Access Point**. Instead, it connects to the internet normally (via Ethernet or wlan0) and also connects to the ESP32-APs through an extra Wi-Fi dongle (wlan1).  
From there, the Pi runs scripts to collect data and monitor the ESP32 devices.

Each ESP32-AP also has a small **OLED display** attached, which shows in real-time which clients are connected.

---
# Restrictions
 - Wi-Fi could not support so many connections
 - No New Router
 - No Ethernet Cable 
 - We needed to check them through phone anytime from anywhere
---

## 🔹 How it works

- Each **ESP32 board acts as an AP** with its own subnet:  
  - ESP32-AP1 → `192.168.11.X`  
  - ESP32-AP2 → `192.168.12.X`  
  - ESP32-AP3 → `192.168.13.X`  
  - ESP32-AP4 → `192.168.14.X`  
  - ESP32-AP5 → `192.168.15.X`  

- **ESP32-CAM clients** connect to their assigned AP.  
  - Example: `192.168.12.5` = D1, `192.168.12.6` = D2, etc.  
  - If a new device (like a phone) connects, the OLED shows it as `&1`, `&2`, etc.

- The **Raspberry Pi**:  
  - Connects to the internet with wlan0 (or Ethernet).  
  - Connects to ESP32-APs using wlan1 (USB Wi-Fi dongle).  
  - Runs Python scripts to collect IP/MAC info and organize devices.  
  - Provides a GUI that shows devices grouped by AP.
  - Displays the cameras through the browser.

- The **OLED displays on ESP32-APs** show live status of which clients are connected.  

---

## 🔹 Features

- Organizes ESP32-CAMs into separate AP networks for better management.  
- Static IPs for each client so they always map to the right device (D1, D2, etc).  
- OLED display on each ESP32 shows connected IDs.  
- Raspberry Pi acts as the “control center” to monitor all networks.  
- Remote access possible with **Tailscale VPN** (so the Pi can be managed from anywhere).  

---

## 🔹 Tech Used
- **ESP32 / ESP32-CAM**  
- **Arduino IDE** (for ESP32 code)  
- **Adafruit SSD1306 OLED** library  
- **Python 3 (Tkinter GUI)** on Raspberry Pi  
- **Raspberry Pi OS**  
- **Tailscale VPN** (remote control)  

---

## 🔹 Repository Contents
- `arduino/` → ESP32-AP and ESP32-CAM Arduino code  
- `raspberry_pi/` → Python scripts & GUI  
- `schematics/` → Circuit diagrams and wiring  
- `3d_designs/` → 3D printed case designs  
- `docs/` → Notes, sketches, and explanations
- `Electronics/` → Schematics
- `Archive/` → Archived files & Drivers
- `Design/` → Fusion 360 / 3D Files  

---

## 🔹 Status
This is a **learning + personal project**.  
It’s not a polished product, but it works and shows how to manage many ESP32-CAM devices with a Pi.  

I’m using this project to learn about:  
- Networking (static IPs, APs, subnets)  
- Embedded programming with ESP32  
- Python GUI programming  
- Remote access with VPNs  

---

## 🔹 Next Steps
- Add a monitor or web dashboard for the Pi (currently only scripts + ESP32 OLEDs).  
- Improve the GUI for better visualization.  
- Test stability with more ESP32-APs and clients.  

---

## 🔹 Credits
Made by Stoikos Christos, as part of my self-learning journey.    
