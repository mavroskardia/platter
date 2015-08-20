class Position(object):
    def __init__(self, x=0, y=0):
        self.lastx = 0
        self.lasty = 0
        self.x = x
        self.y = y
        self.nextx = 0
        self.nexty = 0

    def __repr__(self):
        return '({}, {})'.format(self.x, self.y)
