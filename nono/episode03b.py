from itertools import chain

class Puzzle:
    '''
    Describe the puzzle clues and constants derived from clues
    '''
    
    def __init__(self, some_clues):
        '''
        Puzzle constructor
        '''
        
        # given parameters
        self.given_clues = some_clues
        
        # normalize clues
        self.norm_clues = self.init_norm_clues()
        
        # compute board dimensions
        self.width = len(some_clues['cols']) 
        self.height = len(some_clues['rows']) 
        self.cells_count = self.width * self.height
        self.required_blacks_count = self.get_black_count()
        
        
    def init_norm_clues(self):
        '''
        Turn clues into a list of lists with one or more integers
        '''

        f_norm_clue = lambda clue: clue if isinstance(clue, list) else [clue]
        norm_clues = {
            'rows': [f_norm_clue(clue) for clue in self.given_clues['rows']],
            'cols': [f_norm_clue(clue) for clue in self.given_clues['cols']]
        }
        return norm_clues

    
    def get_black_count(self, axis='rows'):
        '''
        Compute the number of blacks cells required by the clues 
        for either rows or cols
        '''
        
        return sum(chain.from_iterable(self.norm_clues[axis]))
      
        
    def is_consistent(self):
        '''
        Check clues for consistency between rows and cols definition
        '''
        
        return self.get_black_count(axis='rows') == self.get_black_count(axis='cols')    
    
# ------------------------

import numpy as np
from enum import Enum
from itertools import groupby, chain
from operator import mul
from functools import reduce

# constants for mark lette
class BoardMark(Enum):
    INIT = -1
    FILLER = 0
    BLACK = 1

class Board:
    '''
    Manage the board.
    '''
    
    def __init__(self, a_puzzle):
        '''
        Board constructor
        '''
        # given parameters
        self.puzzle = a_puzzle
        
        # compute board dimensions
        self.width = a_puzzle.width
        self.height = a_puzzle.height
        self.cells_count = a_puzzle.cells_count
        
        # create board of type int, initialized with -1
        default_value = BoardMark.INIT.value
        self.states = np.full((self.height, self.width), default_value, dtype=int)
       
    
    def mark(self, row, col, mark):
        '''
        Mark a cell
        '''
        self.states[row, col] = mark.value

        
    def fill_all(self, states):
        '''
        Uodate all cells with states
        '''
        self.states.flat[:] = states 
        
        
    def count_empty(self):
        '''
        Evaluate how much of the board is filled
        '''
        length = reduce(mul, self.states.shape)
        count = len([ c for c in self.states.reshape(length) 
                             if c == BoardMark.INIT.value])
        return count    
    
        
    def prettyprint(self):
        '''
        Pretty print of the board 
        '''
        print("cols:", end=" ")
        print(*self.puzzle.given_clues['cols']) # * unpacks and remove []s
        print("rows:")
        [print(r) for r in self.puzzle.given_clues['rows']]
          
        marks_switcher = {-1: '.', 0: 'x', 1: 'o'}
        # for whatever reason lambda does not work here
        def f_marks(v):
            return marks_switcher[v]
        applyall = np.vectorize(f_marks)
        marks = applyall(self.states)
        print(marks)
        
        
# ------------------------

import numpy as np

import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import LinearSegmentedColormap

class BoardPlotter:
    '''
    Plot the board.
    Requiere %matplotlib inline .
    '''
    
    def __init__(self, a_puzzle):
        self.clues = a_puzzle.given_clues
        
        # board dimensions
        self.width = len(self.clues["rows"])
        self.height = len(self.clues["cols"])
        self.flat_length = self.width * self.height

        # guess the figure size 
        # rule of thumb
        # 1 fits 2 cells
        # 2 fits 5 cols
        self.fig_width = int(self.width/2) 
        self.fig_height = int(self.height /2) 

        # rows labels
        def row_clue_to_label(v):
            return str(v) if not isinstance(v, list) else ' '.join(map(str,v))
        self.rows_labels = list(map(row_clue_to_label, self.clues['rows']))

        # columns labels
        def col_clue_to_label(v):
            #print(v)
            return str(v) if not isinstance(v, list) else '\n'.join(map(str,v))
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
        heatmap = ax.pcolor(data, cmap=self.cmap, vmin=-1, vmax=1)

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
        fillers_coordinates = [(p%self.width + 0.5, int(p/self.width) + 0.5) 
                               for (p,v) in enumerate(data.reshape(self.flat_length)) 
                               if v==0]

        # place an X in the center of each coordinate for fillers
        for coord in fillers_coordinates:
            plt.text(coord[0], coord[1], 'X', 
                 verticalalignment='center_baseline',
                 horizontalalignment='center',
                 fontsize='xx-large')

        plt.show()

# ------------------------

