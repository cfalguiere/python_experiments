## with puzzle class and validation

import numpy as np
from enum import Enum
from itertools import groupby, chain
from operator import mul
from functools import reduce


class Puzzle:
    ''' Define the game clues and constants'''
    
    def __init__(self, some_clues):
        '''
        puzzle constructor
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
        f_norm_clue = lambda clue: clue if isinstance(clue, list) else [clue]
        norm_clues = {
            'rows': [f_norm_clue(clue) for clue in self.given_clues['rows']],
            'cols': [f_norm_clue(clue) for clue in self.given_clues['cols']]
        }
        return norm_clues

    def get_black_count(self, axis='rows'):
        return sum(chain.from_iterable(self.norm_clues[axis]))
      
    def is_valid(self):
        return self.get_black_count(axis='rows') == self.get_black_count(axis='cols')
    
    
    
# constants for mark lette
class BoardMark(Enum):
    INIT = -1
    FILLER = 0
    BLACK = 1

class Board:
    '''
    Manage the board.
    '''
    
    def __init__(self, some_puzzle):
        '''
        board constructor
        '''
        # given parameters
        self.puzzle = some_puzzle
        
        # compute board dimensions
        self.width = some_puzzle.width
        self.height = some_puzzle.height
        self.cells_count = some_puzzle.cells_count
        
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

    def is_done(self):
        done = True
        if done:
            done = self.count_empty() == 0
        if done:
            done = self.get_rows_blocks() == self.puzzle.norm_clues['rows']
        if done:
            done = self.get_cols_blocks() == self.puzzle.norm_clues['cols']
        return done


    def count_empty(self):
        length = reduce(mul, self.states.shape)
        count = len([ c for c in self.states.reshape(length) 
                             if c == -1])
        return count    
    
    def get_rows_blocks(self):
        rows = self.states
        blocks = [ [len(list(g)) for k,g in groupby(line) if k==1]
               for line in rows
        ]
        return blocks

    def get_cols_blocks(self):
        w = self.states.shape[0]
        h = self.states.shape[1]
        length = mul(w, h)
        cols = [ [self.states.reshape(length)[c+r*w]
             for r in range(0, h)]
             for c in range(0, w)]
        blocks = [ [len(list(g)) for k,g in groupby(line) if k==1]
          for line in cols
        ]
        return blocks