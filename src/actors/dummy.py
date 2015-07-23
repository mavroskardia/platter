from sdl2 import *


class Dummy(object):

    def __init__(self, pos, dims, vel):
        self.rect = SDL_Rect(pos.x, pos.y, dims.w, dims.h)
        self.vel = vel

    def render(self, r):

        SDL_SetRenderDrawColor(r, 255, 255, 255, 255)
        SDL_RenderDrawRect(r, self.rect)

    def update(self):
        self.rect.x += self.vel.x
        self.rect.y += self.vel.y

        self.vel.x = int(self.vel.x * 0.99)
        self.vel.y = int(self.vel.y * 0.99)
