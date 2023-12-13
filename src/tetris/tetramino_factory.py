import random
from enum import Enum

from ..components.component import Component


class Tetraminos(Enum):
    L = 1
    LR = 2
    Z = 3
    ZR = 4
    Square = 5
    T = 6
    Long = 7


class Tetramino(Component):
    name: str
    shape: list

    def rotate(self):
        self.shape = list(zip(*self.shape[::-1]))


class TetraminoFactory:
    def __init__(self):
        pass

    def create_random(self):
        return self.create(random.choice(list(Tetraminos)))

    def create(self, tetramino: Tetraminos) -> Tetramino:
        rettet = Tetramino()
        match tetramino:
            case Tetraminos.L:
                rettet.name = 'L'
                rettet.shape = [
                    (0, 0, 0, 0),
                    (1, 0, 0, 0),
                    (1, 0, 0, 0),
                    (1, 1, 0, 0),
                ]
            case Tetraminos.Long:
                rettet.name = 'Long'
                rettet.shape = [
                    (1, 0, 0, 0),
                    (1, 0, 0, 0),
                    (1, 0, 0, 0),
                    (1, 0, 0, 0),
                ]
            case Tetraminos.LR:
                rettet.name = 'LR'
                rettet.shape = [
                    (1, 1, 0, 0),
                    (0, 1, 1, 0),
                    (0, 0, 0, 0),
                    (0, 0, 0, 0),
                ]
            case Tetraminos.Z:
                rettet.name = 'Z'
                rettet.shape = [
                    (1, 1, 0, 0),
                    (0, 1, 1, 0),
                    (0, 0, 0, 0),
                    (0, 0, 0, 0),
                ]
            case Tetraminos.ZR:
                rettet.name = 'ZR'
                rettet.shape = [
                    (1, 1, 0, 0),
                    (0, 1, 1, 0),
                    (0, 0, 0, 0),
                    (0, 0, 0, 0),
                ]
            case Tetraminos.Square:
                rettet.name = 'Square'
                rettet.shape = [
                    (1, 1, 0, 0),
                    (0, 1, 1, 0),
                    (0, 0, 0, 0),
                    (0, 0, 0, 0),
                ]
            case Tetraminos.T:
                rettet.name = 'T'
                rettet.shape = [
                    (1, 1, 0, 0),
                    (0, 1, 1, 0),
                    (0, 0, 0, 0),
                    (0, 0, 0, 0),
                ]
            case _:
                raise Exception(f"Do not know about tetramino {tetramino}")

        return rettet
