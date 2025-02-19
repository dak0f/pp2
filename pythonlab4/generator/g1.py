def square_generator(N):
    for i in range(1, N + 1):
        yield i ** 2

N = 5
squares = square_generator(N)

for square in squares:
    print(square)