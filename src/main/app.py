import sys
import os

try:
    os.environ['PYSDL2_DLL_PATH'] = 'lib'
    from sdl2 import *
except ImportError:
    print('You have to have pysdl2 installed and'
          ' the sdl2 dlls in the lib directory')
    sys.exit(1)

from collections import defaultdict, deque, OrderedDict
from itertools import combinations

from .entity import Entity
from .signaler import Signaler
from .fps import Fps

from .. import config
from ..config.importer import load


class App:

    def __init__(self):
        self.entities = []
        self.systemdb = OrderedDict()
        self.componentdb = defaultdict(list)
        self.signaler = Signaler()
        self.fps = Fps(self.signaler)
        self.deferred_component_removals = []

    def add_system(self, system):
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

    def run(self):

        self.register_global_events()

        self.init_systems()
        self.init_entities()
        self.fps.init()

        self.running = True

        while self.running:
            self.fps.tick_start()

            for componenttypes in self.systemdb:
                for system in self.systemdb[componenttypes]:
                    system.process(signaler=self.signaler,
                                   components=self.componentdb[componenttypes],
                                   elapsed=self.fps.elapsed)

            self.process_deferrals()

            self.fps.tick_end()

    def init_systems(self):
        for system in config.systems:
            s = load(system)()
            print('initializing', s)
            s.init(self.signaler)
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

    def register_global_events(self):
        self.signaler.register('add_entity', self.add_entity)
        self.signaler.register('quit', self.quit)
        self.signaler.register('keydown:Escape', self.quit)
        self.signaler.register('keydown:D', self.debug)
        self.signaler.register('remove_component', self.remove_component)
        self.signaler.register('add_component', self.add_component)
        self.signaler.register('add_entity', self.add_entity)

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

    def quit(self):
        self.running = False

    def debug(self):
        print('FPS:', self.fps)
        # import pdb
        # pdb.set_trace()


if __name__ == '__main__':

    if len(sys.argv) == 1:
        App().run()
    elif sys.argv[1] == 'profile':
        import cProfile
        import io
        import pstats
        profile = cProfile.Profile()
        profile.enable()
        try:
            App().run()
        except:
            pass
        profile.disable()
        sortby = 'cumulative'
        with open('profile.log', 'w') as f:
            ps = pstats.Stats(profile, stream=f).sort_stats(sortby)
            ps.print_stats()

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

            e = Entity('test', [a, b, c, d])

            app.add_entity(e)

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
