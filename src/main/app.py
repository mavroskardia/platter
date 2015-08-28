import sys
import os

try:
    os.environ['PYSDL2_DLL_PATH'] = 'lib'
    from sdl2 import *
except ImportError:
    print('You have to have the sdl2 dlls in the lib directory')
    sys.exit(1)

from collections import defaultdict

import config


class App:

    def __init__(self):
        self.compdb = defaultdict(set)

    def add_system(self, system):
        self.compdb[system.componenttypes].append(system)

    def run(self):

        while self.running:

            for s in self.systems:
                s.process()
