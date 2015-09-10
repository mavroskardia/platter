from .component import Component


class Text(Component):

    def __init__(self, entity, text):
        super().__init__(entity)
        self.text = text
