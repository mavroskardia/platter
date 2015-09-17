from .component import Component


class Sprite(Component):

    def __init__(self, entity, spriteset, *args, **kwargs):
        super().__init__(entity, *args, **kwargs)
        self.spriteset = spriteset
        self.frame = 0
        self.maxframes = 0
        self.span = 0.0
        self.interval = 0.0
