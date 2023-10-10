# _thread 모듈을 사용한 멀티스레드 구현

from socket import *
import _thread

HOST = 'localhost'
PORT = 2500
BUFF = 1024

def response(key) :
    return '서버 응답 메시지'

def handler(clientsock, addr) : # 핸들러 함수
    while True :
        data = clientsock.recv(BUFF)
        print('data : ' + repr(data))

        if not data : break
        clientsock.send(response('').encode())
        print('sent : ' + repr(response('')))

if __name__ == '__main__' :
    ADDR = (HOST, PORT) # 어떤 주소로 소켓을 열것인지
    serversock = socket(AF_INET, SOCK_STREAM)
    # INFT는 IPV4 사용하고, TCP프로토콜을 이용해서 엶
    serversock.setsockopt(SOL_SOCKET,SO_REUSEADDR, 1)
    
    serversock.bind(ADDR)
    # ADDR의 주소를 이용해서 클라이언트 보고 와라고 함
    
    serversock.listen(5)
    # 최대 인원수


    # 원래는 데이터를 주고 받던 것을 메인함수 하나에서만 다 해서 순차적으로 진행 됐던 반면,
    # 멀티 스레드는 서버에 접속이 확인되면 그 클라이언트에 대응하는 스레드를 하나씩 만들어서 실행함
    # 장점은 순차적이여서 기존의 실행이 끝날 때 까지 대기해야 했지만
    # 멀티 스레드를 통해 좀 더 효율적으로 가능
    while True :
        print('Waiting for connection ... ')
        clientsock, addr = serversock.accept()
        print('... connected from : ', addr)
        _thread.start_new_thread(handler, (clientsock, addr))


