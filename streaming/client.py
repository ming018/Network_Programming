import pickle
import struct
import tkinter as tk
import threading
import cv2
import socket
import numpy as np
from PIL import Image, ImageTk

# 서버 IP 주소 및 포트 번호
SERVER_IP = '127.0.0.1'
SERVER_PORT = 2500

# 클라이언트    소켓 설정
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))


root = tk.Tk()
root.title("Video Streaming Client")

# 웹캠 캡처를 위한 스레드
# class VideoStreamThread(threading.Thread):
#     def __init__(self, server_socket):
#         super().__init__()
#         self.server_socket = server_socket
#
#     def run(self):
#         data = b""
#         payload_size = struct.calcsize("Q")  # 데이터는 unsigned Long Long
#         cap = cv2.VideoCapture(0)  # 웹캠 캡처
#         while True:
#             ret, frame = cap.read()
#             if not ret:
#                 break
#             _, img_encoded = cv2.imencode('.jpg', frame)
#             img_bytes = img_encoded.tobytes()
#             self.server_socket.sendall(img_bytes)


def connet_to_server() :
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 2500))

# GUI 생성


# 서버로부터 비디오 스트리밍을 받아 화면에 표시하는 함수
def receive_video_stream():
    while True :
        data = client_socket.recv(4096)
        frame_data_size = struct.unpack("Q", data[:8])[0]
        frame_data = data[8:]

        # 프레임 데이터 수신
        frame_data = b""
        while len(frame_data) < frame_data_size:
            frame_data += client_socket.recv(4096)
        frame_bytes = frame_data[:frame_data_size]
        frame_data = frame_data[frame_data_size:]

        frame = pickle.loads(frame_bytes)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        photo = ImageTk.PhotoImage(image=img)

        root.config(image=photo)
        root.image = photo

        cv2.imshow("Received Frame", frame)

    # while True:
    #     try:
    #         print('요시 그란도 시즌')
    #         print('요시 그란도 시즌2')
    #         img_bytes = client_socket.recv(1024)
    #
    #         img_encoded = np.frombuffer(img_bytes, dtype=np.uint8)
    #         frame = cv2.imdecode(img_encoded, cv2.IMREAD_COLOR)
    #         frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #
    #         photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
    #         frame_label.config(image=photo)
    #         frame_label.image = photo
    #         print('요시 그란도 시즌3')
    #     except Exception as e:
    #         print(e)
    #         break




# 메시지 전송 함수
def send_message():
    message = entry.get()
    client_socket.sendall(message.encode())
    entry.delete(0, tk.END)


# 비디오 프레임 표시를 위한 Label 위젯 생성
# 라벨 위젯을 사용하여 영상 표시 (80%)
frame_label = tk.Frame(root)
frame_label.grid(row=0, column=0, padx=100, pady=10, rowspan=2, sticky="nsew")

# 채팅 창 (Text 위젯) 추가 (20%)
chat_text = tk.Text(root, wrap=tk.WORD, state=tk.DISABLED)
chat_text.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

# 메시지 입력 필드 (20%)
entry = tk.Entry(root)
entry.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

# 메시지 보내기 버튼 (20%)
send_button = tk.Button(root, text="보내기", command=send_message)
send_button.grid(row=1, column=1, padx=10, pady=10, sticky="se")

# 행 및 열 가중치 설정
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=4)  # 비디오 화면이 80% 차지
root.grid_columnconfigure(1, weight=1)  # 채팅 창이 20% 차지

# GUI 시작
#root.mainloop()

# 연결 종료 시 스레드 및 소켓 닫기


if __name__ == '__main__' :
    print('메롱메롱')

    # 비디오 수신 스레드 시작
    video_thread = threading.Thread(target=receive_video_stream)
    video_thread.daemon = True
    video_thread.start()

    view_thread = threading.Thread(target=root.mainloop())
    view_thread.daemon = True
    view_thread.start()

    root.mainloop()

    client_socket.close()


# import tkinter as tk
# import threading
# import cv2
# import socket
# import numpy as np
# from PIL import Image, ImageTk
#
# # 서버 IP 주소 및 포트 번호
# SERVER_IP = '127.0.0.1'
# SERVER_PORT = 250
#
#
# # 웹캠 캡처를 위한 스레드
# class VideoStreamThread(threading.Thread):
#     def __init__(self, server_socket, update_callback):
#         super().__init__()
#         self.server_socket = server_socket
#         self.update_callback = update_callback
#
#     def run(self):
#         cap = cv2.VideoCapture(0)  # 웹캠 캡처
#         while True:
#             ret, frame = cap.read()
#             if not ret:
#                 break
#             _, img_encoded = cv2.imencode('.jpg', frame)
#             img_bytes = img_encoded.tobytes()
#             self.server_socket.sendall(img_bytes)
#
#             # 이미지 업데이트를 메인 스레드로 전달
#             frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
#             self.update_callback(photo)
#
#
# # GUI 생성 함수
#
#     # GUI 생성
# root = tk.Tk()
# root.title("Video Streaming Client")
#
# # 비디오 프레임 표시를 위한 Label 위젯 생성
# frame_label = tk.Label(root)
# frame_label.pack()
#
# # 메시지 입력 필드 및 전송 버튼
# entry = tk.Entry(root, width=50)
# entry.pack()
#
#
# def send_message():
#     message = entry.get()
#     client_socket.sendall(message.encode())
#     entry.delete(0, tk.END)
#
#     send_button = tk.Button(root, text="Send", command=send_message)
#     send_button.pack()
#
#
#
#     # 이미지 업데이트 함수
# def update_image(photo):
#     frame_label.config(image=photo)
#     frame_label.image = photo
#
#     # 비디오 수신 스레드 시작
#     video_thread = VideoStreamThread(client_socket, update_image)
#     video_thread.daemon = True
#     video_thread.start()
#
#     # GUI 시작
#     root.mainloop()
#
#
# # 클라이언트 소켓 설정
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client_socket.connect((SERVER_IP, SERVER_PORT))
#
#
#
#
# # 연결 종료 시 소켓 닫기
# client_socket.close()
