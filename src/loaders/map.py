from configparser import ConfigParser
from collections import OrderedDict
from sdl2.sdlimage import IMG_Load

from .. import signaler
from .. import config


class TileData:

    def __init__(self, name, texture, can_walk):
        self.name = name
        self.texture = texture
        self.can_walk = can_walk


class TilesetLoader:

    trigger = '_internal:convert_surface_to_texture'

    def load(self, filename):
        tiles = OrderedDict()
        cp = ConfigParser()
        cp.read(filename)

        for tilename in cp.sections():
            print('loading tile', tilename)
            data = cp[tilename]
            can_walk = data['walk'].lower() == 'true'

            def add(tex, w, h):
                assert w == config.tile_width, 'Tile width did not match'
                assert h == config.tile_height, 'Tile height did not match'
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
