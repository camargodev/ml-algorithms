import datanb as nb

def match_all_criteria(instance, indexes, values):
    for i in range(len(indexes)):
        if instance[indexes[i]] != values[i]:
            return False
    return True

def calculate_prob_mult(indexes, values):
    count = 0
    num_vars = len(indexes)
    for instance in nb.data:
        if match_all_criteria(instance, indexes, values):
            count +=1
    return count / len(nb.data)

def calculate_prob(index, value):
    return calculate_prob_mult([index], [value])

def question_a():
    print("\nA. A priori, isto é, sem considerar os atributos de cada instância, é menos provável que uma nova instância seja da classe acc do que da classe unacc.")
    prob_acc = calculate_prob(nb.TARGET_INDEX, nb.ACCEPT)
    prob_unnac = calculate_prob(nb.TARGET_INDEX, nb.NOT_ACCEPT)
    print("  P(target=acc): " + str(prob_acc))
    print("  P(target=unacc): " + str(prob_unnac))
    result = "VERDADEIRO" if prob_acc < prob_unnac else "FALSO"
    print("  >> " + result)

def question_c():
    print("\nC. A probabilidade condicional do atributo lug_boot igual à 'med' é maior para a classe acc do que para a classe unacc.\n    Isto é, P(lug_boot=med|target=acc) > P(lug_boot=med|target=unacc).")
    print("  Considerando P(A|B) = P(A^B)/P(B), então: ")

    print("    P(lug_boot=med|target=acc) = P(lug_boot=med ^ target=acc) / P(target=acc)")
    prob_lug_med_and_acc = calculate_prob_mult([nb.LUG_INDEX, nb.TARGET_INDEX], [nb.LUG_MED, nb.ACCEPT])
    prob_acc = calculate_prob(nb.TARGET_INDEX, nb.ACCEPT)
    prob_acc_given_lug_med = prob_lug_med_and_acc / prob_acc
    print("      P(lug_boot=med|target=acc) = " + str(prob_lug_med_and_acc) + " / " + str(prob_acc))
    print("      P(lug_boot=med|target=acc) = " + str(prob_acc_given_lug_med))

    print("    P(lug_boot=med|target=unacc) = P(lug_boot=med ^ target=unacc) / P(target=unacc)")
    prob_lug_med_and_unacc = calculate_prob_mult([nb.LUG_INDEX, nb.TARGET_INDEX], [nb.LUG_MED, nb.NOT_ACCEPT])
    prob_unnac = calculate_prob(nb.TARGET_INDEX, nb.NOT_ACCEPT)
    prob_unacc_given_lug_med = prob_lug_med_and_unacc / prob_unnac
    print("      P(lug_boot=med|target=unacc) = " + str(prob_lug_med_and_unacc) + " / " + str(prob_unnac))
    print("      P(lug_boot=med|target=unacc) = " + str(prob_unacc_given_lug_med))

    result = "VERDADEIRO" if prob_acc_given_lug_med > prob_unacc_given_lug_med else "FALSO"
    print("  >> " + result)

def question_d():
    print("\nD. Nenhuma instância com o atributo safety = low seria predita como acc (aceitável) por este classificador pelo problema da probabilidade zero. Isto é, com base nestes dados de treinamento, P(safety=low|target=acc) = 0.")
    print("  Considerando P(A|B) = P(A^B)/P(B), então: ")

    print("    P(safety=low|target=acc) = P(safety=low ^ target=acc) / P(target=acc)")
    prob_safe_low_and_acc = calculate_prob_mult([nb.SAFE_INDEX, nb.TARGET_INDEX], [nb.SAFE_LOW, nb.ACCEPT])
    prob_acc = calculate_prob(nb.TARGET_INDEX, nb.ACCEPT)
    prob_acc_given_safe_low = prob_safe_low_and_acc / prob_acc
    print("      P(safety=low|target=acc) = " + str(prob_safe_low_and_acc) + " / " + str(prob_acc))
    print("      P(lsafety=low|target=acc) = " + str(prob_acc_given_safe_low))

    result = "VERDADEIRO" if prob_acc_given_safe_low == 0 else "FALSO"
    print("  >> " + result)


question_a()
question_c()
question_d()
