from . import system

from ..components.velocity import Velocity
from ..components.force import Force


class ForceUpdater(system.System):

    componenttypes = Force, Velocity

    def process(self, signaler, components):
        for f, v in components:
            v.vx *= f.x
            v.vy *= f.y
