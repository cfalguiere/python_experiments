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

clues5x5 = {
    'rows': [1, 2, 2, 3, 5],
    'cols': [5, 4, 3, 1, 1]
}

solution5x5 = np.array([[1, 0, 0, 0, 0],
                        [1, 1, 0, 0, 0],
                        [1, 1, 0, 0, 0],
                        [1, 1, 1, 0, 0],
                        [1, 1, 1, 1, 1]])

# xoooo
# xxooo
# xxooo
# xxxoo
# xxxxx

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
    'rows': [1, 3, [1, 1], 3, 5],
    'cols': [1, 4, [2, 2], 4, 1]
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
