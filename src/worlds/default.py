from ..components.bordered import Bordered
from ..components.force import Force
from ..components.position import Position
from ..components.size import Size
from ..components.velocity import Velocity
from ..components.player_controls import PlayerControls
from ..components.worldbound import WorldBound
from ..components.collisions import CanCollide, Static
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
            '.systems.collision_detection.CollisionDetection',
        )

        self.entities = {
            'Player': (Bordered(), CanCollide(), Force(0, 0), Size(50, 50),
                       Position(100, 100), Velocity(0, 0), PlayerControls(),
                       WorldBound(*dimensions)),
            'Ground': (Bordered(), Velocity(0, 0), Size(dimensions[0], 10),
                       Position(0, 700), Force(0, 0), WorldBound(*dimensions),
                       CanCollide(), Static())
        }
