from . import system

from ..components.velocity import Velocity
from ..components.force import Force


class ForceUpdater(system.System):

    componenttypes = Force, Velocity

    gravity = 0.1

    def init(self, signaler):
        signaler.register('collision', self.stop)

    def stop(self, e1, e2, xoverlap, yoverlap, *args, **kwargs):
        pass

    def process(self, signaler, components):
        for f, v in components:
            v.vx += f.x
            v.vy += f.y + self.gravity
