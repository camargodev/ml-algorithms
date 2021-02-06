import csv
import sys

NUMBER_OF_ATTRIBUTES = 30
TARGET = NUMBER_OF_ATTRIBUTES
BENIGNE = 0.0
MALIGNE = 1.0

class evaluated_entry:
    def __init__(self, dist, target):
        self.dist = dist
        self.target = target

def read_csv(name):
    with open(name, newline='') as training:
        entries = []
        rows = list(csv.reader(training, delimiter=' ', quotechar='|'))
        for row in rows[1:]:
            entry = row[0].split(',')
            entry = list(map(float, entry))
            entries.append(entry)
        return entries

def read_training_data(prefix):
    return read_csv('./data/' + prefix + 'cancer_train.csv')

def read_test_data(prefix):
    return read_csv('./data/' + prefix + 'cancer_test.csv')

def distance(traning_entry, entry):
    sum_distance = 0
    for index in range(NUMBER_OF_ATTRIBUTES):
        dist = pow(traning_entry[index]-entry[index], 2)
        sum_distance += dist
    return sum_distance

def get_k_nearest(training_entries, entry, k):
    evaluated_entries = []
    for training_entry in training_entries:
        dist = distance(training_entry, entry)
        evaluated_entries.append(evaluated_entry(dist, training_entry[TARGET]))
    evaluated_entries.sort(key=lambda entry: entry.dist)
    return evaluated_entries[:k]

def get_result_value(nearest_k, k):
    sum_evaluations = 0
    for nearest in nearest_k:
        sum_evaluations += nearest.target
    avg_evaluations = sum_evaluations/k
    return MALIGNE if avg_evaluations > 0.5 else BENIGNE

def print_eval(exp, act):
    res = 'CORRECT' if exp == act else 'WRONG'
    print('EXP: ' + str(exp) + ' | ACT:  ' + str(act) + ' | ' + res)

def is_correct(exp, act):
    return exp == act

def get_prefix():
    use_normalized = int(sys.argv[1])
    return 'normalized/' if use_normalized == 1 else ''

def evaluate(k):
    prefix = get_prefix()
    training_data = read_training_data(prefix)
    testing_data = read_test_data(prefix)
    num_of_entries = len(testing_data)
    num_of_correct = 0
    for test_entry in testing_data:
        nearest_k = get_k_nearest(training_data, test_entry, k)
        result = get_result_value(nearest_k, k)
        if is_correct(test_entry[TARGET], result):
            num_of_correct += 1
    return num_of_correct/num_of_entries

K_VALUES = [1,3,5,7,9,11,13,15]
for k in K_VALUES:
    print(str(k) + ': ' + str(evaluate(k)))
