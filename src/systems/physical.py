from itertools import combinations

from . import system

from ..config import config
from ..components.physical import (Acceleration, AffectedByGravity, Position,
                                   Velocity, CanCollide, Size, Jumping)


class GravityCollisionSystem(system.System):
    '''
        After a collision event, remove the AffectedByGravity component
        to prevent further gravity updates
    '''

    componenttypes = Acceleration, AffectedByGravity, CanCollide

    def process(self, *args, signaler, components, elapsed, **kwargs):

        for acc, abg, cc in components:
            if cc.colliding:
                if abg.affecting:
                    acc.y = 0
                    abg.affecting = False
                cc.colliding = False
            else:
                abg.affecting = True


class GravitySystem(system.System):
    '''
        Applies gravity to velocities susceptible to gravity
    '''

    componenttypes = Acceleration, AffectedByGravity

    gravity = 100.0

    def process(self, *a, signaler, components, elapsed, **k):
        for acc, abg in components:
            if abg.affecting:
                acc.y += self.gravity * elapsed


class JumpingSystem(system.System):

    componenttypes = Acceleration, Jumping

    jump_force = -50.0

    def init(self, signaler):
        self.signaler = signaler
        signaler.register('collision:down', self.done_jumping)

    def done_jumping(self, entity):
        jump = entity.get_component(Jumping)
        if jump:
            self.signaler.trigger('remove_component', jump)

    def process(self, *args, signaler, components, elapsed, **kargs):
        for acc, jump in components:
            if not jump.in_progress:
                acc.y = self.jump_force
                jump.in_progress = True


class AccelerationSystem(system.System):
    '''
        Applies accelerations to velocities
    '''

    componenttypes = Acceleration, Velocity

    def init(self, signaler):
        signaler.register('collision:down', self.collision)
        self.reset_y_acceleration = []

    def collision(self, entity):
        self.reset_y_acceleration.append(entity)

    def process(self, *args, signaler, components, elapsed, **kargs):
        toremove = []

        for acc, vel in components:
            vel.vx += acc.x * elapsed
            vel.vy += acc.y * elapsed

            for e in self.reset_y_acceleration:
                if acc.entity == e:
                    acc.y = 0
                    toremove.append(e)

        for e in toremove:
            self.reset_y_acceleration.remove(e)
        toremove.clear()


class FrictionSystem(system.System):
    '''
        Applies friction to velocities
    '''

    componenttypes = Velocity,

    friction = 0.90

    def process(s, *args, signaler=None, components=None, elapsed=0, **kargs):
        for vel, in components:
            vel.vx *= s.friction
            vel.vy *= s.friction


class Body:

    def __init__(self, x, y, w, h):
        self.x, self.y, self.w, self.h = x, y, w, h

    def __str__(self):
        return 'BODY @ ({s.x}, {s.y}) - {s.w} x {s.h}'.format(s=self)


class CollisionDetectionSystem(system.System):

    componenttypes = CanCollide, Position, Size, Velocity

    def process(self, *args, signaler, components, elapsed, **kwargs):
        if len(components) < 2:
            return

        for combo in combinations(components, 2):
            (cc1, p1, s1, v1), (cc2, p2, s2, v2) = combo

            b1 = Body(p1.x + v1.vx * elapsed,
                      p1.y + v1.vy * elapsed, s1.w, s1.h)
            b2 = Body(p2.x + v2.vx * elapsed,
                      p2.y + v2.vy * elapsed, s2.w, s2.h)

            if self.algo2(b1, b2):
                cc1.colliding = True
                cc2.colliding = True
                for v in (v1, v2):
                    if v.vy > 0:
                        signaler.trigger('collision:down', v.entity)
                        v.vy = -(b1.y + b1.h - b2.y)

            else:
                cc1.colliding = False
                cc2.colliding = False

    def algo1(self, b1, b2):
        x = abs(b1.x - b2.x) * 2 < (b1.w + b2.w)
        y = abs(b1.y - b2.y) * 2 < (b1.h + b2.h)

        return x and y

    def algo2(self, b1, b2):
        x1 = b1.x < b2.x and b1.x + b1.w > b2.x
        x2 = b1.x > b2.x and b1.x < b2.x + b2.w
        y1 = b1.y < b2.y and b1.y + b1.h > b2.y
        y2 = b1.y > b2.y and b1.y < b2.y + b2.h

        return (x1 or x2) and (y1 or y2)


class PositionUpdateSystem(system.System):
    '''
        After everything is done applying its effects to Velocity,
        update the position by the velocity
    '''

    componenttypes = Position, Velocity

    def process(s, *args, signaler=None, components=None, elapsed=0, **kargs):
        for pos, vel in components:
            pos.y += vel.vy
            pos.x += vel.vx
