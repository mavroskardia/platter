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

                if (self.algo2(p1, p2, s1, s2)):
                    signaler.trigger('collision', p1.entity, p2.entity,
                                     abs(p1.x - p2.x), abs(p1.y - p2.y))

                    p1.nextx, p1.nexty = p1.lastx, p1.lasty
                    p2.nextx, p2.nexty = p2.lastx, p2.lasty

    def algo1(self, p1, p2, s1, s2):
        x = abs(p1.x - p2.x) * 2 < (s1.w + s2.w)
        y = abs(p1.y - p2.y) * 2 < (s1.h + s2.h)

        return x and y

    def algo2(self, p1, p2, s1, s2):
        # scenario 1: p1 is up and left of p2

        if ((p1.x < p2.x and p1.x + s1.w > p2.x) or
           (p1.x > p2.x and p1.x < p2.x + s2.w)):
            if ((p1.y < p2.y and p1.y + s1.h > p2.y) or
               (p1.y > p2.y and p1.y < p2.y + s2.h)):
                return True
        return False
