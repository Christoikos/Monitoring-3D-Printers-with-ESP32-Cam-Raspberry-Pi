import tkinter as tk
import subprocess

#AP1 = "ESP32-AP1"
#AP2 = "ESP32-AP2"
#http = "http://192.168."
#Dictionary of cameras with their AP + stream URL
cameras = {
    "Printer 1":{"AP": "ESP32-AP1", "url": "http://192.168.4.5"},
    "Printer 2":{"AP": "ESP32-AP1", "url": "http://192.168.4.6"},
    "Printer 3":{"AP": "ESP32-AP2", "url": "http://192.168.5.5"},
    "Printer 4":{"AP": "ESP32-AP2", "url": "http://192.168.5.6"},
    
}

def connect_and_open(camera_name):
    cam = cameras[camera_name]
    ap = cam["AP"]
    url = cam["url"]
    
    #connect Wi-Fi using nmcli
    subprocess.run(["nmcli", "dev", "wifi", "connect", ap])
    
    #open browser with camera feed
    subprocess.Popen(["xdg-open", url])
    
root=tk.Tk()
root.title("ESP32 Camera Selector")

for cam in cameras.keys():
    tk.Button(root, text=cam, command=lambda c=cam: connect_and_open(c),
              width=20,height=2).pack(pady=5)
    
root.mainloop()