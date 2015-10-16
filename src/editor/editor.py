import sys
import os
import argparse

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
from ..systems.map import MapSystem
from ..main.fps import Fps
from .. import signaler


class Editor:

    def __init__(self, basetile='base'):
        self.basetile = basetile

    def run(self):

        fps = Fps()
        fps.init()

        ecs = EntityComponentSystemManager()

        ecs.add_system(SdlSystem(), init=True)
        ecs.add_system(InputSystem(), init=True)
        ecs.add_system(MapSystem(), init=True)

        signaler.instance.register('quit', self.quit)

        self.running = True

        while self.running:
            ecs.process(fps.tick_start())
            fps.tick_end()

        return 0

    def quit(self):
        self.running = False


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Level editor for Platterman')
    parser.add_argument('-f', '--mapfile', type=str,
                        help='existing map file to edit')
    parser.add_argument('-b', '--basetile', type=str, help='map base tile')
    args = parser.parse_args()

    editor = Editor(args.basetile)
    ret = editor.run()

    sys.exit(ret)
