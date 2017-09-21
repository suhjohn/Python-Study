'''
내장 클래스 Exception을 상속받아 커스텀 예외를 만들 수 있다.

초기화 메서드에서 예외에서 처리할 데이터를 받고, print문으로 사용되고 싶다면 __str__메서드를 오버라이드 해준다.

'''

class CustomException(Exception):
    def __init__(self, data):
        self.data = data

    def __str__(self):
        print("This is the wrong type of data")
l = [1,2,3,4,5]
