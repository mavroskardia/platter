from . import system

from ..components.collisions import CanCollide
from ..components.position import Position
from ..components.size import Size


class CollisionDetection(system.System):

    componenttypes = CanCollide, Position, Size

    def process(self, signaler, components):

        for c, p1, s1 in components:
            for p2, s2 in [(po, sz) for co, po, sz in components
                           if po.entity != p1.entity]:

                if (abs(p1.x - p2.x) * 2 < s1.w + s2.w and
                   abs(p1.y - p2.y) * 2 < s1.h + s2.h):

                    signaler.trigger('collision', p1.entity, p2.entity,
                                     abs(p1.x - p2.x), abs(p1.y - p2.y))
