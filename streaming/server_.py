import threading
import _thread
import tkinter as tk
import cv2
from PIL import Image, ImageTk
from socket import *

# 클라이언트 접속 대기?

port = 2500
ADDR = ('127.0.0.1', port)
server_sock = socket(AF_INET, SOCK_STREAM)
server_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
server_sock.bind(ADDR)
server_sock.listen(5)

client_sock = None
addr = None


def response(key):
    return '서버 응답 메시지'

def handler(clientsock, addr): #핸들러 함수
    while True:
        ret, frame = cap.read()  # 웹캠에서 프레임 읽기
        if not ret:  # 읽기 실패 시 종료
            break

        _, img_encoded = cv2.imencode('.jpg', frame)  # 프레임을 JPG로 인코딩
        img_bytes = img_encoded.tobytes()  # 인코딩된 이미지를 바이트로 변환

        # 메시지 타입 (헤더) 전송
        clientsock.sendall("VIDEO".encode().ljust(16))

        # 전송할 데이터의 길이를 먼저 전송
        data_length = len(img_bytes)
        clientsock.sendall(str(data_length).encode().ljust(16))

        # 실제 데이터 전송
        clientsock.sendall(img_bytes)


# 접속 대기 함수?
def waiting() :
    while True:
        print('waiting for connection...')
        global client_sock, addr
        client_sock, addr = server_sock.accept()
        print('...connected from:', addr)
        _thread.start_new_thread(handler, (client_sock, addr))

# 화면 갱신 함수
def update():
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
        label.config(image=photo)
        label.image = photo
    window.after(10, update)

# 메시지 보내기 함수
def send_message():
    global client_sock

    message = entry.get()
    chat_text.config(state=tk.NORMAL)
    chat_text.insert(tk.END, "나: " + message + "\n")
    chat_text.config(state=tk.DISABLED)
    entry.delete(0, tk.END)

    try :
        if client_sock :
            msg = message.encode()
            client_sock.send(msg)

    except :
        chat_text.insert(tk.END, "나: " + "\n")


# GUI 초기화
window = tk.Tk()
window.title("화상 채팅")

# 웹캠 초기화
cap = cv2.VideoCapture(0)

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
    updating = threading.Thread(target=update)
    updating.daemon = True
    updating.start()

    # 접속 대기 함수 호출
    wait_thread = threading.Thread(target=waiting)
    wait_thread.daemon = True
    wait_thread.start()

    send_thread = threading.Thread(target=send_message)
    send_thread.daemon = True
    send_thread.start()

    # GUI 시작

    window.mainloop()


# 웹캠 해제
cap.release()