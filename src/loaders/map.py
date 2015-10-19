from configparser import ConfigParser
from collections import OrderedDict
from sdl2.sdlimage import IMG_Load

from .. import signaler


class TileData:

    def __init__(self, name, texture, can_walk):
        self.name = name
        self.texture = texture
        self.can_walk = can_walk


class TilesetLoader:

    trigger = '_internal:convert_surface_to_texture'

    def load(self, filename):
        tiles = OrderedDict()
        config = ConfigParser()
        config.read(filename)

        for tilename in config.sections():
            print('loading tile', tilename)
            data = config[tilename]
            can_walk = data['walk'].lower() == 'true'

            def add(tex, w, h):
                tiles[tilename] = TileData(tilename, tex, can_walk)

            imgfile = data['file'].encode()
            signaler.instance.trigger(self.trigger, IMG_Load(imgfile), add)

        return tiles


class MapLoader:

    def load(self, filename, tileset):
        layer = []
        keys = list(tileset.keys())
        with open(filename, 'r') as f:
            x = 0
            y = 0
            for line in f:
                for c in line:
                    try:
                        key = keys[int(c)]
                        print('{}, {}: {}'.format(x, y, key))
                        layer.append(tileset[key])
                    except ValueError:
                        pass
                    x += 1
                y += 1
                x = 0
        return layer
