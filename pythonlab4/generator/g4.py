def squares(a, b):
    for i in range(a, b + 1):
        yield i ** 2

a = 3
b = 6
for square in squares(a, b):
    print(square)