from socket import *
import struct

group_addr = ("224.0.0.255", 5005) # 그룹 주소

# AF_INET 이거 UDP는 이렇게 해야한다네?
s_sock = socket(AF_INET, SOCK_DGRAM) # 데이터그램 소켓 사용
s_sock.settimeout(0.5)

TTL = struct.pack('@i', 2) # TTL = 2, 4바이트의 정수로 표현?
s_sock.setsockopt(IPPROTO_IP, IP_MULTICAST_TTL, TTL)
s_sock.setsockopt(IPPROTO_IP, IP_MULTICAST_LOOP, False)

while True :
    rmsg = input('Msg : ')
    s_sock.sendto(rmsg.encode(), group_addr)

    try :
        response, addr = s_sock.recvfrom(1024)
    except timeout :
        break
    else :
        print('{} from {}'.format(response.decode(), addr))