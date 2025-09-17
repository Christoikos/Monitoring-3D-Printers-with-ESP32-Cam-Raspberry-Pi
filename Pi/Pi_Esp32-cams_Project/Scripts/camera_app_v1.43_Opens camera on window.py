import sys
import subprocess
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer

PRINTERS = {
    "Printer 1": {"ssid": "ESP32-AP1", "ip": "192.168.4.5"},
    "Printer 2": {"ssid": "ESP32-AP1", "ip": "192.168.4.6"},
    "Printer 3": {"ssid": "ESP32-AP2", "ip": "192.168.5.5"},
    "Printer 4": {"ssid": "ESP32-AP2", "ip": "192.168.5.6"},
}

WIFI_INTERFACE = "wlan1"  # your dongle

# ---------------- Worker Thread ----------------
class ConnectAndFetchThread(QThread):
    frame_ready = pyqtSignal(QImage)
    error_signal = pyqtSignal(str)
    
    def __init__(self, printer_info):
        super().__init__()
        self.printer_info = printer_info

    def run(self):
        ssid = self.printer_info["ssid"]
        ip = self.printer_info["ip"]

        # Step 1: Check current SSID
        current_ssid = self.get_current_ssid()
        if current_ssid != ssid:
            result = self.connect_to_ap(ssid)
            if not result:
                self.error_signal.emit(f"Failed to connect to {ssid}")
                return

        # Step 2: Fetch snapshot
        try:
            url = f"http://{ip}/capture"  # snapshot endpoint
            response = requests.get(url, timeout=3)
            if response.status_code != 200:
                self.error_signal.emit(f"Failed to fetch frame from {ip}")
                return

            # Convert to QImage
            image = QImage.fromData(response.content)
            self.frame_ready.emit(image)

        except Exception as e:
            self.error_signal.emit(f"Error: {e}")

    def get_current_ssid(self):
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

    def connect_to_ap(self, ssid):
        try:
            subprocess.run(["nmcli", "device", "wifi", "connect", ssid, "ifname", WIFI_INTERFACE], check=True)
            return True
        except subprocess.CalledProcessError:
            return False

# ---------------- Main GUI ----------------
class CameraApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("3D Printer Camera Viewer")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.label = QLabel("No camera selected")
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)

        # Buttons
        for printer_name, info in PRINTERS.items():
            btn = QPushButton(printer_name)
            btn.clicked.connect(lambda _, name=printer_name: self.select_printer(name))
            self.layout.addWidget(btn)

        self.current_thread = None

    def select_printer(self, printer_name):
        if self.current_thread and self.current_thread.isRunning():
            self.current_thread.terminate()

        printer_info = PRINTERS[printer_name]
        self.label.setText(f"Switching to {printer_info['ssid']}...")
        self.current_thread = ConnectAndFetchThread(printer_info)
        self.current_thread.frame_ready.connect(self.show_frame)
        self.current_thread.error_signal.connect(self.show_error)
        self.current_thread.start()

    def show_frame(self, qimage):
        pixmap = QPixmap.fromImage(qimage).scaled(640, 480, Qt.KeepAspectRatio)
        self.label.setPixmap(pixmap)

    def show_error(self, message):
        self.label.setText(message)

# ---------------- Run App ----------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CameraApp()
    window.show()
    sys.exit(app.exec_())
