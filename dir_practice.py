print(dir())
print(__annotations__)
print(__builtins__)
print(__cached__)
print(__doc__)
print(__file__)
print(__loader__)
print(__name__)
print(__spec__)


x = 100

print("-------------------------------------\n",
        dir())
print(__annotations__)
print(__builtins__)
print(__cached__)
print(__doc__)
print(__file__)
print(__loader__)
print(__name__)
print(__spec__)
              
print("x=100 dir : {}".format(dir(x)))

x = "George"

print("------------------------------------\n",
        dir())
print("x=\"George\" dir : {}".format(dir(x)))
