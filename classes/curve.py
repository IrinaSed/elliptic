#!/usr/bin/python3
from utils import inverse_mod
from classes.poly import Poly


class Curve:
    def __init__(self, a, b, c=None, p=2, n=1, t='S'):
        self.a = a
        self.b = b
        self.c = c
        self.p = p
        self.t = t
        self.n = n
        self.poly = None

    def set_poly(self, poly: Poly):
        if not self.is_valid_poly(poly):
            exit()

        self.poly = poly

    def get_k(self, x1, y1, x2, y2):
        if self.p != 2 and self.p != 3:
            return self.get_k_char_not_2_and_not_3(x1, y1, x2, y2)

        elif self.p == 2 and self.t == 'S':
            return self.get_k_super(x1, y1, x2, y2)

        elif self.p == 2 and self.t == 'N':
            return self.get_k_not_super(x1, y1, x2, y2)

        else:
            self.not_support_curve()

    def get_k_char_not_2_and_not_3(self, x1, y1, x2, y2):
        if x1 == x2:
            k = (3 * x1 * x1 + self.a) * inverse_mod(2 * y1, self.p)
        else:
            k = (y1 - y2) * inverse_mod(x1 - x2, self.p)

        return k

    def get_k_super(self, x1, y1, x2, y2):
        x1_p, y1_p, x2_p, y2_p, a, b = Poly(x1), Poly(y1), Poly(x2), Poly(y2), Poly(self.a), Poly(self.b)
        if x1 == x2:
            k = (x1_p * x1_p + b) * a.inverse(self.poly) % self.poly
        else:
            k = (y2_p + y1_p) * (x2_p + x1_p).inverse(self.poly) % self.poly

        return k

    def get_k_not_super(self, x1, y1, x2, y2):
        x1_p, y1_p, x2_p, y2_p, a, b = Poly(x1), Poly(y1), Poly(x2), Poly(y2), Poly(self.a), Poly(self.b)
        if x1 == x2:
            k = (x1_p * x1_p + a * y1_p) * (a * x1_p).inverse(self.poly)
        else:
            k = (y2_p + y1_p) * (x2_p + x1_p).inverse(self.poly) % self.poly

        return k

    def get_x3_y3(self, k, x1, y1, x2):
        if self.p != 2 and self.p != 3:
            x = k ** 2 - x1 - x2
            y = y1 + k * (x - x1)
            return x % self.p, -y % self.p

        elif self.p == 2 and self.t == 'S':
            x1_p, x2_p, y1_p = Poly(x1), Poly(x2), Poly(y1)
            x3 = x1_p + x2_p + k * k
            y3 = (x3 + x1_p) * k + y1_p
            return (x3 % self.poly).poly_num, ((y3 + Poly(self.a)) % self.poly).poly_num

        elif self.p == 2 and self.t == 'N':
            x1_p, y1_p, x2_p = Poly(x1), Poly(y1), Poly(x2)
            x3 = k * k + Poly(self.a) * k + Poly(self.b)
            if x1 != x2:
                x3 = x3 + x1_p + x2_p

            y3 = k * (x3 + x1_p) + y1_p

            return (x3 % self.poly).poly_num, ((y3 + Poly(self.a) * x3) % self.poly).poly_num

        else:
            self.not_support_curve()

    def not_support_curve(self):
        print('This program don`t work this params:')
        print('p = {0}'.format(self.p))
        print('t = {0}'.format(self.t))
        # exit()

    def to_string(self):
        return 'curve: (a: {0}, b: {1}, c: {2}, p: {3}, t: {4}, n: {5})'.format(
            self.a, self.b, self.c, self.p, self.t, self.n)

    def is_valid_poly(self, poly: Poly):
        deg = poly.degree
        if deg != self.n:
            print('polynom: {0} is not valid, not n == {1}'.format(poly.to_string(), poly.degree))
            return False
        return True
