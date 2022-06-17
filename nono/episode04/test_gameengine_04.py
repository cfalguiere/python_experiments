from episode04.gameengine import BoardGameEngine, NonoGameEngine, SolvedNonoGameEngine
from episode04.samples import clues2x2, solution2x2, clues5x5s, solution5x5s
from episode04.puzzle import Puzzle
from episode04.board import BoardMark


def test_init():
    puzzle2x2 = Puzzle(clues2x2)
    game2x2 = BoardGameEngine(puzzle2x2)
    assert game2x2.puzzle.get_black_count() == 3


def test_play_no_errors():
    puzzle2x2 = Puzzle(clues2x2)
    game2x2 = NonoGameEngine(puzzle2x2)

    game2x2.play(0, 0, BoardMark.BLACK)
    assert game2x2.count_empty() == 3
    assert not game2x2.is_solved()

    game2x2.play(1, 0, BoardMark.BLACK)
    game2x2.play(1, 1, BoardMark.BLACK)

    assert game2x2.count_empty() == 1
    assert game2x2.count_errors() == 0
    assert game2x2.is_solved()


def test_submit_no_errors():
    puzzle2x2 = Puzzle(clues2x2)
    game2x2 = NonoGameEngine(puzzle2x2)

    n_errors = game2x2.submit([1, 0, 1, 1])
    assert n_errors == 0
    assert game2x2.count_empty() == 0
    assert game2x2.count_errors() == 0
    assert game2x2.is_solved()


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


def test_play_with_errors():
    puzzle2x2 = Puzzle(clues2x2)
    game2x2 = SolvedNonoGameEngine(puzzle2x2, solution2x2)
    okay = game2x2.play(0, 0, BoardMark.FILLER)  # error -> fixed but counted error
    assert not okay
    okay = game2x2.play(1, 0, BoardMark.BLACK)  # correct
    assert okay
    assert game2x2.errors == 1


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


def test_solved_play_without_applying():
    puzzle2x2 = Puzzle(clues2x2)
    game2x2 = SolvedNonoGameEngine(puzzle2x2, solution2x2)

    okay = game2x2.play(0, 0, BoardMark.FILLER, apply=False)
    assert not okay
    assert game2x2.count_errors() == 1  # wrong play
    assert game2x2.count_empty() == 4
    assert not game2x2.is_solved()


def test_solved_submit_without_applying():
    puzzle2x2 = Puzzle(clues2x2)
    game2x2 = SolvedNonoGameEngine(puzzle2x2, solution2x2)

    n_errors = game2x2.submit([1, 1, 0, 1], apply=False)
    assert n_errors == 2
    assert game2x2.count_errors() == 2
    assert game2x2.count_empty() == 4
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
