from configparser import ConfigParser
from sdl2.sdlimage import IMG_Load

from .. import signaler


class TileData:

    def __init__(self, name, texture, can_walk):
        self.name = name
        self.texture = texture
        self.can_walk = can_walk


class MapLoader:

    trigger = '_internal:convert_surface_to_texture'

    def load(self, filename):
        tiles = {}
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
