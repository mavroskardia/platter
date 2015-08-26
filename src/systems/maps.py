from sdl2 import SDL_CreateTexture
from sdl2.sdlimage import IMG_Load

from . import system
from ..components.tiles import Tile
from ..components.size import Size
from ..components.position import Position
from ..components.collisions import CanCollide
from ..config import config


class TileData:

    def __init__(self, surface=None, can_walk=True, **kwargs):
        self.surface = surface
        self.can_walk = can_walk


class Tileset:

    trigger = '_internal:convert_surface_to_texture_and_add_to_tileset'

    def __init__(self, tileset_filename, signaler):
        self.tiles = {}

        with open(tileset_filename, 'r') as f:
            for line in f:
                tile_name, img_file, can_walk = self.parse_line(line)
                signaler.trigger(self.trigger, self.tiles,
                                 IMG_Load(img_file.encode()),
                                 tile_name)

                self.tiles[tile_name] = TileData(surface=self.tiles[tile_name],
                                                 can_walk=can_walk)

    def parse_line(self, line):
        line, *endofline = line.split('\n')
        tile_and_file, *params = line.split(' ')
        tile_name, img_file, *rest2 = tile_and_file.split('=')
        can_walk = True

        for p in params:
            key, value = p.split('=')
            if key == 'can_walk' and value == 'False':
                can_walk = False

        return tile_name, img_file, can_walk

    def get(self, t):
        return self.tiles.get(t, None)


class TileHandler(system.System):

    componenttypes = Tile, Position, Size

    def init(self, signaler):
        self.tileset = Tileset(config.tileset, signaler)
        self.first_process = True

    def set_walkability(self, signaler, components):
        for p, s, t in components:
            tile = self.tileset.get(t.name)
            if tile and not tile.can_walk:
                print('adding collision to tile')
                signaler.trigger('add component', t.entity, CanCollide())

    def process(self, signaler, components):

        if self.first_process:
            print('processing map...', end='')
            self.set_walkability(signaler, components)
            self.first_process = False
            print('done')

        for p, s, t in components:

            todraw = self.tileset.get(t.name)

            if todraw:
                signaler.trigger('draw:texture', p, s, todraw.surface)
