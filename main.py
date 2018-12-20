#!/usr/bin/python3
import os

from classes.curve import Curve, Poly
from classes.point import Point
from operation import add, mult
from glob import glob
from sys import argv

def int_n(s):
    bases = {'0x': 16, '0o': 8, '0b': 2}
    key_base = s[:2] if len(s) >= 2 else 0
    base = bases[key_base] if key_base in bases else 10
    return int(s, base)


def main():
    print('This program which sum and multiply elliptical curve points')
    files = glob(os.path.join('tests', '*'))
    if len(argv) > 1:
        files = argv[1:]

    for file_name in files:
        with open(file_name, 'r', encoding='utf-8') as f:
            params = f.readlines()
            params = [x.replace(os.linesep, '').replace('\n', '').replace('\ufeff', '') for x in params]
            if params[0] == '2S' or params[0] == '2N':
                p, t, c, poly, idx = 2, params[0][1], int_n(params[4]), int_n(params[5]), 6
            else:
                p, t, c, idx = int_n(params[0]), '-', 0, 4
            n = int_n(params[1])
            a, b = [int_n(x) for x in params[2:4]]

            curve = Curve(a=a, b=b, c=c, p=p, n=n, t=t)
            if p == 2:
                curve.set_poly(Poly(poly))

            answer = []
            for s in params[idx:]:
                args = s.split(' ')
                op = args[0]
                base = args[1][:2] if len(args[1]) >= 2 else 10
                if op == 'у' or op == 'y':
                    x, y, k = [int_n(x) for x in args[1:]]
                    answer.append(mult(k, Point(x, y), curve).to_string(base) + os.linesep)
                else:
                    x1, y1, x2, y2 = [int_n(x) for x in args[1:]]
                    answer.append(add(Point(x1, y1), Point(x2, y2), curve).to_string(base) + os.linesep)
            cur_file_name = os.path.join('tests_answer', os.path.join(*os.path.split(file_name)[1:]))
            with open(cur_file_name, 'w', encoding='cp866') as f:
                f.writelines(answer)

    print(os.linesep + 'Check directory with name: tests_answer' + os.linesep)


if __name__ == '__main__':
    main()
