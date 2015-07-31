from collections import defaultdict

from .query import Query


class ComponentDb(object):

    def __init__(self):
        self.components = defaultdict(list)

    def add_to_entity(self, entity, component):
        component.entity = entity
        self.components[type(component)].append(component)

    def thatare(self, componentname):
        return Query(self).thatare(componentname)


if __name__ == '__main__':

    from ..engine.entity import Entity
    from ..components.bordered import Bordered
    from ..components.dimensions import Dimensions

    onlybordered = Entity()
    onlydimensions = Entity()
    both = Entity()

    cdb = ComponentDb()

    b1, b2 = Bordered(), Bordered(), Bordered()
    d1, d2 = Dimensions(), Dimensions(), Dimensions()

    cdb.add_to_entity(onlybordered, b1)
    cdb.add_to_entity(onlydimensions, d1)
    cdb.add_to_entity(both, b2)
    cdb.add_to_entity(both, b2)
    cdb.add_to_entity(both, d2)

    bentities = cdb.thatare(Bordered).get()
    dentities = cdb.thatare(Dimensions).get()
    bothentities = cdb.thatare(Bordered).thatare(Dimensions).get()
    bothagain = cdb.thatare(Dimensions).thatare(Bordered).get()

    import pdb
    pdb.set_trace()

    assert len(bentities) == 2, 'should have two instances of Bordered'

    assert onlybordered in list(bentities), '"onlybordered" not in bordered'
    assert both in bentities, '"both" not in bordered'
    assert onlydimensions not in bentities, '"onlydimensions" in bordered'

    assert onlydimensions in dentities, '"onlydimensions" not in dimensions'
    assert both in dentities, '"both" in dimensions'
    assert onlybordered not in dentities, '"onlybordered" in dimensions'

    assert both in bothentities, '"both" not in both'
    assert both in bothagain, '"both" not in bothagain'
    assert onlybordered not in bothentities
    assert onlybordered not in bothagain
    assert onlydimensions not in bothentities
    assert onlydimensions not in bothagain
