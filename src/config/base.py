import os
from .constants import *

title = 'On a Platter'
resolution = (1280, 790)

core = Sdl, Input
physical = Gravity, Force, CollisionDetection, PositionUpdate, PlayerInput
game = Map, SpriteSystem
debug = BorderRenderer, Hud

systems = core + physical + game + debug
