from .signaler import Signaler
from ..componentdb.componentdb import EntityComponentDb


class Engine(object):

    def __init__(self):
        self.systems = set()
        self.deferred = set()
        self.componentdb = EntityComponentDb()
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
            from .entity import Entity
            from ..systems.border_renderer import BorderRenderer
            from ..systems.movement_updater import MovementUpdater
            from ..systems.force_updater import ForceUpdater
            from ..components.size import Size
            from ..components.bordered import Bordered
            from ..components.position import Position
            from ..components.velocity import Velocity
            from ..components.force import Force

            e = Entity('test entity')
            self.componentdb.add_to_entity(e, Position(100, 100))
            self.componentdb.add_to_entity(e, Size(100, 100))
            self.componentdb.add_to_entity(e, Bordered())

            e2 = Entity('test entity 2')
            self.componentdb.add_to_entity(e2, Position(200, 200))
            self.componentdb.add_to_entity(e2, Size(50, 100))
            self.componentdb.add_to_entity(e2, Bordered())
            self.componentdb.add_to_entity(e2, Velocity(1.0, 1.0))
            self.componentdb.add_to_entity(e2, Force(0.99, 0.99))

            self.add_system(BorderRenderer)
            self.add_system(ForceUpdater)
            self.add_system(MovementUpdater)

        self.deferred.add(f)
