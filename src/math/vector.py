import math


class Vec:
    '''
        In keeping with tradition, a re-implementation of the wheel... i mean,
        2d vector.
    '''
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, v):
        return Vec(self.x + v.x, self.y + v.y)

    def __iadd__(self, v):
        self.x += v.x
        self.y += v.y
        return self

    def __sub__(self, v):
        return Vec(self.x - v.x, self.y - v.y)

    def __isub__(self, v):
        self.x -= v.x
        self.y -= v.y
        return self

    def __div__(self, v):
        if isinstance(v, Vec):
            return Vec(self.x / v.x, self.y / v.y)
        return Vec(self.x / v, self.y / v)

    def __rdiv__(self, v):
        if isinstance(v, Vec):
            return Vec(self.x / v.x, self.y / v.y)
        return Vec(self.x / v, self.y / v)

    def __idiv__(self, v):
        if isinstance(v, Vec):
            self.x /= v.x
            self.y /= v.y
        else:
            self.x /= v
            self.y /= v
        return self

    def __mul__(self, v):
        if isinstance(v, Vec):
            return Vec(self.x * v.x, self.y * v.y)
        return Vec(self.x * v, self.y * v)

    def __rmul__(self, v):
        if isinstance(v, Vec):
            return Vec(self.x * v.x, self.y * v.y)
        return Vec(self.x * v, self.y * v)

    def __imul__(self, v):
        if isinstance(v, Vec):
            self.x *= v.x
            self.y *= v.y
        else:
            self.x *= v
            self.y *= v
        return self

    def __neg__(self):
        return Vec(-self.x, -self.y)

    def __eq__(self, v):
        return self.x == v.x and self.y == v.y

    def __str__(self):
        return '<{s.x}, {s.y}>'.format(s=self)

    def __repr__(self):
        return 'Vector: <{s.x}, {s.y}>'.format(s=self)

    def __copy__(self):
        return Vec(self.x, self.y)

    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def lengthsqr(self):
        return self.x * self.x + self.y * self.y

    def normalize(self):
        self *= 1.0 / self.length()
        return self


def dot(v1, v2):
    return v1.x * v2.x + v1.y * v2.y


def norm(v):
    return math.sqrt(v.x * v.x + v.y * v.y)


if __name__ == '__main__':

    v0 = Vec(0, 0)
    v1 = Vec(4, 5)
    v2 = Vec(2, 3)

    assert v1 + v2 == Vec(6, 8)
    assert v0 + v0 == v0
    assert v1 + v1 == Vec(8, 10)
    assert v2 * v2 == Vec(4, 9)
    assert v1 - v0 == Vec(4, 5)
    assert v1 - v2 == Vec(2, 2)

    assert v2 / 2 == Vec(1.0, 1.5), v2 / 2.0

    v0 += v1
    assert v0 == v1

    v2n = v2.normalize()

    assert v2n == Vec(0.5547001962252291, 0.8320502943378437), v2n
