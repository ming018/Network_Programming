import socket

# 클라이언트 소켓 생성
s_sock = socket.socket()
host = "localhost"
port = 2500
# 포트가 비어 있는 이유는?
# 논리적 주소인 IP를 먼저 안 다음에 IP를 통해 pc에 접근하여 pc내에 어떤 프로그램인지 찾기 위해 port를 적는데
# pc마다 가용 포트번호가 다르기때문에 알아서 적으란 거임

# 서버에 연결? 항사 튜플 형태임
s_sock.connect((host,port))

# 서버에 I'am ready 전송
s_sock.send("I'm ready".encode())

# 서버로부터 파일 이름 수신
fn = s_sock.recv(1024).decode()

# 파일을 recv 라는 이름으로 현재 디렉토리에 저장
with open("./dummy/" + "recv", 'wb') as f :
    print("Receiving")
    while True :
        data = s_sock.recv(8192)
        if not data :
            break
        f.write(data)

print("Download complete")
s_sock.close()