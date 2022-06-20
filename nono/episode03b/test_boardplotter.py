from episode01.samples import clues2x2

from episode03b.boardplotter import BoardPlotter
from episode03b.puzzle import Puzzle


def test_init():
    puzzle2x2 = Puzzle(clues2x2)
    plotter = BoardPlotter(puzzle2x2)
    assert plotter.flat_length == 4
