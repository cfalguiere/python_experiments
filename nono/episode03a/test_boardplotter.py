from episode01.samples import clues2x2
from episode03a.boardplotter import BoardPlotter


def test_init():
    plotter = BoardPlotter(clues2x2)
    assert plotter.flat_length == 4
