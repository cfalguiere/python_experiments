# type: ignore
# This is a test file, skipping type checking in it.
from episode03a.samples import clues2x2

from episode03b.board import Board
from episode03b.puzzle import Puzzle

from episode03d.boardplotter import BoardPlotter


def test_init():
    puzzle2x2 = Puzzle(clues2x2)
    plotter = BoardPlotter(puzzle2x2)
    assert plotter.flat_length == 4


def test_append_to_sequence():
    puzzle = Puzzle(clues2x2)
    plotter = BoardPlotter(puzzle)
    assert len(plotter.sequence) == 0
    board = Board(puzzle)
    plotter.append_to_sequence(board)
    assert len(plotter.sequence) == 1
