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

def calculate_prob_all(values):
    return calculate_prob_mult([nb.PRICE_INDEX, nb.LUG_INDEX, nb.SAFE_INDEX, nb.TARGET_INDEX], values)

def calculate_prob_all_no_target(values):
    return calculate_prob_mult([nb.PRICE_INDEX, nb.LUG_INDEX, nb.SAFE_INDEX], values)

def calculate_maximum_a_posteriori(indexes, values, index, value):
    max_a_posteriori = 0
    for i in range(len(indexes)):
        prob_i =  calculate_prob_mult([indexes[i], index], [values[i], value])
        max_a_posteriori = max(max_a_posteriori, prob_i)
    return max_a_posteriori

def question_a():
    print("\nA. A priori, isto é, sem considerar os atributos de cada instância, é menos provável que uma nova instância seja da classe acc do que da classe unacc.")
    prob_acc = calculate_prob(nb.TARGET_INDEX, nb.ACCEPT)
    prob_unacc = calculate_prob(nb.TARGET_INDEX, nb.NOT_ACCEPT)
    print("  P(target=acc): " + str(prob_acc))
    print("  P(target=unacc): " + str(prob_unacc))
    result = "VERDADEIRO" if prob_acc < prob_unacc else "FALSO"
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
    prob_unacc = calculate_prob(nb.TARGET_INDEX, nb.NOT_ACCEPT)
    prob_unacc_given_lug_med = prob_lug_med_and_unacc / prob_unacc
    print("      P(lug_boot=med|target=unacc) = " + str(prob_lug_med_and_unacc) + " / " + str(prob_unacc))
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

def question_e():
    print("\nE. As estimativas das probabilidades a posteriori para uma nova instância x com atributos price=high, lug_boot=med e safety=med seriam aproximadamente P(target=acc|x) = 0.019  e  P(target=unacc|x) = 0.021. Portanto, esta instância será classificada como unacc pelo modelo.")
    print("  Considerando P(yi|X) = P(yi) * ΠP(xj|yi), onde j vai de 1 a d")

    print("    yi = target=acc e x = [price=high, lug_boot=med, safety=med]:")
    prob_acc = calculate_prob(nb.TARGET_INDEX, nb.ACCEPT)
    print("      P(target=acc) = " + str(prob_acc))
    
    prob_acc_and_high_price = calculate_prob_mult([nb.TARGET_INDEX, nb.PRICE_INDEX], [nb.ACCEPT, nb.PRICE_HIGH])
    prob_acc_given_high_price = round((prob_acc_and_high_price / prob_acc), 4)
    print("      P(price=high|target=acc) = " + str(prob_acc_given_high_price))

    prob_acc_and_med_lug = calculate_prob_mult([nb.TARGET_INDEX, nb.LUG_INDEX], [nb.ACCEPT, nb.LUG_MED])
    prob_acc_given_med_lug = round((prob_acc_and_med_lug / prob_acc), 4)
    print("      P(lug_boot=med|target=acc) = " + str(prob_acc_given_med_lug))

    prob_acc_and_med_safe = calculate_prob_mult([nb.TARGET_INDEX, nb.SAFE_INDEX], [nb.ACCEPT, nb.SAFE_MED])
    prob_acc_given_med_safe = round((prob_acc_and_med_safe / prob_acc), 4)
    print("      P(safety=med|target=acc) = " + str(prob_acc_given_med_safe))

    prod_with_acc = round((prob_acc_given_high_price * prob_acc_given_med_lug * prob_acc_given_med_safe), 4)
    print("      ΠP(xj|target=acc) = " + str(prod_with_acc))

    prob_with_acc = round((prod_with_acc * prob_acc), 4)
    print("      P(yi) * ΠP(xj|target=acc) = " + str(prob_with_acc))

    print("    yi = target=unacc e x = [price=high, lug_boot=med, safety=med]:")
    prob_unacc = calculate_prob(nb.TARGET_INDEX, nb.NOT_ACCEPT)
    print("      P(target=unacc) = " + str(prob_unacc))
    
    prob_unacc_and_high_price = calculate_prob_mult([nb.TARGET_INDEX, nb.PRICE_INDEX], [nb.NOT_ACCEPT, nb.PRICE_HIGH])
    prob_unacc_given_high_price = round((prob_unacc_and_high_price / prob_unacc), 4)
    print("      P(price=high|target=unacc) = " + str(prob_unacc_given_high_price))

    prob_unacc_and_med_lug = calculate_prob_mult([nb.TARGET_INDEX, nb.LUG_INDEX], [nb.NOT_ACCEPT, nb.LUG_MED])
    prob_unacc_given_med_lug = round((prob_unacc_and_med_lug / prob_unacc), 4)
    print("      P(lug_boot=med|target=unacc) = " + str(prob_unacc_given_med_lug))

    prob_unacc_and_med_safe = calculate_prob_mult([nb.TARGET_INDEX, nb.SAFE_INDEX], [nb.NOT_ACCEPT, nb.SAFE_MED])
    prob_unacc_given_med_safe = round((prob_unacc_and_med_safe / prob_unacc), 4)
    print("      P(safety=med|target=unacc) = " + str(prob_unacc_given_med_safe))

    prod_with_unacc = round((prob_unacc_given_high_price * prob_unacc_given_med_lug * prob_unacc_given_med_safe), 4)
    print("      ΠP(xj|target=unacc) = " + str(prod_with_unacc))

    prob_with_unacc = round((prod_with_unacc * prob_unacc), 4)
    print("      P(yi) * ΠP(xj|target=unacc) = " + str(prob_with_unacc))


    result = "VERDADEIRO" if prob_with_unacc > prob_with_acc else "FALSO"
    print("  >> " + result)




question_a()
question_c()
question_d()
question_e()
