import math
import random

R = math.cos(math.pi / 4)


class Vec:
    """
    In keeping with tradition, a re-implementation of the wheel... i mean,
    2d vector.
    """

    HashStart = random.randint(1, 123489712983723)

    def __init__(self, x: float = 0.0, y: float = 0.0):
        self.x = x
        self.y = y

    def __hash__(self):
        h = self.HashStart
        return (h * self.x % 2) + (h * self.y % 2)

    def __eq__(self, v):
        return self.x == v.x and self.y == v.y

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

    def __truediv__(self, v):
        if isinstance(v, Vec):
            return Vec(self.x / v.x, self.y / v.y)
        return Vec(self.x / v, self.y / v)

    def __rtruediv__(self, v):
        if isinstance(v, Vec):
            return Vec(self.x / v.x, self.y / v.y)
        return Vec(self.x / v, self.y / v)

    def __itruediv__(self, v):
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

    def __str__(self):
        return "<{s.x}, {s.y}>".format(s=self)

    def __repr__(self):
        return "Vector: <{s.x}, {s.y}>".format(s=self)

    def __copy__(self):
        return Vec(self.x, self.y)

    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def lengthsqr(self):
        return self.x * self.x + self.y * self.y

    def normalize(self):
        self *= 1.0 / (self.length() + 0.00001)
        return self

    def perpendicular(self):
        return Vec(-self.y, self.x)

    def overlaps(self, v, threshold=10):
        return (
            self.x - threshold <= v.x
            and self.x + threshold >= v.x
            and self.y - threshold <= v.y
            and self.y + threshold >= v.y
        )


def dot(v1, v2):
    return v1.x * v2.x + v1.y * v2.y


def norm(v):
    return math.sqrt(v.x * v.x + v.y * v.y)


def direction(v):
    """
    Returns one of 'left', 'right', 'down', or 'up'
    """
    # we'll start by rotating the movement vector by π/4 so the rest is
    # easy peasy

    rv = Vec(R * v.x + R * v.y, -R * v.x + R * v.y)

    if rv.x >= 0 and rv.y >= 0:
        return "down"
    if rv.x >= 0 and rv.y < 0:
        return "right"
    if rv.x < 0 and rv.y >= 0:
        return "left"
    if rv.x < 0 and rv.y < 0:
        return "up"


if __name__ == "__main__":
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
    assert v0.x == v1.x
    assert v0.y == v1.y
    v0 += v1
    assert v0 == Vec(8, 10)

    v2n = v2.normalize()

    assert v2n == Vec(0.5546986577679576, 0.8320479866519364), v2n

    assert Vec(20, 20).overlaps(Vec(25, 25), 10)
    assert not Vec(20, 20).overlaps(Vec(25, 25), 1)
