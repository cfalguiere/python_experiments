from episode01.samples import clues2x2

from episode03b.puzzle import Puzzle

from episode03d.boardplotter import BoardPlotter


def test_init():
    puzzle2x2 = Puzzle(clues2x2)
    plotter = BoardPlotter(puzzle2x2)
    assert plotter.flat_length == 4
