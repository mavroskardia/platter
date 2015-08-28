from sdl2 import *

from . import system
from ..components.decoration import Bordered
from ..components.physical import Size, Position


class BorderRendererSystem(system.System):

    componenttypes = Bordered, Position, Size

    def process(self, signaler, entities):
        print('bordering', len(entities), 'entities')
        for e in entities:
            bordered, dim, pos = e.components
            signaler.trigger('draw:rect', dim, pos)
