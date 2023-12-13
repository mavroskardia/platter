from ..signaler import instance as signaler
from ..systems.sdl import SdlSystem
from ..systems.input import InputSystem
from ..main.entity import Entity
from ..main.fps import Fps
from ..main.ecs import EntityComponentSystemManager

from .hud import HudSystem
from .input import TetrisInputSystem
from .tetramino_renderer import TetraminoRenderer


class Tetris:
    def __init__(self):
        self.fps = Fps()
        self.fps.init()
        self.running = False
        self.ecs = EntityComponentSystemManager()

    def create_global_entities(self):
        """
        Tetris requires a playfield, a hud, a score display, and a level display
        """

        self.ecs.add_entity(Entity(name="Playfield", components=[]))
        self.ecs.add_entity(Entity(name="Hud", components=[]))
        self.ecs.add_entity(Entity(name="Score display", components=[]))
        self.ecs.add_entity(Entity(name="Level display", components=[]))

    def load_systems(self):
        """
        Tetris requires a rendering system, an input system, a set of gameplay
        systems, a set of HUD systems(?), and ...
        """

        self.ecs.add_system(SdlSystem(title="Tetris"), init=True)
        self.ecs.add_system(InputSystem(), init=True)
        self.ecs.add_system(TetrisInputSystem(), init=True)
        self.ecs.add_system(TetraminoRenderer(), init=True)
        self.ecs.add_system(HudSystem(), init=True)

    def register_global_events(self):
        signaler.register("quit", handler=lambda: setattr(self, "running", False))

    def run(self):
        self.create_global_entities()
        self.load_systems()
        self.register_global_events()

        self.running = True

        while self.running:
            dt = self.fps.tick_start()
            self.ecs.process(dt)
            self.fps.tick_end()


if __name__ == "__main__":
    # TODO: put a title card here?

    Tetris().run()
