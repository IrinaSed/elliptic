#!/usr/bin/env python3
def inverse_mod(k, p):
    if k == 0:
        raise ZeroDivisionError('division by zero')

    if k < 0:
        return p - inverse_mod(-k, p)

    gcd, x, y = extended_euclidean_algorithm(k, p)

    assert gcd == 1
    assert (k * x) % p == 1

    return x % p


def extended_euclidean_algorithm(a, b):
    s, old_s = 0, 1
    t, old_t = 1, 0
    r, old_r = b, a

    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    return old_r, old_s, old_t


def poly_mul(poly_num1, poly_num2):
    s = 0
    while poly_num2:
        if poly_num2 & 1:
            s = s ^ poly_num1

        poly_num1 *= 2
        poly_num2 >>= 1
    return s


def little_endian(num, n):
    num_bits = bin(num)[2:][::-1]
    d = n - len(num_bits)
    num_bits += '0' * d

    return int(num_bits, 2)
