from functools import lru_cache
from collections import defaultdict


class Signaler(object):

    def __init__(self):
        self.events = defaultdict(list)

    def register(self, event_name, handler):
        self.events[event_name].append(handler)

    @lru_cache(maxsize=0)
    def trigger(self, event_name, *args, **kwargs):
        for handler in self.events[event_name]:
            handler(*args, **kwargs)
