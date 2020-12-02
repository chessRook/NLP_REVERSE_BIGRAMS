import numpy as np
from scipy.stats import bernoulli as br


def sample(mu):
    sample = br.rvs(size=1, p=mu)[0]
    return sample


def sample_constant(mu):
    return mu


def sample_uniform(mu):
    distance = min(mu, 1 - mu)
    sample = np.random.uniform(mu - distance, mu + distance, size=1)
    return sample


T = 1000
K = int(np.floor(np.float_power(T, 5/6)))


def generate_mus(delta_mult):
    best = 0.5
    delta = delta_mult / np.sqrt(T)
    mus = [best, ] + [best - delta] * (K - 1)
    return mus


def apply_times():
    avg_regret = [0] * len(range(1, 21))
    for delta_mult in range(1, 21):
        avg_regret[delta_mult] = apply_the_algorithm(delta_mult)
    print(range(1, 21))
    print(avg_regret)


def apply_the_algorithm(delta_mult):
    mus = generate_mus(delta_mult)
    regret = algorithm(mus, T)
    expected_regret = np.sqrt(K) * np.sqrt(T)
    avg_reg = regret / expected_regret
    print(f'regret = {regret}.')
    print(f'expected_regret = {expected_regret}')
    print(f'avg_reg = {avg_reg}')
    print(f'root(T) = {np.sqrt(T)}')
    return avg_reg


def update(rewards, mus):
    for i, mu in enumerate(mus):
        rewards[i] += sample(mu)


def algorithm(mus, T_alg):
    rewards = [0] * len(mus)
    mus = sorted(mus)
    best_mu = mus[-1]
    regret = 0
    for t in range(T_alg):
        update(rewards, mus)
        # rewards[0] = mus[0] * (t + 1)
        best_action: int = np.argmax(rewards)
        best_action_mu = mus[best_action]
        current_regret = best_mu - best_action_mu
        regret += current_regret
    return regret


#    a = generate_mus()
#    print(a)
#    print(len(a), K)
#    print('generated mus')
# algorithm(a, T)
# print('algorithm ended')
# apply_the_algorithm(1)


if __name__ == '__main__':
    delta = np.sqrt(K) / np.sqrt(T)
    apply_the_algorithm(delta)