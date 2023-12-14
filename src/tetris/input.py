from .tetramino_factory import TetraminoFactory, Tetramino
from .components.position import Shape

from ..main.entity import Entity
from ..signaler import instance as signaler
from ..systems.system import System


class TetrisInputSystem(System):
    componenttypes = Shape, Tetramino

    def init(self):
        self.debug = True
        self.dx = 0
        self.dy = 0
        self.r = 0
        self.tetramino_factory = TetraminoFactory()
        signaler.register("keydown:D", self.toggle_debug)
        signaler.register("keydown:P", self.pause)
        signaler.register("keydown:A", self.spawn)

        signaler.register("keydown:Left", self.make_move(-1, 0))
        signaler.register("keydown:Right", self.make_move(1, 0))
        signaler.register("keydown:Up", self.make_rotate(1))
        signaler.register("keydown:Down", self.make_rotate(-1))

    def make_rotate(self, dr):
        def rotate():
            self.r = dr

        return rotate

    def make_move(self, dx, dy):
        def move():
            self.dx = dx
            self.dy = dy

        return move

    def pause(self):
        signaler.trigger("breakpoint")

    def toggle_debug(self):
        self.debug = not self.debug
        signaler.trigger("debug:on" if self.debug else "debug:off", self.debug)

    def spawn(self):
        print("spawning new tetramino")
        ent = Entity(
            name="active tetra",
            components=[
                self.tetramino_factory.create_random(),
                Shape(x=0, y=0, w=10, h=10),
            ],
        )
        signaler.trigger("add_entity", ent)

    def process(self, *a, components, elapsed=0, **kw):
        if self.dx or self.dy or self.r:
            for shape, tet in components:
                if tet.frozen:
                    continue
                tet.rotate(self.r)
                shape.x += self.dx * shape.w
                shape.y += self.dy * shape.h

            self.dx = 0
            self.dy = 0
            self.r = 0
