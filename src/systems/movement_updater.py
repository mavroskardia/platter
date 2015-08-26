from . import system

from ..components.position import Position
from ..components.forces import AffectedByGravity
from ..components.velocity import Velocity
from ..components.player_controls import PlayerControls


class MovementUpdater(system.System):

    componenttypes = Position, Velocity

    def init(self, signaler):
        self.showdebug = False
        signaler.register('debug', self.debug)

    def debug(self, *args, **kwargs):
        self.showdebug = True

    def process(self, signaler, components):
        for p, v in components:
            p.prevx.append(p.x)
            p.prevy.append(p.y)
            p.x, p.y = p.nextx, p.nexty

            if self.showdebug:
                print('*** MovementUpdater:', p)

        if self.showdebug:
            self.showdebug = False


class VelocityUpdater(system.System):

    componenttypes = Position, Velocity

    xfriction = 0.9
    yfriction = 0.9
    gravity = 0.1

    def init(self, signaler):
        signaler.register('collision', self.collision)

    def collision(self, e1, e2, dx, dy):
        for v in e1.oftype(Velocity):
            v.vx = 0
            v.vy = 0

    def process(self, signaler, components):
        for p, v in components:
            p.nextx = p.x + v.vx
            p.nexty = p.y + v.vy
            v.vx *= self.xfriction
            v.vy *= self.yfriction


class PlayerMovementUpdater(system.System):

    componenttypes = PlayerControls, Velocity

    def init(self, signaler):
        self.x, self.y = 0, 0

        signaler.register('player:Up', self.up)
        signaler.register('player:Left', self.left)
        signaler.register('player:Right', self.right)
        signaler.register('player:Down', self.down)

    def process(self, signaler, components):
        for pc, v in components:
            v.vx += self.x
            v.vy += self.y

    def up(self, entity, pressed, *args):
        self.y = -int(pressed)

    def down(self, entity, pressed, *args):
        self.y = int(pressed)

    def left(self, entity, pressed, *args):
        self.x = -int(pressed)

    def right(self, entity, pressed, *args):
        self.x = int(pressed)
