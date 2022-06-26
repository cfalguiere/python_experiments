"""Puzzle related components."""
from itertools import chain
from typing import List

from episode04.common import ClueType, CluesType, NormCluesType


class Puzzle:
    """Describe the puzzle clues and constants derived from clues."""

    def __init__(self, some_clues: CluesType):
        """Puzzle constructor."""
        # given parameters
        self.given_clues = some_clues

        # normalize clues
        self.norm_clues = self.init_norm_clues()

        # compute board dimensions
        self.width = len(some_clues['cols'])
        self.height = len(some_clues['rows'])
        self.cells_count = self.width * self.height
        self.required_blacks_count = self.get_black_count()

    def init_norm_clues(self) -> NormCluesType:
        """Turn clues into a list of lists with one or more integers."""
        def f_norm_clue(clue: ClueType) -> List[int]:
            return clue if isinstance(clue, list) else [clue]
        norm_clues = {
            'rows': [f_norm_clue(clue) for clue in self.given_clues['rows']],
            'cols': [f_norm_clue(clue) for clue in self.given_clues['cols']]
        }
        return norm_clues

    def get_black_count(self, axis: str = 'rows') -> int:
        """Compute the number of blacks cells required by the clues.

        Parameters
        ----------
        axis: str
            Should it count blacks for rows or cols.
            Either rows or cols. Default to rows.

        Returns
        -------
        int
            The number of blacks cells required.
        """
        # sums the number of blacks (represented by 1)
        return sum(chain.from_iterable(self.norm_clues[axis]))

    def is_consistent(self) -> bool:
        """Check clues for consistency between rows and cols definition."""
        rows_black_count = self.get_black_count(axis='rows')
        cols_black_count = self.get_black_count(axis='cols')
        return rows_black_count == cols_black_count

#
