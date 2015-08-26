from ..components.bordered import Bordered
from ..components.forces import AffectedByGravity
from ..components.position import Position
from ..components.size import Size
from ..components.velocity import Velocity
from ..components.player_controls import PlayerControls
from ..components.worldbound import WorldBound
from ..components.collisions import CanCollide, Static
from ..components.tiles import Tile
from ..engine.entity import Entity


class TileWorld:

    def __init__(self, dimensions, *args, **kwargs):

        self.systems = (
            # core systems
            '.systems.sdl_core_handler.SdlCoreHandler',
            '.systems.default_input_handler.DefaultInputHandler',
            '.systems.window_handler.WindowHandler',
            # game systems
            '.systems.maps.TileHandler',
            '.systems.player_input_handler.PlayerInputHandler',
            '.systems.movement_updater.MovementUpdater',
            '.systems.movement_updater.VelocityUpdater',
            '.systems.movement_updater.PlayerMovementUpdater',
            '.systems.collision_detection.CollisionDetection',
            '.systems.constraints.WorldBoundConstrainer',
            '.systems.border_renderer.BorderRenderer',
        )

        self.entities = self.load_map(dimensions, **kwargs)

    def load_map(self, dims, *args, **kwargs):

        ret = {}
        ts = kwargs.get('tilesize', 32)
        bg = kwargs.get('bg', None)
        mapfile = kwargs.get('worldfile', 'world.map')

        px, py = 0, 0

        with open(mapfile, 'r') as f:
            y = 0
            for line in f:
                x = 0
                for c in line:
                    if c == '\n':
                        continue
                    if c == 'P':
                        px, py = x * ts, y * ts
                        print('Player starting point: ({},{})'.format(px, py))
                    tilename = 'Tile "{}" ({},{})'.format(c, x, y)
                    ret[tilename] = (Tile(c), Position(x*ts, y*ts), Size(ts, ts),)
                    x += 1
                y += 1

        print('loaded map with {} tiles'.format(len(ret)))

        if bg:
            ret['bg'] = bg

        ret['Player'] = (PlayerControls(), Bordered(), Position(px, py),
                         Size(ts, ts), Velocity(0, 0), WorldBound(*dims),
                         CanCollide())

        return ret


class DefaultWorld:

    def __init__(self, dimensions):

        self.systems = (
            # core systems
            '.systems.sdl_core_handler.SdlCoreHandler',
            '.systems.default_input_handler.DefaultInputHandler',
            '.systems.window_handler.WindowHandler',
            # world-based systems
            '.systems.movement_updater.VelocityUpdater',
            '.systems.movement_updater.MovementUpdater',
            '.systems.movement_updater.PlayerMovementUpdater',
            '.systems.constraints.WorldBoundConstrainer',
            '.systems.border_renderer.BorderRenderer',
            '.systems.player_input_handler.PlayerInputHandler',
            '.systems.collision_detection.CollisionDetection',
        )

        self.entities = {
            'Player': (Bordered(), CanCollide(), Size(50, 50),
                       AffectedByGravity(), Position(100, 100), Velocity(0, 0),
                       PlayerControls(), WorldBound(*dimensions)),
            'Ground': (Bordered(), Velocity(0, 0), Size(dimensions[0], 10),
                       Position(0, 700), WorldBound(*dimensions),
                       CanCollide(), Static())
        }
