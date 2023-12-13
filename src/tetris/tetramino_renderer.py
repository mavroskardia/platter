from .hud import Rect
from ..signaler import instance as signaler
from ..systems.system import System
from .tetramino_factory import Tetramino
from .components.position import Position


class TetraminoRenderer(System):
    componenttypes = Position, Tetramino

    def init(self):
        pass

    def process(self, *a, components, elapsed=0, **kw):
        for pos, tetramino in components:
            """It's always the same 4x4 matrix being rendered"""
            rect = Rect(pos.x, pos.y, 10, 10)
            print(rect)
            signaler.trigger("draw:filledrect", rect)
