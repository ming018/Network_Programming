import socket
import cap_ex

SIZE = 5
sock = socket.socket()
sock.connect(('localhost', 2700))

HEAD = 0x05
addr = 1
seqNo = 1
frame_seq = ""
msg = "Hello World!"

print('전송될 메세지 : ', msg)

for i in range(0 , len(msg), SIZE) :
    frame_seq += cap_ex.frame(HEAD, addr, seqNo, msg[i : i + SIZE])
    seqNo += 1

sock.send(frame_seq.encode())
msg = sock.recv(1024).decode()
print('수신 : ', msg)

r_frame = msg.split(chr(0x05))
del r_frame[0]

p_msg = ''

for field in r_frame :
    p_msg += field[10 : (11 + int(field[6 : 10]))]

print('복원된 메세지 : ', p_msg)

sock.close()

if __name__ == '__main__' :
    stat_ch = 0x05
    addr = 2
    seqNo = 1

    msg = input("MSG : ")
    capsule = cap_ex.frame(start_ch = stat_ch, addr = addr, seqNo = seqNo, msg = msg)
    print(capsule)