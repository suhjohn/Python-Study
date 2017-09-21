#5.위치인자 묶음을 매개변수로 가지며, 위치인자가 몇 개 전달되었는지를 print하고 개수를 리턴해주는 함수를 정의하고 사용해본다.

def how_many_positional_args(*args):
	print(len(args))
	return len(args)

how_many_positional_args(3,4,5,6,7)