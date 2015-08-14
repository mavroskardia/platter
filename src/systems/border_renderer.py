from sdl2 import *

from . import system
from ..components.bordered import Bordered
from ..components.size import Size
from ..components.position import Position


class BorderRenderer(system.System):

    componenttypes = Bordered, Size, Position

    def process(self, signaler, components):
        for bordered, dim, pos in components:
            signaler.trigger('draw:rect', dim, pos)
