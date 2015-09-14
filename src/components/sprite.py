from .component import Component


class Sprite(Component):

    def __init__(self, entity, *args, **kwargs):
        super().__init__(entity, *args, **kwargs)
