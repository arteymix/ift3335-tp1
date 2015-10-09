# -*- coding: utf-8 -*-
__author__ = 'ntak'

from aima.search import Problem, depth_first_graph_search, hill_climbing, greedy_best_first_graph_search, astar_search, simulated_annealing
import numpy as np
from itertools import combinations, product

from sudoku import numpify_state, load_examples, validate_state

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
    normalized = False
    while not normalized:
        normalized = True
        for i, j in zip(*np.where(vlen(state) == 1)):
            line = state[i]
            column = state[:,j]
            square = state[i//3*3:i//3*3+3,j//3*3:j//3*3+3]

            value = state[i,j]

            # reduce line
            for line_j, item in enumerate(line):
                if value < state[i,line_j]:
                    state[i,line_j] -= value
                    normalized = False

            # reduce column
            for column_i, item in enumerate(column):
                if value < state[column_i,j]:
                    state[column_i,j] -= value
                    normalized = False

            # reduce square
            for square_position, item in zip(product(range(0,3), range(0,3)), square.flatten()):
                x, y = i//3*3+square_position[0], j//3*3 + square_position[1]
                if value < state[x,y]:
                    state[x,y] -= value
                    normalized = False

    return state

class Sudoku3(Problem):
    """
    Définition du probleme de Sudoku comme un problème de recherche dans un espace d'états.

    L'état est un tableau 9x9 ou chaque case contient une valeur de 1 à 9 ou un ensemble des possibilités restante pour cette case.
    """

    def __init__(self, initial):
        """ Remplit la grille avec des valeurs qui respectent les carrés."""
        initial = numpify_state(initial)

        state = np.array([frozenset(range(1, 10)) if initial[i,j] == 0 else frozenset([initial[i,j]])
                           for i, j in product(range(9),range(9))]).reshape((9,9))

        self.initial = tuple(normalize_state(state).flatten())

    def actions(self, state):
        """
        les actions sont déterminées en retournant les possibilitiés qui
        manquent simultanément dans une ligne, colonne et grille correspondantes
        à une case.

        La position de la case et la nouvelle valeur possible est retournée sous
        forme d'un triplet (i, j, k).
        """
        state = numpify_state(state)

        for i, j in zip(*np.where(vlen(state) > 1)):
            for k in state[i, j]:
                yield i, j, k

    def result(self, state, action):
        """
        Calcule la configuration résultante à appliquer une action sur une
        configuration.

        Le nouvel état est une copie modifiée de l'état passé en argument.
        """
        state = numpify_state(state)

        # remove the
        i, j, k = action

        state[i,j] = frozenset([k])

        # normalize in-place
        normalized_state = normalize_state(state)

        # the action might be a wrong hypothesis
        if not validate_state(vpretty(normalized_state)):
            print 'wrong hypothesis'
            return self.initial

        print normalized_state

        return tuple(normalized_state.flatten())

    def goal_test(self, state):
        """
        Vérifie si tous les ensembles de la grilles sont composés d'un seul
        élément.
        """
        return all(map(lambda x: len(x) == 1, state))

    def value(self, state):
        """
        La valeur d'une grille est déterminée par la somme des possibilités de
        ses cases. 81 est soustrait, car une case sans possibilités contient au
        moins une valeur, soit l'unique possibilité.
        """
        return sum(map(len, state)) - 81

examples = load_examples('examples/100sudoku.txt')

for example in examples:
    s = Sudoku3(example)
    def h(node):
        return s.value(node.state)

    solution, explored = greedy_best_first_graph_search(s, h, bound=10000)
    print vpretty(numpify_state(solution.state)), explored

