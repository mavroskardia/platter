class System(object):

    componenttypes = set()

    def init(self, signaler):
        pass

    def update(self, signaler, componentdb):
        if not self.componenttypes:
            return

        components = componentdb.thatare(*self.componenttypes).get()

        if components:
            self.process(signaler, components)

    def process(signaler, *components):
        assert False, 'tried to process the base System class'
