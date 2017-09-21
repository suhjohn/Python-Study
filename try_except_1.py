li = [1,2,3,4,5,6,7,8]

loop = 0
while True:
    msg = "숫자입력:" if not loop else "다시 입력하세요"
    loop = 1
    try:
        num = int(input('input a number'))
        li[num]
    except IndexError:
        print("not a valid index")
    else:
        print(li[num])
        break
