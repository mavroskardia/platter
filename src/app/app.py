from imp import importlib

from ..config import config
from ..engine.engine import Engine


class App(object):

    def run(self):
        engine = Engine()

        ch = config.load(config.core_handler)
        ih = config.load(config.input_handler)
        wh = config.load(config.window_handler)

        engine.add_system(ch)
        engine.add_system(ih)
        engine.add_system(wh)

        return engine.run()
