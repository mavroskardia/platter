from . import system


class HudSystem(system.System):

    componenttypes = Body, Text

    def process(self, *args, signaler, components, elapsed, **kwargs):

        for body, text in components:
            pass