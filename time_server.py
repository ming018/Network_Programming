# 클라이언트가 접속하면 현재 시간을 전송하는 서버 프로그램

import socket
import time

# 2. TCP 소켓 생성
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
address = ('', 5000)# ''임의의 주소 지정, 사용 포트넘버 5000
s.bind(address)# 3. 소켓과 주소 결합 단계
s.listen(5)# 4. 서버사이드의 연결 대기, 매게변수 만큼 수용 가능

while True :
    client, addr = s.accept() # 5. 연결 허용, (client socket, rem addr 반환)
    print("Connection requested from ", addr)
    client.send(time.ctime(time.time()).encode())# 6. 현재 시간 전송
    client.close()# 7. 소켓 종료