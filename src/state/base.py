class BaseGameState(object):

    def __init__(self):
        self.actors = []

    def update(self):
        for a in self.actors:
            a.update()

    def reset(self):
        return True, ''
