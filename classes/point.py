#!/usr/bin/python3
from classes.curve import Curve


class Point:
    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y

    @property
    def is_infinity(self):
        return self.x is None and self.y is None

    def is_on_curve(self, curve: Curve, msg="Point: {0} is not on curve."):
        if self.is_infinity:
            return True

        result = (self.y ** 2 - self.x ** 3 - curve.a * self.x - curve.b) % curve.p == 0

        if not result:
            print(msg.format(self.to_string()))
            return

        return result

    def to_string(self, base=10):
        if self.is_infinity:
            return 'infinity'
        bases = {'0x': hex, '0o': oct, '0b': bin, 10: int}
        return '({0}, {1})'.format(bases[base](self.x), bases[base](self.y))

    def point_neg(self, curve: Curve):
        assert self.is_on_curve(curve)

        if self.is_infinity:
            return self

        result = Point(self.x, -self.y % curve.p)

        assert result.is_on_curve(curve)

        return result
