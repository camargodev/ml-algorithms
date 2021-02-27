import datanb as nb

def calculate_prob(index, value):
    count = 0
    for instance in nb.data:
        if instance[index] == value:
            count +=1
    return count / len(nb.data)

def question_a():
    print("a. A priori, isto é, sem considerar os atributos de cada instância, é menos provável que uma nova instância seja da classe acc do que da classe unacc.")
    prob_acc = calculate_prob(nb.TARGET_INDEX, nb.ACCEPT)
    prob_unnac = calculate_prob(nb.TARGET_INDEX, nb.NOT_ACCEPT)
    print("  Probabilidade ACC: " + str(prob_acc))
    print("  Probabilidade UNACC: " + str(prob_unnac))
    result = "VERDADEIRO" if prob_acc < prob_unnac else "FALSO"
    print("  >> " + result)

question_a()
