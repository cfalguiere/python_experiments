import pytest

from episode01.board import BoardMark, Board
from episode01.samples import clues2x2


def test_init():
    board2x2 = Board(clues2x2)
    assert board2x2.states[0, 0] == -1
    assert board2x2.states[0, 1] == -1
    assert board2x2.states[1, 0] == -1
    assert board2x2.states[1, 1] == -1


def test_mark_black():
    board2x2 = Board(clues2x2)
    board2x2.mark(0, 0, BoardMark.BLACK)
    assert board2x2.states[0, 0] == 1
    assert board2x2.states[0, 1] == -1
    assert board2x2.states[1, 0] == -1
    assert board2x2.states[1, 1] == -1


def test_mark_filler():
    board2x2 = Board(clues2x2)
    board2x2.mark(1, 1, BoardMark.FILLER)
    assert board2x2.states[0, 0] == -1
    assert board2x2.states[0, 1] == -1
    assert board2x2.states[1, 0] == -1
    assert board2x2.states[1, 1] == 0


def test_mark_out_of_bound():
    board2x2 = Board(clues2x2)
    with pytest.raises(IndexError):
        board2x2.mark(1, 2, BoardMark.FILLER)


# TODO test prettyprint
