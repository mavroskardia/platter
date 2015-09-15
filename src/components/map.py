from . import component


class Tile(component.Component):

    def __init__(self, entity, name, *args, **kwargs):
        super().__init__(entity)
        self.name = name
