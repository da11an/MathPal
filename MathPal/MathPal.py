import random
import time
import json
import statistics
import os

from .ui_cmd.login import login
from .data import read_log, log_result, hard_problems, compile_stats
from .new_question import addition, subtraction, multiplication, random_pair
from .ui_cmd.utils import let_user_pick, int_input, clear_screen, ready_set_go, encouragement
from .ml.ml_suggestion_engine import pick_question, evaluate_question

DATA_PATH = os.path.join('MathPal', 'data.json')

def main():
    player, session = login(DATA_PATH)
    if not player:
        return None, 1
    print("What would you like to do?")
    make_report = let_user_pick(options = ['Play new game!', 'See report'])
    if make_report == 'See report':
        print("One what subject?")
        subject = let_user_pick(options = ['+', '-', '*'])
        recents = int_input("  How many of your latest sessions would you like to compare to your overall average?: ")
        compile_stats(player, subject, [*range(session-1, session-(1+recents), -1)], DATA_PATH)
        return ""
    print("")
    print(f"Here's a review of facts your learning:")
    missed, slow = hard_problems(player, [session-3, session-2, session-1], DATA_PATH)
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
    print("How do you want me to pick your problems:")
    question_type = let_user_pick(options = ['random', 'easy', 'moderate', 'hard'])
    questions = []
    score_card = []
    time_card = []
    dates = []
    ready_set_go()
    if review == "Yes":
        missed, slow = hard_problems(player, [session-3, session-2, session-1], DATA_PATH)
        review_questions = list(set(missed).union(slow))
    question_map = {'+':addition, '-':subtraction, '*':multiplication}
    if question_type == "random":
        bank = []
        for i in range(n_problems):
            a, b = random_pair(max_value)
            if review == "Yes" and review_questions and random.randint(0, 1):
                bank.append(random.choice(review_questions))
            elif subject == "+":
                bank.append(addition(a, b))
            elif subject == "-":
                bank.append(subtraction(a, b))
            else:
                bank.append(multiplication(a, b))
    else:
        bank = pick_question(
            n_problems, 
            max_value, 
            question_gen = multiplication, 
            question_eval = evaluate_question, 
            diff = question_type, 
            player = player, 
            session = session, 
            filename = DATA_PATH)['bank'].tolist()
        print(bank)

    for i in range(n_problems):
        math_fact = bank[i]
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
            session = session,
            filename = DATA_PATH
        )
    
    clear_screen()
    time.sleep(1)
    score = round(sum(score_card)/len(score_card) * 100)
    print(f'Good Game! You got {sum(score_card)}/{len(score_card)} correct = {score}%')
    print(f'Your average answer time was {round(statistics.mean(time_card))} seconds')
    time.sleep(1)
    print("Facts to review:")
    missed, slow = hard_problems(player, session, DATA_PATH)
    for fact in set(missed).union(slow):
        print(f'   {fact}')
        time.sleep(2)
    print("")
    compile_stats(player, subject, session, DATA_PATH)
    return(score)


if __name__ == "__main__":
    main()
