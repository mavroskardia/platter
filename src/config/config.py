import os

from collections import OrderedDict
from .constants import *

# General

title = 'On a Platter'
resolution = (1280, 790)

tileset = 'tile.set'
tile_width = 32
tile_height = 32

default_spriteset = 'sprite.set'

# Fonts

hud_font = os.path.join('resources', 'aard.ttf')
hud_font_size = 32

# Constant Values

gravity = 2.0
air_friction_x = 0.95
air_friction_y = 0.9
base_friction = 0.99

# Systems

core_systems = SdlInitSystem, SdlWindowSystem, InputSystem,

game_systems = ()  # Map,

physical_systems = (Gravity, Force, CollisionDetection, PositionUpdate,
                    PlayerInput,)

debug_systems = BorderRenderer, Hud

systems = core_systems + game_systems + physical_systems + debug_systems

# Seeded Entities

entities = OrderedDict()

entities['player'] = {
    Bordered: None,
    AffectedByGravity: None,
    CanCollide: None,
    PlayerControl: None,
    Body: (None, {'x': 100, 'y': 300, 'w': 50, 'h': 50, 'vx': 0, 'vy': 0,
                  'nx': 0, 'ny': 0, 'fx': 0, 'fy': 0}),
}

entities['ground'] = {
    Bordered: None,
    CanCollide: None,
    Body: (None, {'x': 0, 'y': resolution[1] - 50, 'w': resolution[0],
                  'h': 50, 'vx': 0, 'vy': 0, 'nx': 0, 'ny': -gravity,
                  'fx': base_friction, 'fy': 1.0}),
}

entities['platform'] = {
    Bordered: None,
    CanCollide: None,
    Body: (None, {'x': 100, 'y': 500, 'w': 200, 'h': 50, 'vx': 0, 'vy': 0,
                  'nx': -10.0, 'ny': -gravity,
                  'fx': base_friction, 'fy': 1.0}),
}

entities['obstacle'] = {
    Bordered: None,
    CanCollide: None,
    Body: (None, {'x': 400, 'y': 690, 'w': 200, 'h': 50, 'vx': 0, 'vy': 0,
                  'nx': -10.0, 'ny': -gravity,
                  'fx': base_friction, 'fy': 1.0}),
}

entities['collider1'] = {
    Bordered: None,
    CanCollide: None,
    Body: (None, {'x': 100, 'y': 100, 'w': 50, 'h': 50, 'vx': 1000, 'vy': 0,
                  'ax': 10.0, 'ay': 0, 'nx': 0.0, 'ny': 0.0})
}

entities['collider2'] = {
    Bordered: None,
    CanCollide: None,
    Body: (None, {'x': 900, 'y': 100, 'w': 50, 'h': 50, 'vx': -1000, 'vy': 0,
                  'ax': -10.0, 'ay': 0, 'nx': 0.0, 'ny': 0.0})
}

entities['testtext'] = {
    Text: (('Hello, World!',), None),
    Body: (None, {'x': 700, 'y': 10, 'w': 500, 'h': 20})
}
