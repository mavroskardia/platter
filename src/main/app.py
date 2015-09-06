import sys
import os
import time

try:
    os.environ['PYSDL2_DLL_PATH'] = 'lib'
    from sdl2 import *
except ImportError:
    print('You have to have pysdl2 installed and'
          ' the sdl2 dlls in the lib directory')
    sys.exit(1)

from collections import defaultdict, deque, OrderedDict
from itertools import combinations

from ..config import config
from ..config.importer import load
from .signaler import Signaler


class Entity:

    def __init__(self, name, components):
        self.name = name
        self.components = components


class App:

    def __init__(self):
        self.entities = []
        self.systemdb = OrderedDict()
        self.componentdb = defaultdict(set)
        self.signaler = Signaler()
        self.deferred_component_removals = []

    def add_system(self, system):
        if system.componenttypes not in self.systemdb:
            self.systemdb[system.componenttypes] = set()
        self.systemdb[system.componenttypes].add(system)

    def add_entity(self, entity_name, components):
        e = Entity(entity_name, components)
        combs, comps = [], list(sorted([type(c) for c in components],
                                       key=lambda x: x.__name__))

        l = len(comps)
        while l > 0:
            combos = combinations(comps, l)
            for c in combos:
                combs.append(tuple(c))
            l -= 1

        for comb in combs:
            self.componentdb[comb].add(tuple(c for c in e.components
                                             if type(c) in comb))

        self.entities.append(e)

    def run(self):

        self.register_global_events()
        self.init_systems()
        self.init_entities()

        self.running = True
        last_time = time.time()

        while self.running:
            current = time.time()
            elapsed = current - last_time

            for componenttypes in self.systemdb:
                for system in self.systemdb[componenttypes]:
                    matchingsets = self.componentdb[componenttypes]
                    system.process(signaler=self.signaler,
                                   components=matchingsets,
                                   elapsed=elapsed)

            self.process_deferrals()

            last_time = current

    def init_systems(self):
        for system in config.systems:
            s = load(system)()
            print('initializing', s)
            s.init(self.signaler)
            self.add_system(s)

    def init_entities(self):
        for entity_name in config.entities:
            entity_components = []

            for component, args in config.entities[entity_name]:
                entity_components.append(load(component)(*args))

            self.add_entity(entity_name, entity_components)

    def register_global_events(self):
        self.signaler.register('add_entity', self.add_entity)
        self.signaler.register('quit', self.quit)
        self.signaler.register('keydown:Escape', self.quit)
        self.signaler.register('keydown:D', self.debug)
        self.signaler.register('remove_component', self.remove_component)

    def process_deferrals(self):
        '''
            Remove all references to a component in the componentdb
        '''
        for comp in self.deferred_component_removals:
            self.remove_from_componentdb(comp)

        self.deferred_component_removals.clear()

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
            print(self.componentdb[typetuple])
            self.componentdb[typetuple].remove(componenttuple)

    def quit(self):
        self.running = False

    def debug(self):
        import pdb
        pdb.set_trace()


if __name__ == '__main__':

    if len(sys.argv) == 1:
        App().run()
    else:
        def test_add_entity():
            class A:
                def __str__(self): return type(self).__class__.__name__

            class B:
                def __str__(self): return type(self).__class__.__name__

            class C:
                def __str__(self): return type(self).__class__.__name__

            class D:
                def __str__(self): return type(self).__class__.__name__

            app = App()

            a, b, c, d = A(), B(), C(), D()

            app.add_entity('test', (c, d, b, a))

            results = [
                (A, B, C, D),
                (A, B, C),
                (A, B, D),
                (A, C, D),
                (B, C, D),
                (A, B),
                (A, C),
                (A, D),
                (B, C),
                (B, D),
                (C, D),
                (A,),
                (B,),
                (C,),
                (D,),
            ]

            for k in app.componentdb.keys():
                assert k in results, k

            app.remove_component(a)

            for types in app.componentdb:
                for s in app.componentdb[types]:
                    assert a not in s, 'found {} in {} [[[ {} ]]]'.format(hex(id(a)), s, types)

        test_add_entity()
