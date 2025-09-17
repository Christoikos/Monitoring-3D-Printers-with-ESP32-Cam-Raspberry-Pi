import sys
import subprocess
import requests
import cv2
import numpy as np

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer

# Printer matrix
PRINTERS = {
    "Printer 1": {"ssid": "ESP32-AP1", "ip": "192.168.4.5"},
    "Printer 2": {"ssid": "ESP32-AP1", "ip": "192.168.4.6"},
    "Printer 3": {"ssid": "ESP32-AP2", "ip": "192.168.5.5"},
    "Printer 4": {"ssid": "ESP32-AP2", "ip": "192.168.5.6"},
}

WIFI_INTERFACE = "wlan1"  # dongle

def get_current_ssid():
    try:
        ssid = subprocess.check_output(
            ["nmcli", "-t", "-f", "active,ssid", "dev", "wifi"],
            text=True
        )
        for line in ssid.splitlines():
            if line.startswith("yes:"):
                return line.split(":")[1]
    except:
        return None

def connect_to_ap(ssid):
    subprocess.run(["nmcli", "device", "wifi", "connect", ssid, "ifname", WIFI_INTERFACE])

class CameraApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("3D Printer Camera Viewer")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # QLabel to display snapshots
        self.label = QLabel("No camera selected")
        self.layout.addWidget(self.label)

        # Add printer buttons
        for printer_name, data in PRINTERS.items():
            btn = QPushButton(printer_name)
            btn.clicked.connect(lambda _, name=printer_name: self.show_camera(name))
            self.layout.addWidget(btn)

        # Timer to refresh snapshots
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

        # current stream url
        self.stream_url = None

    def show_camera(self, printer_name):
        printer = PRINTERS[printer_name]
        target_ssid = printer["ssid"]
        target_ip = printer["ip"]

        current_ssid = get_current_ssid()
        if current_ssid != target_ssid:
            print(f"Switching to {target_ssid}...")
            connect_to_ap(target_ssid)
        else:
            print(f"Already connected to {target_ssid}")

        # set snapshot URL
        self.stream_url = f"http://{target_ip}/"
        self.timer.start(1000)  # refresh every 500 ms

    def update_frame(self):
        if not self.stream_url:
            return
        try:
            resp = requests.get(self.stream_url, timeout=2)
            if resp.status_code != 200:
                print(f"HTTP {resp.status_code} from {self.stream_url}")
                return
            
            img_array = np.asarray(bytearray(resp.content), dtype=np.uint8)
            frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            if frame is not None:
                h, w, ch = frame.shape
                qimg = QImage(frame.data, w, h, ch * w, QImage.Format_BGR888)
                self.label.setPixmap(QPixmap.fromImage(qimg).scaled(640, 480)) # force a bigger preview
                print("Snapshot updated")
            else:
                print("! Failed to decode image from stream")
                
        except Exception as e:
            print("Failed to fetch frame:", e)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CameraApp()
    window.show()
    sys.exit(app.exec_())
