import pytest

from episode01.board import BoardMark, Board
from episode01.samples import clues2x2

from io import StringIO
import sys


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


def test_prettyprint_empty():
    captureOutput = StringIO()
    sys.stdout = captureOutput
    board2x2 = Board(clues2x2)
    board2x2.prettyprint()
    sys.stdout = sys.__stdout__

    captureOutput.seek(0)
    pp = captureOutput.readlines()
    assert len(pp) == 6
    assert pp[0][0:-1] == "cols: 2 1"  # strip \n
    assert pp[1][0:-1] == "rows:"  # strip \n
    assert pp[2][0:-1] == "1"  # strip \n
    assert pp[3][0:-1] == "2"  # strip \n
    assert pp[4][0:-1] == "[['.' '.']"  # strip \n
    assert pp[5][0:-1] == " ['.' '.']]"  # strip \n


def test_prettyprint_mark_black():
    captureOutput = StringIO()
    sys.stdout = captureOutput
    board2x2 = Board(clues2x2)
    board2x2.mark(1, 1, BoardMark.BLACK)
    board2x2.prettyprint()
    sys.stdout = sys.__stdout__

    captureOutput.seek(0)
    pp = captureOutput.readlines()
    assert len(pp) == 6
    assert pp[4][0:-1] == "[['.' '.']"  # strip \n
    assert pp[5][0:-1] == " ['.' 'o']]"  # strip \n


def test_prettyprint_mark_filler():
    captureOutput = StringIO()
    sys.stdout = captureOutput
    board2x2 = Board(clues2x2)
    board2x2.mark(0, 1, BoardMark.FILLER)
    board2x2.prettyprint()
    sys.stdout = sys.__stdout__

    captureOutput.seek(0)
    pp = captureOutput.readlines()
    assert len(pp) == 6
    assert pp[4][0:-1] == "[['.' 'x']"  # strip \n
    assert pp[5][0:-1] == " ['.' '.']]"  # strip \n
