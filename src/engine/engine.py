from .signaler import Signaler
from ..componentdb.componentdb import ComponentDb
from ..systems.border_renderer import BorderRenderer
from .entity import Entity


class Engine(object):

    def __init__(self):
        self.systems = set()
        self.deferred = set()
        self.componentdb = ComponentDb()
        self.signaler = Signaler()
        self.running = True

    def add_system(self, system):
        s = system()
        s.init(self.signaler)
        self.systems.add(s)

    def run(self):

        self.signaler.register('quit', self.quit)
        self.signaler.register('keydown:Escape', self.quit)
        self.signaler.register('keydown:D', self.debug)

        while self.running:
            for s in self.systems:
                s.update(self.signaler, self.componentdb)

            for deferred in self.deferred:
                deferred()

            self.deferred.clear()

    def quit(self):
        self.running = False

    def debug(self):

        def f():
            from ..components.dimensions import Dimensions
            from ..components.bordered import Bordered

            e = Entity()
            self.componentdb.add_to_entity(e, Dimensions)
            self.componentdb.add_to_entity(e, Bordered)

            self.add_system(BorderRenderer)

        self.deferred.add(f)
