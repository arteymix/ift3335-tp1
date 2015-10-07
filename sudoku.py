# -*- coding: utf-8 -*-

from aima.search import Problem, depth_first_graph_search, hill_climbing, greedy_best_first_graph_search, astar_search, simulated_annealing
import numpy as np
from itertools import combinations, product
from random import choice

def numpify_state(state):
    """Génère une représentation facilement manipulable d'un état Sudoku."""
    return np.array(state, dtype=np.uint8).reshape((9,9))

def validate_state(self, state):
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

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""

        i,j,k = action
        state1 = np.array(state1, dtype=np.uint8).reshape((9,9))
        state2 = np.array(state2, dtype=np.uint8).reshape((9,9))

        s = set(state1[i]).union(set(state1[:,j])).union(set(state1[3*(i//3):3*(i//3)+3,3*(j//3):3*(j//3)+3].flatten()))
        return c + 9 - len(s - {0})

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

def remaining_possibilities(node):
    state = numpify_state(node.state)
    possibilities = 0
    for i, j in zip(*np.where(state == 0)):
        line = state[i]
        column = state[:,j]
        square = state[i//3*3:i//3*3+3,j//3*3:j//3*3+3]
        possibilities += len(reduce(np.setdiff1d, [np.arange(1, 10), line, column, square.flatten()]))
    print state, possibilities
    return possibilities

import math

def remaining_lines(node):
    state = numpify_state(node.state)
    empty = 0
    for line in state:
        empty += 2**line[line == 0].size
    print state, empty
    return empty

def remaining_blanks(node):
    state = numpify_state(node.state)
    print state, state[state == 0].size
    return state[state == 0].size
    blanks = 3 * 729
    for i, j in zip(*np.where(state == 0)):
        line = state[i]
        column = state[:,j]
        square = state[i//3*3:i//3*3+3,j//3*3:j//3*3+3]
        blanks -= line[line == 0].size * column[column == 0].size * square[square == 0].flatten().size
    print state, blanks
    return blanks

def conflicts(node):
    state = numpify_state(node.state)
    conflicts = 0
    for i in xrange(9):
        for j in xrange(9):
            value = state[i][j]
            line = state[i]
            #column = state[:,j]
            conflicts += line[line == value].size# + column[column == value].size - 2
    return conflicts

def load_examples(path):
    """Yield examples from the lines of a file."""
    with open(path, 'r') as file:
        for line in file:
            yield tuple(map(int, line[:-1]))

examples = load_examples('examples/100sudoku.txt')

import time
from contextlib import contextmanager

@contextmanager
def bench(name):
    print "running", name
    a = time.clock()
    yield
    print name, "took", str(time.clock() - a) + "s"



# depth first borné à 10000 explorations
# TODO: améliorer la vitesse d'exécution
for example in examples:
#    with bench("simulated annealing"):
#        p = FilledSudoku(example)
#        i = 0
#        while True :
#            i += 1
#            n = simulated_annealing(p)
#            print n, p.goal_test(n.state), p.value(n.state)
#            if p.goal_test(n.state):
#                print "Valid solution found in "+str(i)+" iteration"
                
    with bench("depth first"):
        #solution, explored = depth_first_graph_search(Sudoku(example), bound=10000)
        #print solution, explored
        pass

    with bench("hill climbing"):
        s = FilledSudoku(example)
        solution, explored = hill_climbing(s, bound=100)
        print numpify_state(s.initial), numpify_state(solution), s.value(s.initial), s.value(solution), "explored", explored

    continue

    with bench("greedy best first"):
        # TODO: optimiser la validation d'état
        s = FilledSudoku(example)
        def h(node):
            return s.value(node.state)
        solution, explored = greedy_best_first_graph_search(s, h, bound=10000)
        print solution, explored

    with bench('astar'):
        s = Sudoku(example)
        def h(node):
            return s.value(node.state)
        solution, explored = astar_search(s, bound=10, h=h)
        print solution, explored

#sol = uniform_cost_search(ex[0])
#sol = best_first_graph_search(ex[0], ex[0].value)
#sol = depth_first_tree_search(ex[0])                
                
