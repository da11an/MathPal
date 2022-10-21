import random
import time
import json
import statistics
import os

def login():
    player_log = read_log()
    player_list = list(player_log.keys())
    if type(player_list) != list:
        player_list = [player_list]

    clear_screen()
    print("WELCOME to MATH GAMES! Who are you?\n")
    player = let_user_pick(options = ["Add me, I'm new"] + player_list)

    clear_screen()
    if player == "Add me, I'm new":
        player = input("What's your name: ")
        if len(player) > 2:
            add_player(player)
            session = 1
        else:
            print("Please choose a name with at least 3 characters.")
            player = None
    else: # player stats!!!     
        print("")
        print(f'Welcome back {player}!')
        session = player_log[player]['session'][-1] + 1
        last_seen = duration_str(time.time() - player_log[player]['timestamp'][-1])
        print(f'It has been {last_seen} since you played.')
        print("")
        time.sleep(1)

    return player, session

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

# read JSON log
def read_log(filename='data.json'):
    with open(filename,'r+') as file:
        return json.load(file)
    
def add_player(player, filename='data.json'):
    print(f'Player {player} is being added')
    with open(filename,'r+') as file:
        file_data = json.load(file)
        file_data[player] = {
            "question": [],
            "correct": [],
            "timestamp": [],
            "duration": [],
            "session": []
        }
        file.seek(0)
        json.dump(file_data, file, indent = 4)

# function to add to JSON
def log_result(player, question, correct, timestamp, duration, session, filename='data.json'):
    with open(filename,'r+') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data[player]['question'].append(question)
        file_data[player]['correct'].append(correct)
        file_data[player]['timestamp'].append(timestamp)
        file_data[player]['duration'].append(duration)
        file_data[player]['session'].append(session)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4)
 
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

def ready_set_go():
    print(" --- Ready -------------")
    time.sleep(0.5)
    print(" --------- Set ---------")
    time.sleep(0.5)
    print(" --------------- Go! ---")
    time.sleep(0.5)

def start_game():
    player, session = login()
    if not player:
        return None, 1

    print(f"Here's a quick review:")
    missed, slow = hard_problems(player, [session-3, session-2, session-1])
    for fact in set(missed).union(slow):
        print(f'   {fact}')
        time.sleep(2)
    print("")
    print("Would you like to mix in review questions?")
    review = let_user_pick(options = ['Yes', 'No'])
    print("")
    print("What would you like to work on?")
    subject = let_user_pick(options = ['+', '-', '*'])
    n_problems = int_input('How many problems do you want to try: ')
    max_value = int_input("What's the biggest number you want to try: ")
    questions = []
    score_card = []
    time_card = []
    dates = []
    ready_set_go()
    if review == "Yes":
        missed, slow = hard_problems(player, [session-3, session-2, session-1])
        review_questions = list(set(missed).union(slow))

    for i in range(n_problems):
        if review == "Yes" and random.randint(0, 1):
            math_fact = random.choice(review_questions)
        elif subject == "+":
            math_fact = addition(max_value)
        elif subject == "-":
            math_fact = subtraction(max_value)
        else:
            math_fact = multiplication(max_value)

        question, solution = math_fact.split(" = ")

        clear_screen()
        start_time = time.time()
        answer = int_input(f'#{str(i+1).ljust(8)} {question} = ')
        duration = time.time() - start_time

        identical = answer == int(solution)

        dates.append(time.time())
        questions.append(math_fact)
        time_card.append(duration)
        score_card.append(identical)

        if identical:
            print(f'Correct! {encouragement(identical)}')
            time.sleep(2)
        else:
            print(f'Actually, {math_fact} {encouragement(identical)}')
            time.sleep(4)
            ready_set_go()
        print("")

        log_result(
            player = player,
            question = math_fact,
            correct = identical,
            timestamp = time.time(),
            duration = duration,
            session = session
        )
    
    clear_screen()
    time.sleep(1)
    score = round(sum(score_card)/len(score_card) * 100)
    print(f'Good Game! You got {sum(score_card)}/{len(score_card)} correct = {score}%')
    print(f'Your average answer time was {round(statistics.mean(time_card))} seconds')
    time.sleep(1)
    print("Facts to review:")
    missed, slow = hard_problems(player, session)
    for fact in set(missed).union(slow):
        print(f'   {fact}')
        time.sleep(2)
    print("")
    compile_stats(player, subject)
    return(score)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def hard_problems(player, session):
    if type(session) != list:
        session = [session]
    
    player_log = read_log()
    session_list = player_log[player]['session']
    window_ind = [i for i in range(len(session_list)) if session_list[i] in session]
    durations = [player_log[player]['duration'][i] for i in window_ind]
    questions = [player_log[player]['question'][i] for i in window_ind]
    corrects = [player_log[player]['correct'][i] for i in window_ind]
    missed = [questions[i] for i in range(len(questions)) if not corrects[i]]
    slow = [questions[i] for i in range(len(questions)) if (len(questions) > 1 and durations[i] > (statistics.mean(durations) + 1*statistics.stdev(durations)))]
    return missed, slow

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

def compile_stats(player, subject = "*"):
    dat = read_log()
    dat_player = dat[player]
    sub_mask = [q.split()[1] == "*" for q in dat_player['question']]
    question = [dat_player['question'][i] for i in range(len(dat_player['question'])) if sub_mask[i]]
    correct = [dat_player['correct'][i] for i in range(len(dat_player['question'])) if sub_mask[i]]
    duration = [dat_player['duration'][i] for i in range(len(dat_player['question'])) if sub_mask[i]]
    quest_split = [q.split()[0:3:2] for q in question]
    
    right = []
    wrong = []
    for i in range(len(correct)):
        if correct[i]:
            right.append(quest_split[i][0])
            right.append(quest_split[i][1])
        else:
            wrong.append(quest_split[i][0])
            wrong.append(quest_split[i][1])

    numbers = {int(i) for i in (set(right).union(set(wrong)))}

    for i in numbers:
        dur_mean = round(statistics.mean([duration[j] for j in range(len(question)) if str(i) in question[j]]), 1)
        score = int(round(100 * right.count(str(i))/(1e-15 + right.count(str(i)) + wrong.count(str(i)))))
        tries = (right.count(str(i)) + wrong.count(str(i)))
        print(f'[{str(i).rjust(2)} {subject} ?]: {str(score).rjust(3)}% /{tries} (t = {dur_mean} s)')


def int_input(prompt = ""):
    inp = input(prompt)
    while not inp.isdigit():
        print("Wups! Please try a whole number.")
        inp = input(prompt)
    return int(inp)

def let_user_pick(options):

    for idx, element in enumerate(options):
        print("{}) {}".format(idx + 1, element))

    i = int_input("Enter number of choice: ")
    try:
        if 0 < int(i) <= len(options):
            return options[int(i) - 1]
    except:
        pass
    return None

if __name__ == "__main__":
    start_game()