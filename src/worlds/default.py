from ..components.bordered import Bordered
from ..components.force import Force
from ..components.position import Position
from ..components.size import Size
from ..components.velocity import Velocity
from ..components.player_controls import PlayerControls
from ..components.worldbound import WorldBound
from ..engine.entity import Entity


class DefaultWorld:

    def __init__(self, dimensions):

        self.systems = (
            # core systems
            '.systems.sdl_core_handler.SdlCoreHandler',
            '.systems.default_input_handler.DefaultInputHandler',
            '.systems.window_handler.WindowHandler',
            # world-based systems
            '.systems.movement_updater.MovementUpdater',
            '.systems.force_updater.ForceUpdater',
            '.systems.constraints.WorldBoundConstrainer',
            '.systems.border_renderer.BorderRenderer',
            '.systems.player_input_handler.PlayerInputHandler',
            '.systems.movement_updater.PlayerMovementUpdater',
        )

        self.entities = {
            'Player': (Bordered(), Force(0, 0), Position(100, 100),
                       Velocity(0, 0), Size(50, 50), PlayerControls()),
            'Ground': (Bordered(), Velocity(0, 0), Size(dimensions[0], 10),
                       Position(0, 700), Force(0, 0), WorldBound(*dimensions))
        }
