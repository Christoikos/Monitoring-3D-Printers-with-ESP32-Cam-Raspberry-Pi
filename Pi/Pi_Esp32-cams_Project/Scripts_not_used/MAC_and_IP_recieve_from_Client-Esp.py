import socket

# Settings
UDP_PORT = 12345
BUFFER_SIZE = 1024

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', UDP_PORT))

print(f"[+] Listening for ESP32 clients on UDP port {UDP_PORT}...")

# Store IP/MAC entries
clients = {}

while True:
    data, addr = sock.recvfrom(BUFFER_SIZE)
    message = data.decode('utf-8').strip()
    
    try:
        mac, ip = message.split(',')
        mac = mac.strip()
        ip = ip.strip()

        clients[mac] = ip

        print(f"[?] Received from {addr[0]}: MAC = {mac} | IP = {ip}")

    except Exception as e:
        print(f"[!] Invalid message: {message} | Error: {e}")
