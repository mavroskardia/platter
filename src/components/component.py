class Component:
    def __init__(self, entity, *args):
        self.entity = entity

    def __str__(self):
        return self.__class__.__name__
