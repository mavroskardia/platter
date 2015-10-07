from .system import System
from ..components.decoration import Bordered
from ..components.physical import Body


class BorderRendererSystem(System):

    componenttypes = Body, Bordered

    def process(self, *args, signaler, components, elapsed, **kwargs):
        for body, bordered, in components:
            signaler.trigger('draw:rect', body.as_rect())
