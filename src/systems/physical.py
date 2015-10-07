from copy import copy
from itertools import combinations

from .system import System

from .. import config
from ..math.vector import Vec, dot
from ..components.physical import (AffectedByGravity, Body, CanCollide,
                                   HasPhysics)


class GravitySystem(System):
    '''
        Applies gravity to bodies susceptible to gravity
    '''

    componenttypes = AffectedByGravity, Body

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


class PhysicsSystem(System):

    componenttypes = Body, CanCollide, HasPhysics

    class Manifold:

        def __init__(self, a, b):
            self.a = a
            self.b = b
            self.n = None
            self.penetration = 0.0

    def aabb_vs_aabb(self, a, b):
        manifold = self.Manifold(a, b)
        n = b.pos - a.pos

        ax_extent = a.w / 2.0
        bx_extent = b.w / 2.0
        xoverlap = ax_extent + bx_extent - abs(n.x)
        if xoverlap > 0.0:
            ay_extent = a.h / 2.0
            by_extent = b.h / 2.0
            yoverlap = ay_extent + by_extent - abs(n.y)

            if yoverlap > 0.0:

                if xoverlap > yoverlap:
                    manifold.n = Vec(-1.0, 0.0) if n.x < 0.0 else Vec(1.0, 0.0)
                    manifold.penetration = xoverlap
                    return True, manifold
                else:
                    manifold.n = Vec(0.0, -1.0) if n.y < 0.0 else Vec(0.0, 1.0)
                    manifold.penetration = yoverlap
                    return True, manifold

        return False, manifold

    def process(self, *args, components, elapsed, **kwargs):

        for (body, r, rr), (otherbody, s, ss) in combinations(components, 2):
            if body.inv_mass == 0 and otherbody.inv_mass == 0:
                continue

            a = copy(body)
            a.x = body.pos.x + body.vel.x * elapsed
            a.y = body.pos.y + body.vel.y * elapsed

            b = copy(otherbody)
            b.x = otherbody.pos.x + otherbody.vel.x * elapsed
            b.y = otherbody.pos.y + otherbody.vel.y * elapsed

            colliding, manifold = self.aabb_vs_aabb(a, b)

            if colliding:
                rel_vel = b.vel - a.vel
                vel_norm = dot(rel_vel, manifold.n)

                if vel_norm > 0.0:  # moving away from each other
                    continue

                e = min(a.restitution, b.restitution)
                j = -(1 + e) * vel_norm
                j /= a.inv_mass + b.inv_mass
                impulse = j * manifold.n

                body.vel = a.vel - a.inv_mass * impulse
                otherbody.vel = b.vel + b.inv_mass * impulse

                body.colliding = True
                otherbody.colliding = True
            else:
                body.colliding, otherbody.colliding = False, False
                body, otherbody = a, b

        for body, _, __ in components:

            if not body.colliding:
                body.pos += body.vel * elapsed


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
