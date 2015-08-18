from . import system


class CollisionDetection(system.System):

    componenttypes = Colliding, Position

    def process(self, signaler, components):

        for col, pos in components:
            pass
