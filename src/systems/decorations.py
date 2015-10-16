from .system import System
from .. import signaler
from ..math.vector import Vec
from ..components.decoration import Bordered
from ..components.physical import Body


class BorderRendererSystem(System):

    componenttypes = Body, Bordered

    def process(self, *args, components, elapsed, **kwargs):
        for body, bordered, in components:
            signaler.instance.trigger('draw:rect', body.as_rect())


class VectorRendererSystem(System):

    componenttypes = Body,

    sf = 0.5
    head_sf = 2.0

    def process(self, *args, components, elapsed, **kwargs):
        for body, in components:
            dimvec = Vec(body.w/2, body.h/2)
            c = body.pos + dimvec
            cv = c + (body.vel * self.sf)

            p1 = cv + (cv - c).perpendicular().normalize() * self.head_sf
            p2 = cv - (cv - c).perpendicular().normalize() * self.head_sf

            signaler.instance.trigger('draw:line',
                                      c.x, c.y,
                                      cv.x, cv.y,
                                      color=(255, 255, 255, 50))

            signaler.instance.trigger('draw:line',
                                      cv.x, cv.y,
                                      p1.x, p1.y,
                                      color=(255, 255, 255, 50))

            signaler.instance.trigger('draw:line',
                                      cv.x, cv.y,
                                      p2.x, p2.y,
                                      color=(255, 255, 255, 50))
