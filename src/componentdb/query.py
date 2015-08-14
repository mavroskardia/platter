from collections import defaultdict


class Query(object):

    def __init__(self, componentdb, *components):
        self.db = componentdb
        self.types = set(components)

    def get(self):
        for e in self.db.entities:
            if self.types & {type(c) for c in e.components} == self.types:
                ret = (c for c in e.components if type(c) in self.types)
                yield sorted(ret, key=lambda c: c.__class__.__name__)
