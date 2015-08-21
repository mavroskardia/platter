from . import system

from ..components.position import Position
from ..components.forces import AffectedByGravity
from ..components.velocity import Velocity
from ..components.player_controls import PlayerControls


class MovementUpdater(system.System):

    componenttypes = Position, Velocity

    def init(self, signaler):
        signaler.register('collision', self.collision)
        signaler.register('worldbound', self.worldbound)

    def collision(self, e1, e2, dx, dy):
        print('collision!')

    def worldbound(self, p):
        pass

    def process(self, signaler, components):
        for p, v in components:
            p.lastx, p.lasty = p.x, p.y
            p.x, p.y = p.nextx, p.nexty


class VelocityUpdater(system.System):

    componenttypes = Position, Velocity

    gravity = 0.1
    friction = 0.9

    def process(self, signaler, components):
        for p, v in components:
            v.vx *= self.friction
            v.vy *= self.friction
            p.nextx = p.x + v.vx
            p.nexty = p.y + v.vy


class PlayerMovementUpdater(system.System):

    componenttypes = PlayerControls, Velocity

    def init(self, signaler):
        self.x, self.y = 0, 0

        signaler.register('player:Up', self.up)
        signaler.register('player:Down', self.down)
        signaler.register('player:Left', self.left)
        signaler.register('player:Right', self.right)

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
