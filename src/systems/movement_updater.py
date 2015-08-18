from . import system

from ..components.position import Position
from ..components.force import Force
from ..components.velocity import Velocity
from ..components.player_controls import PlayerControls


class MovementUpdater(system.System):

    componenttypes = Position, Velocity

    def process(self, signaler, components):
        for p, v in components:
            p.x += v.vx
            p.y += v.vy


class PlayerMovementUpdater(system.System):

    componenttypes = PlayerControls, Force

    def init(self, signaler):
        self.x = 1
        self.y = 1

        signaler.register('player:Up', self.up)
        signaler.register('player:Down', self.down)
        signaler.register('player:Left', self.left)
        signaler.register('player:Right', self.right)

    def process(self, signaler, components):
        for f, pc in components:
            pass

    def up(self, entity, pressed, *args):
        pass

    def down(self, entity, pressed, *args):
        pass

    def left(self, entity, pressed, *args):
        pass

    def right(self, entity, pressed, *args):
        pass
