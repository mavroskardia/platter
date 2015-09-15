from . import system
from .. import config

from ..main.entity import Entity
from ..math.vector import Vec
from ..components.map import Tile
from ..components.physical import Body
from ..loaders.map import MapLoader


class MapSystem(system.System):

    componenttypes = Body, Tile

    def init(self, signaler):
        self.tileset = MapLoader(signaler).load(config.tileset)
        basetile = self.tileset['base']

        w = config.resolution[0] // config.tile_width
        h = config.resolution[1] // config.tile_height + 1

        tile_entities = []

        for x in range(w):
            for y in range(h):
                name = 'Tile "{}" ({}, {})'.format(basetile.name, x, y)
                entity = Entity(name)
                tile = Tile(entity, basetile.name)
                body = Body(entity)
                body.pos = Vec(x * config.tile_width, y * config.tile_height)
                entity.components = [body, tile]
                tile_entities.append(entity)

        print('going to add tiles')
        for e in tile_entities:
            print('adding', e)
            signaler.trigger('add_entity', e)
        print('done')

    def process(self, *args, signaler, components, elapsed, **kwargs):
        for body, tile in components:
            texture = self.tileset[tile.name].texture
            signaler.trigger('draw:texture', body, texture)
