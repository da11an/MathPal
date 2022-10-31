import os
import time
import random

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def int_input(prompt = ""):
    inp = input(prompt)
    while not inp.isdigit():
        print("Wups! Please try a whole number.")
        inp = input(prompt)
    return int(inp)

def let_user_pick(options):

    for idx, element in enumerate(options):
        print("    {}) {}".format(idx + 1, element))

    i = int_input("  Enter number of choice: ")
    try:
        if 0 < int(i) <= len(options):
            return options[int(i) - 1]
    except:
        pass
    return None
 
def duration_str(duration):
    duration = round(duration)
    if duration < 60:
        return  f'{int(duration)} seconds'
    elif duration < 3600:
        seconds = duration % 60
        minutes = (duration - seconds)/60
        return f'{int(minutes)} minutes and {int(seconds)} seconds'
    elif duration < 3600*24:
        dur_min = round(duration/60)
        minutes = dur_min % 60
        hours = (dur_min - minutes)/60
        return f'{int(hours)} hours and {int(minutes)} minutes'
    else:
        dur_hr = round(duration/3600)
        hours = dur_hr % 24
        days = (dur_hr - hours)/24
        return f'{int(days)} days and {int(hours)} hours'

def ready_set_go():
    print(" --- Ready -------------")
    time.sleep(0.5)
    print(" --------- Set ---------")
    time.sleep(0.5)
    print(" --------------- Go! ---")
    time.sleep(0.5)

def encouragement(answer = True):
    right = [
        "Good job!",
        "You're a rock star!",
        "Fantastic!",
        "Keep going!",
        "Perfect!",
        "Right on!",
        "Splendid!",
        "Success is not final."
	   "You are the bom diggity!"        
    ]
    wrong = [
        "Better luck next time!",
        "Don't give up!",
        "Keep going!",
        "You've got this!",
        "Nice try!",
        "Yarshiblah, keep trying!",
        "Blouwers, blouwers, hasai, hasai, don't give up!",
        "Gosh I feel so bad for you right now. A-ho a-ho a-ho!",
        "Stink, sigh, blouwers",
        "I smell something fishy, learn from failure",
        "You just dropped a stinker, keep working",
        "If you're never wrong, you're not learning",
        "Failure is not fatal",
        "It is courage to continue that counts.",
        "I can accept failure",
        "That's incorrect, but Grandpa loves you",
        "Everyone fails at something",
        "I can't accept not trying",
        "Failure is the key to success",
        "Each mistake teaches us something",
        "Dare to fail greatly",
        "Don't fear failure",
        "Fear not trying",
        "Winners are not afraid of losing.",
        "Failure is part of success.",
        ""
    ]
    if answer:
        return random.choice(right)
    else:
        return random.choice(wrong)

