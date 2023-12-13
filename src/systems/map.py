from collections import OrderedDict
from sdl2 import *

from .system import System

from .. import config
from .. import signaler

from ..main.entity import Entity
from ..math.vector import Vec
from ..components.map import Tile
from ..components.physical import Body
from ..loaders.map import TilesetLoader, MapLoader


class MapSystem(System):

    def init(self, *args, **kwargs):
        self.map_width = kwargs.pop('width', config.map_width)
        self.map_height = kwargs.pop('height', config.map_height)
        self.map_file = kwargs.pop('map_file', config.map_file)
        self.screen_tiles_wide = config.resolution[0] // config.tile_width
        self.screen_tiles_tall = config.resolution[1] // config.tile_height
        self.offset = Vec(0, 0)
        self.set_renderer()
        self.init_map()
        signaler.instance.register('get:map', self.get_map)
        signaler.instance.register('handle_tile_collision', self.check_collide)
        signaler.instance.register('get:tile_at', self.get_tile_at_cb)

    def get_map(self, cb):
        cb(self)

    def check_collide(self, nextpos, shape, cb, nocb):
        x, y = nextpos.x, nextpos.y

        if shape.direction == 'right':
            x += shape.w

        if shape.direction != 'up':
            y += shape.h

        t = self.get_tile_at(x, y)
        if t.can_walk:
            cb(nextpos, shape)
        else:
            nocb(nextpos, shape)

    def get_tile_at(self, x, y, layer='base'):
        tx = int(x // config.tile_width)
        ty = int(y // config.tile_height)
        return self.layers[layer][ty * self.map_width + tx]

    def get_tile_at_cb(self, pos, cb, *args):
        cb(self.get_tile_at(pos.x, pos.y), pos, *args)

    def set_renderer(self):
        def setr(renderer):
            self.renderer = renderer

        signaler.instance.trigger('get_renderer', setr)

    def init_map(self):
        self.tileset = TilesetLoader().load(config.tileset)
        self.layers = OrderedDict()
        if self.map_file:
            self.layers['base'] = MapLoader().load(self.map_file, self.tileset)
        else:
            self.layers['base'] = [self.tileset['base']
                                   for _ in
                                   range(self.map_width * self.map_height)]

        print('made base layer with {} tiles'.format(len(self.layers['base'])))

    def process(self, *args, components, elapsed, **kwargs):
        '''
            first determine where in the map to draw based on the offset,
            then grab the tiles in those bounds
            [xxxxxx(xxxxx)xxx]
        '''

        start_x_tile = self.offset.x // config.tile_width
        start_y_tile = self.offset.y // config.tile_height

        for layer, tiles in self.layers.items():
            for x in range(start_x_tile, self.screen_tiles_wide + 1):
                for y in range(start_y_tile, self.screen_tiles_tall + 1):
                    tile = tiles[y * self.map_width + x]
                    if not tile:
                        continue
                    tex = self.tileset[tile.name].texture
                    SDL_RenderCopy(self.renderer, tex, None,
                                   SDL_Rect(
                                    x*config.tile_width, y*config.tile_height,
                                    config.tile_width, config.tile_height))











































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
