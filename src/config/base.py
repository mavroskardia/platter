import os
from .constants import *

title = 'On a Platter'
resolution = (1280, 790)

core = SdlInitSystem, SdlWindowSystem, InputSystem
physical = Gravity, Force, CollisionDetection, PositionUpdate, PlayerInput
game = Map,
debug = BorderRenderer, Hud

systems = core + physical + game + debug
# systems = core + physical + debug
