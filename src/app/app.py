from imp import importlib

from ..config import config
from ..engine.engine import Engine
from ..engine.entity import Entity


class App(object):

    def run(self):
        engine = Engine()

        world = config.load(config.default_world)(config.resolution)

        for system in world.systems:
            s = config.load(system)
            engine.add_system(s)

        for e in world.entities:
            entity = Entity(e)
            components = world.entities[e]
            for c in components:
                engine.componentdb.add_to_entity(entity, c)

        return engine.run()
