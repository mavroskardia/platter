import os

from sdl2.sdlimage import IMG_Load

from configparser import ConfigParser
from collections import defaultdict

from .. import config
from ..main.signaler import Signaler


class SpriteData:

    def __init__(self, tex, w, h):
        self.tex = tex
        self.w = w
        self.h = h


class SpritesetLoader:

    def __init__(self, signaler):
        self.signaler = signaler

    def load(self, filename):
        parsed_spriteset = ConfigParser()
        parsed_spriteset.read(filename)

        spriteset = defaultdict(list)

        for section_name in parsed_spriteset.sections():
            frames = parsed_spriteset[section_name]

            def add_to_spriteset(texture, w, h):
                sd = SpriteData(texture, w, h)
                spriteset[section_name].append(sd)

            for frame in frames:
                imgfile = os.path.join(os.path.dirname(filename),
                                       frames[frame]).encode()

                self.signaler.trigger('_internal:convert_surface_to_texture',
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
