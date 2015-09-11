from . import system


class DataUpdateSystem(system.System):

    componenttypes = DynamicData,

    def process(self, *args, signaler, components, elapsed, **kwargs):

        for dd, in components:
            dd.update(elapsed)
