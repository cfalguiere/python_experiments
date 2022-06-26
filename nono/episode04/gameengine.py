"""Board game and Nonogram related components."""

from itertools import groupby
from operator import mul
from typing import List

from episode04.board import Board, BoardMark
from episode04.boardplotter import BoardPlotter
from episode04.common import NormClueType, SolutionType
from episode04.puzzle import Puzzle


class BoardGameEngine:
    """Provide utilities for board game."""

    def __init__(self, a_puzzle: Puzzle):
        """Construct a GameEngine."""
        self.puzzle = a_puzzle

        # init a board
        self.board = Board(a_puzzle)
        self.plotter = BoardPlotter(a_puzzle)

    def play(self,
             row: int, col: int, mark: BoardMark,
             apply: bool = True) -> bool:
        """Play one cell.

        Implementation should be provided by the subclass.

        Parameters
        ----------
        row: int
            vertical position of the mark. Should be between 0 and height-1.
        col: int
            horizontal position of the mark. Should be between 0 and wirth-1.
        mark: BoardMark
            The mark to be place. it is defined by the Enum BoardMark.
        apply: bool
            True if the mark should change the current board state.
            Default to True.
        """
        pass

    def play_multiple(self,
                      row: int, col: int, mark: BoardMark,
                      axis: int, count: int) -> None:
        # TODO magic
        """Play multiple cells."""
        if axis == 0:  # row
            for i in range(col, min(self.puzzle.width, col + count)):
                self.play(row, i, mark)
        if axis == 1:  # row
            for i in range(row, min(self.puzzle.height, row + count)):
                self.play(i, col, mark)

    def show(self) -> None:
        """Plot the board."""
        self.plotter.show(self.board)


class NonoGameEngine(BoardGameEngine):
    """Provide utilities for nonogram game without a given solution."""

    def __init__(self, a_puzzle: Puzzle, track: bool = False):
        """Construct a GameEngine."""
        super().__init__(a_puzzle)

        self.track = track
        self.board_states_history: List[Board] = []

    # TODO isoler check de play
    # TODO verif partielle
    def play(self,
             row: int, col: int, mark: BoardMark,
             apply: bool = True) -> bool:
        """Play one cell.

        Play the game by sending the state of one cell.
        If apply, update the board.
        Always return True.

        Parameters
        ----------
        row: int
            vertical position of the mark. Should be between 0 and height-1
        col: int
            horizontal position of the mark. Should be between 0 and wirth-1
        mark: BoardMark
            The mark to be placed. it is defined by the Enum BoardMark
        apply: bool
            True if the mark should change the current board state

        Returns
        -------
        bool
            Always True
        """
        if apply:
            # apply the given state
            self.board.mark(row, col, mark)
            if self.track:
                # will be added to the sequence of solutions
                self.board_states_history.append(self.board.states.copy())
        return True

    # todo append submissions`
    # todo autofill
    # TODO isoler check de play
    def submit(self, states_list: List[int]) -> int:
        """Submit the solution.

        Submit the solution and give all the cells's state in one action.
        It is not required to provides all the cells values.
        Missing Blacks are counted as errors. Fillers are ignored.
        Returns the number of errors.
        The submission ends the game.

        Parameters
        ----------
        states_list: List[int]
            The cell states as a one dimension list of -1,0,1
            corresponding to marks defined in BoardMark.

        Returns
        -------
        int
            The number of errors.
        """
        # end the game with this solutions
        self.board.fill_all(states_list)
        if self.track:
            # will be added to the sequence of solutions
            self.board_states_history.append(self.board.states.copy())

        # board is okay if without errors on blacks
        return self.count_errors()

    def is_solved(self) -> bool:
        """Check whether the puzzle is solved.

        Accept that filler cells are left undefined.
        In other words it only takes blacks into account.

        returns
        -------
        bool
            True if the game is solved
        """
        return self.count_errors() == 0

    def count_empty(self) -> int:
        """Get the number of empty cells."""
        return self.board.count_empty()

    # todo document that ignore unfilled
    def count_errors(self) -> int:
        """Compute the difference between given board states sum and clues."""
        def axis_errors(blocks: List[List[int]],
                        clues: List[NormClueType]) -> int:
            sums_blocks = [sum(b) for b in blocks]
            sums_clues = [sum(c) for c in clues]
            errors = sum([abs(b - c)
                          for (b, c)
                          in zip(sums_blocks, sums_clues)])
            return errors

        rows_errors = axis_errors(self.get_rows_blocks(),
                                  self.puzzle.norm_clues["rows"])

        cols_errors = axis_errors(self.get_cols_blocks(),
                                  self.puzzle.norm_clues["cols"])

        return int((rows_errors + cols_errors) / 2)  # row error => col error

    def get_rows_blocks(self) -> List[List[int]]:
        """Compute blocks for each rows."""
        rows = self.board.states
        blocks = [[len(list(g)) for k, g in groupby(line) if k == 1]
                  for line in rows]
        return blocks

    def get_cols_blocks(self) -> List[List[int]]:
        """Compute blocks for each cols."""
        w = self.board.states.shape[0]
        h = self.board.states.shape[1]
        length = mul(w, h)
        cols = [[self.board.states.reshape(length)[c + r * w]
                 for r in range(0, h)]
                for c in range(0, w)]
        blocks = [[len(list(g)) for k, g in groupby(line) if k == 1]
                  for line in cols]
        return blocks

    def show_all(self) -> None:
        """Plot the board states.

        States are captured by submit and play.
        Silent is track is off.
        """
        if self.track:
            self.plotter.show_many(self.board_states_history)
        else:
            print("tracking is off")


class SolvedNonoGameEngine(NonoGameEngine):
    """Provide utilities for nonogram game with a given solution."""

    def __init__(self,
                 a_puzzle: Puzzle, a_solution: SolutionType,
                 track: bool = False):
        """Construct a GameEngine."""
        super().__init__(a_puzzle, track)

        self.solution = a_solution
        cells = self.puzzle.cells_count
        self.flat_solution = self.solution.reshape(cells).tolist()

        # init score
        self.errors = 0

    # TODO check position for bounds
    # TODO isoler check de play
    def play(self,
             row: int, col: int, mark: BoardMark,
             apply: bool = True) -> bool:
        """Play one cell.

        Play the game by sending the state of one cell.
        Check whether an action is valid given a solution.
        If apply is True, update the board.

        Parameters
        ----------
        row: int
            vertical position of the mark. Should be between 0 and height-1
        col: int
            horizontal position of the mark. Should be between 0 and wirth-1
        mark: BoardMark
            The mark to be placed. it is defined by the Enum BoardMark
        apply: bool
            True if the mark should change the current board state

        Returns
        -------
        bool
            True if the mark is correct
            (same mark in the solution at the same location)
        """
        okay = self.solution[row, col] == mark.value
        if not okay:
            self.errors += 1

        if apply:
            # apply the real state which is what games usually do
            true_mark = BoardMark(self.solution[row, col])
            self.board.mark(row, col, true_mark)
            if self.track:
                # will be added to the sequence of solutions
                self.board_states_history.append(self.board.states.copy())

        # __eq__ returns a type Any - workaround to pass mypy check
        return bool(okay)

    # TODO accept np array
    # TODO same semantic ad not solved and add a compare
    # TODO isoler check de play
    def submit(self, states_list: List[int], apply: bool = True) -> int:
        """Submit the solution.

        Submit the solution and give all the cells's state in one action.
        It is not required to provide all the cells values;
        Only Blacks are taken into account.
        Check whether the states is correct given the registered solution.

        Parameters
        ----------
        states_list: List[int]
            The cell states as a one dimension list of -1,0,1
            corresponding to marks defined in BoardMark.
        apply: bool
            Tell whether this solution is the end of the game.
            If True the board will be filled with states and it ends the game.
            If False this fonction can be used to compute the number of errors.

        Returns
        -------
        int
            The number of errors computed as the number of black cells that
            do not match the solution.
        """
        if apply:
            # end the game with this solutions
            self.board.fill_all(states_list)
            if self.track:
                # will be added to the sequence of solutions
                self.board_states_history.append(self.board.states.copy())

        # board is okay when blacks are correrct
        self.errors = sum([abs(p - e)
                           for (p, e) in zip(states_list, self.flat_solution)
                           if p >= 0])
        return self.errors

    # todo document that ignore unfilled
    def count_errors(self) -> int:
        """Get the number of errors.

        By convention, unfilled are not errors.

        Returns
        -------
        int
            The number of errors. Unfilled are not considered as error.
        """
        return self.errors
