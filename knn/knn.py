import csv

NUMBER_OF_ATTRIBUTES = 30
TARGET = NUMBER_OF_ATTRIBUTES
BENIGNE = 0.0

class evaluated_entry:
    def __init__(self, dist, target):
        self.dist = dist
        self.target = target

def read_training_data():
    with open('./data/normalized/cancer_train.csv', newline='') as training:
        entries = []
        rows = list(csv.reader(training, delimiter=' ', quotechar='|'))
        for row in rows[1:]:
            entry = row[0].split(',')
            entry = list(map(float, entry))
            entries.append(entry)
        return entries

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

entries = read_training_data()
nearest_k = get_k_nearest(entries, entries[234], 3)
i = 0
for nearest in nearest_k:
    print(str(i) + ': ' + str(nearest.dist) + ' = ' + str(nearest.target))
    i += 1
