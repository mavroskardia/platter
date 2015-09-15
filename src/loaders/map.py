from configparser import ConfigParser
from sdl2.sdlimage import IMG_Load


class TileData:

    def __init__(self, name, texture, can_walk):
        self.name = name
        self.texture = texture
        self.can_walk = can_walk


class MapLoader:

    trigger = '_internal:convert_surface_to_texture'

    def __init__(self, signaler):
        self.signaler = signaler

    def load(self, filename):
        tiles = {}
        config = ConfigParser()
        config.read(filename)

        for tilename in config.sections():
            print('loading tile', tilename)
            data = config[tilename]
            can_walk = data['walk'].lower() == 'true'

            def add(tex):
                tiles[tilename] = TileData(tilename, tex, can_walk)

            imgfile = data['file'].encode()
            self.signaler.trigger(self.trigger, IMG_Load(imgfile), add)

        return tiles
