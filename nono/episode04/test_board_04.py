import pytest

from episode04.samples import clues2x2, solution2x2
from episode04.board import BoardMark, Board
from episode04.puzzle import Puzzle


def test_init():
    puzzle2x2 = Puzzle(clues2x2)
    board2x2 = Board(puzzle2x2)
    assert board2x2.states[0, 0] == -1
    assert board2x2.states[0, 1] == -1
    assert board2x2.states[1, 0] == -1
    assert board2x2.states[1, 1] == -1


def test_mark_black():
    puzzle2x2 = Puzzle(clues2x2)
    board2x2 = Board(puzzle2x2)
    board2x2.mark(0, 0, BoardMark.BLACK)
    assert board2x2.states[0, 0] == 1
    assert board2x2.states[0, 1] == -1
    assert board2x2.states[1, 0] == -1
    assert board2x2.states[1, 1] == -1


def test_mark_filler():
    puzzle2x2 = Puzzle(clues2x2)
    board2x2 = Board(puzzle2x2)
    board2x2.mark(1, 1, BoardMark.FILLER)
    assert board2x2.states[0, 0] == -1
    assert board2x2.states[0, 1] == -1
    assert board2x2.states[1, 0] == -1
    assert board2x2.states[1, 1] == 0


def test_mark_out_of_bound():
    puzzle2x2 = Puzzle(clues2x2)
    board2x2 = Board(puzzle2x2)
    with pytest.raises(IndexError):
        board2x2.mark(1, 2, BoardMark.FILLER)


def test_count_2_empty_after_2_marks():
    puzzle2x2 = Puzzle(clues2x2)
    board2x2 = Board(puzzle2x2)
    board2x2.mark(0, 0, BoardMark.BLACK)
    board2x2.mark(0, 1, BoardMark.FILLER)
    assert board2x2.count_empty() == 2


def test_count_0_empty_after_4_marks():
    puzzle2x2 = Puzzle(clues2x2)
    board2x2 = Board(puzzle2x2)
    board2x2.mark(0, 0, BoardMark.BLACK)
    board2x2.mark(0, 1, BoardMark.FILLER)
    board2x2.mark(1, 0, BoardMark.BLACK)
    board2x2.mark(1, 1, BoardMark.BLACK)
    assert board2x2.count_empty() == 0


def test_count_0_empty_after_fill_all():
    puzzle2x2 = Puzzle(clues2x2)
    board2x2 = Board(puzzle2x2)
    board2x2.fill_all(solution2x2)
    assert board2x2.count_empty() == 0
