from .system import System

from .. import config

from ..loaders.spriteset import SpritesetLoader
from ..components.physical import Body
from ..components.sprite import Sprite


class SpriteSystem(System):

    componenttypes = Body, Sprite

    def init(self, signaler):
        self.spritesets = {}

    def process(self, *args, signaler, components, elapsed, **kwargs):
        for body, sprite in components:
            try:
                ss = self.spritesets[sprite.spriteset]
            except KeyError:
                ss = self.load_spriteset(signaler, sprite.spriteset, sprite)
                self.spritesets[sprite.spriteset] = ss

            data = ss[body.direction][sprite.frame]
            rect = Body.Rect(body.pos.x, body.pos.y, data.w, data.h)
            signaler.trigger('draw:texture', data.tex, rect)

            sprite.span += elapsed
            if sprite.span > sprite.interval:
                sprite.frame += 1
                sprite.span = 0.0

            if sprite.frame >= sprite.maxframes:
                sprite.frame = 0

    def load_spriteset(self, signaler, spriteset, sprite):
        print('loading spriteset', spriteset)
        loader = SpritesetLoader(signaler)
        ss = loader.load(config.spritesets[spriteset])
        sprite.maxframes = max([len(f) for f in ss.values()])

        self.spritesets[spriteset] = ss
        return ss
