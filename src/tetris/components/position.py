from dataclasses import dataclass
from ...components.component import Component


@dataclass
class Position(Component):
    x: int
    y: int
