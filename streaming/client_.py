# import tkinter as tk
# import threading
# import cv2
# import socket
# import numpy as np
# from PIL import Image, ImageTk
#
# # 서버 IP 주소 및 포트 번호
# SERVER_IP = '127.0.0.1'
# SERVER_PORT = 2500
#
# # 클라이언트 소켓 설정
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client_socket.connect((SERVER_IP, SERVER_PORT))
#
#
# # GUI 생성
# root = tk.Tk()
# root.title("Video Streaming Client")
#
# # 비디오 프레임 표시
# frame_label = tk.Label(root)
#
# def receive_video_stream():
#     while True:
#         try:
#             # 프레임의 길이를 먼저 수신 16바이트로 고정
#             length = client_socket.recv(16)
#             frame_length = int(length)
#
#             # 프레임 데이터 수신
#             img_bytes = b""
#             while frame_length:
#                 data = client_socket.recv(4096)
#                 if not data:
#                     break
#                 img_bytes += data
#                 frame_length -= len(data)
#
#             img_encoded = np.frombuffer(img_bytes, dtype=np.uint8)
#
#             # 프레임 디코딩 및 표시
#             frame = cv2.imdecode(img_encoded, cv2.IMREAD_COLOR)
#             frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
#             frame_label.config(image=photo)
#             frame_label.image = photo
#         except Exception as e:
#             print(e)
#             break
#
# # 메시지 전송 함수
# def send_message():
#     message = entry.get()
#     client_socket.send(message.encode())
#     entry.delete(0, tk.END)
#
# def receive_message() :
#     while True :
#         msg = client_socket.recv(4068)
#         try :
#             msg = msg.decode()
#             chat_text.config(state=tk.NORMAL)
#             chat_text.insert(tk.END, "상대방: " + msg + "\n")
#             chat_text.insert(tk.END, "try임  " + "\n")
#             chat_text.config(state=tk.DISABLED)
#         except :
#             chat_text.insert(tk.END, "상대방: " + "\n")
#
#
# # GUI 구성요소 생성
# frame_label.grid(row=0, column=0, padx=10, pady=10, rowspan=2, sticky="nsew")
#
# chat_text = tk.Text(root, wrap=tk.WORD, state=tk.DISABLED)
# chat_text.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
#
# # entry
# entry = tk.Entry(root)
# entry.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
#
# # send_button
# send_button = tk.Button(root, text="보내기", command=send_message)
# send_button.grid(row=1, column=1, padx=10, pady=10, sticky="se")
#
# # 행 및 열 가중치 설정
# root.grid_rowconfigure(0, weight=1)
# root.grid_columnconfigure(0, weight=4)  # 비디오 화면이 80% 차지
# root.grid_columnconfigure(1, weight=1)  # 채팅 창이 20% 차지
#
#
# if __name__ == '__main__' :
#
#     # 비디오 수신 스레드 시작
#     video_thread = threading.Thread(target=receive_video_stream)
#     video_thread.daemon = True
#     video_thread.start()
#
#     # sending_thread = threading.Thread(target=send_message)
#     # sending_thread.daemon = True
#     # sending_thread.start()
#
#     receiving_thread = threading.Thread(target=receive_message)
#     receiving_thread.daemon = True
#     receiving_thread.start()
#
#     # GUI 시작
#     root.mainloop()
#
#     # 연결 종료 시 스레드 및 소켓 닫기
#     client_socket.close()

import tkinter as tk
import threading
import cv2
import socket
import numpy as np
from PIL import Image, ImageTk

SERVER_IP = '127.0.0.1'
VIDEO_PORT = 2500
TEXT_PORT = 2501

video_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
video_client_socket.connect((SERVER_IP, VIDEO_PORT))

text_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
text_client_socket.connect((SERVER_IP, TEXT_PORT))

root = tk.Tk()
root.title("비디오 스트리밍 클라이언트")
frame_label = tk.Label(root)
frame_label.grid(row=0, column=0, padx=10, pady=10, rowspan=2, sticky="nsew")


def receive_video_stream():
    while True:
        length = video_client_socket.recv(16).decode().strip()
        frame_length = int(length)
        img_bytes = b""
        while frame_length:
            data = video_client_socket.recv(4096)
            if not data:
                break
            img_bytes += data
            frame_length -= len(data)

        img_encoded = np.frombuffer(img_bytes, dtype=np.uint8)
        frame = cv2.imdecode(img_encoded, cv2.IMREAD_COLOR)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
        frame_label.config(image=photo)
        frame_label.image = photo


def send_message():
    message = entry.get()
    text_client_socket.send(message.encode())
    entry.delete(0, tk.END)


def receive_message():
    while True:
        msg = text_client_socket.recv(4096).decode()
        chat_text.config(state=tk.NORMAL)
        chat_text.insert(tk.END, "서버: " + msg + "\n")
        chat_text.config(state=tk.DISABLED)


chat_text = tk.Text(root, wrap=tk.WORD, state=tk.DISABLED)
chat_text.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

entry = tk.Entry(root)
entry.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

send_button = tk.Button(root, text="보내기", command=send_message)
send_button.grid(row=1, column=1, padx=10, pady=10, sticky="se")

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=4)
root.grid_columnconfigure(1, weight=1)

video_thread = threading.Thread(target=receive_video_stream)
video_thread.daemon = True
video_thread.start()

receiving_thread = threading.Thread(target=receive_message)
receiving_thread.daemon = True
receiving_thread.start()

root.mainloop()
video_client_socket.close()
text_client_socket.close()

