import csv

NUMBER_OF_ATTRIBUTES = 30
TARGET = NUMBER_OF_ATTRIBUTES
BENIGNE = 0.0

def read_training_data():
    with open('./data/normalized/cancer_train.csv', newline='') as training:
        entries = []
        rows = list(csv.reader(training, delimiter=' ', quotechar='|'))
        for row in rows[1:]:
            entry = row[0].split(',')
            entry = list(map(float, entry))
            entries.append(entry)
        return entries

entries = read_training_data()
for index in range(len(entries)):
    print(entries[index])
