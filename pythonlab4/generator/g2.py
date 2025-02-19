def even_number_generator(n):
    for i in range(n + 1):
        if i % 2 == 0:
            yield i

n = int(input("Enter a number (n): "))

even_numbers = even_number_generator(n)

result = ",".join(map(str, even_numbers))

print(result)