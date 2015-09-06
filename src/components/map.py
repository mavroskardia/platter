from . import component


class Tile(component.Component):

    def __init__(self, entity, name, *args):
        super().__init__(entity, *args)
        self.name = name
