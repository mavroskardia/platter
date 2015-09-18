import time


class Fps:

    UpdateInterval = 60

    def __init__(self, signaler):
        self.signaler = signaler
        self.fps = 0
        self.ticks = 0
        self.current = 0
        self.elapsed = 0
        self.delay_multiplier = 0.02

    def init(self):
        self.ticks = 0
        self.last_time = time.time()

    def tick_start(self):
        self.current = time.time()
        self.elapsed = (self.current - self.last_time) # * self.delay_multiplier
        self.fps = 1 / (self.elapsed + 0.00001)
        self.ticks += 1

    def tick_end(self):
        self.last_time = self.current
        if self.ticks == Fps.UpdateInterval:
            self.ticks = 0
            self.signaler.trigger('fps_update', self.fps)
