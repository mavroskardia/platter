import random

from ..components.position import Position
from ..components.dimensions import Dimensions
from ..components.vec2 import Vec2
from ..actors.dummy import Dummy


class Engine(object):

    def __init__(self, state=None, events=None, graphics=None,
                 *args, **kwargs):

        self.events = events
        self.graphics = graphics
        self.state = state

    def reset(self):
        for subsystem in (self.events, self.graphics, self.state):
            result, msg = subsystem.reset()
            if not result:
                print(msg)
                return False

        self.events.register('quit', lambda evt: self.quit())
        self.events.register('key:d', lambda evt: self.do_debug())
        self.events.register('key:t', lambda evt: self.do_tests())

        return True

    def run(self):
        self.done = False

        if not self.reset():
            print('Failed to reset subsystems, quitting.')
            return 1

        while not self.done:
            self.events.handle()
            self.state.update()
            # having to inject state tells me this is happening at the wrong
            # abstraction layer.
            # TODO: how to resolve?
            self.graphics.render(self.state)

        return 0

    def quit(self):
        self.done = True

    def do_debug(self):
        import pdb; pdb.set_trace()

    def do_tests(self):
        print('running tests')

        pos = Position(random.randint(0, self.graphics.resolution[0]),
                       random.randint(0, self.graphics.resolution[1]))
        dims = Dimensions(random.randint(10, 150), random.randint(10, 150))
        vel = Vec2(random.randint(-50, 50), random.randint(-50, 50))
        dummy = Dummy(pos, dims, vel)

        self.state.actors.append(dummy)
