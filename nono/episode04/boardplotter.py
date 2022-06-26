"""Board plotter components."""

from functools import partial
from math import ceil
from typing import Any, List

from episode04.board import Board
from episode04.common import NormClueType
from episode04.puzzle import Puzzle

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

import numpy as np


class BoardPlotter:
    """Plot the board.

    Require %matplotlib inline.
    """

    def __init__(self, a_puzzle: Puzzle):
        """Construct a BoardPlotter."""
        self.clues = a_puzzle.given_clues

        # board dimensions
        self.width = len(self.clues['rows'])
        self.height = len(self.clues['cols'])
        self.flat_length = self.width * self.height

        # guess the figure size
        # rule of thumb
        # 1 fits 2 cells
        # 2 fits 5 cols
        self.fig_width = int(self.width / 2)
        self.fig_height = int(self.height / 2)

        # labels
        def to_label(v: NormClueType, sep: str = '') -> str:
            return sep.join(map(str, v))

        rows_to_label = partial(to_label, sep=' ')
        cols_to_label = partial(to_label, sep='\n')

        norm_clues = a_puzzle.norm_clues
        self.rows_labels = list(map(rows_to_label, norm_clues['rows']))
        self.columns_labels = list(map(cols_to_label, norm_clues['cols']))

        # color map
        self.cmap = self.build_color_map()

        # collection of boards to be plotted
        self.sequence: List[Board] = []

    def build_color_map(self) -> Any:
        """Build a colormap for black/white boards.

        Color switch at 0.5.

        Returns
        -------
        Any
            The color map built by LinearSegmentedColormap
        """
        cdict = {'red': [(0.0, 0.6196078431372549, 0.6196078431372549),
                         (0.5, 1.0, 1.0),
                         (1.0, 0.03137254901960784, 0.03137254901960784)],
                 'green': [(0.0, 0.792156862745098, 0.792156862745098),
                           (0.5, 1.0, 1.0),
                           (1.0, 0.18823529411764706, 0.18823529411764706)],
                 'blue': [(0.0, 0.8823529411764706, 0.8823529411764706),
                          (0.5, 1.0, 1.0),
                          (1.0, 0.4196078431372549, 0.4196078431372549)],
                 'alpha': [(0.0, 1.0, 1.0),
                           (0.5, 1.0, 1.0),
                           (1.0, 1.0, 1.0)]}
        nono_cmap = LinearSegmentedColormap('nono', cdict)
        return nono_cmap

    def show(self, a_board: Board) -> None:
        """Plot the board."""
        # set some canvas
        fig, ax = plt.subplots(figsize=(self.fig_width, self.fig_height))
        self._plot(a_board, ax)
        plt.show()  # plt is static

    def append_to_sequence(self, a_board: Board) -> None:
        """Append a board to a sequence of boards (history of states)."""
        self.sequence.append(a_board)

    def show_sequence(self) -> None:
        """Show the sequence of boards."""
        self.show_many(self.sequence)

    def show_many(self, some_boards: List[Board]) -> None:
        """Plot several boards."""
        # max 12
        # TODO nb depending on board size
        cols_mapping = {2: 7, 5: 5}
        n_cols = cols_mapping[self.width]
        n_lines = ceil(len(some_boards) / n_cols)

        fig = plt.figure()
        fig.subplots_adjust(left=5, right=15, top=13, bottom=5)

        for i, board in enumerate(some_boards):
            # enumerate is base 0. figures are labelled base 1
            # TODO explain slots names
            plt.rcParams['figure.figsize'] = [self.fig_width, self.fig_height]
            ax = fig.add_subplot(n_lines, n_cols, i + 1)
            self._plot(board, ax)

    # private method
    def _plot(self, a_board: Board, ax: Any) -> None:
        # WARNING :  the board is row col, while the fig is col row
        if isinstance(a_board, Board):
            data = a_board.states
        else:
            data = a_board  # assumes an np array

        # set some canvas
        # fig, ax = plt.subplots(figsize=(self.fig_width, self.fig_height))

        # draw a heatmap
        ax.pcolor(data, cmap=self.cmap, vmin=-1, vmax=1)

        # ensure square cells
        ax.set_aspect("equal")

        # put the major ticks at the middle of each cell
        ax.set_xticks(np.arange(data.shape[1]) + 0.5, minor=False)
        ax.set_yticks(np.arange(data.shape[0]) + 0.5, minor=False)

        # put labels on top
        ax.invert_yaxis()
        ax.xaxis.tick_top()

        # set labels
        ax.set_xticklabels(self.columns_labels, minor=False)
        ax.set_yticklabels(self.rows_labels, minor=False)

        # annotate fillers
        # expect (col,row) is (1,0) for row=0 col=1
        fillers_coordinates =\
            [(p % self.width + 0.5, int(p / self.width) + 0.5)
             for (p, v) in enumerate(data.reshape(self.flat_length))
             if v == 0]

        # place an X in the center of each coordinate for fillers
        for coord in fillers_coordinates:
            ax.text(coord[0], coord[1], 'X',
                    verticalalignment='center_baseline',
                    horizontalalignment='center',
                    fontsize='xx-large')
