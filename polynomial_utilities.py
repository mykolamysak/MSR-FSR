import numpy as np


# Generates the C sequence using the shift register.
def generate_C(polynomial_coef, T_C):
    n = len(polynomial_coef)
    S = np.random.randint(2, size=n)
    C = []
    for _ in range(T_C):
        C.append(S[0])
        next_bit = sum(polynomial_coef[i] * S[i] for i in range(1, n)) % 2
        S = np.roll(S, 1)
        S[0] = next_bit
    return C


# Generates all possible states of the shift register with the length degree
def generate_states(polynomial_coef, degree):
    states = []
    n = len(polynomial_coef)

    for i in range(2 ** degree):
        state = np.zeros(degree, dtype=int)
        state[-1] = 1
        for j in range(degree):
            state[j] = (i >> j) & 1
        states.append(state)
    return states


# Generate ACF graph
def compute_ACF(C, degree):
    T_C = 2 ** degree - 1
    corr_result = np.correlate(C, C, mode='full')
    if corr_result.any():
        max_corr = max(corr_result)
    else:
        max_corr = 0
    n = len(C)
    R = np.zeros(n)
    for tau in range(n):
        R[tau] = np.sum([C[t] * C[(t - tau) % T_C] for t in range(T_C)]) / T_C / max_corr

    min_normalized_value = -1 / n
    R = (R - np.min(R)) / (np.max(R) - np.min(R)) * (1 - min_normalized_value) + min_normalized_value

    return R


# Find exp period
def find_experimental_period(C, degree):
    T_C = 2 ** degree - 1
    ACF = compute_ACF(C, degree)
    max_ACF = max(ACF)
    for tau in range(1, T_C):
        if ACF[tau] == max_ACF:
            return tau
    return None


class Polynomial:
    def __init__(self, j, g8, power):
        self.j = j
        self.g8 = g8
        self.g2 = self._g8_to_g2(g8)
        self.power = power

    # Convert 8 to 2 value
    @staticmethod
    def _g8_to_g2(octal_number: int):
        binary_string = bin(int(str(octal_number), 8))[2:]
        binary_list = [int(bit) for bit in binary_string]
        return binary_list

    # Get period of matrix
    def get_period(self):
        return (2 ** self.power) - 1

    # Get coefficient
    def get_coefficient(self):
        return self.g2[1:]

