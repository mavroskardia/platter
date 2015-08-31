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
    '.systems.map.MapSystem',
    '.systems.physical.ForceSystem',
    '.systems.physical.PositionUpdateSystem',
    '.systems.player.PlayerSystem',
    '.systems.decorations.BorderRendererSystem'
    )

entities = {
    'player': (
        ('.components.decoration.Bordered', ()),
        ('.components.physical.Acceleration', (0, 0)),
        ('.components.physical.Position', (100, 100)),
        ('.components.physical.Size', (50, 50)),
        ('.components.physical.Velocity', (0, 0)),
        ('.components.player.PlayerControl', ()),
    ),
    'notplayer': (
        ('.components.decoration.Bordered', ()),
        ('.components.physical.Position', (300, 200)),
        ('.components.physical.Size', (50, 50)),
    ),
    'notbordered': (
        ('.components.physical.Position', (100, 200)),
        ('.components.physical.Size', (50, 50)),
    )
}
