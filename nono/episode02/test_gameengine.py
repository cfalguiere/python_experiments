from gameengine import GameEngine
from samples import clues2x2, solution2x2


def test_init():
    engine2x2 = GameEngine(clues2x2, solution2x2)
    assert engine2x2.width == 2
    assert engine2x2.height == 2
    assert engine2x2.cells_count == 4
    assert engine2x2.black_count == 3
    assert engine2x2.is_board_valid([1, 0, 1, 1])
    assert not engine2x2.is_board_valid([1, 1, 0, 1])
