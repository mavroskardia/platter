import sys
import os

try:
    os.environ['PYSDL2_DLL_PATH'] = 'lib'
    from sdl2 import *
except:
    sys.exit(1)


class Editor:

    def __init__(self):
        self.running = False
        self.window = None
        self.renderer = None

    def run(self):
        self.running = True

        self.init()

        while self.running:

            self.handle_events()
            self.update_state()
            self.render()
            SDL_Delay(15)

    def init(self):
        SDL_Init(SDL_INIT_EVERYTHING)
        self.window = SDL_CreateWindow("Level Editor".encode(),
                                       SDL_WINDOWPOS_CENTERED,
                                       SDL_WINDOWPOS_CENTERED,
                                       800, 600,
                                       SDL_WINDOW_SHOWN)
        self.renderer = SDL_CreateRenderer(self.window, -1,
                                           SDL_RENDERER_ACCELERATED)

    def handle_events(self):
        evt = SDL_Event()

        while SDL_PollEvent(evt):

            if evt.type == SDL_QUIT:
                self.running = False

    def update_state(self):
        pass

    def render(self):
        SDL_SetRenderDrawColor(self.renderer, 0, 0, 0, 255)
        SDL_RenderClear(self.renderer)

        # draw state

        SDL_RenderPresent(self.renderer)


if __name__ == '__main__':

    mapfile = sys.argv[1]

    Editor().run()
