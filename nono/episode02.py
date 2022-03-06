import numpy as np

# ---------------
solution2x2 = np.array([[1, 0],  
                        [1, 1]])

solution5x5s = np.array([[0, 0, 1, 0, 0],
                        [0, 1, 1, 1, 0],
                        [0, 1, 0, 1, 0],
                        [0, 1, 1, 1, 0],
                        [1, 1, 1, 1, 1]])
# ---------------

class GameEngine:
    def __init__(self, some_clues, a_solution):
        self.clues = some_clues
        self.solution = a_solution
        
        self.width = len(some_clues['cols'])
        self.height = len(some_clues['rows'])
        self.black_count = sum(some_clues['rows'])
        self.cells_count = self.width * self.height
        
    def is_action_valid(self, row, col, mark):
        return self.solution[row, col] == mark.value        
    
    def is_board_valid(self, states_list):
        flat_solution = self.solution.reshape(self.cells_count).tolist()
        return  flat_solution == states_list
    