from .component import Component


class Sprite(Component):

    def __init__(self, entity, *args, **kwargs):
        sprite_file = kwargs.pop('spriteset', config.default_spriteset)

        super().__init__(entity, *args, **kwargs)

        config = ConfigParser()
        config.read(os.path.join('resources', sprite_file))

        spriteset = {}

        for frame_name in config.sections():
            frame = config[frame_name]
            frame_file = frame['file'].encode()

            def add_to_spriteset(texture):
                spritset[frame_name] = texture

            signaler.trigger('_internal:convert_surface_to_texture',
                             IMG_Load(frame_file), add_to_spriteset)
