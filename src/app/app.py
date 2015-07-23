from ..engine.engine import Engine
from ..graphics.sdl import SdlGraphics
from ..input.sdl import SdlInput
from ..state.base import BaseGameState


class App(object):
    '''App's job is to compose all of the engine subsystems, send them to
       the engine runner, kick off the runner, then return whatever
       exit code at the end.
    '''

    def __init__(self, *args, **kwargs):
        resolution = kwargs.pop('resolution', (1280, 790))
        graphics = kwargs.pop('graphics', SdlGraphics(resolution=resolution))
        input = kwargs.pop('input', SdlInput())
        state = kwargs.pop('state', BaseGameState())

        self.engine = kwargs.pop('engine', Engine(state=state,
                                                  graphics=graphics,
                                                  input=input,
                                                  *args, **kwargs))

    def run(self):
        return self.engine.run()
