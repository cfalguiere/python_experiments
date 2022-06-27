# type: ignore
# This is a test file, skipping type checking in it.
from episode04.board import BoardMark
from episode04.puzzle import Puzzle
from episode04.samples import clues2x2, clues5x5s, solution2x2, solution5x5s

from episode05.gameengine import NonoGameEngine, SolvedNonoGameEngine


def test_nb_trials_is_1_at_start():
    puzzle2x2 = Puzzle(clues2x2)
    game2x2 = NonoGameEngine(puzzle2x2)
    assert game2x2.puzzle.get_black_count() == 3
    assert game2x2.nb_trials == 1


def test_count_empty_is_4_at_start_of_2x2():
    puzzle2x2 = Puzzle(clues2x2)
    game2x2 = NonoGameEngine(puzzle2x2)
    assert game2x2.count_empty() == 4


def test_count_black_is_0_at_start_on_2x2():
    puzzle2x2 = Puzzle(clues2x2)
    game2x2 = NonoGameEngine(puzzle2x2)
    assert game2x2.count_black() == 0


def test_count_empty_is_3_after_valid_move_on_2x2():
    puzzle2x2 = Puzzle(clues2x2)
    game2x2 = NonoGameEngine(puzzle2x2)
    game2x2.play(0, 0, BoardMark.BLACK)
    assert game2x2.errors == 0
    assert game2x2.count_empty() == 3


def test_count_empty_is_3_after_invalid_move_on_2x2():
    puzzle2x2 = Puzzle(clues2x2)
    game2x2 = NonoGameEngine(puzzle2x2)
    game2x2.play(0, 0, BoardMark.FILLER)
    # assert game2x2.errors == 1  # on ne sait pas le detecterTODO
    assert game2x2.count_empty() == 3


def test_count_black_is_1_after_valid_move_on_2x2():
    puzzle2x2 = Puzzle(clues2x2)
    game2x2 = NonoGameEngine(puzzle2x2)
    game2x2.play(0, 0, BoardMark.BLACK)
    assert game2x2.errors == 0
    assert game2x2.count_black() == 1


def test_count_black_is_0_after_invalid_move_on_2x2():
    puzzle2x2 = Puzzle(clues2x2)
    game2x2 = NonoGameEngine(puzzle2x2)
    game2x2.play(0, 0, BoardMark.FILLER)
    assert game2x2.errors == 0  # on ne sait pas les detecger TODO
    assert game2x2.count_black() == 0


def test_count_black_is_1_after_invalid_move_on_2x2_autofix():
    puzzle2x2 = Puzzle(clues2x2)
    game2x2 = SolvedNonoGameEngine(puzzle2x2, solution2x2)
    game2x2.play(0, 0, BoardMark.FILLER)
    assert game2x2.errors == 1
    # move will be fixed
    assert game2x2.count_black() == 1


def test_nb_trials_is_2_after_reset():
    puzzle2x2 = Puzzle(clues2x2)
    game2x2 = NonoGameEngine(puzzle2x2)
    game2x2.reset_trial()
    assert game2x2.nb_trials == 2


def test_count_empty_is_4_after_reset():
    puzzle2x2 = Puzzle(clues2x2)
    game2x2 = NonoGameEngine(puzzle2x2)
    game2x2.play(0, 0, BoardMark.BLACK)
    assert game2x2.count_empty() == 3
    game2x2.reset_trial()
    assert game2x2.count_empty() == 4


def test_count_errors_is_0_after_reset():
    puzzle2x2 = Puzzle(clues2x2)
    game2x2 = SolvedNonoGameEngine(puzzle2x2, solution2x2)
    game2x2.play(0, 0, BoardMark.FILLER)
    assert game2x2.errors == 1
    game2x2.reset_trial()
    assert game2x2.errors == 0


def test_count_black_is_0_after_reset():
    puzzle2x2 = Puzzle(clues2x2)
    game2x2 = NonoGameEngine(puzzle2x2)
    game2x2.play(0, 0, BoardMark.BLACK)
    assert game2x2.count_black() == 1
    game2x2.reset_trial()
    assert game2x2.count_black() == 0


def test_solved_by_submit_on_2x2():
    puzzle2x2 = Puzzle(clues2x2)
    game2x2 = NonoGameEngine(puzzle2x2)
    n_errors = game2x2.submit([1, 0, 1, 1])
    assert n_errors == 0
    assert game2x2.is_solved()


def test_solved_by_submit_on_2x2_solved():
    puzzle2x2 = Puzzle(clues2x2)
    game2x2 = SolvedNonoGameEngine(puzzle2x2, solution2x2)
    n_errors = game2x2.submit([1, 0, 1, 1])
    assert n_errors == 0
    assert game2x2.is_solved()


def test_not_solved_after_reset():
    puzzle2x2 = Puzzle(clues2x2)
    game2x2 = NonoGameEngine(puzzle2x2)
    n_errors = game2x2.submit([1, 0, 1, 1])
    assert n_errors == 0
    assert game2x2.is_solved()
    game2x2.reset_trial()
    assert not game2x2.is_solved()


def test_solved_in_3_moves_on_2x2():
    puzzle2x2 = Puzzle(clues2x2)
    game2x2 = NonoGameEngine(puzzle2x2)
    game2x2.play(0, 0, BoardMark.BLACK)
    game2x2.play(1, 0, BoardMark.BLACK)
    game2x2.play(1, 1, BoardMark.BLACK)
    assert game2x2.is_solved()


def test_solved_in_3_moves_on_2x2_solved():
    puzzle2x2 = Puzzle(clues2x2)
    game2x2 = SolvedNonoGameEngine(puzzle2x2, solution2x2)
    game2x2.play(0, 0, BoardMark.BLACK)
    game2x2.play(1, 0, BoardMark.BLACK)
    game2x2.play(1, 1, BoardMark.BLACK)
    assert game2x2.is_solved()


def test_not_solved_in_3_moves_on_2x2_autofix():
    puzzle2x2 = Puzzle(clues2x2)
    game2x2 = SolvedNonoGameEngine(puzzle2x2, solution2x2)
    game2x2.play(0, 0, BoardMark.BLACK)
    game2x2.play(1, 0, BoardMark.BLACK)
    game2x2.play(1, 1, BoardMark.FILLER)  # autofix
    assert not game2x2.is_solved()
    assert game2x2.errors == 1


def test_not_solved_bin_2_moves_on_2x2():
    puzzle2x2 = Puzzle(clues2x2)
    game2x2 = NonoGameEngine(puzzle2x2)
    game2x2.play(0, 0, BoardMark.BLACK)
    game2x2.play(1, 0, BoardMark.BLACK)
    assert not game2x2.is_solved()


def test_not_solved_in_2_moves_on_2x2_solved():
    puzzle2x2 = Puzzle(clues2x2)
    game2x2 = SolvedNonoGameEngine(puzzle2x2, solution2x2)
    game2x2.play(0, 0, BoardMark.BLACK)
    game2x2.play(1, 0, BoardMark.BLACK)
    assert not game2x2.is_solved()


# ----------


def test_submit_with_errors():
    puzzle2x2 = Puzzle(clues2x2)
    game2x2 = NonoGameEngine(puzzle2x2)

    n_errors = game2x2.submit([1, 1, 0, 1])
    assert n_errors == 2
    assert game2x2.count_empty() == 0
    assert game2x2.count_errors() == 2
    assert not game2x2.is_solved()


def test_play_bar():
    puzzle2x2 = Puzzle(clues2x2)
    game2x2 = NonoGameEngine(puzzle2x2)

    game2x2.play_multiple(0, 0, BoardMark.BLACK, 1, 2)
    game2x2.play_multiple(1, 0, BoardMark.BLACK, 0, 2)

    assert game2x2.count_empty() == 1
    assert game2x2.count_errors() == 0


def test_play_bar_out_of_bound():
    puzzle2x2 = Puzzle(clues2x2)
    game2x2 = NonoGameEngine(puzzle2x2)

    game2x2.play_multiple(0, 0, BoardMark.BLACK, 1, 2)
    game2x2.play_multiple(1, 1, BoardMark.BLACK, 0, 2)

    assert game2x2.count_empty() == 1
    assert game2x2.count_errors() == 0


def test_submit_5x5s_no_errors():
    puzzle5x5s = Puzzle(clues5x5s)
    assert puzzle5x5s.is_consistent()

    game5x5s = NonoGameEngine(puzzle5x5s)

    game5x5s.submit(solution5x5s.reshape(puzzle5x5s.cells_count).tolist())
    assert game5x5s.is_solved()


def test_solved_submit_no_errors():
    puzzle2x2 = Puzzle(clues2x2)
    game2x2 = SolvedNonoGameEngine(puzzle2x2, solution2x2)

    n_errors = game2x2.submit([1, 0, 1, 1])
    assert n_errors == 0
    assert game2x2.count_empty() == 0
    assert game2x2.count_errors() == 0
    assert game2x2.is_solved()


def test_solved_submit_with_errors():
    puzzle2x2 = Puzzle(clues2x2)
    game2x2 = SolvedNonoGameEngine(puzzle2x2, solution2x2)

    n_errors = game2x2.submit([1, 1, 0, 1])
    assert n_errors == 2
    assert game2x2.count_empty() == 0
    assert game2x2.count_errors() == 2
    assert not game2x2.is_solved()


def test_solved_play_bar():
    puzzle2x2 = Puzzle(clues2x2)
    game2x2 = SolvedNonoGameEngine(puzzle2x2, solution2x2)

    game2x2.play_multiple(0, 0, BoardMark.BLACK, 1, 2)
    game2x2.play_multiple(1, 0, BoardMark.BLACK, 0, 2)

    assert game2x2.count_empty() == 1
    assert game2x2.count_errors() == 0


def test_submit_5x5s():
    puzzle5x5s = Puzzle(clues5x5s)
    assert puzzle5x5s.is_consistent()

    game5x5s = NonoGameEngine(puzzle5x5s)

    game5x5s.submit(solution5x5s.reshape(puzzle5x5s.cells_count).tolist())
    assert game5x5s.is_solved()


def test_solved_submit_5x5s():
    puzzle5x5s = Puzzle(clues5x5s)
    assert puzzle5x5s.is_consistent()

    game5x5s = SolvedNonoGameEngine(puzzle5x5s, solution5x5s)

    game5x5s.submit(solution5x5s.reshape(puzzle5x5s.cells_count).tolist())
    assert game5x5s.is_solved()
