from .tetramino_factory import Tetramino
from .components.position import Shape

from ..systems.system import System
from ..config.base import resolution


class TetrisUpdateSystem(System):
    componenttypes = Shape, Tetramino

    def init(self):
        self.frame_interval = 10
        self.frames = 0

    def process(self, *a, components, elapsed=0, **kw):
        self.frames += 1
        if self.frames >= self.frame_interval:
            self.frames = 0
            for shape, tetramino in components:
                if tetramino.frozen:
                    continue
                if shape.y + shape.h*2 >= resolution[1]:
                    tetramino.frozen = True
                else:
                    shape.y += shape.h
