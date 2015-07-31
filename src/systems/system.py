class System(object):

    componenttypes = ()

    def init(self, signaler):
        pass

    def update(self, signaler, componentdb):

        q = componentdb.thatare(self.componenttypes[0])

        for ctype in self.componenttypes[1:]:
            q = q.thatare(ctype)

        components = q.get()

        if components:
            self.process(signaler, *components)

    def process(signaler, *components):
        pass
