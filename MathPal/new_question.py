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

def teach_homerow(biggest_number = 3):
    instruction = [
        '[L2] Left index',
        '[L3] Left middle',
        '[L4] Left ring',
        '[L5] Left pinky',
        '[R2] Right index',
        '[R3] Right middle',
        '[R4] Right ring',
        '[R5] Right pinky'
    ]
    problem = [
        'a',
        's',
        'd',
        'f',
        'j',
        'k',
        'l',
        ';',
    ]
    ix = [random.randint(0, len(problem)-1) for i in range(biggest_number)]
    problems = [f'{problem[i]}' for i in ix]
    instructions = [instruction[i] for i in ix]
    if biggest_number > 3:
        instructions = ''
    elif biggest_number > 1:
        instructions = [i.split(' ')[0] for i in instructions]
    return f"{''.join(problems)} = {''.join(problems)}", '\n'.join(instructions)
    