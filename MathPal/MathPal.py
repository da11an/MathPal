import random
import time
import json
import statistics
import os


DATA_PATH = os.path.join('MathPal', 'data.json')

def login():
    clear_screen()
    print("WELCOME to MATH GAMES! I'm Math Pal.\n\nWho are you?\n")
    
    player_log = read_log()
    player_list = list(player_log.keys())
    if type(player_list) != list:
        player_list = [player_list]

    player = let_user_pick(options = ["Add me, I'm new"] + player_list)

    clear_screen()
    if player == "Add me, I'm new":
        player = add_player_dialog()
        session = 1
    else: # player stats!!!     
        print("")
        print(f'Welcome back {player}!')
        if player_log[player]['session']:
            session = player_log[player]['session'][-1] + 1
            last_seen = duration_str(time.time() - player_log[player]['timestamp'][-1])
        else:
            session = 1
            last_seen = "forever"
        print(f'It has been {last_seen} since you played.')
        print("")
        time.sleep(1)

    return player, session

def add_player_dialog():
    player = input("What's your name: ")
    if len(player) > 2:
        add_player(player)
        session = 1
    else:
        print("Please choose a name with at least 3 characters.")
        player = add_player_dialog()
    return player

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
def read_log(filename=DATA_PATH):
    if not os.path.exists(DATA_PATH):
        fp = open(DATA_PATH, 'w')
        fp.write('{}')
        fp.close()
        #add_player_dialog()
    with open(filename,'r+') as file:
        return json.load(file)
    
def add_player(player, filename=DATA_PATH):
    print(f'Player {player} is being added')
    with open(filename,'r+') as file:
        file_data = json.load(file)
        if not file_data:
            file_data = {}
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
def log_result(player, question, correct, timestamp, duration, session, filename=DATA_PATH):
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
    print("What would you like to do?")
    make_report = let_user_pick(options = ['Play new game!', 'See report'])
    if make_report == 'See report':
        print("One what subject?")
        subject = let_user_pick(options = ['+', '-', '*'])
        recents = int_input("  How many of your latest sessions would you like to compare to your overall average?: ")
        compile_stats(player, subject, [*range(session-1, session-(1+recents), -1)])
        return ""
    print("")
    print(f"Here's a review of facts your learning:")
    missed, slow = hard_problems(player, [session-3, session-2, session-1])
    for fact in set(missed).union(slow):
        print(f'   {fact}')
        time.sleep(0.5)
    print("")
    print("Would you like to mix in review questions?")
    review = let_user_pick(options = ['Yes', 'No'])
    print("")
    print("What would you like to work on?")
    subject = let_user_pick(options = ['+', '-', '*'])
    n_problems = int_input('How many problems do you want to try: ')
    max_value = min(int_input("What's the biggest number you want to try: "), 99999)
    questions = []
    score_card = []
    time_card = []
    dates = []
    ready_set_go()
    if review == "Yes":
        missed, slow = hard_problems(player, [session-3, session-2, session-1])
        review_questions = list(set(missed).union(slow))

    for i in range(n_problems):
        if review == "Yes" and review_questions and random.randint(0, 1):
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
            time.sleep(1)
        else:
            print(f'Actually, {math_fact} {encouragement(identical)}')
            time.sleep(3)
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
    compile_stats(player, subject, session)
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

def tabulate_correct(quest_split, correct):
    right = []
    wrong = []
    for i in range(len(correct)):
        if correct[i]:
            right.append(quest_split[i][0])
            right.append(quest_split[i][1])
        else:
            wrong.append(quest_split[i][0])
            wrong.append(quest_split[i][1])
    return right, wrong

def compile_stats(player, subject = "*", session = []):
    if type(session) != list:
        session = [session]
    dat = read_log()
    #import pdb; pdb.set_trace()
    dat_player = dat[player]
    session_mask = [s in session for s in dat_player['session']]
    if session:
        dat_session = { k:[dat_player[k][i] for i in range(len(dat_player[k])) if session_mask[i]] for k in dat_player }
        sub_mask_s = [q.split()[1] == subject for q in dat_session['question']]
        question_s = [dat_session['question'][i] for i in range(len(dat_session['question'])) if sub_mask_s[i]]
        correct_s = [dat_session['correct'][i] for i in range(len(dat_session['question'])) if sub_mask_s[i]]
        duration_s = [dat_session['duration'][i] for i in range(len(dat_session['question'])) if sub_mask_s[i]]
        quest_split_s = [q.split()[0:3:2] for q in question_s]
        duration_mean_s = statistics.mean(duration_s)
        right_s, wrong_s = tabulate_correct(quest_split_s, correct_s)
    sub_mask = [q.split()[1] == subject for q in dat_player['question']]
    question = [dat_player['question'][i] for i in range(len(dat_player['question'])) if sub_mask[i]]
    correct = [dat_player['correct'][i] for i in range(len(dat_player['question'])) if sub_mask[i]]
    duration = [dat_player['duration'][i] for i in range(len(dat_player['question'])) if sub_mask[i]]
    quest_split = [q.split()[0:3:2] for q in question]
    if len(duration) < 2:
        print(question)
        return('Do more math to see your statistics!')
    duration_sd = statistics.stdev(duration)
    duration_mean = statistics.mean(duration)
    mid = "+"
    mark = "x"
    speed_sum_str = mid.ljust(11).rjust(21)
    speed_sum = round(10*(duration_mean - duration_mean_s) / duration_sd)
    speed_sum = min(max(speed_sum, -10), 10)
    speed_sum_str = list(speed_sum_str)
    speed_sum_str[speed_sum + 10] = mark
    speed_sum_str = "".join(speed_sum_str)
    right, wrong = tabulate_correct(quest_split, correct)
    numbers = {int(i) for i in (set(right).union(set(wrong)))}
    comp = round(len(right)/(len(right) + len(wrong))*100)
    w_rep = 71
    print('='*w_rep)
    print(f"STATISTICS for {player}; selected session = {session} ")
    print('='*w_rep)
    print(f' [{subject}]   ---- All Sessions --- | Selected Session | This ({mark}) vs <--All-->')
    print(f"Group: Cmp% right/total Time | right/total Time | < Slower  {mid}  Faster > ")
    print('-'*w_rep)
    for i in numbers:
        dur_list = [duration[j] for j in range(len(question)) if str(i) in quest_split[j]]
        dur_mean = statistics.mean(dur_list)
        speed = round(10*(duration_mean - dur_mean) / duration_sd)
        speed = min(max(speed, -10), 10)
        if speed < 0:
            speed_str = ("<".ljust(-speed, '-') + "+".ljust(11)).rjust(21)
        else:
            speed_str = ("+".rjust(11) + ">".rjust(speed, '-')).ljust(21)
        dur_list_s = [duration_s[j] for j in range(len(question_s)) if str(i) in quest_split_s[j]]
        if dur_list_s:
            dur_mean_s = statistics.mean(dur_list_s)
            dur_mean_s_str = str(round(dur_mean_s,1)).rjust(4)
            speed_s = round(10*(duration_mean - dur_mean_s) / duration_sd)
            speed_s = min(max(speed_s, -10), 10)
            speed_str = list(speed_str)
            speed_str[speed_s + 10] = mark
            speed_str = "".join(speed_str)
        else:
            dur_mean_s_str = "".ljust(4)
        score = int(round(100 * right.count(str(i))/(1e-15 + right.count(str(i)) + wrong.count(str(i)))))
        rightcount = right.count(str(i))
        tries = (rightcount + wrong.count(str(i)))
        rightcount_s = right_s.count(str(i))
        tries_s = (rightcount_s + wrong_s.count(str(i)))
        print(f'{str(i).rjust(5)}: {str(score).rjust(3)}% {str(rightcount).rjust(5)}/{str(tries).ljust(5)} {str(round(dur_mean,1)).rjust(4)} | {str(rightcount_s).rjust(5)}/{str(tries_s).ljust(5)} {dur_mean_s_str} | {speed_str}')
    print('-'*w_rep)
    print(f"Total: {str(comp).rjust(3)}% {str(len(right)).rjust(5)}/{str(len(right)+len(wrong)).ljust(5)} {str(round(duration_mean,1)).rjust(4)} | {str(len(right_s)).rjust(5)}/{str(len(right_s)+len(wrong_s)).ljust(5)} {str(round(duration_mean_s,1)).rjust(4)} | {speed_sum_str}")
    print('='*w_rep + '\n')


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

def main():
    start_game()

if __name__ == "__main__":
    main()
