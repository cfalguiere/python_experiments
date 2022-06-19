from episode04.boardplotter import BoardPlotter
from episode04.puzzle import Puzzle
from episode04.samples import clues2x2


def test_init():
    puzzle2x2 = Puzzle(clues2x2)
    plotter = BoardPlotter(puzzle2x2)
    assert plotter.flat_length == 4
