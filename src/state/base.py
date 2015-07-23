class BaseGameState(object):

    def update(self):
        pass

    def reset(self):
        return True, ''
