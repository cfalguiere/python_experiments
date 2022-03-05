# built in imports
from enum import Enum

# need to import numpy library
# it is provided in most Python environment. If not you install it with pip install numpy
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

# ------------------------

class BoardMark(Enum):
    '''
    Constants for board marks
    '''
    INIT = -1
    FILLER = 0
    BLACK = 1

class Board:
    '''
    Manage the board.
    '''
    
    def __init__(self, some_clues):
        '''
        board constructor
        '''
        # given parameters
        self.clues = some_clues
        
        # compute board dimensions
        self.width = len(self.clues['cols']) 
        self.height = len(self.clues['rows'])
        
        # create board of type int, initialized with -1
        default_value = BoardMark.INIT.value
        self.states = np.full((self.height, self.width), default_value, dtype=int)
        
    def mark(self, row, col, mark):
        '''
        fill the cell with a mark
        '''
        self.states[row, col] = mark.value

    def prettyprint(self):
        '''
        pretty print of the board 
        '''
        print("cols:", end=" ")
        print(*self.clues['cols']) # * unpacks and remove []s
        print("rows:")
        [print(r) for r in self.clues['rows']]
          
        # dictionnaries are used in Python to describe swich cases depending on the value
        marks_switches = {BoardMark.INIT.value:   '.', 
                          BoardMark.FILLER.value: 'x', 
                          BoardMark.BLACK.value:  'o'}
        
        # The switch can be applyed to the full array
        # numpy provides ways to apply a function to all the cells
        # must use vectorize, for whatever reason lambda does not work here
        def switch_mark(v):
            return marks_switches[v]
        
        apply_all_switch_mark = np.vectorize(switch_mark)
        states_repr = apply_all_switch_mark(self.states)
        states_repr        
        
        print(states_repr)
