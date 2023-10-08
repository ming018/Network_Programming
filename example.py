# *
# **
# ***
# ****
# *****

# N이라는 길이를 입력받고, N에 따라 규칙에 맞게 가변하는 프로그램을 짜십쇼

size = int(input("원하는 길이 : "))


for i in range(size) :
    for k in range(i + 1) :
        print('*', end = '')
    print()