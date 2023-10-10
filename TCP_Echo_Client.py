import socket

port = int(input("Port num : "))
address = ("localhost", port) # 주소는 (ip, port)인 튜플
BUFSIZE = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(address) # 서버에 연결 요청

while True :
    msg = input("Message to send : ")

    s.send(msg.encode()) # 서버에게 메세지 전송
    data = s.recv(BUFSIZE) # 서버로부터 메세지 받음
    print("Received Message : %s " %data.decode()) # 바
    # 이트 형을 문자열로 출력