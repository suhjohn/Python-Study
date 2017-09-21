#리스트 컴프리헨션을 사용하여 구구단 결과를 갖는 리스트를 만들고, 해당 리스트를 for문을 사용해 구구단 형태로 나오도록 출력해본다.

#각 단마다 한 번 더 줄바꿈을 넣어준다.

li = [n for n in range(1, 100) if (n<10 and n % 3 == 0) or (n > 10 and int(str(n)[1]) % 3 == 0)]        
for e in li:
    print(e, end="\n")

