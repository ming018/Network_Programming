import socket

BUFFSIZE = 1024
port = 250

# 서버와 통신 유형의 소켓 생성
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


while True :
    msg = input() # Hello UDP select
    if msg == 'stop' :
        break

    sock.sendto(msg.encode(),('localhost', port)) # 메세지 송신
    data, addr = sock.recvfrom(BUFFSIZE) # 메세지 수신
    print("Server says : ", data.decode())