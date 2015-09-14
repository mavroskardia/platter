import os

from configparser import ConfigParser
from collections import defaultdict

from .component import Component
from ..config import config


class Sprite(Component):

    def __init__(self, entity, *args, **kwargs):
        filename = kwargs.pop('spriteset', config.default_spriteset)

        super().__init__(entity, *args, **kwargs)

        self.spriteset = self.parse_spriteset(filename)

    def parse_spriteset(self, filename):
        parsed_spriteset = ConfigParser()
        parsed_spriteset.read(os.path.join('resources', filename))

        print('parsed following sections:', parsed_spriteset.sections())

        spriteset = defaultdict(list)

        for direction in parsed_spriteset.sections():
            print('pulling frames for direction "{}"'.format(direction))
            frames = parsed_spriteset[frame_name]
            for frame in frames:
                imgfile = frames[frame].encode()

            def add_to_spriteset(texture):
                spritset[direction].append(texture)

            signaler.trigger('_internal:convert_surface_to_texture',
                             IMG_Load(frame_file), add_to_spriteset)

        return spriteset


if __name__ == '__main__':
    spriteset_filename = config.default_spriteset

    print('loading spriteset "{}"...'.format(spriteset_filename), end='')

    sss = Sprite(None, spriteset=spriteset_filename)

    print('done')

    import pdb
    pdb.set_trace()
