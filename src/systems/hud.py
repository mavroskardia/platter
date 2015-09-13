from . import system
from ..components.physical import Body
from ..components.hud import Text


class HudSystem(system.System):

    componenttypes = Body, Text

    def process(self, *args, signaler, components, elapsed, **kwargs):

        for body, text in components:
            signaler.trigger('draw:text', body, text)
