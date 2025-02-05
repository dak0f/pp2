import math 

#Task 1 
x = float(input("enter the gram : "))
def conv(gram):
    ounces = 28.3495231 * gram
    print(ounces) 
    return ounces
conv(x)

#Task 2
    
y = float(input("enter the F : "))
def degree(F):
    C = (F - 32)*(5 / 9) 
    print(C )
    return C 
degree(y)

#Task 3 

def solve(numheads, numlegs):
    for chickens in range(numheads + 1):
        rabbits = numheads - chickens  
        if (2 * chickens + 4 * rabbits) == numlegs:  
            return chickens, rabbits
    return "No solution"  

numheads = 35
numlegs = 94
result = solve(numheads, numlegs)
print(f"Chickens: {result[0]}, Rabbits: {result[1]}")

#Task 4 

list = [1 , 2 , 3 , 4]
def filter(s):
    for i in s:
        if i%2==0:
            print(i)
            print(" ")
filter(list)

#Task 5 
from itertools import permutations

def permutations(x):
    perms = [''.join(p) for p in permutations(x)]
    for perm in perms:
        print(perm)

l = input("Enter a string: ")
permutations(l)

#Task 6 
def reverse(sentence):
    words = sentence.split()
    rewords = words[::-1]
    reversed = ' '.join(rewords)

    return reversed

v = input("Enter a sentence: ")
result = reverse(v)
print(result)

#Task 7
def has3(nums):
    for i in range(len(nums) - 1):
        if nums[i] == 3 and nums[i + 1] == 3:
            return True
    return False

numbers = [1, 3, 3, 4, 5]
result = has3(numbers)
print(result)

#Task 8
def spy_game(nums):
    sequence = [0, 0, 7]
    index = 0
    for num in nums:
        if num == sequence[index]:
            if index == len(sequence):
                return True
    return False

print(spy_game([1, 2, 4, 0, 0, 7, 5]))  # True

#Task 9 
import math

def volume(radius):
    return (4/3) * math.pi * (radius ** 3)

radius = float(input("Enter the radius of the sphere: "))
print("Volume of the sphere:",volume(radius))

#Task 10 

def unique(l):
    unique_list = []
    for item in l:
        if item not in unique_list:
            unique_list.append(item)
    return unique_list

input_list = [1, 2, 2, 3, 4, 4, 5]
print("Unique elements:", unique(input_list))

#Task 11 

def palindrome(s):
    s = s.replace(" ", "").lower()
    return s == s[::-1]

word = input("Enter a word or phrase: ")
if palindrome(word):
    print("It's a palindrome!")
else:
    print("It's not a palindrome.")

#Task 12 

def histogram(numbers):
    for num in numbers:
        print('*' * num)

histogram([4, 9, 7])

#Task 13 

import random

def guess_the_number():
    print("Hello! What is your name?")
    name = input()

    print(f"Well, {name}, I am thinking of a number between 1 and 20.")
    number_to_guess = random.randint(1, 20)
    guesses_taken = 0

    while True:
        print("Take a guess.")
        guess = int(input())
        guesses_taken += 1

        if guess < number_to_guess:
            print("Your guess is too low.")
        elif guess > number_to_guess:
            print("Your guess is too high.")
        else:
            print(f"Good job, {name}! You guessed my number in {guesses_taken} guesses!")
            break

guess_the_number()

#Task 14