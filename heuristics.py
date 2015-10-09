# -*- coding: utf-8 -*-

import math
import numpy as np
from sudoku import numpify_state

def remaining_possibilities(node):
    state = numpify_state(node.state)
    possibilities = 0
    for i, j in zip(*np.where(state == 0)):
        line = state[i]
        column = state[:,j]
        square = state[i//3*3:i//3*3+3,j//3*3:j//3*3+3]
        possibilities += len(reduce(np.setdiff1d, [np.arange(1, 10), line, column, square.flatten()]))
    return possibilities

def remaining_lines(node):
    """ heuristic for sudoku """
    state = numpify_state(node.state)
    empty = 0
    for line in state:
        empty += 2**line[line == 0].size
    return empty

def remaining_blanks(node):
    """ heuristic for soduku """
    state = numpify_state(node.state)
    return state[state == 0].size
    blanks = 3 * 729
    for i, j in zip(*np.where(state == 0)):
        line = state[i]
        column = state[:,j]
        square = state[i//3*3:i//3*3+3,j//3*3:j//3*3+3]
        blanks -= line[line == 0].size * column[column == 0].size * square[square == 0].flatten().size
    return blanks

def non_inferable_cells(node):
    """
    Compte le nombre de cases qui ne peuvent pas être inférées, soit les cases
    qui ont plus d'une possibilité.
    """
    state = numpify_state(node.state)
    non_inferable = 0
    for i, j in zip(*np.where(state == 0)):
        line = state[i]
        column = state[:,j]
        square = state[i//3*3:i//3*3+3,j//3*3:j//3*3+3]
        possibilities = len(reduce(np.setdiff1d, [np.arange(1, 10), line, column, square.flatten()]))
        if possibilities > 1:
            non_inferable += 1
    return non_inferable

def conflicts(node):
    """heuristic for FilledSudoku """
    state = numpify_state(node.state)
    conflicts = 0
    for i in xrange(9):
        for j in xrange(9):
            value = state[i][j]
            line = state[i]
            column = state[:,j]
            conflicts += line[line == value].size + column[column == value].size - 2
    return conflicts

