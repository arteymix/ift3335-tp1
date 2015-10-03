# -*- coding: utf-8 -*-

from aima.search import *
import numpy as np

class Sudoku(Problem):
    """
    Définition du probleme de Sudoku comme un problème de recherche dans
    l'espace d'états.

    L'état initial est supposé valide.
    """

    def actions(self, state):
        """
        Les actions sont déterminées en retournant les possibilitiés qui
        manquent simultanément dans une ligne, colonne et grille correspondantes
        à une case.

        La position de la case et la nouvelle valeur possible est retournée sous
        forme d'un triplet (i, j, k).
        """
        for i, j in zip(*np.where(state == 0)):
            line = state[i]
            column = state[:,j]
            print("ij",i,j)
            square = state[i//3:i//3+3,j//3:j//3+3]
            print("s",square)
            for k in range(1, 10):
                # valide la nouvelle configuration et s'assurant qu'une même
                # valeur non-nulle n'apparait pas plus d'une fois dans la ligne,
                # colonne et carré correspondant
                if k not in line and k not in column and k not in square:
                    yield (i,j,k)

    def _validate(self, state):
        """Détermine si une configuration donnée est valide."""
        for i, j in zip(*np.where(state > 0)):
            line = state[i]
            column = state[:,j]
            square = state[i//3:i//3+3,j//3:j//3+3]

            if any([max(x) > 1 for x in map(lambda x: np.bincount(x) if len(x)>2 else [0],
                    [line[line.nonzero()],
                    column[column.nonzero()],
                        square[square.nonzero()]])]):
                return False
        return True


    def result(self, state, action):
        """
        Calcule la configuration résultante à appliquer une action sur une
        configuration.

        Le nouvel état est une copie modifiée de l'état passé en argument.
        """
        i,j,k = action
        new_state = np.array(state)
        new_state.itemset((i, j), k)
        return new_state

    def goal_test(self, state):
        """Vérifie si une grille est complète en supposant que l'état est valide"""
        return 0 not in state

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""

        i,j,k = action

        s = set(state1[i]).union(set(state1[:,j])).union(set(state1[i//3:i//3+3,j//3:j//3+3].flatten()))
        return 9 - len(s - {0})

    def value(self, state):
        """
        The value of a state is determined by the sum of remaining possibilities
        for each cell in the grid.
        """
        state = np.array(state) # manipulate a copy
        possibilities = 0
        for i, j in zip(*np.where(state == 0)):
            for k in range(1, 10):
                if self._validate(state.itemset((i, j), k)):
                    possibilities += 1
            state.itemset((i, j), 0)
        return possibilities

def load_example(path):
    """" load file at path and each line to cast to Sudoku instance"""

    file = open(path,'r')
    example_list = []
    for line in file:
        m = np.array([int(c) for c in list(line)[:-1]])
        m = np.array(m.reshape([9,9]))
        example_list.append(Sudoku(m))

    return example_list

ex = load_example('examples/100sudoku.txt')

import time

#Décommenter la ligne pour faire un dept-first-search. Attention, ça prends longtemps.

a = time.clock()
print(ex[0].initial)
#sol = depth_first_tree_search(ex[0])
b = time.clock()
#print(sol)
print(b-a)
