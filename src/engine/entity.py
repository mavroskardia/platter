class Entity(object):

    def __init__(self, name):
        self.name = name
        self.components = set()

    def __repr__(self):
        return self.name

    def hastype(self, T):
        return T in (type(t) for t in self.components)

    def oftype(self, T):
        return (t for t in self.components if type(t) is T)
