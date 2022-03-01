import numpy as np
from enum import Enum

# constants for mark lette
class BoardMark(Enum):
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
        mark a cell
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
          
        marks_switcher = {-1: '.', 0: 'x', 1: 'o'}
        # for whatever reason lambda does not work here
        def f_marks(v):
            return marks_switcher[v]
        applyall = np.vectorize(f_marks)
        marks = applyall(self.states)
        print(marks)
