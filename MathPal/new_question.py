import random

def multiplication(biggest_number = 12):
    a = random.randint(1, biggest_number)
    b = random.randint(1, biggest_number)
    return f'{a} * {b} = {a*b}'

def addition(biggest_number = 12):
    a = random.randint(1, biggest_number)
    b = random.randint(1, biggest_number)
    return f'{a} + {b} = {a+b}'

def subtraction(biggest_number = 12):
    a = random.randint(1, biggest_number)
    b = random.randint(1, biggest_number)
    if b > a:
        a, b = b, a
    return f'{a} - {b} = {a-b}'
