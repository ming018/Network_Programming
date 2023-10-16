import tkinter as tk
import threading
import cv2
import socket
import numpy as np
from PIL import Image, ImageTk

SERVER_IP = '127.0.0.1'
SERVER_PORT = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))

root = tk.Tk()
root.title("Video Streaming Client")

frame_label = tk.Label(root)
frame_label.pack()

def receive_video_stream():
    while True:
        try:
            length_header = client_socket.recv(20).decode().strip()
            img_length = int(length_header)

            img_bytes = b""
            while len(img_bytes) < img_length:
                to_read = img_length - len(img_bytes)
                img_bytes += client_socket.recv(4096 if to_read > 4096 else to_read)

            img_encoded = np.frombuffer(img_bytes, dtype=np.uint8)
            frame = cv2.imdecode(img_encoded, cv2.IMREAD_COLOR)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            frame_label.config(image=photo)
            frame_label.image = photo
        except Exception as e:
            print(e)
            break

def send_message():
    message = entry.get()
    client_socket.sendall(message.encode())
    entry.delete(0, tk.END)

entry = tk.Entry(root, width=50)
entry.pack()
send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack()

video_thread = threading.Thread(target=receive_video_stream)
video_thread.daemon = True
video_thread.start()

send_thread = threading.Thread(target=send_message())
send_thread.daemon = True
send_thread.start()

rooting = threading.Thread(target=root.mainloop())
rooting.daemon = True
rooting.start()

client_socket.close()
