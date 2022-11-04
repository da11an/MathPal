import random
import time
import json
import statistics
import os

from .ui_cmd.login import login
from .data import read_log, log_result, hard_problems, compile_stats
from .new_question import addition, subtraction, multiplication, teach_homerow
from .ui_cmd.utils import let_user_pick, int_input, clear_screen, ready_set_go, encouragement

DATA_PATH = os.path.join('MathPal', 'data.json')

def main():
    player, session = login(DATA_PATH)
    if not player:
        return None, 1
    print("What would you like to do?")
    make_report = let_user_pick(options = ['Play new game!', 'See report'])
    if make_report == 'See report':
        print("One what subject?")
        subject = let_user_pick(options = ['+', '-', '*', 'typing: homerow'])
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
    subject = let_user_pick(options = ['+', '-', '*', 'typing: homerow'])
    n_problems = int_input('How many problems do you want to try: ')
    max_value = min(int_input("What's the biggest number you want to try: "), 99999)
    questions = []
    score_card = []
    time_card = []
    dates = []
    ready_set_go()
    if review == "Yes":
        missed, slow = hard_problems(player, [session-3, session-2, session-1], DATA_PATH)
        review_questions = list(set(missed).union(slow))

    for i in range(n_problems):
        hint = ''
        if review == "Yes" and review_questions and random.randint(0, 1):
            math_fact = random.choice(review_questions)
        elif subject == "+":
            math_fact = addition(max_value)
        elif subject == "-":
            math_fact = subtraction(max_value)
        elif subject == "*":
            math_fact = multiplication(max_value)
        elif subject == "typing: homerow":
            math_fact, hint = teach_homerow(max_value)

        question, solution = math_fact.split(" = ")
        clear_screen()
        start_time = time.time()
        if solution.isdigit():
            answer = int_input(f'#{str(i+1).ljust(8)} {question} = ')
        else:
            if hint:
                print(f'Hint:\n\n{hint}\n')
            answer = input(f'#{str(i+1).ljust(8)} {question}\n {"".ljust(8)} ')
        duration = time.time() - start_time

        if solution.isdigit():
            identical = answer == int(solution)
        else:
            identical = answer == solution

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
