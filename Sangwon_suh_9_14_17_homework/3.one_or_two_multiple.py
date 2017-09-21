#3.한 개 또는 두 개의 숫자 인자를 전달받아, 하나가 오면 제곱, 두개를 받으면 두 수의 곱을 반환해주는 함수를 정의하고 사용해본다.

def one_or_two_multiple(*args):
	if len(args) == 1:
		return args[0] * args[0]
	elif len(args) == 2:
		return args[0] * args[1]

one_or_two_multiple(3, 4)
one_or_two_multiple(7)
