from . import component


class Tile(component.Component):

    def __init__(self, entity, name, pos, *args, **kwargs):
        super().__init__(entity)
        self.name = name
        self.pos = pos
