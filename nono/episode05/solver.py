"""Solver components."""
from random import randint, seed

from episode04.board import BoardMark

from episode05.gameengine import NonoGameEngine


class NonoSolver:
    """Base class for solvers."""

    def __init__(self, a_game: NonoGameEngine):
        """Construct a Solver.

        SBase of all solvers

        Parameters
        ----------
        a_game: NonoGameEngine
            The game to solve.
        """
        self.game = a_game
        self.puzzle = a_game.puzzle

    def solve(self) -> None:
        """Solve the game."""
        pass


class TryAndErrorSolver(NonoSolver):
    """Try & Error solver.

    Play random moves. May require multiple trials until the board is solved.
    """

    def __init__(self, a_game: NonoGameEngine):
        """Construct a Solver.

        SBase of all solvers

        Parameters
        ----------
        a_game: NonoGameEngine
            The game to solve.
        """
        super().__init__(a_game)
        seed(42)

    def solve(self) -> None:
        """Solve the game."""
        for row in range(self.puzzle.height):
            for col in range(self.puzzle.width):
                self.game.play(row, col, BoardMark.BLACK)


class RandomSolver(NonoSolver):
    """Random solver.

    Build random board and submit them.
    May require multiple trials until the board is solved.
    """

    def __init__(self, a_game: NonoGameEngine):
        """Construct a Solver.

        SBase of all solvers

        Parameters
        ----------
        a_game: NonoGameEngine
            The game to solve.
        """
        super().__init__(a_game)
        seed(42)

    def solve(self) -> None:
        """Solve the game."""
        MAX_COUNT = 10
        while not self.game.is_solved() and self.game.nb_trials < MAX_COUNT:
            self.game.reset_trial()
            states = []
            for i in range(self.puzzle.height * self.puzzle.width):
                v = randint(0, 1)
                states.append(v)

            self.game.submit(states)
