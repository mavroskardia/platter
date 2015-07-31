class Query(object):

    def __init__(self, componentdb):
        self.db = componentdb
        self.types = set()

    def thatare(self, componentcls):
        self.types.add(componentcls)
        return self

    def get(self):
        return ((c for c in self.db.components[t]) for t in self.types)
