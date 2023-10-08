# 프레이밍
# 데이터를 프레임단위로 만드는거 ?
# 예시는, 시작문자 1, 주소 2, 순서번호 4, 길이 4, 페이로드
# 로 각각 숫자만큼의 바이트로 할꺼임

def frame(start_ch, addr, seqNo, msg) :
    addr = str(addr).zfill(2) # zfill n 자리가 될때 까지 앞을 0으로 채움
    seqNo = str(seqNo).zfill(4)
    length = str(len(msg)).zfill(4)

    return chr(start_ch) + ' ' + addr + ' ' + seqNo + ' ' + length + ' ' +  msg

if __name__ == '__main__' :
    stat_ch = 0x05
    addr = 2
    seqNo = 1

    msg = input("MSG : ")
    capsule = frame(start_ch = stat_ch, addr = addr, seqNo = seqNo, msg = msg)
    print(capsule)