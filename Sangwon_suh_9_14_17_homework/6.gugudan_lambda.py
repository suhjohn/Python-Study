#6.람다함수와 리스트 컴프리헨션을 사용해 한 줄로 구구단의 결과를 갖는 리스트를 생성해본다.

def gugudan_lambda():
    return [(lambda x, y : x * y)(x, y) for x in range(2, 10) for y in range(1,10)]
