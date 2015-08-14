from imp import importlib

# Configuration Variables
resolution = (1280, 790)
title = 'Platter'
core_handler = '.systems.sdl_core_handler.SdlCoreHandler'
input_handler = '.systems.default_input_handler.DefaultInputHandler'
window_handler = '.systems.window_handler.WindowHandler'


# Configuration utility functions
def load(module_and_class):
    parts = module_and_class.split('.')
    mod = '.'.join(parts[:-1])
    m = importlib.import_module(mod, package='src')
    return getattr(m, parts[-1])


if __name__ == '__main__':
    import os

    os.environ['PYSDL2_DLL_PATH'] = 'lib'

    wh = load('.systems.window_handler.WindowHandler')

    print(wh)
