import sys
import os
import time

try:
    os.environ['PYSDL2_DLL_PATH'] = 'lib'
    from sdl2 import *
except ImportError:
    print('You have to have the sdl2 dlls in the lib directory')
    sys.exit(1)

from collections import defaultdict

from ..config import config
from ..config.importer import load
from .signaler import Signaler


class Entity:

    def __init__(self, name, components):
        self.name = name
        self.components = components


class App:

    def __init__(self):
        self.systemdb = defaultdict(set)
        self.componentdb = defaultdict(set)
        self.signaler = Signaler()

    def add_system(self, system):
        self.systemdb[system.componenttypes].add(system)

    def add_entity(self, entity_name, components):
        e = Entity(entity_name, components)
        comps = components[:]
        types = tuple(sorted((type(c) for c in comps),
                             key=lambda x: x.__class__.__name__))

        while comps:
            print('{}:\n\t{}\n\t{}'.format(types, entity_name, comps))
            self.componentdb[types].add(e)
            comps.pop()

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
                                   entities=matchingsets,
                                   elapsed=elapsed)

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

    def quit(self):
        self.running = False

    def debug(self):
        print('*** DEBUG: {} in the component db'.format(
            len(self.componentdb.values())))


if __name__ == '__main__':

    App().run()
