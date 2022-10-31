import os
import json
import statistics

# read JSON log

def read_log(filename):
    if not os.path.exists(filename):
        fp = open(filename, 'w')
        fp.write('{}')
        fp.close()
        #add_player_dialog()
    with open(filename,'r+') as file:
        return json.load(file)

def add_player(player, filename):
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
def log_result(player, question, correct, timestamp, duration, session, filename):
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
 
# what was hard 
def hard_problems(player, session, filename):
    if type(session) != list:
        session = [session]
    
    player_log = read_log(filename)
    session_list = player_log[player]['session']
    window_ind = [i for i in range(len(session_list)) if session_list[i] in session]
    durations = [player_log[player]['duration'][i] for i in window_ind]
    questions = [player_log[player]['question'][i] for i in window_ind]
    corrects = [player_log[player]['correct'][i] for i in window_ind]
    missed = [questions[i] for i in range(len(questions)) if not corrects[i]]
    slow = [questions[i] for i in range(len(questions)) if (len(questions) > 1 and durations[i] > (statistics.mean(durations) + 1*statistics.stdev(durations)))]
    return missed, slow

def compile_stats(player, subject = "*", session = [], filename = 'data.json'):
    if type(session) != list:
        session = [session]
    dat = read_log(filename)
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

