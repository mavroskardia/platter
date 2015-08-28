import sys
import os

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
        self.systemdb = {}
        self.componentdb = {}
        self.signaler = Signaler()

    def add_system(self, system):
        self.systemdb[system.componenttypes].add(system)

    def add_entity(self, entity_name, components):
        types = (type(c) for c in components)
        types = tuple(sorted(types, key=lambda x: x.__class__.__name__))
        print('adding entity with components', types)
        self.componentdb[types].add(Entity(entity_name, components))

    def run(self):

        self.init_systems()
        self.init_entities()
        self.register_global_events()

        self.running = True
        while self.running:
            for componenttypes in self.systemdb:
                for system in self.systemdb[componenttypes]:
                    system.process(self.signaler,
                                   self.componentdb[componenttypes])

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
        self.signaler.register('quit', self.quit)

    def quit(self):
        self.running = False


if __name__ == '__main__':

    App().run()
