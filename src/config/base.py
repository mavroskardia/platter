import os
from .constants import *

title = 'On a Platter'
resolution = (1280, 790)

core = Sdl, Input
physical = PlayerInput, Gravity, Force, CollisionDetection, PositionUpdate
game = Map, SpriteSystem
debug = BorderRenderer, Hud

systems = core + physical + game + debug
