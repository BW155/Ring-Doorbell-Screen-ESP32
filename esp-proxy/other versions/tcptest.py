import io
import signal
import socket
import sys

from PIL import Image

# Load and compress the JPEG image
image_path = "image.jpg"
image = Image.open(image_path)
compressed_image_io = io.BytesIO()
image.save(compressed_image_io, format='JPEG', quality=70)  # Adjust quality as needed
jpeg_data = compressed_image_io.getvalue()

# Set up the TCP server
TCP_IP = "0.0.0.0"
TCP_PORT = 5005
BUFFER_SIZE = 1024

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((TCP_IP, TCP_PORT))
server_socket.listen(1)

print(f"TCP server up and listening on {TCP_IP}:{TCP_PORT}")

def signal_handler(sig, frame):
    print("Interrupt received, stopping server...")
    server_socket.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

while True:
    try:
        conn, addr = server_socket.accept()
        print(f"Connection from {addr}")

        total_bytes_sent = 0
        for i in range(0, len(jpeg_data), BUFFER_SIZE):
            chunk = jpeg_data[i:i+BUFFER_SIZE]
            conn.sendall(chunk)
            total_bytes_sent += len(chunk)
            print(f"Sent chunk of {len(chunk)} bytes, Total: {total_bytes_sent} bytes")

        print(f"Finished sending image to {addr}")
        conn.close()
    except Exception as e:
        print(f"Error: {e}")
        break
