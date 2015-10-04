# -*- coding: utf-8 -*-

from aima.search import *
import numpy as np
from itertools import combinations
from random import choice

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
     #       print("ij",i,j)
            square = state[i//3:3*i//3+3,j//3:j//3+3]
  #          print("s",square)
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
        return [[j for j in i] for i in new_state] #Le code de hill-climbing n<accepte pas les np.array

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
        return c + 9 - len(s - {0})

    def value(self, state):
        """
        The value of a state is determined by the sum of remaining possibilities
        for each cell in the grid.
        """
        state = np.array(state) # manipulate a copy
        possibilities = 0
        for i, j in zip(*np.where(state == 0)):
            for k in range(1, 10):
                state.itemset((i, j), k)
                if self._validate(state):
                    possibilities += 1
            state.itemset((i, j), 0)
        return possibilities

class Sudoku2(Problem):
    """
    Définition du probleme de Sudoku comme un problème de recherche dans
    l'espace d'états.
    """

    def __init__(self, initconfig):
        initconfig = np.array(initconfig)
        self.initial = [[j for j in i] for i in initconfig]
        self.not_initialised = {}

        if False : #Premiere methode d'initialisation. Pas tres bonne.
            for i in range(3):
                for j in range(3):
                    square = initconfig[3*i:i*3+3,j*3:j*3+3]
                    self.not_initialised[(i,j)] = set()
                    s = set(range(10)) - set(square.flatten())

                    for x,y in zip(*np.where(square == 0)):

                        # Cree un dictionnaire qui map l'indice des carres a un ensemble de position non-initialise
                        self.not_initialised[(i,j)].add((i*3+x,j*3+y))

                        #placer un element de s et retirer de s
                        w = choice(list(s))
                        s.remove(w)
                        initconfig.itemset((i*3+x,j*3+y),w)

                    assert len(s) == 0
            self.initial = [[j for j in i] for i in initconfig]

        else : #Heuristique d'initialisation
            for i in range(3):
                for j in range(3):
                    square = initconfig[3*i:i*3+3,j*3:j*3+3]
                    missing = set(range(10)) - set(square.flatten())
                    l = []
                    self.not_initialised[(i,j)] = set()
                    for x,y in zip(*np.where(square == 0)):

                        # Cree un dictionnaire qui map l'indice des carres a un ensemble de position non-initialise
                        self.not_initialised[(i,j)].add((i*3+x,j*3+y))

                        l.append(((3*i+x,3*j+y),self._getPossibilities(initconfig,3*i+x,3*j+y)))

                    while len(l) > 0 :
                        l.sort(lambda x, y : len(x[1]) < len(y[1]))
                        z = l.pop(0)
                        if len(z[1]) >0:
                            w = choice(list(z[1]))
                        else :
                            w = choice(list(missing))
                        missing.remove(w)
                        for x,y in l:
                            if w in y :
                                y.remove(w)
                        self.initial[z[0][0]][z[0][1]] = w
                     #   print("puttted ",w," in ", z[0])
                    assert len(missing) == 0

   #     self.initial = [[j for j in i] for i in initconfig]


    def _getPossibilities(self,state,i,j):
        """if state[i][j] == 0 return a set containing all possible numbers to be placed there.
        state must be a numpy array.
        """

        if state[i][j] == 0 :
            line = state[i]
            column = state[:,j]
            square = state[3*(i//3):3*(i//3)+3,3*(j//3):3*(j//3)+3]
            return set(range(10)) - set(square.flatten()) - set(line) - set(column)

        else :
            return set(state[i][j])

    def actions(self, state):
        """
        Enumere toute les permutation possb
        En excluant tous les indices
        returns i1, j1, i2,j2
        """
        for i in range(3):
            for j in range(3):
                for x,y in combinations(self.not_initialised[(i,j)],2):

                    yield x,y




    def _validate(self, state):
        """Détermine si une configuration donnée est valide."""
        state = np.array(state)
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
        """
        x, y = action
        new_state = np.array(state)
        temp = new_state[x]
        new_state.itemset(x, new_state[y])
        new_state.itemset(y, temp)
        return [[j for j in i] for i in new_state] #Le code de hill-climbing n<accepte pas les np.array

    def goal_test(self, state):
        """Vérifie si une grille est complète en supposant que l'état est valide"""
        return self._validate(state)

    def path_cost(self, c, state1, action, state2):
        return c + 1

    def value(self, state):
        """
        La valeur d'un état est déterminé par le nombre de cases
        non-conflictuelles, considérant qu'il n'y a pas de conflits sur les
        carrés.
        """
        state = np.array(state)
        conflicts = 0
        for i in range(9):
            for j in range(9):
                value = state[i][j]
                line = state[i]
                column = state[:,j]
                conflicts += line[line == value].size + column[column == value].size - 2
        # on cherche à minimiser les conflits (au plus 81 * 4 = 324)
        return 324 - conflicts

def load_examples(path):
    """Yield examples from the lines of a file."""
    with open(path, 'r') as file:
        for line in file:
            yield np.array(map(int, line[:-1]), dtype=np.uint8).reshape((9, 9))

ex = load_examples('examples/100sudoku.txt')

import time
#Décommenter la ligne pour faire un dept-first-search. Attention, ça prends longtemps.


#Hill-Climbing


for i in ex :
    a = time.clock()
    print(i)
    s = Sudoku2(i)
    print(np.array(s.initial))
    print('# de non-conflits', s.value(s.initial))
    sol = hill_climbing(s)
    #b = time.clock()
    print(np.array(sol))
    print('# de non-conflits', s.value(s.initial))
    b = time.clock()
    print(b-a)


#sol = uniform_cost_search(ex[0])
#sol = best_first_graph_search(ex[0], ex[0].value)
#sol = depth_first_tree_search(ex[0])

