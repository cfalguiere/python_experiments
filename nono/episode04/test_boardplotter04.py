# type: ignore
# This is a test file, skipping type checking in it.
from episode04.board import Board
from episode04.boardplotter import BoardPlotter
from episode04.puzzle import Puzzle
from episode04.samples import clues2x2


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
