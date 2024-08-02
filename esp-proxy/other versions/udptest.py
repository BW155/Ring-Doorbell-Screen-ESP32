import signal
import socket
import sys
import time

import numpy as np

# Load the converted RGB565 image
image_rgb565_path = "./converted_image_rgb565.npy"
image_data = np.load(image_rgb565_path).tobytes()

# Set up the UDP server
UDP_IP = "0.0.0.0"
UDP_PORT = 5005
CHUNK_SIZE = 1024  # Define the size of each chunk

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"UDP server up and listening on {UDP_IP}:{UDP_PORT}")

def signal_handler(sig, frame):
    print("Interrupt received, stopping server...")
    sock.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

while True:
    try:
        data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
        if data.decode() == "GET_IMAGE":
            print(f"Received request from {addr}")
            # Send the image data in chunks
            for i in range(0, len(image_data), CHUNK_SIZE):
                chunk = image_data[i:i+CHUNK_SIZE]
                sock.sendto(chunk, addr)
                time.sleep(0.01)  # Adjust the delay to control the streaming rate
            print(f"Image sent to {addr}")
    except Exception as e:
        print(f"Error: {e}")
        break
