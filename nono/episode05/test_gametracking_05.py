# type: ignore
# This is a test file, skipping type checking in it.
import sys
from io import StringIO

from episode04.board import Board, BoardMark
from episode04.puzzle import Puzzle
from episode04.samples import clues2x2

from episode05.gameengine import GameTracker

import numpy as np


def test_when_created_there_is_0_trial():
    gt = GameTracker()
    assert len(gt.states_history) == 0
    assert gt.current == -1


def test_when_next_trial_there_is_1_trial():
    gt = GameTracker()
    gt.next_trial()
    assert len(gt.states_history) == 1
    assert gt.current == 0
    assert len(gt.states_history[gt.current]) == 0


def test_when_add_1_move_len_is_1_in_first_trial():
    gt = GameTracker()
    gt.next_trial()
    puzzle = Puzzle(clues2x2)
    board = Board(puzzle)
    board.mark(0, 0, BoardMark.BLACK)
    gt.add_move(board)
    assert gt.current == 0
    assert len(gt.states_history[gt.current]) == 1


def test_when_add_2_moves_len_is_2_in_first_trial():
    gt = GameTracker()
    gt.next_trial()
    puzzle = Puzzle(clues2x2)
    board = Board(puzzle)
    board.mark(0, 0, BoardMark.BLACK)
    gt.add_move(board)
    board.mark(0, 1, BoardMark.BLACK)
    gt.add_move(board)
    assert gt.current == 0
    board_state_1 = gt.states_history[gt.current][0]
    board_state_2 = gt.states_history[gt.current][1]
    assert not np.array_equal(board_state_1, board_state_2)


def test_when_add_1_trial_and_1_move_len_is_1_in_second_trial():
    gt = GameTracker()
    gt.next_trial()
    gt.next_trial()
    puzzle = Puzzle(clues2x2)
    board = Board(puzzle)
    board.mark(0, 0, BoardMark.BLACK)
    gt.add_move(board)
    assert gt.current == 1
    assert len(gt.states_history[gt.current]) == 1


def test_when_add_1_trial_and_1_error_count_there_is_1_in_second_trial():
    gt = GameTracker()
    gt.next_trial()
    gt.next_trial()
    puzzle = Puzzle(clues2x2)
    board = Board(puzzle)
    board.mark(0, 0, BoardMark.BLACK)
    gt.record_error_count(2)
    assert gt.current == 1
    assert gt.error_count_history[gt.current] == 2


def test_print_stats_for_2_trials():
    gt = GameTracker()
    gt.next_trial()
    gt.record_error_count(4)
    gt.next_trial()
    gt.record_error_count(3)

    captureOutput = StringIO()
    sys.stdout = captureOutput
    gt.print_stats()
    sys.stdout = sys.__stdout__

    captureOutput.seek(0)
    pp = captureOutput.readlines()
    assert len(pp) == 3
    assert pp[0][0:-1] == "Nb trials: 2"  # strip \n
    assert pp[1][0:-1] == "1: 4 errors"  # strip \n
    assert pp[2][0:-1] == "2: 3 errors"  # strip \n
