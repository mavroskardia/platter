import os
from .constants import *

title = 'On a Platter'
resolution = (1280, 790)

sdl = Sdl, Input
# physical = PlayerInput, Gravity, Force, CollisionDetection, PositionUpdate
physical = PlayerInput, Physics, PositionUpdate
game = Map, SpriteSystem, PlayerDataSystem
debug = BorderRenderer,  # Hud

systems = sdl + physical + game + debug
