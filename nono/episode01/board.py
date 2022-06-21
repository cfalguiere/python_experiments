"""Board components."""

# built in imports
from enum import Enum

# need to import numpy library
# it is provided in most Python environment.
# If not you install it with pip install numpy
import numpy as np


class BoardMark(Enum):
    """Constants for board marks."""

    INIT = -1
    FILLER = 0
    BLACK = 1


class Board:
    """Manage the board."""

    def __init__(self, some_clues):
        """Construct a Board."""
        # given parameters
        self.clues = some_clues

        # compute board dimensions
        self.width = len(self.clues['cols'])
        self.height = len(self.clues['rows'])

        # create board of type int, initialized with -1
        default_value = BoardMark.INIT.value
        self.states = np.full((self.height, self.width),
                              default_value, dtype=int)

    def mark(self, row, col, mark):
        """Alter the state of the cell with the given mark."""
        self.states[row, col] = mark.value

    def prettyprint(self):
        """Pretty print of the board."""
        print("cols:", end=" ")
        print(*self.clues['cols'])  # * unpacks and remove []s
        print("rows:")
        [print(r) for r in self.clues['rows']]

        # dictionnaries are used in Python to describe swich cases
        # depending on the value
        marks_switches = {BoardMark.INIT.value: '.',
                          BoardMark.FILLER.value: 'x',
                          BoardMark.BLACK.value: 'o'}

        # The switch can be applyed to the full array
        # numpy provides ways to apply a function to all the cells
        # must use vectorize, for whatever reason lambda does not work here
        def switch_mark(v):
            return marks_switches[v]

        apply_all_switch_mark = np.vectorize(switch_mark)
        states_repr = apply_all_switch_mark(self.states)
        states_repr

        print(states_repr)
