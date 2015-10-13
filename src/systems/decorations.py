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

    sf = 1.0
    head_sf = 10.0

    def process(self, *args, components, elapsed, **kwargs):
        for body, in components:
            dimvec = Vec(body.w/2, body.h/2)
            c = body.pos + dimvec
            c_plus_vel = c + (body.vel * self.sf)

            p1 = c_plus_vel + (c_plus_vel - c).perpendicular().normalize() * self.head_sf
            p2 = c_plus_vel - (c_plus_vel - c).perpendicular().normalize() * self.head_sf

            signaler.instance.trigger('draw:line',
                                      c.x, c.y,
                                      c_plus_vel.x, c_plus_vel.y)

            signaler.instance.trigger('draw:line',
                                      c_plus_vel.x, c_plus_vel.y,
                                      p1.x, p1.y)

            signaler.instance.trigger('draw:line',
                                      c_plus_vel.x, c_plus_vel.y,
                                      p2.x, p2.y)
