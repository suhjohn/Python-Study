# 2.1번에서 작성한 함수에 docstring을 작성하여 함수에 대한 설명을 달아보고, help(함수명)으로 해당 설명을 출력해본다.

def fruits(s):
	
	"""
	문자열이 red면 apple을 리턴
	문자열이 yellow면 banana를 리턴
	문자열이 green이면 melon을 리턴
	그 외의 문자열이면 I don\'t know를 리턴
	"""

	if s == "red":
		return "apple"

	elif s == "yellow":
		return "banana"

	elif s == "green":
		return "melon"

	else:
		return "I don't know"

help(fruits)
print(fruits("red"))
print(fruits("yellow"))
print(fruits("green"))
print(fruits("blue"))

