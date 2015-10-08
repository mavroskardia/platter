from .system import System
from .. import signaler
from ..components.decoration import Bordered
from ..components.physical import Body


class BorderRendererSystem(System):

    componenttypes = Body, Bordered

    def process(self, *args, components, elapsed, **kwargs):
        for body, bordered, in components:
            signaler.instance.trigger('draw:rect', body.as_rect())


class VectorRendererSystem(System):

    componenttypes = Body,

    def process(self, *args, components, elapsed, **kwargs):

        for body, in components:
            n = body.pos + body.vel
            signaler.instance.trigger('draw:line',
                                      n.x, n.y, body.pos.x, body.pos.y)
