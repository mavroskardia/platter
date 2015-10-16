from .component import Component


class PlayerControl(Component):
    pass


class PlayerData(Component):

    def __init__(self, entity):
        super().__init__(entity)
        self.lives = 3
        self.score = 0

    def __str__(self):
        return '{s.lives} - {s.score}'.format(s=self)
