from collections import defaultdict
from .signaler import Signaler
from ..componentdb.componentdb import EntityComponentDb


class Engine(object):

    def __init__(self):
        self.systems = defaultdict()
        self.deferred = set()
        self.componentdb = EntityComponentDb()
        self.signaler = Signaler()
        self.running = True

    def add_system(self, system):
        s = system()
        s.init(self.signaler)

        if type(s) not in self.systems:
            self.systems[type(s)] = s

    def run(self):

        self.signaler.register('quit', self.quit)
        self.signaler.register('keydown:Escape', self.quit)
        self.signaler.register('keydown:D', self.debug)

        while self.running:
            for s in self.systems:
                self.systems[s].update(self.signaler, self.componentdb)

            for deferred in self.deferred:
                deferred()

            self.deferred.clear()

    def quit(self):
        self.running = False

    def debug(self):
        pass
