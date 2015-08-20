from . import system
from ..components.worldbound import WorldBound
from ..components.position import Position
from ..components.size import Size
from ..components.velocity import Velocity


class WorldBoundConstrainer(system.System):

    componenttypes = Position, Size, Velocity, WorldBound

    def process(self, signaler, components):
        for p, s, v, wb in components:
            if p.x < 0:
                p.nextx = 0
                v.vx = 0
                signaler.trigger('worldbound', p)
            if p.x + s.w > wb.maxx:
                p.nextx = wb.maxx - s.w
                v.vx = 0
                signaler.trigger('worldbound', p)
            if p.y < 0:
                p.nexty = 0
                v.vy = 0
                signaler.trigger('worldbound', p)
            if p.y + s.h >= wb.maxy:
                p.nexty = wb.maxy - s.h
                v.vy = 0
                signaler.trigger('worldbound', p)
