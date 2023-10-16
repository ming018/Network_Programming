import _thread
import threading
import tkinter as tk
import cv2
from PIL import Image, ImageTk
import socket
import pickle
import struct
import imutils

##
def response(key):
    return '서버 응답 메시지'

def handler(clientsock, addr): #핸들러 함수
    while True:
        data = clientsock.recv(1024)
        print('data:' + repr(data))
        if not data: break
        clientsock.send(response('').encode())
        print('sent:' + repr(response('')))


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 2500
BUFFSIZE = 1024
sock = socket.socket()
sock.bind(('', port))

sock.listen(5)



##

# 화면 갱신 함수
def update():
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
        label.config(image=photo)
        label.image = photo
    window.after(10, update)

def wait_client() :
    while True :
        print('waiting for connection...')
        clientsock, addr = sock.accept()
        print('...connected from:', addr)
        _thread.start_new_thread(handler, (clientsock, addr))


# 메시지 보내기 함수
def send_message():
    message = entry.get()
    chat_text.config(state=tk.NORMAL)
    chat_text.insert(tk.END, "나: " + message + "\n")
    chat_text.config(state=tk.DISABLED)
    entry.delete(0, tk.END)

def recive_message() :
    data = sock.recv(1024)  # ➎ client에서 읽기 이벤트
    msg = data.decode()

    chat_text.config(state=tk.NORMAL)
    chat_text.insert(tk.END, "누군가: " + msg + "\n")
    chat_text.config(state=tk.DISABLED)

def receive_message(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()  # 클라이언트로부터 메시지 수신
            if not message:
                break
            print("상대방:", message)  # 받은 메시지를 콘솔에 출력하거나 다른 처리를 할 수 있음
        except Exception as e:
            print(e)
            break

# GUI 초기화
window = tk.Tk()
window.title("화상 채팅")

# 웹캠 초기화
cap = cv2.VideoCapture(0)

def send_video() :
    print('왜 안됨 진짜')
    while True:
        client_socket, addr = server_socket.accept()
        print(addr, '와 연결됨')
        ret, frame = cap.read()

        if client_socket:
            vid = cv2.VideoCapture(0)  # 웹캠 연결
            if vid.isOpened():
                print(vid.get(3), vid.get(4))
            while vid.isOpened():
                # img, frame = vid.read()  # 프레임 획득
                # frame = imutils.resize(frame, width=640)  # 프레임 크기 조절

                frame_bytes = pickle.dumps(frame)  # 프레임을 바이트 스트림으로 변환
                msg = struct.pack("Q", len(frame_bytes)) + frame_bytes

                # 메시지 Q unsigned long long d으로 보낼 데이터 크기 전송
                client_socket.sendall(msg)

                cv2.imshow('s', frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    client_socket.close()
    # while True:
    #     client_socket, addr = server_socket.accept()
    #     print(addr, '와 연결됨')
    #     if client_socket:
    #         vid = cv2.VideoCapture(0)  # 웹캠 연결
    #         if vid.isOpened():
    #             print(vid.get(3), vid.get(4))
    #         while vid.isOpened():
    #             img, frame = vid.read()  # 프레임 획득
    #             frame = imutils.resize(frame, width=640)  # 프레임 크기 조절
    #             frame_bytes = pickle.dumps(frame)  # 프레임을 바이트 스트림으로 변환
    #             msg = struct.pack("Q", len(frame_bytes)) + frame_bytes
    #             # 메시지 Q unsigned long long d으로 보낼 데이터 크기 전송
    #             client_socket.sendall(msg)
    #
    #             cv2.imshow('s', frame)
    #             key = cv2.waitKey(1) & 0xFF
    #             if key == ord('q'):
    #                 client_socket.close()

# 라벨 위젯을 사용하여 영상 표시 (80%)


label = tk.Label(window)
label.grid(row=0, column=0, padx=10, pady=10, rowspan=2, sticky="nsew")

# 채팅 창 (Text 위젯) 추가 (20%)
chat_text = tk.Text(window, wrap=tk.WORD, state=tk.DISABLED)
chat_text.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

# 메시지 입력 필드 (20%)
entry = tk.Entry(window)
entry.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

# 메시지 보내기 버튼 (20%)
send_button = tk.Button(window, text="보내기", command=send_message)
send_button.grid(row=1, column=1, padx=10, pady=10, sticky="se")

# 행 및 열 가중치 설정
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=4)  # 비디오 화면이 80% 차지
window.grid_columnconfigure(1, weight=1)  # 채팅 창이 20% 차지

if __name__ == '__main__' :
    # 갱신 함수 호출
    updating = threading.Thread(target=update())
    updating.daemon = True
    updating.start()

    # GUI 시작
    window_ = threading.Thread(target=window.mainloop())
    window_.daemon = True
    window_.start()

    #연결 감지 함수?
    connecting = threading.Thread(target=wait_client())
    connecting.daemon = True
    connecting.start()


    # 비디오 보내기?
    send_video_thread = threading.Thread(target=send_video())
    send_video_thread.daemon = True
    send_video_thread.start()

    # print('waiting for connection...')
    # clientsock, addr = sock.accept()
    # print('...connected from:', addr)
    # _thread.start_new_thread(handler, (clientsock, addr))

# 웹캠 해제
cap.release()

