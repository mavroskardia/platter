import math

from copy import copy
from itertools import combinations

from .system import System

from .. import config
from ..math.vector import Vec, dot, norm
from ..components.physical import (Body, CanCollide, HasPhysics)


class GravitySystem(System):
    '''
        Applies gravity to bodies susceptible to gravity
    '''

    componenttypes = Body, HasPhysics

    g = Vec(0, config.gravity)

    def process(self, *args, components, elapsed, **kwargs):
        return

        for abg, body in components:
            if not body.colliding:
                body.vel += self.g


class ForceSystem(System):
    '''
        Applies other forces to bodies
    '''

    componenttypes = Body,

    air_friction = Vec(config.air_friction_x, config.air_friction_y)

    def process(self, *args, components, elapsed, **kwargs):
        return
        for body, in components:
            # body.vel += body.acc
            body.vel *= self.air_friction


class Manifold:

    g = Vec(0, 10.0)
    epsilon = 0.0001
    smoothing = 0.7

    def __init__(self, a, b, dt):
        self.a = a
        self.b = b
        self.dt = dt

        self.e = min(a.restitution, b.restitution)

        self.sf = 0.0
        self.df = 0.0

        self.n = Vec(0, 0)
        self.penetration = 0.0

    def init(self):
        self.sf = math.sqrt(self.a.static_friction * self.b.static_friction)
        self.df = math.sqrt(self.a.dynamic_friction * self.b.dynamic_friction)

        rv = self.b.vel - self.a.vel
        if rv.lengthsqr() < (self.g.lengthsqr() + self.epsilon):
            self.e = 0.0

    def solve(self):
        a, b, n = self.a, self.b, self.b.pos - self.a.pos
        aextent, bextent = a.pos + Vec(a.w/2, a.h), b.pos + Vec(b.w/2, b.h)
        xoverlap = aextent.x + bextent.x - abs(n.x)
        if xoverlap >= 0.0:
            yoverlap = aextent.y + bextent.y - abs(n.y)
            if yoverlap >= 0.0:
                if xoverlap > yoverlap:
                    self.n = Vec(-1.0, 0.0) if n.x < 0.0 else Vec(1.0, 0.0)
                    self.penetration = xoverlap
                    return True
                else:
                    self.n = Vec(0.0, -1.0) if n.y < 0.0 else Vec(0.0, 1.0)
                    self.penetration = yoverlap
                    return True

        return False

    def resolve(self):
        a, b, r = self.a, self.b, self.b.pos - self.a.pos
        vn = dot(r, self.n)

        if vn > 0:
            return  # moving away from each other

        j = -(1.0 + self.e) * vn
        j /= (a.im + b.im)

        a.apply_impulse(-j * self.n)
        b.apply_impulse(j * self.n)

        t = r - self.n * vn
        if t.length() > self.epsilon:
            t.normalize()

        jt = -dot(r, t)
        jt /= (a.im + b.im)

        ajt = abs(jt)

        if ajt < self.epsilon:
            return  # don't bother applying friction to such a tiny impulse

        t *= jt if ajt < j * self.sf else -j * self.df

        a.apply_impulse(-t)
        b.apply_impulse(t)

    def correct(self):
        a, b = self.a, self.b

        pct, slop = 0.15, 0.5001
        m = max(self.penetration - slop, 0.0) / (a.im + b.im)

        c = m * self.n * pct * self.dt

        oa = copy(a.pos)
        ob = copy(b.pos)

        a.pos = a.pos - (c * a.im)
        b.pos = b.pos + (c * b.im)

        # smoothing function
        a.pos = (a.pos * self.smoothing) + (oa * (1.0 - self.smoothing))
        b.pos = (b.pos * self.smoothing) + (ob * (1.0 - self.smoothing))

        if a.im != 0:
            if self.n.y == 1.0:
                a.vel -= self.g

        if b.im != 0:
            if self.n.y == 1.0:
                b.vel -= self.g


class PhysicsSystem(System):

    componenttypes = Body, CanCollide, HasPhysics

    gravity = Vec(0, config.gravity)

    def find_collisions(self, components, dt):
        self.contacts = []
        for a, *_ in components:
            for b, *_ in components:
                if a is b or a.im == 0 and b.im == 0:
                    continue

                if a.is_overlapping(b):
                    m = Manifold(a, b, dt)
                    if m.solve():
                        self.contacts.append(m)
                        # TODO: move this to somewhere less offensive
                        a.jumping, b.jumping = False, False

    def integrate_forces(self, components):
        for body, *_ in components:
            body.integrate_forces(self.gravity)

    def initialize_collisions(self):
        for c in self.contacts:
            c.init()

    def integrate_velocities(self, components, dt):
        for body, *_ in components:
            if body.im != 0:
                body.pos += body.vel * dt
                body.vel += self.gravity
                body.vel *= Vec(0.95, 1)  # global friction application
                body.vel.x = max(-100, min(100, body.vel.x))
                body.vel.y = max(-200, min(200, body.vel.y))

    def resolve_collisions(self):
        for i in range(iterations):
            for c in self.contacts:
                c.resolve()

    def correct_positions(self):
        for c in self.contacts:
            c.correct()

    def process(self, *args, components, elapsed, **kwargs):
        self.find_collisions(components, elapsed)
        self.integrate_forces(components)

        for c in self.contacts:
            # c.init()
            c.resolve()

        self.integrate_velocities(components, elapsed)
        self.correct_positions()


class CollisionDetectionSystem0(System):

    componenttypes = Body, CanCollide

    def process(self, *args, components, elapsed, **kwargs):

        if len(components) < 2:
            return

        for body, _ in components:
            for otherbody, __ in components:

                if body == otherbody:
                    continue

                b1 = Body(body.entity,
                          x=body.pos.x + body.vel.x * elapsed,
                          y=body.pos.y + body.vel.y * elapsed,
                          w=body.w, h=body.h)

                b2 = Body(body.entity,
                          x=otherbody.pos.x + otherbody.vel.x * elapsed,
                          y=otherbody.pos.y + otherbody.vel.y * elapsed,
                          w=otherbody.w, h=otherbody.h)

                if self.arecolliding(b1, b2):
                    # body.vel = copy(otherbody.vel)
                    # body.acc = copy(otherbody.norm)
                    body.colliding_with.add(otherbody)
                    body.jumping = False
                else:
                    try:
                        body.colliding_with.remove(otherbody)
                    except KeyError:  # safely ignore non-existent value
                        pass

    def arecolliding(self, b1, b2):
        return (b1.pos.x < b2.pos.x + b2.w and
                b1.pos.x + b1.w > b2.pos.x and
                b1.pos.y < b2.pos.y + b2.h and
                b1.pos.y + b1.h > b2.pos.y)


class PositionUpdateSystem(System):
    '''
        After everything is done applying its effects to Velocity,
        update the position by the velocity
    '''

    componenttypes = Body,

    def process(s, *args, components=None, elapsed=0, **kargs):
        for body, in components:
            body.pos += body.vel * elapsed
