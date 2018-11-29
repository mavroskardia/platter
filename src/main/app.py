import sys
import os

try:
    if sys.platform == 'win32':
        os.environ['PYSDL2_DLL_PATH'] = 'lib'
    from sdl2 import *
    from sdl2.sdlttf import *
except ImportError:
    print('You have to have pysdl2 installed and'
          ' the sdl2 dlls in the lib directory')
    sys.exit(1)

from .fps import Fps
from .ecs import EntityComponentSystemManager

from .. import signaler
from .. import config


class TitleApp:

    def __init__(self):
        def set_renderer(renderer):
            self.renderer = renderer

        signaler.instance.trigger('get_renderer', set_renderer)

    def run(self):

        font = TTF_OpenFont(config.title_font.encode(), config.title_font_size)

        ts = TTF_RenderUTF8_Blended(font, 'Platterman'.encode(),
                                    SDL_Color(255, 255, 255, 255))

        title = SDL_CreateTextureFromSurface(self.renderer, ts)
        title_rect = SDL_Rect(100, 100, ts.contents.w, ts.contents.h)

        while True:

            evt = SDL_Event()
            while SDL_PollEvent(evt):
                if evt.type == SDL_QUIT:
                    return False
                elif evt.type == SDL_KEYDOWN:
                    if evt.key.keysym.scancode == SDL_SCANCODE_RETURN:
                        return True

            SDL_RenderCopy(self.renderer, title, None, title_rect)
            SDL_RenderPresent(self.renderer)
            SDL_SetRenderDrawColor(self.renderer, 0, 0, 0, 255)
            SDL_RenderClear(self.renderer)

        return False


class App:

    def __init__(self):
        self.ecs = EntityComponentSystemManager()
        self.fps = Fps()

    def run(self):

        self.register_global_events()
        self.fps.init()

        self.ecs.init_systems()

        if not TitleApp().run():
            return

        self.ecs.init_entities()

        self.running = True

        while self.running:
            dt = self.fps.tick_start()
            self.ecs.process(dt)
            self.fps.tick_end()

    def register_global_events(self):
        s = signaler.instance
        s.register('add_entity', self.ecs.add_entity)
        s.register('quit', self.quit)
        s.register('keydown:Escape', self.quit)
        s.register('keydown:D', self.debug)
        s.register('remove_component', self.ecs.remove_component)
        s.register('add_component', self.ecs.add_component)

    def quit(self):
        self.running = False

    def debug(self):
        print('FPS:', self.fps)
        # import pdb
        # pdb.set_trace()


if __name__ == '__main__':

    if len(sys.argv) == 1:
        App().run()
    elif sys.argv[1] == 'profile':
        import cProfile
        import io
        import pstats
        profile = cProfile.Profile()
        profile.enable()
        try:
            App().run()
        except:
            pass
        profile.disable()
        sortby = 'cumulative'
        with open('profile.log', 'w') as f:
            ps = pstats.Stats(profile, stream=f).sort_stats(sortby)
            ps.print_stats()
