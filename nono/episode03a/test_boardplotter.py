# type: ignore
# This is a test file, skipping type checking in it.
from episode03a.boardplotter import BoardPlotter
from episode03a.samples import clues2x2


def test_init():
    plotter = BoardPlotter(clues2x2)
    assert plotter.flat_length == 4
