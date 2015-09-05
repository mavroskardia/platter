from sdl2 import *

from . import system
from ..components.decoration import Bordered
from ..components.physical import Size, Position


class BorderRendererSystem(system.System):

    componenttypes = Bordered, Position, Size

    def process(self, *args, signaler=None, entities=None, elapsed=0, **kargs):

        for e in entities:
            bordered, dim, pos, *rest = e.components
            signaler.trigger('draw:rect', dim, pos)
