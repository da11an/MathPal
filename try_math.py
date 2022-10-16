import random
import time
import json
import statistics


def login():
    player_log = read_log()
    player_list = list(player_log.keys())
    if type(player_list) != list:
        player_list = [player_list]
    player = let_user_pick(options = ["Add me, I'm new"] + player_list)
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
        print(f"Here's a quick review:")
        missed, slow = hard_problems(player, [session-3, session-2, session-1])
        {print(f'   {fact}') for fact in set(missed).union(slow)}
        print("")
        time.sleep(5)

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
        "Keep going!"
    ]
    wrong = [
        "Better luck next time!",
        "Don't give up!",
        "Keep going!",
        "You've got this",
        "Nice try",
        "Yarshiblah, keep trying",
        "Blouwers, blouwers, hasai, hasai, don't give up",
        "Gosh I feel so bad for you right now a-ho a-ho a-ho",
        "Stink, sigh, blouwers",
        "I smell something fishy, learn from failure",
        "You just dropped a stinker, keep working",
        "If you're never wrong, you're not learning"
    ]
    if answer:
        return random.choice(right)
    else:
        return random.choice(wrong)

def start_game():
    player, session = login()
    if not player:
        return None, 1
    subject = let_user_pick(options = ['addition', 'subtraction', 'multiplication'])
    n_problems = int_input('How many problems do you want to try: ')
    max_value = int_input("What's the biggest number you want to try: ")
    questions = []
    score_card = []
    time_card = []
    dates = []
    print(" --- Ready -------------")
    time.sleep(0.5)
    print(" --------- Set ---------")
    time.sleep(0.5)
    print(" --------------- Go! ---")
    time.sleep(0.5)
    spacer = '+---------------------------------------+'

    for i in range(n_problems):
        if subject == "addition":
            math_fact = addition(max_value)
        elif subject == "subtraction":
            math_fact = subtraction(max_value)
        else:
            math_fact = multiplication(max_value)

        question, solution = math_fact.split(" = ")

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
        else:
            print(f'Actually, {math_fact} {encouragement(identical)}')
            time.sleep(5)
        print("")

        log_result(
            player = player,
            question = math_fact,
            correct = identical,
            timestamp = time.time(),
            duration = duration,
            session = session
        )
    
    print(spacer)
    time.sleep(1)
    score = round(sum(score_card)/len(score_card) * 100)
    print(f'Fun Game! You got {sum(score_card)}/{len(score_card)} correct = {score}%')
    print(f'Your average answer time was {round(statistics.mean(time_card))} seconds')
    time.sleep(1)
    print("Facts to review:")
    missed, slow = hard_problems(player, session)
    {print(f'   {fact}') for fact in set(missed).union(slow)}
    print(spacer)
    print("")

    return(score)

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

def review():
    pass

def int_input(prompt = ""):
    inp = input(prompt)
    while not inp.isdigit():
        print("Wups! Please try a whole number.")
        inp = input(prompt)
    return int(inp)

def let_user_pick(options):
    print("Please choose:")

    for idx, element in enumerate(options):
        print("{}) {}".format(idx + 1, element))

    i = int_input("Enter number: ")
    try:
        if 0 < int(i) <= len(options):
            return options[int(i) - 1]
    except:
        pass
    return None

if __name__ == "__main__":
    start_game()