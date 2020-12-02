import numpy as np
import scipy.special as sp


def bin_coeff(n, k):
    return sp.binom(n, k)


def bin_dist(n, k, epsilon):
    epsilon_complement = 1 - epsilon
    return bin_coeff(n, k) * np.power(epsilon, k) * np.power(epsilon_complement, n - k)


def square(x):
    return x * x


t = 1000
eps = 0.01
start = 20


def summer():
    return sum(square(bin_dist(t, k, eps)) for k in range(start, t))


if __name__ == '__main__':
    print(np.sqrt(summer()))
