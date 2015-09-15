from .system import System
from ..components.physical import Body
from ..components.hud import Text


class HudSystem(System):

    componenttypes = Body, Text

    # TODO: cache the fps texture and update it instead of building it
    #       anew each cycle

    def init(self, signaler):
        self.fps = 0

        def update_fps(fps):
            self.fps = fps

        signaler.register('fps_update', update_fps)

    def process(self, *args, signaler, components, elapsed, **kwargs):
        for body, text in components:
            signaler.trigger('draw:text', text.text, body.as_rect())

        signaler.trigger('draw:text', '{:6.2f}'.format(self.fps),
                         Body.Rect(0, 0, 0, 0))
