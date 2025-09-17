import sys
import subprocess
import webbrowser
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel

PRINTERS = {
    "Printer 1": {"ssid": "ESP32-AP1", "ip": "192.168.4.5"},
    "Printer 2": {"ssid": "ESP32-AP1", "ip": "192.168.4.6"},
    "Printer 3": {"ssid": "ESP32-AP2", "ip": "192.168.5.5"},
    "Printer 4": {"ssid": "ESP32-AP2", "ip": "192.168.5.6"},
}

WIFI_INTERFACE = "wlan1"  # dongle interface

def get_current_ssid():
    """Return SSID currently connected on wlan1"""
    try:
        ssid_output = subprocess.check_output(
            ["nmcli", "-t", "-f", "active,ssid", "dev", "wifi"],
            text=True
        )
        for line in ssid_output.splitlines():
            if line.startswith("yes:"):
                return line.split(":")[1]
    except Exception as e:
        print("Error getting current SSID:", e)
    return None

def connect_to_ap(ssid, password="12345678"):
    """Connect wlan1 to the given SSID"""
    # Disconnect wlan1 first
    subprocess.run(["nmcli", "dev", "disconnect", WIFI_INTERFACE])
    # Connect
    result = subprocess.run(
        ["nmcli", "dev", "wifi", "connect", ssid, "password", password, "ifname", WIFI_INTERFACE],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        print(f"Connected to {ssid}")
        return True
    else:
        print(f"Failed to connect to {ssid}: {result.stderr}")
        return False

class CameraApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("3D Printer Camera Viewer")
        self.layout = QVBoxLayout()

        # Status label
        self.status_label = QLabel("Select a printer to connect")
        self.layout.addWidget(self.status_label)

        # Add printer buttons
        for printer_name in PRINTERS:
            btn = QPushButton(printer_name)
            btn.clicked.connect(lambda _, name=printer_name: self.select_printer(name))
            self.layout.addWidget(btn)

        self.setLayout(self.layout)

    def select_printer(self, printer_name):
        printer = PRINTERS[printer_name]
        target_ssid = printer["ssid"]
        target_ip = printer["ip"]

        current_ssid = get_current_ssid()
        if current_ssid != target_ssid:
            self.status_label.setText(f"Connecting to {printer_name} ({target_ssid})...")
            print(f"Connecting to {target_ssid}...")
            if not connect_to_ap(target_ssid):
                self.status_label.setText(f"Failed to connect to {printer_name} ({target_ssid})")
                return
        else:
            print(f"Already connected to {target_ssid}")

        # Open camera in default browser
        self.status_label.setText(f"Opening {printer_name} camera at {target_ip}")
        webbrowser.open(f"http://{target_ip}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CameraApp()
    window.show()
    sys.exit(app.exec_())
