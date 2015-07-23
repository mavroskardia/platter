class Engine(object):

    def __init__(self, state=None, input=None, graphics=None, *args, **kwargs):
        self.input = input
        self.graphics = graphics
        self.state = state

    def reset(self):
        for subsystem in (self.input, self.graphics, self.state):
            result, msg = subsystem.reset()
            if not result:
                print(msg)
                return False

        self.input.register('quit', lambda evt: self.quit())

        return True

    def run(self):
        self.done = False

        if not self.reset():
            print('Failed to reset subsystems, quitting.')
            return 1

        while not self.done:
            self.input.handle()
            self.state.update()
            self.graphics.render()

        return 0

    def quit(self):
        self.done = True
