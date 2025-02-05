import math

# Task 1
class handler:
    def __init__(self):
        self.s = ""
    
    def getstring(self):
        self.s = input("Enter a string: ")
    
    def printString(self):
        print(self.s.upper())

# Task 2
class shape:
    def area(self):
        return 0

class Square(shape):
    def __init__(self, length):
        self.length = length
    
    def area(self):
        return self.length ** 2

# Task 3
class Rectangle(shape):
    def __init__(self, length, width):
        self.length = length
        self.width = width
    
    def area(self):
        return self.length * self.width

# Task 4
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def show(self):
        print(f"Point({self.x}, {self.y})")
    
    def move(self, new_x, new_y):
        self.x = new_x
        self.y = new_y
    
    def dist(self, other_point):
        return math.sqrt((self.x - other_point.x) ** 2 + (self.y - other_point.y) ** 2)

# Task 5
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance
    
    def deposit(self, amount):
        self.balance += amount
        print(f"Deposited {amount}. New balance: {self.balance}")
    
    def withdraw(self, amount):
        if amount > self.balance:
            print("Insufficient funds")
        else:
            self.balance -= amount
            print(f"Withdrawn {amount}. New balance: {self.balance}")
