def inner(x):
    x += 3
    return x

f1 = inner(10)
inner(f1)
inner(f1)
print(f1)
