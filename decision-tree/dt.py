import graphviz 
from sklearn.datasets import load_iris
from sklearn import tree

ENTROPY = "entropy"
GINI = "gini"

def read_training_data():
    return load_iris(return_X_y=True)

def train(criterion, parameters, classes):
    decision_tree = tree.DecisionTreeClassifier(criterion=criterion)
    return decision_tree.fit(parameters, classes)

def train_with_entropy(parameters, classes):
    return train(ENTROPY, parameters, classes)

def train_with_gini(parameters, classes):
    return train(GINI, parameters, classes)
    
def export_output(name, decision_tree):
    dot_data = tree.export_graphviz(decision_tree, out_file=None, 
                        filled=True, rounded=True,  
                        special_characters=True)  
    graph = graphviz.Source(dot_data)  
    graph.render(name) 


parameters, classes = read_training_data()
decision_tree = train_with_entropy(parameters, classes)
export_output("test", decision_tree)