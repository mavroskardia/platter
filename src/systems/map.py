from sdl2 import *

from .system import System

from .. import config
from .. import signaler
from ..main.entity import Entity
from ..math.vector import Vec
from ..components.map import Tile
from ..components.physical import Body
from ..loaders.map import MapLoader


class MapSystem(System):

    def process(self, *args, components, elapsed, **kwargs):
        self.tileset = MapLoader().load(config.tileset)
        basetile = self.tileset['base']

        # keep tile flyweight












































class OldMapSystem(System):

    componenttypes = Tile,

    def init(self):
        self.set_renderer()
        self.create_map()

    def set_renderer(self):
        def setr(renderer):
            self.renderer = renderer

        signaler.instance.trigger('get_renderer', setr)

    def create_map(self):
        self.tileset = MapLoader().load(config.tileset)
        basetile = self.tileset['base']

        w = config.resolution[0] // config.tile_width
        h = config.resolution[1] // config.tile_height + 1

        tile_entities = []

        for x in range(w):
            for y in range(h):
                name = 'Tile "{}" ({}, {})'.format(basetile.name, x, y)
                entity = Entity(name)
                pos = Vec(x * config.tile_width, y * config.tile_height)
                tile = Tile(entity, basetile.name, pos)
                entity.components = [tile]
                tile_entities.append(entity)

        for e in tile_entities:
            signaler.instance.trigger('add_entity', e)

    def process(self, *args, components, elapsed, **kwargs):
        for tile, in components:
            texture = self.tileset[tile.name].texture
            x, y, w, h = (tile.pos.x, tile.pos.y,
                          config.tile_width, config.tile_height)
            SDL_RenderCopy(self.renderer, texture, None, SDL_Rect(x, y, w, h))
