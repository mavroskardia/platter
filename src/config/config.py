from imp import importlib

# Configuration Variables
resolution = (1280, 790)
title = 'Platter'

default_world = '.worlds.default.DefaultWorld'


# Configuration utility functions
def load(module_and_class, *args, **kwargs):
    parts = module_and_class.split('.')
    mod = '.'.join(parts[:-1])
    m = importlib.import_module(mod, package='src')
    return getattr(m, parts[-1])


if __name__ == '__main__':
    import os

    os.environ['PYSDL2_DLL_PATH'] = 'lib'

    wh = load('.systems.window_handler.WindowHandler')

    print(wh)
