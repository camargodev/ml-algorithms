import graphviz 
import csv

from sklearn import tree
from sklearn.model_selection import train_test_split

from pandas import DataFrame
from pandas import read_csv

ENTROPY = "entropy"
GINI = "gini"
TEST_SIZE = 0.2

class AcuracyResults:
  def __init__(self, avg, maxi, mini):
    self.tree = tree
    self.avg = avg
    self.maxi = maxi
    self.mini = mini

class DecisionTreeResult:
  def __init__(self, tree, acuracy, features, classes):
    self.tree = tree
    self.acuracy = acuracy
    self.features = features
    self.classes = classes

class SimpleTrainer:
    def train(self, criterion, features, target, min_samples_leaf, max_depth):
        decision_tree = tree.DecisionTreeClassifier(criterion=criterion)
        return decision_tree.fit(features, target)

class MinLeafsMaxDepthTrainer:
    def train(self, criterion, features, target, min_samples_leaf, max_depth):
        decision_tree = tree.DecisionTreeClassifier(criterion=criterion, min_samples_leaf=min_samples_leaf, max_depth=max_depth)
        return decision_tree.fit(features, target)

def read_training_data():
    return read_csv('data/vote.tsv', sep='\t', header=0)

def holdout(training_data):
    training_data_frame =  DataFrame(training_data)
    features = training_data_frame.drop("target", axis=1)
    target = training_data_frame["target"]
    return train_test_split(features, target, test_size=TEST_SIZE)

def export_output(name, result):
    dot_data = tree.export_graphviz(result.tree, out_file=None, 
                        feature_names=result.features,
                        class_names=result.classes,
                        filled=True, rounded=True, special_characters=True)  
    graph = graphviz.Source(dot_data)  
    graph.render(name) 

def get_features_names(features):
    return features.columns

def get_class_names(target):
    return list(dict.fromkeys(target.values))

def calculate_acuracy(decision_tree, features, targets):
    predictions = decision_tree.predict(features)
    targets = targets.values.tolist()
    correct = 0
    for i in range(len(predictions)):
        if predictions[i] == targets[i]:
            correct += 1
    return correct/len(predictions)

def compare_entropy_and_gini(training_data):
    entropy = execute(ENTROPY, training_data, SimpleTrainer())
    print("AVG With Entropy: " + str(entropy.acuracy.avg))
    print("MIN With Entropy: " + str(entropy.acuracy.mini))
    print("MAX With Entropy: " + str(entropy.acuracy.maxi))

    gini = execute(GINI, training_data, SimpleTrainer())
    print("AVG With Gini: " + str(gini.acuracy.avg))
    print("MIN With Gini: " + str(gini.acuracy.mini))
    print("MAX With Gini: " + str(gini.acuracy.maxi))

    export_output("generated/ex1entropy", entropy)
    export_output("generated/ex1gini", gini)

def execute(criterion, training_data, trainer, number_of_repetitions=100, min_samples_leaf=None, max_depth=None):
    total_acuracy = 0
    min_val, max_val = 1000, 0
    for _ in range(number_of_repetitions):
        train_features, test_features, train_target, test_target = holdout(training_data)
        decision_tree = trainer.train(criterion, train_features, train_target, min_samples_leaf, max_depth)
        acuracy = calculate_acuracy(decision_tree, test_features, test_target)
        total_acuracy += acuracy
        min_val = min(min_val, acuracy)
        max_val = max(max_val, acuracy)
    avg_acuracy = total_acuracy/number_of_repetitions
    acuracy = AcuracyResults(avg_acuracy, max_val, min_val)
    features_names = get_features_names(train_features)
    class_names = get_class_names(train_target)
    return DecisionTreeResult(decision_tree, acuracy, features_names, class_names)

def compare_versions_max_depth_min_samples_leaf(training_data):
    max_depths = [5, 7, 10]
    min_samples_leafs = [1, 5, 25, 50]
    for max_depth in max_depths:
        for min_samples_leaf in min_samples_leafs:
            entropy = execute(ENTROPY, training_data, MinLeafsMaxDepthTrainer(), min_samples_leaf=min_samples_leaf, max_depth=max_depth)
            name = "md-" +str(max_depth) + "--msl-" + str(min_samples_leaf)
            print("\nAVG With " + name + ": " + str(entropy.acuracy.avg))
            export_output("generated/" + name, entropy)



training_data = read_training_data()

# Exercise 1
# compare_entropy_and_gini(training_data)

# Exercise 2
compare_versions_max_depth_min_samples_leaf(training_data)
