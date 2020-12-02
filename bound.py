import numpy as np


def func(delta_i, delta_2):
    exp_arg = 2 * (delta_i - delta_2) * (delta_i - delta_2)
    # print(exp_arg)
    numerator = np.exp(exp_arg) - 1
    denominator = delta_i
    return denominator / numerator


def expectation(i, K):
    return (K + 1 - i) / (K + 3)


def expectation_1(i, K):
    if i == 0:
        return (K - 1) / K
    if i == 1:
        return (K - 2) / K
    return (K - 3) / K


def summer():
    K = 1000000
    mus = [expectation_1(i, K) for i in range(K)]
    #print(mus)
    deltas = [mus[0] - mu for mu in mus]
    deltas_2 = deltas[1]
    # print(deltas)
    regret = sum(func(deltas[i], deltas_2) for i in range(2, K))
    return regret / (K*K)


if __name__ == '__main__':
    print(summer())
