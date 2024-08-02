import signal
import socket
import sys
import time

import cv2

# Load the video file
video_path = "video.mp4"  # Replace with the path to your video file
cap = cv2.VideoCapture(video_path)

# Get video properties
fps = cap.get(cv2.CAP_PROP_FPS)
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
duration = frame_count / fps

# Set up the TCP server
TCP_IP = "0.0.0.0"
TCP_PORT = 5005
BUFFER_SIZE = 1024

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((TCP_IP, TCP_PORT))
server_socket.listen(1)

print(f"TCP server up and listening on {TCP_IP}:{TCP_PORT}")

def signal_handler(sig, frame):
    print("Interrupt received, stopping server...")
    server_socket.close()
    cap.release()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

start_time = time.time()

while True:
    try:
        conn, addr = server_socket.accept()
        print(f"Connection from {addr}")

        while True:
            request = conn.recv(BUFFER_SIZE)
            if not request or request.decode().strip() != "GET_IMAGE":
                continue

            # Calculate the current frame based on the elapsed time
            elapsed_time = time.time() - start_time
            current_frame = int((elapsed_time % duration) * fps)

            # Set the video capture to the current frame
            cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame)

            # Read the frame from the video
            ret, frame = cap.read()
            if not ret:
                # If reading the frame fails, loop the video
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue

            # Convert the frame to JPEG
            _, jpeg = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 60])
            jpeg_data = jpeg.tobytes()

            # Send the JPEG data over TCP
            total_bytes_sent = 0
            for i in range(0, len(jpeg_data), BUFFER_SIZE):
                chunk = jpeg_data[i:i+BUFFER_SIZE]
                conn.sendall(chunk)
                total_bytes_sent += len(chunk)
                print(f"Sent chunk of {len(chunk)} bytes, Total: {total_bytes_sent} bytes")

            print("DONE!")
            # Ensure the connection is properly closed
            conn.close()
            break

    except Exception as e:
        print(f"Error: {e}")
        break
