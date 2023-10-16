# import threading
# import _thread
# import tkinter as tk
# import cv2
# from PIL import Image, ImageTk
# from socket import *
#
# # 클라이언트 접속 대기?
#
# port = 2500
# ADDR = ('127.0.0.1', port)
# server_sock = socket(AF_INET, SOCK_STREAM)
# server_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
# server_sock.bind(ADDR)
# server_sock.listen(5)
#
# client_sock = None
# addr = None
#
#
# def response(key):
#     return '서버 응답 메시지'
#
# def handler(clientsock, addr): #핸들러 함수
#     while True:
#        # data = clientsock.recv(1024)
#
#         #######################
#
#         # 내가 출력 하고자 하는 방법이 안되는건가?
#         # 서버랑 클라이언트가 같은 캠을 공유할 수 있는가
#         # 핸들러는 한번만 실행이 되는건가?
#         # 여러 클라이언트 접속이 안되는 이유는?
#
#         # receive_thread = threading.Thread(target=waiting, args=(data,))
#         # receive_thread.daemon = True
#         # receive_thread.start()
#         # 65536
#         '''
#         def handler(clientsock, addr): #핸들러 함수
#             while True:
#                 data = clientsock.recv(BUFF)
#                 print('data:' + repr(data))
#                 if not data: break
#                 clientsock.send(response('').encode())
#                 print('sent:' + repr(response('')))
#
#         '''
#
#         ##################
#
#
#         ret, frame = cap.read()  # 웹캠에서 프레임 읽기
#         if not ret:  # 읽기 실패 시 종료
#             break
#
#         _, img_encoded = cv2.imencode('.jpg', frame)  # 프레임을 JPG로 인코딩
#         img_bytes = img_encoded.tobytes()  # 인코딩된 이미지를 바이트로 변환
#
#         # 전송할 데이터의 길이를 먼저 전송
#         data_length = len(img_bytes)
#         clientsock.sendall(str(data_length).encode().ljust(16))
#
#         # 실제 데이터 전송
#         clientsock.sendall(img_bytes)
#
# # 접속 대기 함수?
# def waiting() :
#     while True:
#         print('waiting for connection...')
#         global client_sock, addr
#         client_sock, addr = server_sock.accept()
#         print('...connected from:', addr)
#         _thread.start_new_thread(handler, (client_sock, addr))
#
# # 화면 갱신 함수
# def update():
#     ret, frame = cap.read()
#     if ret:
#         frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
#         label.config(image=photo)
#         label.image = photo
#     window.after(10, update)
#
# # 메시지 보내기 함수
# def send_message():
#     global client_sock
#
#     message = entry.get()
#     chat_text.config(state=tk.NORMAL)
#     chat_text.insert(tk.END, "나: " + message + "\n")
#     chat_text.config(state=tk.DISABLED)
#     entry.delete(0, tk.END)
#
#     try :
#         if client_sock :
#             msg = message.encode()
#             client_sock.send(msg)
#             print('asd')
#
#     except :
#         chat_text.insert(tk.END, "나: " + "\n")
#
#
# # GUI 초기화
# window = tk.Tk()
# window.title("화상 채팅")
#
# # 웹캠 초기화
# cap = cv2.VideoCapture(0)
#
# # 라벨 위젯을 사용하여 영상 표시 (80%)
# label = tk.Label(window)
# label.grid(row=0, column=0, padx=10, pady=10, rowspan=2, sticky="nsew")
#
# # 채팅 창 (Text 위젯) 추가 (20%)
# chat_text = tk.Text(window, wrap=tk.WORD, state=tk.DISABLED)
# chat_text.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
#
# # 메시지 입력 필드 (20%)
# entry = tk.Entry(window)
# entry.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
#
# # 메시지 보내기 버튼 (20%)
# send_button = tk.Button(window, text="보내기", command=send_message)
# send_button.grid(row=1, column=1, padx=10, pady=10, sticky="se")
#
# # 행 및 열 가중치 설정
# window.grid_rowconfigure(0, weight=1)
# window.grid_columnconfigure(0, weight=4)  # 비디오 화면이 80% 차지
# window.grid_columnconfigure(1, weight=1)  # 채팅 창이 20% 차지
#
#
# if __name__ == '__main__' :
#     # 갱신 함수 호출
#     updating = threading.Thread(target=update)
#     updating.daemon = True
#     updating.start()
#
#     # 접속 대기 함수 호출
#     wait_thread = threading.Thread(target=waiting)
#     wait_thread.daemon = True
#     wait_thread.start()
#
#     send_thread = threading.Thread(target=send_message)
#     send_thread.daemon = True
#     send_thread.start()
#
#     # GUI 시작
#
#
#
# # 웹캠 해제
# cap.release()


import numpy as np

import threading
import _thread
import tkinter as tk
import cv2
from PIL import Image, ImageTk
from socket import *


from PIL import ImageTk

from streaming.server import cap

VIDEO_PORT = 2500
TEXT_PORT = 2501
ADDR = ('127.0.0.1', VIDEO_PORT)

# 비디오 소켓 설정
video_server_sock = socket(AF_INET, SOCK_STREAM)
video_server_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
video_server_sock.bind(ADDR)
video_server_sock.listen(5)

# 텍스트 소켓 설정
text_server_sock = socket(AF_INET, SOCK_STREAM)
text_server_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
text_server_sock.bind(('127.0.0.1', TEXT_PORT))
text_server_sock.listen(5)

# GUI 초기화
root = tk.Tk()
root.title("화상 채팅_")


def handler(clientsock, addr):  # 비디오 핸들러 함수
    cap = cv2.VideoCapture(0)  # 카메라에서 캡처

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 이미지를 RGB 형식으로 변환
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # 프레임을 JPEG 형식으로 변환
        _, buffer = cv2.imencode('.jpg', frame)
        jpg_as_text = np.array(buffer).tobytes()

        # 먼저 JPEG 문자열의 길이를 전송
        length = len(jpg_as_text)
        clientsock.sendall(str(length).encode().ljust(16))

        # 그다음 JPEG 문자열을 전송
        clientsock.sendall(jpg_as_text)
    cap.release()


def text_handler(clientsock, addr):  # 텍스트 핸들러 함수
    while True:
        data = clientsock.recv(4096).decode()
        if not data:
            break
        print("받은 데이터:", data)


def waiting_for_video():
    while True:
        print('비디오 연결 대기 중...')
        video_client_sock, addr = video_server_sock.accept()
        print('비디오 연결됨:', addr)
        _thread.start_new_thread(handler, (video_client_sock, addr))


def waiting_for_text():
    while True:
        print('텍스트 연결 대기 중...')
        text_client_sock, addr = text_server_sock.accept()
        print('텍스트 연결됨:', addr)
        _thread.start_new_thread(text_handler, (text_client_sock, addr))

    frame_label = tk.Label(root)

    # 화면 갱신 함수
    def update():
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            frame_label.config(image=photo)
            frame_label.image = photo
        root.after(10, update)


    frame_label.grid(row=0, column=0, padx=10, pady=10, rowspan=2, sticky="nsew")

    chat_text = tk.Text(root, wrap=tk.WORD, state=tk.DISABLED)
    chat_text.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    entry = tk.Entry(root)
    entry.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

    send_button = tk.Button(root, text="보내기", command=send_message)
    send_button.grid(row=1, column=1, padx=10, pady=10, sticky="se")

    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=4)
    root.grid_columnconfigure(1, weight=1)



if __name__ == '__main__':

    video_wait_thread = threading.Thread(target=waiting_for_video)
    video_wait_thread.daemon = True
    video_wait_thread.start()

    text_wait_thread = threading.Thread(target=waiting_for_text)
    text_wait_thread.daemon = True
    text_wait_thread.start()

    root.mainloop()


    while True:
        pass
