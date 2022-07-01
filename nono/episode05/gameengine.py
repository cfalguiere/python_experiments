"""Board game and Nonogram related components."""

from functools import reduce
from itertools import chain, groupby
from operator import mul
from typing import List

from episode04.board import Board, BoardMark
from episode04.boardplotter import BoardPlotter
from episode04.puzzle import Puzzle

from episode05.common import BoardStates, NormClueType, SolutionType


class BoardGameEngine:
    """Provide utilities for board game."""

    # TODO separer track board et track check_move
    def __init__(self, a_puzzle: Puzzle, track: bool = False):
        """Construct a GameEngine."""
        self.puzzle = a_puzzle
        self.track = track

        # init the experiment
        self.plotter = BoardPlotter(a_puzzle)
        self.tracker = GameTracker()
        self.nb_trials = 0

        # init a trial
        self.reset_trial()

    def reset_trial(self) -> None:
        """Reset the board and error count for a new trial.

        Does not alter history.
        """
        # init board
        self.board = Board(self.puzzle)
        # init score
        self.errors = 0
        # increment trials counter
        self.nb_trials += 1
        self.tracker.next_trial()

    def count_empty(self) -> int:
        """Get the number of empty cells."""
        return self.board.count_empty()

    # TODO move to board and factor in
    def count_black(self) -> int:
        """Evaluate the number of black cells."""
        length = reduce(mul, self.board.states.shape)
        count = len([c for c in self.board.states.reshape(length)
                     if c == BoardMark.BLACK.value])
        return count

    def count_errors(self) -> int:
        """Get the number of errors.

        By convention, empty cells are not errors.

        Returns
        -------
        int
            The number of errors. Empty cells  are not considered as error.
        """
        return self.errors

    def check_solved(self) -> None:
        """Check whether the puzzle is solved and store the result.

        Accept that filler cells are left undefined.
        In other words it only takes blacks into account.
        """
        is_completed = self.puzzle.get_black_count() == self.count_black()
        self.tracker.mark_solved(self.errors == 0 and is_completed)

    def is_solved(self) -> bool:
        """Return True if the puzzle is solved.

        Accept that filler cells are left undefined.
        In other words it only takes blacks into account.

        returns
        -------
        bool
            True if the game is solved
        """
        return self.tracker.is_solved

    def play(self, row: int, col: int, mark: BoardMark) -> bool:
        """Play one cell.

        Parameters
        ----------
        row: int
            vertical position of the mark. Should be between 0 and height-1.
        col: int
            horizontal position of the mark. Should be between 0 and wirth-1.
        mark: BoardMark
            The mark to be place. it is defined by the Enum BoardMark.

        Returns
        -------
        bool
            True if the move is correct
        """
        success = self.check_move(row, col, mark)
        # apply the given state
        effective_mark = self.fix_move(row, col, mark)
        self.board.mark(row, col, effective_mark)
        self.check_solved()
        if self.track:
            # will be added to the sequence of solutions
            self.tracker.add_move(self.board)
            self.tracker.record_error_count(self.errors)
        return success

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

    # TODO accept np array
    # TODO same semantic ad not solved and add a compare
    # TODO isoler check de play
    def submit(self, states_list: List[int]) -> int:
        """Submit the solution.

        Submit the solution and give all the cells's state in one action.
        It is not required to provide all the cells values;
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
            The number of errors computed as the number of black cells that
            do not match the solution.
        """
        # end the game with this solutions
        self.board.fill_all(states_list)

        # board is okay when blacks are correrct
        self.check_board(states_list)
        self.check_solved()

        if self.track:
            # will be added to the sequence of solutions
            self.tracker.add_board(self.board)
            self.tracker.record_error_count(self.errors)

        return self.errors

    def check_move(self, row: int, col: int, mark: BoardMark) -> bool:
        """Check whether the move is correst.

        Must be implemented by the sub class

        Parameters
        ----------
        row: int
            vertical position of the mark. Should be between 0 and height-1
        col: int
            horizontal position of the mark. Should be between 0 and wirth-1
        mark: BoardMark
            The mark to be place. it is defined by the Enum BoardMark
        """
        pass

    def fix_move(self, row: int, col: int, mark: BoardMark) -> BoardMark:
        """Get the true value in the solution.

        Does nothing by default

        Parameters
        ----------
        row: int
            vertical position of the mark. Should be between 0 and height-1
        col: int
            horizontal position of the mark. Should be between 0 and wirth-1
        mark: BoardMark
            The mark to be place. it is defined by the Enum BoardMark

        Returns
        -------
        BoardMark
            The mark given by the solver
        """
        return mark

    def check_board(self, states_list: List[int]) -> None:
        """Compute the number of errors on the board.

        It is not required to provide all the cells values;
        Only Blacks are taken into account.

        Parameters
        ----------
        states_list: List[int]
            The cell states as a one dimension list of -1,0,1
            corresponding to marks defined in BoardMark.
        """
        pass

    def show(self) -> None:
        """Plot the board."""
        self.plotter.show(self.board.states)

    def show_all(self) -> None:
        """Plot the board states.

        States are captured by submit and play.
        Silent is track is off.
        """
        if self.track:
            if self.tracker.mode == 0:  # obly submitted boards
                flatten_history = chain(*self.tracker.states_history)
                print(flatten_history)
                self.plotter.show_many(list(flatten_history))
            else:  # multiple moves
                for pos in range(len(self.tracker.states_history)):
                    self.plotter.show_many(self.tracker.states_history[pos])
            # TODO separer moves et board submit
        else:
            print("tracking is off")


class NonoGameEngine(BoardGameEngine):
    """Provide utilities for nonogram game without a given solution."""

    def __init__(self, a_puzzle: Puzzle, track: bool = False):
        """Construct a GameEngine."""
        super().__init__(a_puzzle, track)

        self.track = track

    def check_move(self, row: int, col: int, mark: BoardMark) -> bool:
        """Check whether the move is correst.

        Always return True. To be implemented.

        Parameters
        ----------
        row: int
            vertical position of the mark. Should be between 0 and height-1
        col: int
            horizontal position of the mark. Should be between 0 and wirth-1
        mark: BoardMark
            The mark to be place. it is defined by the Enum BoardMark

        Returns
        -------
        bool
            True if the mark is correct
        """
        # TODO
        return True

    def check_board(self, states_list: List[int]) -> None:
        """Compute the difference between given board states sum and clues.

        It is not required to provides all the cells values.
        Missing Blacks are counted as errors. Fillers are ignored.

        Parameters
        ----------
        states_list: List[int]
            The cell states as a one dimension list of -1,0,1
            corresponding to marks defined in BoardMark.
        """
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

        # row error => col error
        self.errors = int((rows_errors + cols_errors) / 2)

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

    def check_move(self, row: int, col: int, mark: BoardMark) -> bool:
        """Compute the difference between given cell and solution.

        Parameters
        ----------
        row: int
            vertical position of the mark. Should be between 0 and height-1
        col: int
            horizontal position of the mark. Should be between 0 and wirth-1
        mark: BoardMark
            The mark to be place. it is defined by the Enum BoardMark

        Returns
        -------
        bool
            True if the mark is correct
            (same mark in the solution at the same location)
        """
        okay = self.solution[row, col] == mark.value
        if not okay:
            self.errors += 1
        return bool(okay)

    def fix_move(self, row: int, col: int, mark: BoardMark) -> BoardMark:
        """Get the true value in the solution.

        Parameters
        ----------
        row: int
            vertical position of the mark. Should be between 0 and height-1
        col: int
            horizontal position of the mark. Should be between 0 and wirth-1
        mark: BoardMark
            The mark to be place. it is defined by the Enum BoardMark

        Returns
        -------
        BoardMark
            The mark given by the solution
        """
        true_mark = BoardMark(self.solution[row, col])
        return true_mark

    def check_board(self, states_list: List[int]) -> None:
        """Compute the difference between given board states and solution.

        Check whether the states is correct given the registered solution.

        The number of errors computed as the number of black cells that
        do not match the solution.

        Parameters
        ----------
        states_list: List[int]
            The cell states as a one dimension list of -1,0,1
            corresponding to marks defined in BoardMark.
        """
        self.errors = sum([abs(p - e)
                           for (p, e) in zip(states_list, self.flat_solution)
                           if p >= 0])


class GameTracker:
    """Provide utilities for board game tracking."""

    def __init__(self) -> None:
        """Construct a GameTracker."""
        self.states_history: List[List[BoardStates]] = []
        self.error_count_history: List[BoardStates] = []
        self.current = -1
        self.mode = 0  # board
        self.is_solved = False

    def mark_solved(self, status: bool = True) -> None:
        """Mark the game solved if status is True.

        Parameters
        ----------
        status: bool
            the status True (if solved)  or False (failed)
        """
        self.is_solved = status

    def next_trial(self) -> None:
        """Switch to a new trial.

        Ignore repeated next_trial at startup
        """
        self.is_solved = False

        if self.current == 0:
            no_state = len(self.states_history[0]) == 0
            no_count = self.error_count_history[0] == -1
            if no_state and no_count:
                # repeated next_trial
                return

        self.current += 1
        self.states_history.append([])
        self.error_count_history.append(-1)

    def add_move(self, board: Board) -> None:
        """Add a move."""
        self.mode = 1  # move
        self.add_board(board)

    def add_board(self, board: Board) -> None:
        """Add a board."""
        self.states_history[self.current].append(board.states.copy())

    def record_error_count(self, count: int) -> None:
        """Set the number of errors for the current trial."""
        self.error_count_history[self.current] = count

    def print_stats(self) -> None:
        """Print statistics."""
        nb = len(self.error_count_history)
        print(f'Nb trials: {nb}')
        status = 'solved' if self.is_solved else 'failed'
        print(f'Status: {status}')
        for i, c in enumerate(self.error_count_history):
            print(f'{i+1}: {c} errors')
