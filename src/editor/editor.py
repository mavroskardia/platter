import sys
import os

try:
    os.environ['PYSDL2_DLL_PATH'] = 'lib'
    from sdl2 import *
    from sdl2.sdlttf import *
except ImportError:
    print('Could not import SDL2')
    sys.exit(1)


from ..main.ecs import EntityComponentSystemManager
from ..systems.sdl import SdlSystem
from ..systems.input import InputSystem
from ..main.fps import Fps
from .. import signaler

running = True


class Editor:

    def run(self):

        fps = Fps()
        fps.init()

        ecs = EntityComponentSystemManager()

        ecs.add_system(SdlSystem(), init=True)
        ecs.add_system(InputSystem(), init=True)

        def quit():
            running = False

        signaler.instance.register('quit', quit)

        while running:
            ecs.process(fps.tick_start())
            fps.tick_end()


if __name__ == '__main__':

    editor = Editor()
    ret = editor.run()

    sys.exit(ret)
