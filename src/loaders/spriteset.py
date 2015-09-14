from configparser import ConfigParser
from collections import defaultdict

from ..config import config
from ..main.signaler import Signaler


class SpritesetLoader:

    def __init__(self, signaler):
        self.signaler = signaler

    def load(self, filename):
        parsed_spriteset = ConfigParser()
        parsed_spriteset.read(filename)

        spriteset = defaultdict(list)

        for direction in parsed_spriteset.sections():
            frames = parsed_spriteset[direction]

            def add_to_spriteset(texture):
                spriteset[direction].append(texture)

            for frame in frames:
                imgfile = frames[frame].encode()
                signaler.trigger('_internal:convert_surface_to_texture',
                                 IMG_Load(imgfile), add_to_spriteset)

        return spriteset


if __name__ == '__main__':

    import os
    os.environ['PYSDL2_DLL_PATH'] = 'lib'

    from sdl2 import *
    from sdl2.sdlimage import *

    def f(surface, cb, *args):
        print('called convert for', surface)
        cb(surface)

    signaler = Signaler()
    signaler.register('_internal:convert_surface_to_texture', f)

    ssl = SpritesetLoader(signaler)
    spriteset = ssl.load(config.default_spriteset)
