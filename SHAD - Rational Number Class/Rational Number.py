import sys


def gcd(a, b):
    """

    :param a: lhs of greatest common divisor
    :param b: rhs of greatest common divisor
    :return: greatest common divisor of a, b
    """

    while b:
        a, b = b, a % b
    return a


class Rational(object):
    """
    Represents a rational number kind of p/q, where p and q are integer

    """
    def __init__(self, p: int=0, q: int=1):
        divisor = gcd(p, q)
        self.p = p / divisor
        self.q = q / divisor

    def __add__(self, other):
        return Rational(self.p * other.q + other.p * self.q, other.q * self.q)

    def __neg__(self):
        return Rational(-self.p, self.q)

    def __sub__(self, other):
        return self + (-other)

    def __str__(self):
        return '%d/%d' % (self.p, self.q)

    def __mul__(self, other):
        return Rational(self.p * other.p, self.q * other.q)

    def __truediv__(self, other):
        return Rational(self.p * other.q, self.q * other.p)

    def __eq__(lhs, rhs):
        return (lhs.p == rhs.p) and (lhs.q == rhs.q)

    def __ne__(lhs, rhs):
        return (lhs.p != rhs.p) or (lhs.q != rhs.q)


exec(sys.stdin.read())
