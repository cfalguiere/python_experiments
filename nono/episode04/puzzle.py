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

        def f_norm_clue(clue): return clue if isinstance(clue, list) else [clue]
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

#
