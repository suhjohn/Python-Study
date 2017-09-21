def print_string(string):
    print(string)
    print(type(string))

def print_int(n):
    print(n)
    print(type(n))

def print_arg_type(func):
    def return_function(*args):
        for arg in args:
            print('%s type: %s' %(arg, type(arg))
        return func(*args)
    return return_function
