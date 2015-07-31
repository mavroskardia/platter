from sdl2 import *

from .system import System
from ..components.bordered import Bordered
from ..components.dimensions import Dimensions


class BorderRenderer(System):

    componenttypes = Bordered, Dimensions

    def process(self, signaler, *components):
        import pdb
        pdb.set_trace()
        for bordered, dims in components:
            print('would render', bordered, dims)
