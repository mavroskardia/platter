from sdl2 import *


class SdlEvents(object):

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

    def trigger(self, evt, event_name):
        for handler in self.signals.get(event_name, []):
            handler(evt)

    def quit(self, evt):
        for handler in self.signals.get('quit', []):
            handler(evt)

    def key(self, evt, sym):
        letter = 'key:{}'.format(chr(sym))
        for handler in self.signals.get(letter, []):
            handler(evt)

    def keydown(self, evt):
        keysym = evt.key.keysym

        # temporarily quit based on standard-ish quit keys
        if keysym.sym == SDLK_ESCAPE or keysym.sym == SDLK_q:
            self.quit(evt)
        else:
            self.key(evt, keysym.sym)
