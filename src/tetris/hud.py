from dataclasses import dataclass
from ..signaler import instance as signaler
from ..systems.system import System


@dataclass
class Rect:
    x: int
    y: int
    w: int
    h: int


class HudSystem(System):
    def init(self):
        self.w, self.h = 0, 0
        self.fps = 0
        self.debug = True
        self.border_color = (0, 100, 255, 255)

        def update_dims(w, h):
            self.w = w
            self.h = h

        signaler.trigger("get:screen_dimensions", update_dims)
        signaler.register("fps_update", self.update_fps)
        signaler.register("debug:on", self.toggle_debug)
        signaler.register("debug:off", self.toggle_debug)

    def toggle_debug(self, debug):
        self.debug = debug

    def update_fps(self, fps):
        self.fps = fps

    def process(self, *args, components=None, elapsed=0, **kwargs):
        # draw borders

        signaler.trigger(
            "draw:rect", Rect(0, 0, self.w - 1, self.h - 1), color=self.border_color
        )

        signaler.trigger(
            "draw:line", self.w * 0.8, 0, self.w * 0.8, self.h, color=self.border_color
        )

        # draw fps (TODO: debug only)
        if self.debug:
            signaler.trigger(
                "draw:text",
                f"FPS: {int(self.fps)}",
                Rect(self.w * 0.8 + 2, 1, 0, 0),
                color=(255, 255, 255, 255),
            )
