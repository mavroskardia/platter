from functools import lru_cache
from collections import defaultdict


class Signaler(object):

    def __init__(self):
        self.events = defaultdict(list)

    def register(self, event_name, handler):
        self.events[event_name].append(handler)

    def unregister(self, event_name, handler):
        if handler in self.events[event_name]:
            self.events[event_name].remove(handler)

    def has_handler_for_event(self, event_name):
        return event_name in self.events and self.events[event_name]

    @lru_cache(maxsize=0)
    def trigger(self, event_name, *args, **kwargs):
        for handler in self.events[event_name]:
            handler(*args, **kwargs)
