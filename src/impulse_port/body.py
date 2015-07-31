import math
import random

from .vec2 import Vec2
from .shape import Shape


class Body(object):

    def __init__(self, shape, x, y):
        self.position = Vec2(float(x), float(y))
        self.velocity = Vec2(0.0, 0.0)

        self.angular_velocity = 0.0
        self.torque = 0.0
        self.orient = random.uniform(-math.pi, math.pi)

        self.force = Vec2(0.0, 0.0)

        self.I = 0.0     # moment of inertia
        self.iI = 0.0    # inverse inertia
        self.m = 0.0     # mass
        self.im = 0.0    # inverse mass

        self.static_friction = 0.5
        self.dynamic_friction = 0.3
        self.restitution = 0.2

        self.shape = shape
        self.shape.body = self
        self.shape.init()

        self.r = random.uniform(0.2, 1.0)
        self.g = random.uniform(0.2, 1.0)
        self.b = random.uniform(0.2, 1.0)

    def apply_force(self, f):
        self.force += f

    def apply_impulse(self, impulse, contact_vector):
        self.velocity += self.im * impulse
        self.angular_velocity += self.iI * cross(contact_vector, impulse)

    def set_static(self):
        self.I = 0.0
        self.iI = 0.0
        self.m = 0.0
        self.im = 0.0

    def set_orient(self, radians):
        self.orient = radians
        self.shape.set_orient(radians)
