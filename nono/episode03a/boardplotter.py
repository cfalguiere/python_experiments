import numpy as np

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap


class BoardPlotter:
    '''
    Plot the board.
    Requiere %matplotlib inline .
    '''

    def __init__(self, some_clues):
        self.clues = some_clues

        # board dimensions
        self.width = len(self.clues["rows"])
        self.height = len(self.clues["cols"])
        self.flat_length = self.width * self.height

        # guess the figure size
        # rule of thumb
        # 1 fits 2 cells
        # 2 fits 5 cols
        self.fig_width = int(self.width/2)
        self.fig_height = int(self.height/2)

        # rows labels
        def row_clue_to_label(v):
            return str(v) if not isinstance(v, list) else ' '.join(map(str, v))
        self.rows_labels = list(map(row_clue_to_label, self.clues['rows']))

        # columns labels
        def col_clue_to_label(v):
            # print(v)
            return str(v) if not isinstance(v, list) else '\n'.join(map(str, v))
        self.columns_labels = list(map(col_clue_to_label, self.clues['cols']))

        # color map
        self.cmap = self.build_color_map()

    def build_color_map(self):
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
        # WARNING :  the board is row col, while the fig is col row
        data = a_board.states

        # set some canvas
        fig, ax = plt.subplots(figsize=(self.fig_width, self.fig_height))

        # draw a heatmap
        # ensure value range is -1 to 1
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
        fillers_coordinates = [(p % self.width + 0.5, int(p/self.width) + 0.5)
                               for (p, v) in enumerate(data.reshape(self.flat_length))
                               if v == 0]

        # place an X in the center of each coordinate for fillers
        for coord in fillers_coordinates:
            plt.text(coord[0],
                     coord[1],
                     'X',
                     verticalalignment='center_baseline',
                     horizontalalignment='center',
                     fontsize='xx-large')

        plt.show()
