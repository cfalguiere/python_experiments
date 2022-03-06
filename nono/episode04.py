import numpy as np

# ------------------------

# given input for a 2x2 puzzle

# Please note that list are base 0 in Python 
# Thus clues['cols'][0] is the left most column
#     and clues['cols'][1] is the second columns from the left

# 1 denotes that the row has 1 contiguous black cells 
#     and a filler of 1 which position is unknown
# 2 denotes that all cells are black

clues2x2 = {
    'rows': [1, 2],
    'cols': [2, 1]
}

# If o marks blacks and x marks fillers, the solution is 
# ox
# xx 

solution2x2 = np.array([[1, 0],  
                        [1, 1]])

# ------------------------

# game instructions for a 5x5 game

# Please note that list are base 0 in Python 
# Thus clues['cols'][0] is the left most column
#     and clues['cols'][1] is the second columns from the left

# 4 denotes that the col has 4 contiguous black cells 
#     and a filler of 1 which position is unknown
# [2,2] denotes that col split blocks 
#     2 contiguous black cells, 
#     a filler which size is unknows 
#     and 2 contiguous black cels

clues5x5s = {
    'rows': [1, 3, [1,1], 3, 5],
    'cols': [1, 4, [2,2], 4, 1]
}

# If o marks blacks and x marks fillers, the solution is 
# xxoxx
# xooox
# xoxox
# xooox
# ooooo

solution5x5s = np.array([[0, 0, 1, 0, 0],
                        [0, 1, 1, 1, 0],
                        [0, 1, 0, 1, 0],
                        [0, 1, 1, 1, 0],
                        [1, 1, 1, 1, 1]])

# ------------------------

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
    Plot the board
    Require %matplotlib inline .
    '''
    
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
    
    
    def __init__(self, a_board):
        '''
        Plotter contructor
        '''
        self.board = a_board
        self.clues = self.board.puzzle.given_clues
      
        def row_clue_to_label(v):
            #print(v)
            return str(v) if not isinstance(v, list) else ' '.join(map(str,v))
        self.rows_labels = list(map(row_clue_to_label, self.clues['rows']))

        def col_clue_to_label(v):
            #print(v)
            return str(v) if not isinstance(v, list) else '\n'.join(map(str,v))
        self.cols_labels = list(map(col_clue_to_label, self.clues['cols']))
    
    
    def show(self):
        '''
        Show the plotter
        '''
        # WARNING :  the board is row col, while the fig is col row
        data = self.board.states
        w = self.board.width
        h = self.board.height
        nc = self.board.width * self.board.height
        
        # set some canvas
        # guess the figure size 
        # 1 fits 2 cells
        # 2 fits 5 cols
        figw = int(w/2) 
        figh = int(h/2) 
        fig, ax = plt.subplots(figsize=(figw,figh))
        # draw a heatmap
        # ensure value range is -1 to 1
        heatmap = ax.pcolor(data, cmap=self.nono_cmap, vmin=-1, vmax=1)

        # ensure square cells
        ax.set_aspect("equal")

        # put the major ticks at the middle of each cell
        ax.set_xticks(np.arange(data.shape[1]) + 0.5, minor=False)
        ax.set_yticks(np.arange(data.shape[0]) + 0.5, minor=False)

        # put labels on top
        ax.invert_yaxis()
        ax.xaxis.tick_top()
        

        # set labels
        column_labels = self.clues['cols']
        row_labels = self.clues['rows']

        ax.set_xticklabels(self.cols_labels, minor=False)
        ax.set_yticklabels(self.rows_labels, minor=False)


        # annotate fillers
        # expect (col,row) is (1,0) for row=0 col=1
        fillers_coordinates = [(p%w + 0.5, int(p/w) + 0.5) 
                               for (p,v) in enumerate(data.reshape(nc)) 
                               if v==0]
        # place an X in the center of each coordinate
        for coord in fillers_coordinates:
            plt.text(coord[0], coord[1], 'x', 
                 verticalalignment='center',
                 horizontalalignment='center',
                 fontsize='xx-large')

        plt.show()
        
# ------------------------

class GameEngine:
    '''
    Provide utilities for this game
    '''
    
    def __init__(self, a_puzzle, a_solution):
        '''
        Engine constructor
        '''
            
        self.puzzle = a_puzzle
        self.solution = a_solution
        
        # init a board
        self.board = Board(a_puzzle)
        self.plotter = BoardPlotter(self.board)
        
        
    def show_board(self):
        ''' 
        Plot the board
        '''
        self.plotter.show()  
        
        
    def is_action_valid(self, row, col, mark):
        ''' 
        Check whether an action is valid given a solution 
        '''
        return self.solution[row, col] == mark.value        
    
    
    def is_expected_solution(self, states_list):
        ''' 
        Check whether the states given a the regidtered solution 
        '''
        flat_solution = self.solution.reshape(self.cells_count).tolist()
        return  flat_solution == states_list
    
    
    def is_solved(self):
        '''
        Check whether the puzzle is solved
        '''
        
        done = True
        if done:
            done = self.board.count_empty() == 0
        if done:
            done = self.get_rows_blocks() == self.puzzle.norm_clues['rows']
        if done:
            done = self.get_cols_blocks() == self.puzzle.norm_clues['cols']
        return done
    
    
    def get_rows_blocks(self):
        '''
        Compute blocks for each rows
        '''
        
        rows = self.board.states
        blocks = [ [len(list(g)) for k,g in groupby(line) if k==1]
               for line in rows
        ]
        return blocks

    
    def get_cols_blocks(self):
        '''
        Compute blocks for each cols
        '''
        
        w = self.board.states.shape[0]
        h = self.board.states.shape[1]
        length = mul(w, h)
        cols = [ [self.board.states.reshape(length)[c+r*w]
             for r in range(0, h)]
             for c in range(0, w)]
        blocks = [ [len(list(g)) for k,g in groupby(line) if k==1]
          for line in cols
        ]
        return blocks
    
    
# ------------------------

