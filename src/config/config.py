title = 'On a Platter'

resolution = (1280, 790)

tileset = 'tile.set'
tile_width = 32
tile_height = 32

systems = (
    # core systems
    '.systems.sdlcore.SdlInitSystem',
    '.systems.sdlcore.SdlWindowSystem',
    '.systems.input.InputSystem',
    # game systems
    # '.systems.map.MapSystem',
    # the physical systems must be in this order
    '.systems.physical.GravitySystem',
    '.systems.physical.GravityCollisionSystem',
    '.systems.physical.AccelerationSystem',
    '.systems.physical.FrictionSystem',
    '.systems.physical.CollisionDetectionSystem',
    '.systems.physical.PositionUpdateSystem',
    '.systems.player.PlayerSystem',
    # debugging systems
    '.systems.decorations.BorderRendererSystem'
    )

entities = {
    'player': (
        ('.components.decoration.Bordered', ()),
        ('.components.physical.Acceleration', (0, 0)),
        ('.components.physical.AffectedByGravity', ()),
        ('.components.physical.CanCollide', ()),
        ('.components.player.PlayerControl', ()),
        ('.components.physical.Position', (100, 100)),
        ('.components.physical.Size', (50, 50)),
        ('.components.physical.Velocity', (0, 0)),
    ),
    'ground': (
        ('.components.decoration.Bordered', ()),
        ('.components.physical.CanCollide', ()),
        ('.components.physical.Position', (0, resolution[1]-50)),
        ('.components.physical.Size', (resolution[0], 50)),
        ('.components.physical.Velocity', (0, 0)),
    ),
    'platform': (
        ('.components.decoration.Bordered', ()),
        ('.components.physical.CanCollide', ()),
        ('.components.physical.Position', (100, 500)),
        ('.components.physical.Size', (200, 50)),
        ('.components.physical.Velocity', (0, 0)),
    )
}
