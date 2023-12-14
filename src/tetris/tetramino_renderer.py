from .hud import Rect
from ..signaler import instance as signaler
from ..systems.system import System
from .tetramino_factory import Tetramino
from .components.position import Shape


class TetraminoRenderer(System):
    componenttypes = Shape, Tetramino

    def process(self, *a, components, elapsed=0, **kw):
        for shape, tetramino in components:
            """It's always the same 4x4 matrix being rendered"""
            for rindex, row in enumerate(tetramino.shape):
                for cindex, cell in enumerate(row):
                    if cell == 0:
                        continue
                    x = shape.x + shape.w * cindex
                    y = shape.y + shape.h * rindex
                    rect = Rect(x, y, shape.w, shape.h)
                    signaler.trigger("draw:filledrect", rect)
