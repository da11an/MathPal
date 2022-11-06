import random

def random_pair(biggest_number = 12):
    a = random.randint(1, biggest_number)
    b = random.randint(1, biggest_number)
    return a, b

def multiplication(a, b):
    return f'{a} * {b} = {a*b}'

def addition(a, b):
    return f'{a} + {b} = {a+b}'

def subtraction(a, b):
    if b > a:
        a, b = b, a
    return f'{a} - {b} = {a-b}'
