from collections import defaultdict, OrderedDict
from itertools import combinations

from .entity import Entity

from .. import signaler
from .. import config
from ..config.importer import load


class EntityComponentSystemManager:

    def __init__(self):
        self.signaler = signaler.instance
        self.entities = []
        self.systemdb = OrderedDict()
        self.componentdb = defaultdict(list)
        self.deferred_component_removals = []

    def init_systems(self):
        for system in config.systems:
            s = load(system)()
            print('initializing', s)
            s.init()
            self.add_system(s)

    def init_entities(self):
        for entity_name in config.entities:
            entity = Entity(entity_name)
            components = []

            for compname in config.entities[entity_name]:
                Component = load(compname)

                args = config.entities[entity_name][compname]
                if not args:
                    components.append(Component(entity=entity))
                    continue

                args, kwargs = args
                if not args:
                    args = ()
                if not kwargs:
                    kwargs = {}

                components.append(Component(entity, *args, **kwargs))

            entity.components = sorted(components,
                                       key=lambda c: c.__class__.__name__)

            self.add_entity(entity)

    def add_system(self, system, init=False):
        if init:
            system.init()

        if system.componenttypes not in self.systemdb:
            self.systemdb[system.componenttypes] = []

        self.systemdb[system.componenttypes].append(system)

    def add_entity(self, entity):
        combs, comps = [], list(sorted([type(c) for c in entity.components],
                                       key=lambda x: x.__name__))

        l = len(comps)
        while l > 0:
            combos = combinations(comps, l)
            for c in combos:
                combs.append(tuple(c))
            l -= 1

        for comb in combs:
            t = tuple(c for c in entity.components if type(c) in comb)
            self.componentdb[comb].append(t)

        if entity not in self.entities:
            self.entities.append(entity)

    def process(self, elapsed):
        for componenttypes in self.systemdb:
            for system in self.systemdb[componenttypes]:
                system.process(signaler=self.signaler,
                               components=self.componentdb[componenttypes],
                               elapsed=elapsed)

        self.process_deferrals()

    def process_deferrals(self):
        '''
            Remove all references to a component in the componentdb
        '''
        for comp in self.deferred_component_removals:
            self.remove_from_componentdb(comp)
            comp.entity.components.remove(comp)

        self.deferred_component_removals.clear()

    def add_component(self, component):
        types = [type(c) for c in component.entity.components]
        if type(component) not in types:
            component.entity.components.append(component)
            self.add_entity(component.entity)

    def remove_component(self, component, *args, **kwargs):
        self.deferred_component_removals.append(component)

    def remove_from_componentdb(self, component):
        componenttype = type(component)

        toremove = []

        for typetuple in self.componentdb:
            if typetuple and componenttype in typetuple:
                for componenttuple in self.componentdb[typetuple]:
                    if component in componenttuple:
                        toremove.append((typetuple, componenttuple))

        for typetuple, componenttuple in toremove:
            self.componentdb[typetuple].remove(componenttuple)

if __name__ == '__main__':

    signaler = Signaler()
    ecs = EntityComponentSystemManager(signaler)

    ecs.process(0)

    print('tested successfully')

