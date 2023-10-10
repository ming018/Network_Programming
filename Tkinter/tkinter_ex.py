from tkinter import *

root = Tk() # 객체 생성

root.title("opt window") # 타이틀 변경
root.geometry("300x200+300+300") # 크기 + 좌표 설정
root.resizable(False,False) # 창 크기 변경 가능 여부

label = Label(root, text = "Hello TKINTER") # label 생성

label.pack() # 레이블을 화면에 배치


#########


count = 0

def count_plus() :
    global count
    count += 1
    label.config(text = str(count))

def count_minus() :
    global count
    count -= 1
    label.config(text = str(count))

label = Label(root, text = count)
label.pack()

button1 = Button(root, width = 10, text = "증가", overrelief = "solid", command = count_plus)
# command 이벤트를 가지는 버튼 생성
button1.pack()


button2 = Button(root, width = 10, text = "감소", overrelief = "solid", command = count_minus)
button2.pack()

############################

# entry << 입력창
def calc(event) :
    label.config(text = "계산 결과 : " + str(eval(entry.get())))
    # eval() ()안의 값을 계산 하겠다?

label = Label(root, text = "0")
label.pack()

entry = Entry(root, width = 30) # Entry 생성
entry.bind("<Return>", calc) # Entry에 이벤트 할당, <Return>이랑 함수 이거 중요하다는데?
entry.pack()


root.mainloop() # 출력
