"""Board plotter components."""

from math import ceil

from episode03b.board import Board

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

import numpy as np


class BoardPlotter:
    """Plot the board.

    Require %matplotlib inline.
    """

    def __init__(self, a_puzzle):
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

        # rows labels
        def row_clue_to_label(v):
            is_value = not isinstance(v, list)
            return str(v) if is_value else ' '.join(map(str, v))
        self.rows_labels = list(map(row_clue_to_label, self.clues['rows']))

        # columns labels
        def col_clue_to_label(v):
            # print(v)
            is_value = not isinstance(v, list)
            return str(v) if is_value else '\n'.join(map(str, v))
        self.columns_labels = list(map(col_clue_to_label, self.clues['cols']))

        # color map
        self.cmap = self.build_color_map()

        # collection of boards to be plotted
        self.boards = []

    def build_color_map(self):
        """Build a colormap for black/white boards.

        Color switch at 0.5.
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

    def show(self, a_board):
        """Plot the board."""
        # set some canvas
        # a_board.prettyprint()
        _fig, ax = plt.subplots(figsize=(self.fig_width, self.fig_height))
        self._plot(a_board, ax)
        plt.show()  # plt is static

    def append_board(self, a_board):
        """Append a board to a list of boards (history of states)."""
        self.boards.append(a_board)

    def show_all(self, some_boards=None):
        """Plot several boards."""
        boards = some_boards
        if some_boards is None:
            boards = self.boards

        # max 12
        # TODO nb depending on board size
        cols_mapping = {2: 7, 5: 5}
        n_cols = cols_mapping[self.width]
        n_lines = ceil(len(boards) / n_cols)

        fig = plt.figure()
        fig.subplots_adjust(left=5, right=15, top=13, bottom=5)

        for i, board in enumerate(boards):
            # enumerate is base 0. figures are labelled base 1
            # TODO explain slots names
            plt.rcParams['figure.figsize'] = [self.fig_width, self.fig_height]
            ax = fig.add_subplot(n_lines, n_cols, i + 1)
            self._plot(board, ax)

        plt.show()  # plt is static

    # private method
    def _plot(self, a_board, ax):
        # WARNING :  the board is row col, while the fig is col row
        if isinstance(a_board, Board):
            print("data is a board")
            data = a_board.states
        else:
            print("data is an array")
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
