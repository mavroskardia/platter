from .tetramino_factory import TetraminoFactory
from .components.position import Position

from ..main.entity import Entity
from ..signaler import instance as signaler
from ..systems.system import System


class TetrisInputSystem(System):
    def init(self):
        self.debug = True
        self.tetramino_factory = TetraminoFactory()
        signaler.register("keydown:D", self.toggle_debug)
        signaler.register("keydown:P", self.pause)
        signaler.register("keydown:A", self.spawn)

    def pause(self):
        signaler.trigger("breakpoint")

    def toggle_debug(self):
        self.debug = not self.debug
        signaler.trigger("debug:on" if self.debug else "debug:off", self.debug)

    def spawn(self):
        print("spawning new tetramino")
        ent = Entity(
            name="active tetra",
            components=[self.tetramino_factory.create_random(), Position(x=0, y=0)],
        )
        signaler.trigger("add_entity", ent)

    def process(self, *a, components=None, elapsed=0, **kw):
        pass
