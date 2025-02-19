def divisible_by_3_and_4(n):
    for i in range(n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i

n = 50
divisible_numbers = divisible_by_3_and_4(n)

for number in divisible_numbers:
    print(number)