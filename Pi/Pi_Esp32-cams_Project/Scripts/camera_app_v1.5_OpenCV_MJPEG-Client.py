import cv2

#Replace with your ESP32-CAM IP
camera_ip = "192.168.4.5"
url = f"http://{camera_ip}/stream"

cap = cv2.VideoCapture(url)

if not cap.isOpened():
    print("Failed to open camera stream")
    exit()
    
while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to fetch frame")
        break
    
    cv2.imshow("ESP32-CAM 1", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    
cap.release()
cv2.destroyAllWindows()
