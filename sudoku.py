# -*- coding: utf-8 -*-

from aima.search import Problem
import numpy as np

class Sudoku(Problem):
    """
    Définition du probleme de Sudoku comme un problème de recherche dans
    l'espace d'états.

    L'état initial est supposé valide.
    """
    def actions(self, state):
        for i, j in np.where(state == 0):
            for k in range(1, 10):
                new_state = np.array(state)
                new_state.itemset([i, j], k)

                line = new_state[i]
                column = new_state[:,j]
                square = new_state[i//3:i//3+3,j//3:j//3+3]

                # valide la nouvelle configuration
                if all(lambda x: x <= 1, map(stats.mode, [line[line>0], column[column>0], square[square>0]])):
                    yield new_state

    def goal_test(self, state):
        """Vérifie si une grille est complète en supposant que l'état est valide"""
        return None not in state
