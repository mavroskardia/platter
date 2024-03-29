from collections import OrderedDict
from .constants import (
    Body,
    Bordered,
    CanCollide,
    HasPhysics,
    PlayerControl,
    PlayerData,
    Sprite,
)
from .base import (
    resolution,
)

entities = OrderedDict()

entities["player"] = {
    Body: (None, {"x": 100, "y": 300, "w": 37, "h": 64, "r": 1.0, "mass": 100.0}),
    CanCollide: None,
    HasPhysics: None,
    PlayerControl: None,
    PlayerData: None,
    Sprite: (("default",), {}),
}

entities["ground"] = {
    Bordered: None,
    CanCollide: None,
    HasPhysics: ((True,), {}),
    Body: (
        None,
        {"x": -5, "y": resolution[1] - 50, "w": 10000, "h": 55, "mass": 0, "r": 1.0},
    ),
}

entities["platform"] = {
    Bordered: None,
    CanCollide: None,
    HasPhysics: ((True,), {}),
    Body: (None, {"x": 100, "y": 500, "w": 200, "h": 50, "mass": 0, "r": 1.0}),
}

entities["obstacle"] = {
    Bordered: None,
    CanCollide: None,
    HasPhysics: ((True,), {}),
    Body: (None, {"x": 400, "y": 680, "w": 200, "h": 50, "mass": 0, "r": 1.0}),
}

entities["collider1"] = {
    Bordered: None,
    CanCollide: None,
    HasPhysics: ((False, False), {}),
    Body: (
        None,
        {
            "x": 100,
            "y": 100,
            "w": 50,
            "h": 50,
            "vx": 100,
            "vy": 0,
            "mass": 15.0,
            "r": 0.1,
        },
    ),
}

entities["collider2"] = {
    Bordered: None,
    CanCollide: None,
    HasPhysics: ((False, False), {}),
    Body: (
        None,
        {
            "x": 900,
            "y": 100,
            "w": 50,
            "h": 50,
            "vx": -100,
            "vy": 0,
            "mass": 10.0,
            "r": 0.1,
        },
    ),
}

# entities['testtext'] = {
#     Text: (('Hello, World!',), None),
#     Body: (None, {'x': 700, 'y': 10, 'w': 500, 'h': 20})
# }
