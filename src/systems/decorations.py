from sdl2 import *

from . import system
from ..components.decoration import Bordered
from ..components.physical import Size, Position


class BorderRendererSystem(system.System):

    componenttypes = Bordered, Position, Size

    def process(self, *args, signaler, components, elapsed, **kwargs):
        for bordered, dim, pos in components:
            signaler.trigger('draw:rect', dim, pos)
