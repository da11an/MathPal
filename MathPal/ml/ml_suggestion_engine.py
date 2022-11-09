# objective function v1
# minimize incorrect answers
# minimize time to answer
# maximize number of math facts mastered

# objective function v2
# get user to 95%+ expected accuracy for math facts table
# keep missed answer rate below 10%

# objective function v3
# loss function is sum mastery rate of attempted math facts (e.g. total number of math facts - incorrect rate - not attempted)

# could give action option of providing a review problem including ans

from sklearn import linear_model
import pandas as pd

from MathPal.data import read_log
from MathPal.new_question import multiplication, addition, subtraction

# https://stackoverflow.com/questions/29055669/how-to-count-carries-in-multiplication
def count_addition_carries_rec(nums, answer=0, carries=0):

    dig_count = max(len(str(nums[0])), len(str(answer)))
    carries_list = [0]
    new_answer = ''
    # convert to string, apply left-padding, and reverse
    rnums = [str(x).zfill(dig_count)[::-1] for x in [nums[0], answer]]

    for i in range(dig_count):
        dig_sum = str(sum([int(num[i]) for num in rnums]) + carries_list[i])
        if i < dig_count - 1:
            new_answer = dig_sum[-1] + new_answer
            carries_list.append(int(dig_sum[:-1].zfill(1)))
        else:
            new_answer = dig_sum + new_answer

    carries_list = [car for car in carries_list if car != 0]

    if len(nums) == 1:
        # If this is the last number in the list, 
        # return the answer and the number of carries that 
        # occurred in the current as well as previous operations.
        return int(new_answer), carries + len(carries_list)
    else:
        # if there are more numbers in the list,
        # repeat the operation with a sublist, consisting of the next
        # number onwards, passing the current sum (new_answer) and 
        # the current count of carries 
        return count_addition_carries_rec(nums[1:],
                                          new_answer,
                                          carries + len(carries_list))

def count_multiplication_carries_rec(num1, num2, answer=0, carries=0):

    num1, num2 = str(num1), str(num2)

    # if num2 is smaller than num1, 
    # then reverse their assignments, and apply left-padding
    # to the smaller number. 

    if int(num2) < int(num1):
        num1, num2 = num2.zfill(len(num1)), num1
    else:
        num1, num2 = num1.zfill(len(num2)), num2

    carries_list = [0]
    new_answer = ''

    for i in range(len(num2)):
        dig_mul = str(int(num1[-1])*int(num2[len(num2) - i - 1]) + carries_list[i])
        if i < len(num2) - 1:
            new_answer = dig_mul[-1] + new_answer
            carries_list.append(int(dig_mul[:-1].zfill(1)))
        else:
            new_answer = dig_mul + new_answer

    new_answer += '0'*(len(num2)-len(str(int(num1))))
    carries_list = [car for car in carries_list if car != 0]

    if len(str(int(num1))) == 1:
        # If this is the last digit in num1,
        # then return the sum of the answer of the previous operation
        # and the answer of the current operation, counting
        # the addition carries in the process. 
        # Return the final answer as well as the count 
        # of multiplication and addition carries.
        return count_addition_carries_rec([int(answer), int(new_answer)],
                                          answer=0,
                                          carries=carries+len(carries_list))
    else:
        # If there are more digits in num1, repeat the operation
        # with num1 stripped of its last digit.
        return count_multiplication_carries_rec(num1[:-1],
                                                num2,
                                                *count_addition_carries_rec([int(answer), int(new_answer)],
                                                                            answer=0,
                                                                            carries=carries+len(carries_list)))

def mutate_carries(X, op):
    if op == '*':
        X['carries'] = X.apply(lambda x: count_multiplication_carries_rec(x['x1'], x['x2'])[1], axis=1)
    elif op == '+':
        X['carries'] = X.apply(lambda x: count_addition_carries_rec(x['x1'], x['x2'])[1], axis=1)
    elif op == '-':
        X['carries'] = X.apply(lambda x: count_addition_carries_rec(x['x2'], x['ans'])[1], axis=1)
    elif op == '/':
        X['carries'] = X.apply(lambda x: count_multiplication_carries_rec(x['x2'], x['ans'])[1], axis=1)
    return X

def XY_data(filename, player, op = '*'):
    '''
    Prepare data (and feature engineer, move to another function later)
    '''
    df = pd.DataFrame(read_log(filename)[player])
    try:
        df[['x1', 'op', 'x2', 'eq', 'ans']] = df['question'].str.split(' ', expand=True)
        df = df[df['op'] == op]
    except:
        return None
    Y = df[['correct', 'duration']]
    X = df[['session', 'x1', 'x2', 'ans']]
    X = mutate_carries(X, op)
    return X, Y

def evaluate_question(player, question = "1 + 1 = 2", session = 1, filename = 'data.json'):
    """
    Returns probability to correct answer and expected time to completion
    """
    if type(question) is not list:
        question = [question]
    assert type(session) == int
    session = [session for i in question]
    X_new = pd.DataFrame(list(zip(question, session)), columns = ['question', 'session'])
    X_new[['x1', 'op', 'x2', 'eq', 'ans']] = X_new['question'].str.split(' ', expand=True)
    op_new = X_new['op'].tolist()[0]
    X_new = mutate_carries(X_new, op_new)

    X, Y = XY_data(filename, player, op = op_new)
    if len(X) == 0:
        print('Keep playing to get questions that are just right.')
        flat = [1 for i in range(X_new['question'].count())]
        return flat, flat

    # reg = linear_model.LinearRegression() # this does okay
    # reg = linear_model.Ridge(alpha=0.5)   # this seems to do worse than linear
    reg = linear_model.MultiTaskElasticNet(alpha=1, l1_ratio = 0.5) # this seems better than ridge and linear
    reg.fit(X, Y)
    pred = reg.predict(X_new.loc[:, X.keys()])
    return pred[:,0].tolist(), pred[:,1].tolist()

def pick_question(n_problems, question_gen = multiplication, question_eval = evaluate_question, diff = 5, player = 'Dallan', session = 1, filename = 'data.json'):
    '''
    Desired difficulty on scale of 1-10
    '''
    target = 2.3 - diff/10
    biggest_number = min(diff**2, 1000)
    bank = []
    for a in range(1, biggest_number + 1):
        for b in range(1, biggest_number + 1):
            bank.append(question_gen(a, b))

    bank = list(set(bank))
    for i in range(n_problems - len(bank)):
        bank.append(question_gen(a, b))

    prob, dur = question_eval(player, bank, session, filename)
    dur = [max(i, 0.1) for i in dur]
    score_target = [abs(prob[i] + (1 - dur[i]/20) - target) for i in range(len(prob))]
    full_bank_sorted = pd.DataFrame(list(zip(bank, score_target, prob, dur)), columns = ['bank', 'target', 'prob', 'dur']).sort_values(by='target')
    bank_shuffled = full_bank_sorted[0:n_problems].sample(frac = 1)
    return bank_shuffled
        