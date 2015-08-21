from sdl2 import SDL_CreateTexture
from sdl2.sdlimage import IMG_Load

from . import system
from ..components.tiles import Tile
from ..components.size import Size
from ..components.position import Position
from ..config import config


class Tileset:

    trigger = '_internal:convert_surface_to_texture_and_add_to_tileset'

    def __init__(self, tileset_filename, signaler):
        self.tiles = {}

        with open(tileset_filename, 'r') as f:
            for line in f:
                tile_name, img_file, *rest = line.split('=')
                signaler.trigger(self.trigger, self.tiles,
                                 IMG_Load(img_file.encode()),
                                 tile_name)

    def get(self, t):
        return self.tiles.get(t, None)


class TileHandler(system.System):

    componenttypes = Tile, Position, Size

    def init(self, signaler):
        self.tileset = Tileset(config.tileset, signaler)

    def process(self, signaler, components):

        for p, s, t in components:

            todraw = self.tileset.get(t.encodedvalue)

            if todraw:
                signaler.trigger('draw:texture', p, s, todraw)
