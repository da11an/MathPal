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

    df = pd.DataFrame(read_log(filename)[player]) 
    df[['x1', 'op', 'x2', 'eq', 'ans']] = df['question'].str.split(' ', expand=True)
    df = df[df['op'] == op_new]
    if len(df) == 0:
        #return 2/(X_new[['x1']] + X_new[['x2']]), 10
        return 0.5, 10

    reg = linear_model.LinearRegression()
    Y = df[['correct', 'duration']]
    X = df[['session', 'x1', 'x2']]
    reg.fit(X, Y)
    pred = reg.predict(X_new[['session', 'x1', 'x2']])
    return pred[:,0].tolist(), pred[:,1].tolist()

def pick_question(n_problems, biggest_number = 12, question_gen = multiplication, question_eval = evaluate_question, diff = 'easy', player = 'Dallan', session = 1, filename = 'data.json'):
    if diff == 'easy':
        target = 1.5 + 1
    elif diff == 'moderate':
        target = 1 + 0.9
    elif diff == 'hard':
        target = 0.7 + 0.7
    bank = []
    biggest_number = max(biggest_number, 1000)
    for a in range(1, biggest_number):
        for b in range(1, biggest_number):
            bank.append(question_gen(a, b))

    bank = list(set(bank))
    prob, dur = question_eval(player, bank, session, filename)
    dur = [max(i, 0.1) for i in dur]
    prob_target = [abs(prob[i] + (1 - dur[i]/20) - target) for i in range(len(prob))]
    bank_sorted = pd.DataFrame(list(zip(bank, prob_target, prob, dur)), columns = ['bank', 'target', 'prob', 'dur']).sort_values(by='target')
    return bank_sorted[0:n_problems]
        