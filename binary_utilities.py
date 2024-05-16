from polynomial_utilities import Polynomial

# Creating a table with abbreviated binary values
def binary_table(binary_string):
    n = len(binary_string)
    table = []
    table.append(binary_string[1:])
    for i in range(1, n-1):
        row = "0" * (i - 1) + "1" + "0" * (n - i - 1)
        table.append(row)

    return table


# 8 to 2
def oct_to_bin(octal):
    decimal_number = 0
    power = 0
    while octal != 0:
        digit = octal % 10
        decimal_number += digit * (8 ** power)
        power += 1
        octal //= 10
    return format(decimal_number, 'b')


# Find gcd between 2 numbers
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


# Validate values of chosen polynomials
def validate(f_poly: Polynomial, s_poly: Polynomial):
    pass


# Convert to binary sequence
def convert_to_bin_seq(sequence):
    return [-1 if it == 1 else 1 for it in sequence]


# Create Binary C sequence
def Binary_C(sequence):
    binary_sequence = []
    for bit in sequence:
        if bit == 0:
            binary_sequence.append('1')
        else:
            binary_sequence.append('-1')
    return ' '.join(binary_sequence)


# Get function F value from binary value of polynomial
def binary_to_F(binary_value):
    polynomial = []
    binary_str = str(binary_value)
    length = len(binary_str)

    for i, bit in enumerate(binary_str):
        if bit == '1':
            exponent = length - i - 1
            if exponent == 0:
                polynomial.append("1")
            elif exponent == 1:
                polynomial.append("x")
            else:
                polynomial.append(f"x^{exponent}")

    return ' + '.join(polynomial)

