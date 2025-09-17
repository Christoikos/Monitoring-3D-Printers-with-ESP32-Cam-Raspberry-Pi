import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

class CameraApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ESP32-CAM Viewer")
        self.setGeometry(100, 100, 800, 600)

        # Map printers to their AP SSID and camera URL
        # You can modify URLs or IPs according to your setup
        self.printer_to_info = {
            "Printer 1": {"ssid": "ESP32-AP1", "url": "http://192.168.4.5:80"},
            "Printer 2": {"ssid": "ESP32-AP1", "url": "http://192.168.4.6:80"},
            "Printer 3": {"ssid": "ESP32-AP2", "url": "http://192.168.5.5:80"},
            "Printer 4": {"ssid": "ESP32-AP2", "url": "http://192.168.5.6:80"}
        }

        # Current connected SSID for dongle
        self.current_ssid = None

        # Layouts
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Buttons for each printer
        for printer_name in self.printer_to_info:
            btn = QPushButton(printer_name)
            btn.clicked.connect(lambda checked, name=printer_name: self.show_camera(name))
            self.layout.addWidget(btn)

        # Web view to show camera stream
        self.web_view = QWebEngineView()
        self.layout.addWidget(self.web_view)

    def connect_to_ap(self, ssid):
        """Connect the dongle to the given AP if not already connected."""
        if self.current_ssid == ssid:
            print(f"Already connected to {ssid}")
            return

        print(f"Connecting to {ssid}...")
        # Example command using nmcli for NetworkManager (adjust if needed)
        try:
            subprocess.run(["nmcli", "dev", "wifi", "connect", ssid], check=True)
            self.current_ssid = ssid
            print(f"Connected to {ssid}")
        except subprocess.CalledProcessError:
            print(f"Failed to connect to {ssid}")

    def show_camera(self, printer_name):
        info = self.printer_to_info[printer_name]
        self.connect_to_ap(info["ssid"])  # ensure dongle connects to correct AP
        camera_url = info["url"]
        print(f"Showing {printer_name} at {camera_url}")
        self.web_view.setUrl(QUrl(camera_url))  # display stream in web view


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CameraApp()
    window.show()
    sys.exit(app.exec_())
