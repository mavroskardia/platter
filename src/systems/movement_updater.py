from . import system

from ..components.position import Position
from ..components.force import Force
from ..components.velocity import Velocity
from ..components.player_controls import PlayerControls


class MovementUpdater(system.System):

    componenttypes = Position, Velocity

    def init(self, signaler):
        signaler.register('collision', self.stop)

    def stop(self, e1, e2, xoverlap, yoverlap, *args, **kwargs):
        for v in e1.oftype(Velocity):
            if v.directions['up'] or v.directions['down']:
                v.vy = 0
            if v.directions['left'] or v.directions['right']:
                v.vx = 0

    def process(self, signaler, components):
        for p, v in components:
            v.directions['right'] = v.vx > 0
            v.directions['left'] = v.vx < 0
            v.directions['up'] = v.vy < 0
            v.directions['down'] = v.vy > 0
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
