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
    try:
        df[['x1', 'op', 'x2', 'eq', 'ans']] = df['question'].str.split(' ', expand=True)
        df = df[df['op'] == op_new]
    except:
        print('Keep playing to get questions that are just right.')
        flat = [1 for i in range(X_new['question'].count())]
        return flat, flat

    # reg = linear_model.LinearRegression() # this does okay
    # reg = linear_model.Ridge(alpha=0.5)   # this seems to do worse than linear
    reg = linear_model.MultiTaskElasticNet(alpha=0.1) # this seems better than ridge and linear
    Y = df[['correct', 'duration']]
    X = df[['session', 'x1', 'x2']]
    reg.fit(X, Y)
    pred = reg.predict(X_new[['session', 'x1', 'x2']])
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
        