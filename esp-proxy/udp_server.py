import socket
import threading
import time
from queue import Queue

import cv2
import numpy as np

# Set up the TCP server
TCP_IP = "0.0.0.0"
TCP_PORT = 5005
BUFFER_SIZE = 4096  # A reasonable buffer size for chunking

tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcp_sock.bind((TCP_IP, TCP_PORT))
tcp_sock.listen(5)

print(f"TCP server up and listening on {TCP_IP}:{TCP_PORT}")

# Queue to hold the latest frame
frame_queue = Queue(maxsize=1)

def read_frames():
    cap = cv2.VideoCapture("rtsp://localhost:8554/live")
    while True:
        ret, frame = cap.read()
        if ret:
            _, jpeg = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 50])
            if frame_queue.full():
                frame_queue.get()
            frame_queue.put(jpeg.tobytes())
        else:
            print("Failed to read frame from RTSP stream")

# Start a thread to read frames from the RTSP stream
frame_thread = threading.Thread(target=read_frames)
frame_thread.daemon = True
frame_thread.start()

def handle_client_connection(client_socket):
    try:
        request = client_socket.recv(BUFFER_SIZE)
        if request.decode().strip() != "GET_IMAGE":
            client_socket.close()
            return

        if not frame_queue.empty():
            jpeg_data = frame_queue.get()
            total_bytes_sent = 0
            for i in range(0, len(jpeg_data), BUFFER_SIZE):
                chunk = jpeg_data[i:i+BUFFER_SIZE]
                client_socket.sendall(chunk)
                total_bytes_sent += len(chunk)
            print(f"Sent {total_bytes_sent} bytes to client")
        client_socket.close()
    except Exception as e:
        print(f"Error: {e}")
        client_socket.close()

while True:
    client_sock, addr = tcp_sock.accept()
    print(f"Accepted connection from {addr}")
    client_handler = threading.Thread(target=handle_client_connection, args=(client_sock,))
    client_handler.start()
    time.sleep(0)
