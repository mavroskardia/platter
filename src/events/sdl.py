from sdl2 import *


class SdlInput(object):

    def __init__(self):
        self.signals = {}
        self.event_handlers = {
            SDL_QUIT: self.quit,
            SDL_KEYDOWN: self.keydown,
        }

    def register(self, signal_name, func):
        if signal_name not in self.signals:
            self.signals[signal_name] = []

        self.signals[signal_name].append(func)

    def reset(self):
        return True, None

    def handle(self):
        evt = SDL_Event()

        while SDL_PollEvent(evt):
            self.event_handlers.get(evt.type, self.nop)(evt)

    def nop(self, evt):
        pass

    def quit(self, evt):
        for handler in self.signals.get('quit', []):
            handler(evt)

    def keydown(self, evt):
        evt = evt.key
