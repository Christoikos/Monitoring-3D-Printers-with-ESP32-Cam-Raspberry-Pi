import sys
import subprocess
import cv2
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap

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
    except Exception:
        return None

def connect_to_ap(ssid):
    subprocess.run(["nmcli", "device", "wifi", "connect", ssid, "ifname", WIFI_INTERFACE])


class CameraApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("3D Printer Camera Viewer")
        self.layout = QVBoxLayout()

        # Label for video stream
        self.video_label = QLabel("Camera feed will appear here")
        self.layout.addWidget(self.video_label)

        # Buttons for printers
        for printer_name in PRINTERS.keys():
            btn = QPushButton(printer_name)
            btn.clicked.connect(lambda _, name=printer_name: self.start_stream(name))
            self.layout.addWidget(btn)

        self.setLayout(self.layout)

        # OpenCV video capture
        self.cap = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

    def start_stream(self, printer_name):
        printer = PRINTERS[printer_name]
        target_ssid = printer["ssid"]
        target_ip = printer["ip"]

        current_ssid = get_current_ssid()
        if current_ssid != target_ssid:
            print(f"Switching to {target_ssid}...")
            connect_to_ap(target_ssid)
        else:
            print(f"Already connected to {target_ssid}")

        url = f"http://{target_ip}"  # ESP32-CAM stream URL
        print(f"Opening stream from {url}")

        # Stop previous stream if running
        if self.cap is not None:
            self.cap.release()

        self.cap = cv2.VideoCapture(url)
        if not self.cap.isOpened():
            print("Failed to open video stream.")
            return

        self.timer.start(30)  # update every 30 ms

    def update_frame(self):
        if self.cap is None:
            return
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            qt_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            self.video_label.setPixmap(QPixmap.fromImage(qt_image))
        else:
            print("Frame not received.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CameraApp()
    window.show()
    sys.exit(app.exec_())

