title = 'On a Platter'

resolution = (1280, 790)

systems = (
    '.systems.sdlcore.SdlInitSystem',
    '.systems.sdlcore.SdlWindowSystem',
    '.systems.input.InputSystem',
    # game systems
    '.systems.decorations.BorderRendererSystem'
    )

entities = {
    'player': (
        ('.components.decoration.Bordered', ()),
        ('.components.physical.Position', (100, 100)),
        ('.components.physical.Size', (50, 50)),
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
