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

        def update_player(body):
            self.player_body = body

        signaler.register('fps_update', update_fps)
        signaler.register('player_update', update_player)

    def process(self, *args, signaler, components, elapsed, **kwargs):
        for body, text in components:
            signaler.trigger('draw:text', text.text, body.as_rect())

        signaler.trigger('draw:text', '{:6.2f}'.format(self.fps),
                         Body.Rect(0, 0, 0, 0))

        pvec = 'P: {:3.2f}, {:3.2f}'.format(self.player_body.pos.x,
                                            self.player_body.pos.y)

        vvec = 'V: {:3.2f}, {:3.2f}'.format(self.player_body.vel.x,
                                            self.player_body.vel.y)

        avec = 'A: {:3.2f}, {:3.2f}'.format(self.player_body.acc.x,
                                            self.player_body.acc.y)

        print(vvec)

        signaler.trigger('draw:text', pvec, Body.Rect(900, 0, 0, 0))
        signaler.trigger('draw:text', vvec, Body.Rect(900, 30, 0, 0))
        signaler.trigger('draw:text', avec, Body.Rect(900, 60, 0, 0))
