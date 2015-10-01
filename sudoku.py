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
        print "non-empty index", np.where(state == 0)
        for i, j in zip(*np.where(state == 0)):
            for k in range(1, 10):
                new_state = np.array(state)
                new_state.itemset((i, j), k)

                line = new_state[i]
                column = new_state[:,j]
                print("ij",i,j)

                square = new_state[i//3:i//3+3,j//3:j//3+3]
                print("s",square)
                # valide la nouvelle configuration et s'assurant qu'une même
                # valeur non-nulle n'apparait pas plus d'une fois dans la ligne,
                # colonne et carré correspondant
                if all([x.max() <= 1 for x in map(lambda x: np.bincount(x) if len(x)>2 else 1,
                                                                [line[line.nonzero()],
                                                                column[column.nonzero()],
#                                                                square[square.nonzero()].flatten()])]): #
                                                                square[square.nonzero()]])]):
                    yield new_state

    def result(self, state, action):
        return action

    def goal_test(self, state):
        """Vérifie si une grille est complète en supposant que l'état est valide"""
        return 0 not in state

    def value(self, state) :
        pass

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

a = time.clock()
print(ex[0].initial)
sol = depth_first_tree_search(ex[0])
b = time.clock()
print(sol)
print(b-a)
