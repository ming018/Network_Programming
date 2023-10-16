import threading
import tkinter as tk
import Thread

import cv2
import socket
from PIL import Image, ImageTk

# 서버 초기화
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 12345))
server_socket.listen(1)
client_socket, addr = server_socket.accept()

def update():
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
        label.config(image=photo)
        label.image = photo

        # 프레임을 클라이언트로 전송
        _, img_encoded = cv2.imencode('.jpg', frame)
        img_bytes = img_encoded.tobytes()
        message_size = len(img_bytes)
        client_socket.sendall(f"{message_size:<20}".encode() + img_bytes)

        # 메시지 수신
        message = client_socket.recv(1024).decode()
        chat_text.config(state=tk.NORMAL)
        chat_text.insert(tk.END, "Client: " + message + "\n")
        chat_text.config(state=tk.DISABLED)

    window.after(10, update)

# 메시지 보내기 함수
def send_message():
    message = entry.get()
    chat_text.config(state=tk.NORMAL)
    chat_text.insert(tk.END, "나: " + message + "\n")
    chat_text.config(state=tk.DISABLED)
    entry.delete(0, tk.END)

# GUI 초기화
window = tk.Tk()
window.title("화상 채팅")

# 웹캠 초기화
cap = cv2.VideoCapture(0)

label = tk.Label(window)
label.grid(row=0, column=0, padx=10, pady=10, rowspan=2, sticky="nsew")

chat_text = tk.Text(window, wrap=tk.WORD, state=tk.DISABLED)
chat_text.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

entry = tk.Entry(window)
entry.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

send_button = tk.Button(window, text="보내기", command=send_message)
send_button.grid(row=1, column=1, padx=10, pady=10, sticky="se")

window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=4)
window.grid_columnconfigure(1, weight=1)

updating = threading.Thread(target=update())
updating.daemon = True
updating.start()

window.mainloop()

cap.release()
client_socket.close()
