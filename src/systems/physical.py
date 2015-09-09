from itertools import combinations

from . import system

from ..config import config
from ..math.vector import Vec
from ..components.physical import AffectedByGravity, Body, CanCollide


class GravitySystem(system.System):
    '''
        Applies gravity to bodies susceptible to gravity
    '''

    componenttypes = AffectedByGravity, Body

    g = Vec(0, config.gravity)

    def process(self, *args, signaler, components, elapsed, **kwargs):
        for abg, body in components:
            body.acc += self.g


class ForceSystem(system.System):
    '''
        Applies other forces to bodies
    '''

    componenttypes = Body,

    friction = 0.9

    def process(self, *args, signaler, components, elapsed, **kwargs):
        for body, in components:
            body.vel += body.acc
            body.vel *= self.friction


class CollisionDetectionSystem(system.System):

    componenttypes = Body, CanCollide

    def process(self, *args, signaler, components, elapsed, **kwargs):

        if len(components) < 2:
            return

        for body, _ in components:
            for otherbody, __ in components:

                if body == otherbody:
                    continue

                b1 = Body(x=body.pos.x + body.vel.x * elapsed,
                          y=body.pos.y + body.vel.y * elapsed,
                          w=body.w, h=body.h)

                b2 = Body(x=otherbody.pos.x + otherbody.vel.x * elapsed,
                          y=otherbody.pos.y + otherbody.vel.y * elapsed,
                          w=otherbody.w, h=otherbody.h)

                if self.arecolliding(b1, b2):
                    body.vel = otherbody.vel.copy()
                    body.acc = otherbody.norm.copy()
                    print(body)

    def arecolliding(self, b1, b2):
        return (b1.pos.x < b2.pos.x + b2.w and
                b1.pos.x + b1.w > b2.pos.x and
                b1.pos.y < b2.pos.y + b2.h and
                b1.pos.y + b1.h > b2.pos.y)


class NormalUpdateSystem(system.System):
    '''
        Re-calculates normals. Not using this unless I add rotations
    '''

    componenttypes = Body,

    def process(self, *args, signaler, components, elapsed, **kwargs):
        for body, in components:
            body.ny = -config.gravity


class PositionUpdateSystem(system.System):
    '''
        After everything is done applying its effects to Velocity,
        update the position by the velocity
    '''

    componenttypes = Body,

    def process(s, *args, signaler=None, components=None, elapsed=0, **kargs):
        for body, in components:
            body.pos += body.vel * elapsed
