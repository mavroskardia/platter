from ..tetramino_factory import TetraminoFactory, Tetraminos


def test_create():
    factory = TetraminoFactory()
    long = factory.create(Tetraminos.Long)
    assert long.shape == [
        (1, 0, 0, 0),
        (1, 0, 0, 0),
        (1, 0, 0, 0),
        (1, 0, 0, 0),
    ]
    lr = factory.create(Tetraminos.LR)
    assert lr.shape == [
        (1, 1, 0, 0),
        (0, 1, 1, 0),
        (0, 0, 0, 0),
        (0, 0, 0, 0),
    ]


def test_rotate():
    factory = TetraminoFactory()
    ltet = factory.create(Tetraminos.L)

    assert ltet.shape == [
        (0, 0, 0, 0),
        (1, 0, 0, 0),
        (1, 0, 0, 0),
        (1, 1, 0, 0),
    ]

    ltet.rotate()

    assert ltet.shape == [(1, 1, 1, 0), (1, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0)]

    ltet.rotate()

    assert ltet.shape == [(0, 0, 1, 1), (0, 0, 0, 1), (0, 0, 0, 1), (0, 0, 0, 0)]

    ltet.rotate()

    assert ltet.shape == [(0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 1), (0, 1, 1, 1)]

    ltet.rotate()

    assert ltet.shape == [(0, 0, 0, 0), (1, 0, 0, 0), (1, 0, 0, 0), (1, 1, 0, 0)]
