from collections import OrderedDict
from .constants import *

# General

title = 'On a Platter'
resolution = (1280, 790)
tileset = 'tile.set'
tile_width = 32
tile_height = 32

# Constant Values

gravity = 2.0

# Systems

core_systems = SdlInitSystem, SdlWindowSystem, InputSystem,

game_systems = ()  # Map,

physical_systems = (Gravity, Force, CollisionDetection, PositionUpdate,
                    PlayerInput,)

debug_systems = BorderRenderer,

systems = core_systems + game_systems + physical_systems + debug_systems

# Seeded Entities

entities = OrderedDict()

entities['player'] = {
    Bordered: None,
    AffectedByGravity: None,
    CanCollide: None,
    PlayerControl: None,
    Body: (None, {'x': 100, 'y': 100, 'w': 50, 'h': 50, 'vx': 0, 'vy': 0,
                  'nx': 0, 'ny': 0}),
}

entities['ground'] = {
    Bordered: None,
    CanCollide: None,
    Body: (None, {'x': 0, 'y': resolution[1] - 50, 'w': resolution[0],
                  'h': 50, 'vx': 0, 'vy': 0, 'nx': 0, 'ny': -gravity}),
}

entities['platform'] = {
    Bordered: None,
    CanCollide: None,
    Body: (None, {'x': 100, 'y': 500, 'w': 200, 'h': 50, 'vx': 0, 'vy': 0,
                  'nx': -10.0, 'ny': -gravity}),
}

entities['obstacle'] = {
    Bordered: None,
    CanCollide: None,
    Body: (None, {'x': 400, 'y': 690, 'w': 200, 'h': 50, 'vx': 0, 'vy': 0,
                  'nx': -10.0, 'ny': -gravity}),
}
