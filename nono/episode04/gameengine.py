"""Board game and Nonogram related componenets."""

from itertools import groupby
from operator import mul

from episode04.board import Board, BoardMark
from episode04.boardplotter import BoardPlotter


class BoardGameEngine:
    """Provide utilities for board game."""

    def __init__(self, a_puzzle):
        """Construct a GameEngine."""
        self.puzzle = a_puzzle

        # init a board
        self.board = Board(a_puzzle)
        self.plotter = BoardPlotter(a_puzzle)

    def play(self, row, col, mark, apply=True):
        """Play one cell.

        Implementation shouod be provided by the subclass.
        It is used in play_multiple.
        """
        pass

    def play_multiple(self, row, col, mark, axis, count):
        """Play multiple cells."""
        if axis == 0:  # row
            for i in range(col, min(self.puzzle.width, col + count)):
                self.play(row, i, mark)
        if axis == 1:  # row
            for i in range(row, min(self.puzzle.height, row + count)):
                self.play(i, col, mark)

    def show(self):
        """Plot the board."""
        self.plotter.show(self.board)


class NonoGameEngine(BoardGameEngine):
    """Provide utilities for nonogram game without a given solution."""

    def __init__(self, a_puzzle, track=False):
        """Construct a GameEngine."""
        super().__init__(a_puzzle)

        self.track = track
        self.board_states_history = []

    def play(self, row, col, mark, apply=True):
        """Play one cell.

        Play the game by sending the state of one cell.
        Always return True.
        If apply, update the board.
        """
        if apply:
            # apply the given state
            self.board.mark(row, col, mark)
            if self.track:
                self.board_states_history.append(self.board.states.copy())
        return True

    # todo append submissions`
    # todo autofill
    def submit(self, states_list):
        """Submit the solution.

        Submit the solution and give all the cells's state in one action.
        Check whether the states given a the registered solution
        Returns the number of errors.
        Missing Blacks are counted as errors - fillers are ignored.
        """
        self.board.fill_all(states_list)
        if self.track:
            self.board_states_history.append(self.board.states.copy())

        # board is okay if without errors on blacks
        return self.count_errors()

    def is_solved(self):
        """Check whether the puzzle is solved.

        Accept that filler cells are left undefined.
        In other words it only takes blacks into account.
        """
        return self.count_errors() == 0

    def count_empty(self):
        """Get the number of empty cells."""
        return self.board.count_empty()

    # todo document that ignore unfilled
    def count_errors(self):
        """Compute the difference between given board states sum and clues."""
        # for rows
        board_rows = self.get_rows_blocks()
        clues_rows = self.puzzle.norm_clues['rows']
        rows_errors = sum([abs(sum(b) - sum(c))
                           for (b, c) in zip(board_rows, clues_rows)])
        # for cols
        board_cols = self.get_cols_blocks()
        clues_cols = self.puzzle.norm_clues['cols']
        cols_errors = sum([abs(sum(b) - sum(c))
                           for (b, c) in zip(board_cols, clues_cols)])
        return int((rows_errors + cols_errors) / 2)  # row error => col error

    def get_rows_blocks(self):
        """Compute blocks for each rows."""
        rows = self.board.states
        blocks = [[len(list(g)) for k, g in groupby(line) if k == 1]
                  for line in rows]
        return blocks

    def get_cols_blocks(self):
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

    def show_all(self):
        """Plot the board states.

        States are captured by submit and play.
        Silent is track is off.
        """
        if self.track:
            self.plotter.show_all(self.board_states_history)
        else:
            print("tracking is off")


class SolvedNonoGameEngine(NonoGameEngine):
    """Provide utilities for nonogram game with a given solution."""

    def __init__(self, a_puzzle, a_solution, track=False):
        """Construct a GameEngine."""
        super().__init__(a_puzzle, track)

        self.solution = a_solution
        cells = self.puzzle.cells_count
        self.flat_solution = self.solution.reshape(cells).tolist()

        # init score
        self.errors = 0

    def play(self, row, col, mark, apply=True):
        """Play one cell.

        Play the game by sending the state of one cell.
        Check whether an action is valid given a solution.
        If apply is True, update the board.
        """
        okay = self.solution[row, col] == mark.value
        if not okay:
            self.errors += 1

        if apply:
            # apply the real state which is what games usually do
            true_mark = BoardMark(self.solution[row, col])
            self.board.mark(row, col, true_mark)
            if self.track:
                self.board_states_history.append(self.board.states.copy())
        return okay

    # TODO accept np array
    def submit(self, states_list, apply=True):
        """Submit the solution.

        Submit the solution and give all the cells's state in one action.
        Check whether the states given a the registered solution.
        """
        if apply:
            self.board.fill_all(states_list)

        if self.track:
            self.board_states_history.append(self.board.states.copy())

        # board is okay when blacks are correrct
        self.errors = sum([abs(p - e)
                           for (p, e) in zip(states_list, self.flat_solution)
                           if p >= 0])
        return self.errors

    # todo document that ignore unfilled
    def count_errors(self):
        """Get the number of errors.

        By convention, unfilled are not errors.

        Returns:
            int: The number of errors.
        """
        return self.errors
