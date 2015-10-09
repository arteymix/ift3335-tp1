# -*- coding: utf-8 -*-

import numpy as np
from sudoku import numpify_state

def most_constrained_cell(node):
    if node.parent is None:
        return 0
    state = numpify_state(node.parent.state)
    i, j, k = node.action

    line = state[i]
    column = state[:,j]
    square = state[i//3*3:i//3*3+3,j//3*3:j//3*3+3]
    return len(reduce(np.setdiff1d, [np.arange(1, 10), line, column, square.flatten()]))

def remaining_blanks(node):
    """Heuristique basée sur le nombre de cases vides."""
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
    """Heuristique qui compte le nombre de conflits dans une grille pour un
    Sudoku remplit aléatoirement."""
    state = numpify_state(node.state)
    conflicts = 0
    for i in xrange(9):
        for j in xrange(9):
            value = state[i][j]
            line = state[i]
            column = state[:,j]
            conflicts += line[line == value].size + column[column == value].size - 2
    return conflicts

