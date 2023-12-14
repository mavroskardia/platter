from dataclasses import dataclass
from ...components.component import Component


@dataclass
class Position(Component):
    x: int
    y: int


@dataclass
class Shape(Component):
    x: int
    y: int
    w: int
    h: int
