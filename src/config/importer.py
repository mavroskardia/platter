from imp import importlib


def load(module_and_class, *args, **kwargs):
    parts = module_and_class.split('.')
    mod = '.'.join(parts[:-1])
    m = importlib.import_module(mod, package='src')
    return getattr(m, parts[-1])

if __name__ == '__main__':

    sis = load('.systems.sdlinit.SdlInitSystem')

    print(sis)
    print(sis.componenttypes)
