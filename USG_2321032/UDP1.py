import socket

# UDP 소켓 생성
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 소켓을 포트 10001에 바인딩
s.bind(('', 10001))

# 메시지를 인코딩하고, 'localhost'의 10001번 포트로 전송
msg = '2321032 박민규'
s.sendto(msg.encode(), ('localhost', 10001))

# 소켓 닫기 (필요한 경우)
s.close()
