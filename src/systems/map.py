from configparser import ConfigParser

import os
try:
    os.environ['PYSDL2_DLL_PATH'] = 'lib'
except:
    pass

from sdl2.sdlimage import IMG_Load

from . import system
from ..config import config
from ..components.map import Tile
from ..components.physical import Size, Position


class TileData:

    def __init__(self, name, texture, can_walk):
        self.name = name
        self.texture = texture
        self.can_walk = can_walk


class TileSet:

    trigger = '_internal:convert_surface_to_texture'

    def __init__(self, tileset_filename, signaler):
        self.tiles = {}
        self.parse_tileset(tileset_filename, signaler)

    def parse_tileset(self, filename, signaler):
        config = ConfigParser()
        config.read(filename)

        for tilename in config.sections():
            section = config[tilename]
            can_walk = section['walk'].lower() == 'true'
            signaler.trigger(self.trigger,
                             IMG_Load(section['file'].encode()),
                             lambda tex: self.add_to_tiles(tilename,
                                                           tex,
                                                           can_walk))

    def add_to_tiles(self, name, texture, can_walk):
        self.tiles[name] = TileData(name, texture, can_walk)

    def get_base_tile(self):
        return self.tiles.get('base', None)


class MapSystem(system.System):

    componenttypes = Position, Size, Tile

    def init(self, signaler):
        tile_file = os.path.join('resources', config.tileset)
        self.tileset = TileSet(tile_file, signaler)
        base_tile = self.tileset.get_base_tile()

        w = config.resolution[0] // config.tile_width
        h = config.resolution[1] // config.tile_height + 1

        size = Size(config.tile_width, config.tile_height)
        tile = Tile(base_tile.name)

        for x in range(w):
            for y in range(h):
                name = 'Tile "{}" ({}, {})'.format(base_tile.name, x, y)
                pos = Position(x * config.tile_width, y * config.tile_height)
                signaler.trigger('add_entity', name, [pos, size, tile])

    def process(s, *args, signaler=None, components=None, elapsed=0, **kargs):
        for pos, size, tile in components:
            texture = s.tileset.tiles[tile.name].texture
            signaler.trigger('draw:texture', pos, size, texture)
