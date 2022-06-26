"""Board components."""

from enum import Enum
from functools import reduce
from operator import mul
from typing import Any, List

from episode04.puzzle import Puzzle

import numpy as np


# constants for mark lette
class BoardMark(Enum):
    """Constants for board marks."""

    INIT = -1
    FILLER = 0
    BLACK = 1


class Board:
    """Manage the board."""

    def __init__(self, a_puzzle: Puzzle):
        """Construct a Board."""
        # given parameters
        self.puzzle = a_puzzle

        # compute board dimensions
        self.width = a_puzzle.width
        self.height = a_puzzle.height
        self.cells_count = a_puzzle.cells_count

        # create board of type int, initialized with -1
        default_value = BoardMark.INIT.value
        self.states: Any = np.full((self.height, self.width),
                                   default_value,
                                   dtype=int)

    def mark(self, row: int, col: int, mark: BoardMark) -> None:
        """Alter the state of the cell with the given mark."""
        self.states[row, col] = mark.value

    def fill_all(self, states: List[int]) -> None:
        """Update all cells with the given states."""
        self.states.flat[:] = states

    def count_empty(self) -> int:
        """Evaluate how much of the board is still empty."""
        length = reduce(mul, self.states.shape)
        count = len([c for c in self.states.reshape(length)
                     if c == BoardMark.INIT.value])
        return count

    def prettyprint(self) -> None:
        """Pretty print of the board."""
        print("cols:", end=" ")
        print(*self.puzzle.given_clues['cols'])  # * unpacks and remove []s
        print("rows:")
        [print(r) for r in self.puzzle.given_clues['rows']]

        marks_switcher = {-1: '.', 0: 'x', 1: 'o'}

        def f_marks(v: int) -> str:
            return marks_switcher[v]
        applyall = np.vectorize(f_marks)
        marks = applyall(self.states)
        print(marks)
