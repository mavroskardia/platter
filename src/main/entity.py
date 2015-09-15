class Entity:

    def __init__(self, name, components=None):
        self.name = name
        self.components = components

    def __str__(self):
        return self.name

    def get_component(self, type):
        for c in self.components:
            if isinstance(c, type):
                return c
        return None
