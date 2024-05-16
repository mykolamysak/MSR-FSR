import numpy as np
from math import lcm
from polynomial_utilities import Polynomial
from binary_utilities import convert_to_bin_seq


class Calculator:

    def __init__(self, a_poly: Polynomial, b_poly: Polynomial, i: int, j: int):
        self.a_poly = a_poly
        self.b_poly = b_poly
        self.matrix_A = np.array(self._get_matrix_a(self.a_poly))
        self.matrix_B = np.array(self._get_matrix_b(self.b_poly))
        self.n = a_poly.power
        self.r = 1
        self.i = i
        self.j = j
        self.t = a_poly.get_period() * b_poly.get_period()
        self.bin_seq = None

    # Get matrix A
    @staticmethod
    def _get_matrix_a(polynomial: Polynomial):
        matrix = [polynomial.get_coefficient()]

        for i in range(polynomial.power - 1):
            additional_vector = [0] * polynomial.power
            additional_vector[i] = 1
            matrix.append(additional_vector)

        return matrix

    # Get matrix B
    @staticmethod
    def _get_matrix_b(polynomial: Polynomial):
        matrix = [[0] * polynomial.power for _ in range(polynomial.power)]
        poly_coefs = polynomial.get_coefficient()

        for i in range(polynomial.power):
            matrix[i][0] = poly_coefs[i]

        for i in range(1, polynomial.power):
            matrix[i - 1][i] = 1

        return matrix

    # Calculating Hamming weight
    def get_hamming_weight(self):
        return (2 ** self.r - 1) * (2 ** (self.a_poly.power + self.b_poly.power - self.r - 1))

    # Calculating matrix S
    def new_matrix_s(self, r):
        matrix_s = [[0] * self.b_poly.power for _ in range(self.a_poly.power)]

        for i in range(r):
            matrix_s[i][i] = 1

        return matrix_s

    # Get matrix S period
    def get_matrix_s_period(self, r):
        return lcm(self.a_poly.get_period(), self.b_poly.get_period())

    # Calculate subsequence
    def calculate(self):
        matrix_s = np.array(self.new_matrix_s(self.r))
        limit = matrix_s.copy()
        subsequence = []

        while True:

            matrix_s = np.matmul(np.matmul(self.matrix_A, matrix_s) % 2, self.matrix_B) % 2
            subsequence.append(matrix_s[self.i, self.j])

            if np.all(matrix_s == limit):
                self.bin_seq = convert_to_bin_seq(subsequence)
                return subsequence

    # Calculate autocorrelation
    def get_acf(self):
        T_A = self.a_poly.get_period()  # Period of sequence A
        T_S = self.get_matrix_s_period(self.r)  # Period of matrix S

        bin_seq = np.array(self.bin_seq)
        output_acf = []

        # Calculate ACF values for all shifts in one go using numpy operations
        for teta in range(T_S):
            shifted_seq = np.roll(bin_seq, teta)
            acf_value = np.sum(bin_seq * shifted_seq) / T_A
            output_acf.append(acf_value)

        # Normalize ACF values
        max_acf_value = np.max(output_acf)
        min_acf_value = np.min(output_acf)
        min_normalized_value = -1 / T_A

        if max_acf_value != min_acf_value:
            normalized_acf = (output_acf - min_acf_value) / (max_acf_value - min_acf_value)
            output_acf = normalized_acf * (1 - min_normalized_value) + min_normalized_value
        else:
            normalized_acf_value = 1 if max_acf_value == 1 else min_normalized_value
            output_acf = [normalized_acf_value] * T_S

        return output_acf






