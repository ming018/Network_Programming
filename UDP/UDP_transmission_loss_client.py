import socket

BUFFER = 1024
port = 250

# 서버와 통신 유형의 소켓 생성
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.connect(('localhost', port))

for i in range(10) :
    delay = 0.1
    data = 'Testing'
    while True :
        sock.send(data.encode())
        print('Watting up to {} seconds for a reply'.format(delay))
        sock.settimeout(delay) # 타임아웃 설정
        try:
            data = sock.recv(BUFFER)
        except socket.timeout:
            delay *= 2 # 대기시간 2배 증가
            if delay > 2.0 : # 시간 초과
                break
        else :
            print('Response : ', data.decode())
            break