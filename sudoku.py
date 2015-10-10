# -*- coding: utf-8 -*-

__author__ = 'ntak'

import numpy as np
from itertools import combinations, product
from random import shuffle

from aima.search import Problem, depth_first_graph_search, hill_climbing, greedy_best_first_graph_search

from utils import numpify_state, validate_state, count_possibilities, normalize_state, vlen

class Sudoku(Problem):
    """
    Définition du probleme de Sudoku comme un problème de recherche dans
    l'espace d'états.

    L'état, représenté par un tuple de 81 entiers, est supposé valide.
    """

    def actions(self, state):
        """
        les actions sont déterminées en retournant les possibilitiés qui
        manquent simultanément dans une ligne, colonne et grille correspondantes
        à une case.

        La position de la case et la nouvelle valeur possible est retournée sous
        forme d'un triplet (i, j, k).
        """
        state = numpify_state(state)
        for i, j in zip(*np.where(state == 0)):
            line = state[i]
            column = state[:,j]
            square = state[i//3*3:i//3*3+3,j//3*3:j//3*3+3]
            for k in xrange(1, 10):
                # valide la nouvelle configuration et s'assurant qu'une même
                # valeur non-nulle n'apparait pas plus d'une fois dans la ligne,
                # colonne et carré correspondant
                if k not in line and k not in column and k not in square:
                    yield i, j, k

    def result(self, state, action):
        """
        Calcule la configuration résultante à appliquer une action sur une
        configuration.

        Le nouvel état est une copie modifiée de l'état passé en argument.
        """
        i, j, k = action
        new_state = list(state)
        new_state[i * 9 + j] = k
        return tuple(new_state)

    def goal_test(self, state):
        """Vérifie si une grille est complète en supposant que l'état est valide"""
        return 0 not in state

    def value(self, state):
        """
        The value of a state is determined by the sum of remaining possibilities
        for each cell in the grid.
        """
        state = numpify_state(state)
        possibilities = 729
        for i, j in zip(*np.where(state == 0)):
            line = state[i]
            column = state[:,j]
            square = state[i//3*3:i//3*3+3,j//3*3:j//3*3+3]
            possibilities -= len(reduce(np.setdiff1d, [np.arange(1, 10), line, column, square.flatten()]))
        return possibilities

class RandomizedSudoku(Sudoku):
    """Définition du problème de Sudoku avec branchement aléatoire."""
    def actions(self, state):
        a = list(Sudoku.actions(self, state))
        shuffle(a)
        return a

class SortedSudoku(Sudoku):
    """
    Définition du problème de Sudoku avec branchement triés selon le nombre de
    possibilités pour un choix d'action.
    """
    def actions(self, state):
        return sorted(Sudoku.actions(self, state), key=lambda x: count_possibilities(state, x[0], x[1]))

class FilledSudoku(Sudoku):
    """
    Définition du problème de Sudoku avec initialisation et actions basées sur
    des permutations.
    """

    def __init__(self, initial):
        """Remplit la grille avec des valeurs qui respectent les carrés."""
        state = numpify_state(initial)

        # préserve les positions initiales
        self.initial_positions = list(zip(*np.where(state == 0)))

        # initialise la grille en respect des carrés
        for i, j in zip(*np.where(state == 0)):
            square = state[i//3*3:i//3*3+3,j//3*3:j//3*3+3]
            possibilities = np.setdiff1d(np.arange(1, 10), square.flatten())
            state.itemset((i, j), possibilities[0])

        self.initial = tuple(state.flatten())

    def actions(self, state):
        """
        Énumère les permutations dans les carrés pour chaque position mutable.
        """

        # propose des permutations (x, y) carré par carré
     #   for i, j in product(xrange(3), xrange(3)):
      #      mutable_positions = set(product(range(i*3, i*3+3), range(j*3, j*3+3))) - set(self.initial_positions)
       #     for swap in combinations(mutable_positions, 2):
        #        yield swap
#        return

        #Super-branchement. Génère une enorme quantite de branchement. Mais augmente les chances de trouver un bon resultat.
        #a tester. Faut modifier la fonction result() si ce morceaux la de code est utilisé
        mutable_positions = [[None for i in range(3)] for j in range(3)]
        for i, j in product(range(3), range(3)):
            mutable_positions[i][j] = set(product(range(3*i, 3*i+3), range(3*j, 3*j+3))) - set(self.initial_positions)
            for swap in combinations(mutable_positions[i][j], 2):
                    yield [swap]
                    
        for i in range(3):

            for x, ap in reduce(product,[combinations(mutable_positions[i][j], 2) for j in range(3)]):

            #for x, ap in product([combinations(mutable_positions[i][j], 2) for j in range(3)]):
                s, w = x
                yield s,w,ap
            for x, ap in reduce(product,[combinations(mutable_positions[j][i], 2) for j in range(3)]):
                s,w = x
#            for s, w, ap in product([combinations(mutable_positions[j][i], 2) for j in range(3)]):
                yield s,w,ap

        for x, ap in reduce(product,[combinations(mutable_positions[j][j], 2) for j in range(3)]):
            s,w = x
#        for s, w, ap in product([combinations(mutable_positions[j][j], 2) for j in range(3)]):
            yield s,w,ap

        for x, ap in reduce(product,[combinations(mutable_positions[2-j][j], 2) for j in range(3)]):
            s,w = x
#        for s, w, ap in product([combinations(mutable_positions[2-j][j], 2) for j in range(3)]):
            yield s,w,ap



    def result(self, state, action):
        """Effectue une permutation au sein d'un carré."""
 #       x, y = action
 #       state, new_state = tuple(map(numpify_state, [state]*2))


        # permutate les deux positions (x, y)
#        new_state.itemset(x, state[y])
#        new_state.itemset(y, state[x])

#        return tuple(new_state.flatten())

        #Si le super-branchement est utilisé, il faut utiliser ca comme fonction poru result() :

        state, new_state = tuple(map(numpify_state, [state]*2))

        for x,y in action:
            new_state.itemset(x, state[y])
            new_state.itemset(y, state[x])

        return tuple(new_state.flatten())



    def goal_test(self, state):
        """
        Détermine si une configuration donnée est valide en supposant les carrés
        valides.

        Seul les lignes et les colonnes sont vérifiées.
        """
        state = numpify_state(state)
        for line in state:
            if np.bincount(line).max() > 1:
                return False
        for column in state.T:
            if np.bincount(column).max() > 1:
                return False
        return True

    def path_cost(self, c, state1, action, state2):
        return c + 1

    def value(self, state):
        """
        La valeur d'un état est déterminé par le nombre de cases
        non-conflictuelles, considérant qu'il n'y a pas de conflits sur les
        carrés.
        """
        state = numpify_state(state)
        conflicts = 0
        for i in xrange(9):
            for j in xrange(9):
                if (i, j) not in self.initial_positions:
                    value = state[i][j]
                    line = state[i]
                    column = state[:,j]
                    conflicts += line[line == value].size + column[column == value].size - 2
        # on cherche à minimiser les conflits (au plus 81 * 4 = 324)
        return 324 - conflicts

class NormalizedSudoku(Problem):
    """
    Définition du probleme de Sudoku comme un problème de recherche dans un
    espace d'états avec normalisation.

    L'état est une grille où chaque case contient un ensemble de possibilités
    pour cette case. Une case dont l'ensemble est de cardinalité 1 vaut son
    unique élément.
    """

    def __init__(self, initial):
        """ Remplit la grille avec des valeurs qui respectent les carrés."""

        state = np.array([frozenset(range(1, 10) if k == 0 else [k])
                          for k in initial]).reshape((9,9))

        state = normalize_state(state)

        self.initial = tuple(state.flatten())

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

        i, j, k = action

        state.itemset((i, j), frozenset([k]))

        # normalize
        normalized_state = normalize_state(state)

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
        return sum(map(len, state))

