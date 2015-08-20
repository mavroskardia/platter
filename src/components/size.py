class Size(object):

    def __init__(self, width=0, height=0):
        self.w = width
        self.h = height

    def __repr__(self):
        return '{}x{}'.format(self.w, self.h)
