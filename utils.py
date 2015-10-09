# -*- coding: utf-8 -*-

"""
Utilitaires pour manipuler, valider et calculer sur un état d'une grille de
Sudoku.
"""

from itertools import product
import numpy as np

def compact(state):
    if isinstance(state[0], frozenset):
        return compact(map(lambda i: list(i)[0] if len(i) == 1 else 0, state))
    return ''.join(map(str, state))

def load_examples(path):
    with open(path, 'r') as f:
        for line in f:
            yield tuple(map(int, line[:-1]))

def numpify_state(state):
    """Génère une représentation facilement manipulable d'un état Sudoku."""
    return np.array(state).reshape((9,9))

def validate_state(state):
    """Valide l'état d'une grille de Sudoku"""
    state = numpify_state(state)
    for i, j in zip(*np.where(state > 0)):
        line = state[i]
        column = state[:,j]
        square = state[3*(i//3):3*(i//3)+3,3*(j//3):3*(j//3)+3]

        if any([max(x) > 1 for x in map(lambda x: np.bincount(x) if len(x)>2 else [0],
                [line[line.nonzero()],
                column[column.nonzero()],
                    square[square.nonzero()]])]):
            return False
    return True

def count_possibilities(state, i, j):
    """
    Compte les possibilités dans une case donnée étant donné une représentation
    par ensembles de possibilités.
    """
    state = numpify_state(state)
    line = state[i]
    column = state[:,j]
    square = state[i//3*3:i//3*3+3,j//3*3:j//3*3+3]
    return len(reduce(np.setdiff1d, [np.arange(1, 10), line, column, square.flatten()]))

vlen = np.vectorize(len)
vpretty = np.vectorize(lambda x: list(x)[0] if len(x) == 1 else 0)

def normalize_state(state):
    """
    Reduce the state in its np.array representation to its minimal
    expression by applying iteratively all possible logical inference.

    'None' is returned if the normalization leads to an invalid state (due to a
    wrong hypothesis).
    """
    state = np.array(state) # mutate a copy
    while True:
        to_normalize = state[vlen(state) == 1].size # nombre de positions à réduire
        for i, j in zip(*np.where(vlen(state) == 1)):
            line = state[i]
            column = state[:,j]
            square = state[i//3*3:i//3*3+3,j//3*3:j//3*3+3]

            value = state[i,j]

            # reduce line
            for line_j, item in enumerate(line):
                if value < state[i,line_j]:
                    state[i,line_j] = item - value

            # reduce column
            for column_i, item in enumerate(column):
                if value < state[column_i,j]:
                    state[column_i,j] = item - value

            # reduce square
            for square_position, item in zip(product(range(0,3), range(0,3)), square.flatten()):
                x, y = i//3*3+square_position[0], j//3*3 + square_position[1]
                if value < state[x,y]:
                    state[x,y] = item - value

        if state[vlen(state) == 1].size == to_normalize:
            break # aucune réduction appliquée

    return state
