#!/usr/bin/python3
from classes.curve import Curve, Poly
from classes.point import Point


def add(point1: Point, point2: Point, curve: Curve):
    if point1.is_infinity:
        return point2
    if point2.is_infinity:
        return point1

    x1, y1 = point1.x, point1.y
    x2, y2 = point2.x, point2.y

    if x1 == x2 and (y1 != y2 or x1 == 0 and curve.t == 'N'):
        return Point()

    k = curve.get_k(x1, y1, x2, y2)
    x, y = curve.get_x3_y3(k, x1, y1, x2)

    result = Point(x, y)

    return result


def get_poly_from_number(arr):
    return [Poly(bin(x)[2:]) for x in arr]


def mult(num, point: Point, curve: Curve):
    if curve.p != 2:
        assert point.is_on_curve(curve)

    if point.is_infinity:
        return point

    if num < 0:
        return mult(-num, point.point_neg(curve), curve)

    result = Point()
    addend = point

    while num:
        if num & 1:
            result = add(result, addend, curve)

        addend = add(addend, addend, curve)

        num >>= 1

    if curve.p != 2:
        assert result.is_on_curve(curve)

    return result

#
# if __name__ == '__main__':
#     curve = Curve(2, 3, p=97)
#     print(mult(1, Point(3, 6)).to_string())
#     print(mult(7, Point(41, 120)).to_string())
#     curve = Curve(a=1, b=1, c=1, p=2, t='N', n=4)
#     curve.set_poly(Poly(0b10011))
#
#     print(add(Point(0b1000, 0b0010), Point(0b1010, 0b0101)).to_string())

