## with validation

import numpy as np
from enum import Enum
from itertools import groupby, chain

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
        
        # normalize clues
        self.norm_clues = self.check_clues(some_clues)
        
        # compute board dimensions
        self.width = len(self.clues['cols']) 
        self.height = len(self.clues['rows']) 
        self.count_cells = self.width * self.height
        self.total_blacks = sum(chain.from_iterable(self.norm_clues['rows']))
        
        # create board of type int, initialized with -1
        default_value = BoardMark.INIT.value
        self.states = np.full((self.height, self.width), default_value, dtype=int)
    
    def check_clues(self, clues):
        f_norm_clue = lambda clue: clue if isinstance(clue, list) else [clue]
        norm_clues = {
            'rows': [f_norm_clue(clue) for clue in clues['rows']],
            'cols': [f_norm_clue(clue) for clue in clues['cols']]
        }
        return norm_clues
        
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

    def count_cells_left(self):
        return len([ c 
                  for c in self.states.reshape(self.count_cells) 
                  if c == BoardMark.INIT.value])


    def does_hold_clues(self):

        rows = self.states
        rows_blocks = [ [len(list(g)) for k,g in groupby(row) if k==1]
          for row in rows
        ]
        rows_status = rows_blocks == self.norm_clues['rows'] 
        
        cols = [ [self.states.reshape(self.count_cells)[c+r*self.width]
         for r in range(0, self.height)]
         for c in range(0, self.width)]
        cols_blocks = [ [len(list(g)) for k,g in groupby(col) if k==1]
          for col in cols
        ]
        cols_status = cols_blocks == self.norm_clues['cols'] 

        return rows_status and cols_status
    
    
    def is_done(self):
        no_cells_left = self.count_cells_left() == 0
        return no_cells_left and self.does_hold_clues()
