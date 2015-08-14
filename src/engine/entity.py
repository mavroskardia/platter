class Entity(object):

    def __init__(self, name):
        self.name = name
        self.components = set()

    def __repr__(self):
        return self.name
