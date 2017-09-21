from functools import reduce
def args_practice(*args):
    print(reduce(lambda x, y : x * y,  args))
    

args_practice(2, 3, 10)
args_practice(300)
