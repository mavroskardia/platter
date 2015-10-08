from .system import System

from .. import config
from .. import signaler

from ..loaders.spriteset import SpritesetLoader
from ..components.physical import Body
from ..components.sprite import Sprite


class SpriteSystem(System):

    componenttypes = Body, Sprite

    def init(self):
        self.spritesets = {}

    def process(self, *args, components, elapsed, **kwargs):
        for body, sprite in components:
            try:
                ss = self.spritesets[sprite.spriteset]
            except KeyError:
                ss = self.load_spriteset(sprite.spriteset, sprite)
                self.spritesets[sprite.spriteset] = ss

            data = ss[body.direction][sprite.frame]
            rect = Body.Rect(body.pos.x, body.pos.y, data.w, data.h)
            signaler.instance.trigger('draw:texture', data.tex, rect)

            if not body.moving:
                continue

            sprite.span += elapsed
            if sprite.span > sprite.interval:
                sprite.frame += 1
                sprite.span = 0.0

            if sprite.frame >= sprite.maxframes:
                sprite.frame = 0

    def load_spriteset(self, spriteset, sprite):
        print('loading spriteset', spriteset)

        loader = SpritesetLoader()
        ss = loader.load(config.spritesets[spriteset])

        sprite.maxframes = max([len(f) for f in ss.values()])
        sprite.interval = 1.0 / sprite.maxframes

        self.spritesets[spriteset] = ss
        return ss
