import time

from itertools import chain
from collections import defaultdict

from .query import Query


class EntityComponentDb(object):

    def __init__(self):
        self.components = defaultdict(set)
        self.entities = set()

    def add_to_entity(self, entity, component):
        component.entity = entity
        entity.components.add(component)
        self.entities.add(entity)
        self.components[type(component)].add(component)

    def thatare(self, *componentcls):
        return Query(self, *componentcls)


if __name__ == '__main__':

    from ..engine.entity import Entity
    from ..components.bordered import Bordered
    from ..components.dimensions import Size

    bordered = Entity('bordered')
    dimensions = Entity('dimensions')
    both = Entity('both')
    both2 = Entity('both2')

    ecdb = EntityComponentDb()

    b1, b2, b3 = Bordered(), Bordered(), Bordered()
    d1, d2 = Size(), Size()

    ecdb.add_to_entity(bordered, b1)
    ecdb.add_to_entity(bordered, b2)
    ecdb.add_to_entity(dimensions, d1)
    ecdb.add_to_entity(both, b3)
    ecdb.add_to_entity(both, d2)

    time.clock()

    bcomps = ecdb.thatare(Bordered).get()
    dcomps = ecdb.thatare(Size).get()
    bdcomps = ecdb.thatare(Bordered, Size).get()

    print('relevant part of process ran for {} seconds'.format(time.clock()))

    try:
        bcomps = list(bcomps)
        assert len(bcomps) == 2, ('Should have found 2 groups of Bordered, but'
                                  'found {} instead'.format(len(bcomps)))
        assert {b1, b2} in bcomps, 'Should have one set of b1,b2'
        assert {b3} in bcomps, 'Should have one set of b3'

        bdcomps = list(bdcomps)
        assert len(bdcomps) == 1, ('Should have found 1 group of '
                                   'Bordered, Dimensions but found '
                                   '{} instead'.format(len(bdcomps)))

    except Exception as e:
        print(e)
        import pdb
        pdb.set_trace()
