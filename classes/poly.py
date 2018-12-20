#!/usr/bin/python3
from utils import poly_mul
from math import log


class Poly:
    def __init__(self, poly_num):
        self.poly_num = poly_num

    def __mod__(self, other: 'Poly'):
        result_poly = Poly(self.poly_num)
        while len(result_poly) >= len(other):
            result_poly += Poly(other.poly_num << (len(result_poly) - len(other)))
        return result_poly

    def __mul__(self, other: 'Poly'):
        return Poly(poly_mul(self.poly_num, other.poly_num))

    def __add__(self, other: 'Poly'):
        return Poly(self.poly_num ^ other.poly_num)

    def __str__(self):
        return bin(self.poly_num)[2:]

    def __len__(self):
        return 1 if self.poly_num == 0 else int(log(self.poly_num, 2)) + 1

    @property
    def degree(self):
        return len(self) - 1

    def to_string(self):
        arr = []
        poly_str = bin(self.poly_num)
        for x, index in zip(poly_str[2:], range(self.degree, 1, -1)):
            if x == '1':
                arr.append('x^{0}'.format(index))
        if poly_str[::-1][1] == '1':
            arr.append('x')
        if poly_str[::-1][0] == '1':
            arr.append('1')
        return ' + '.join(arr)

    def inverse(self, mod: 'Poly'):
        poly1, poly2 = Poly(self.poly_num), Poly(mod.poly_num)
        x1, x2 = Poly(1), Poly(0)

        while poly2.poly_num != 1:
            p1_len = len(poly1)
            p2_len = len(poly2)

            if p1_len == p2_len:
                poly1, poly2 = poly2, poly1 + poly2
                x1, x2 = x2, x1 + x2
            elif p1_len < p2_len:
                poly1, poly2 = poly2, Poly(poly1.poly_num << (p2_len - p1_len)) + poly2
                x1, x2 = x2, Poly(x1.poly_num << (p2_len - p1_len)) + x2
            else:
                poly1, poly2 = poly2, Poly(poly2.poly_num << (p1_len - p2_len)) + poly1
                x1, x2 = x2, Poly(x2.poly_num << (p1_len - p2_len)) + x1

        return x2 % mod
