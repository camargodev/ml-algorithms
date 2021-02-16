import graphviz 
import csv

from sklearn import tree
from sklearn.model_selection import train_test_split

from pandas import DataFrame
from pandas import read_csv

ENTROPY = "entropy"
GINI = "gini"
TEST_SIZE = 0.2
SEED = 1405

def read_training_data():
    return read_csv('data/vote.tsv', sep='\t', header=0)

def holdout(training_data):
    training_data_frame =  DataFrame(training_data)
    features = training_data_frame.drop("target", axis=1)
    target = training_data_frame["target"]
    return train_test_split(features, target, test_size=TEST_SIZE, random_state=SEED)

def train(criterion, features, target):
    decision_tree = tree.DecisionTreeClassifier(criterion=criterion)
    return decision_tree.fit(features, target)

def train_with_entropy(features, target):
    return train(ENTROPY, features, target)

def train_with_gini(features, target):
    return train(GINI, features, target)


def export_output(name, decision_tree, features, target):
    dot_data = tree.export_graphviz(decision_tree, out_file=None, 
                        feature_names=features.columns,
                        class_names=list(dict.fromkeys(target.values)),
                        filled=True, rounded=True, special_characters=True)  
    graph = graphviz.Source(dot_data)  
    graph.render(name) 

training_data = read_training_data()
train_features, test_features, train_target, test_target = holdout(training_data)
decision_tree = train_with_entropy(train_features, train_target)
export_output("entropy", decision_tree, train_features, train_target)