__author__ = 'ntak'

from sudoku import *

class Sudoku3(Problem):
   """
    Définition du probleme de Sudoku comme un problème de recherche dans un espace d'états.

    L'état est un tableau 9x9 ou chaque case contient une valeur de 1 à 9 ou un ensemble des possibilités restante pour cette case.
    """

    def __init__(self, initial):
        """Remplit la grille avec des valeurs qui respectent les carrés."""
        initial = numpify_state(initial)

        state = np.array([[set([i+1 for i in range(9)]) for x in range(9)] for y in range(9)])

        # initialise la grille en respect des carrés
        for i, j in zip(*np.where(initial != 0)):
            state = _result(state, (i,j,initial[i][j]))

        self.initial = self.normalise_state(state)

    def normalise_state(self, state):
        """ State must be a 9x9 numpy array filled with set object"""
        modif = True

        while modif :
            modif = False
            x = np.array(state)

            map(lambda y : 1 if len(y) == 1, x)

            for i in range(9):
                line = x[i]
                if sum(line) == 8 :
                    y = np.where(line != 1)
                    k = set(range(1,10)) - set([state[i][j] if j != y for j in range(9)])
                    assert len(k) == 1
                    state = _result(state, (i,j,k))
                    modif = True


            for j in range(9):
                column = x[:,j]
                if sum(column) == 8 :
                    y = np.where(column != 1)
                    k = set(range(1,10)) - set([state[i][j] if i != y for i in range(9)])
                    assert len(k) == 1
                    state = _result(state, (i,j,k))
                    modif = True

            for i,j in product(range(3),range(3)):
                square = x[i//3*3:i//3*3+3,j//3*3:j//3*3+3].flatten()
                if sum(square) == 8 :
                    y = np.where(square != 1)
                    k = set(range(1,10)) - set([state[i][j] if i != y for i in range(9)])
                    assert len(k) == 1
                    state = _result(state, (i,j,k))
                    modif = True


        return tuple(map(lambda x : frozenset(x), state))



    def actions(self, state):
        """
        les actions sont déterminées en retournant les possibilitiés qui
        manquent simultanément dans une ligne, colonne et grille correspondantes
        à une case.

        La position de la case et la nouvelle valeur possible est retournée sous
        forme d'un triplet (i, j, k).
        """

        for i in range(9):
            for j in range(9):
                if len(state[i][j]) > 1 :
                    for x in state[i][j]:
                        yield i,j,x

    def _result(self, state,action):
        """ Takes a numpy reprensentation of state with mutable set. make in-place modification"""
        i, j, k = action

        line = state[i]
        column = state[:,j]
        square = state[i//3*3:i//3*3+3,j//3*3:j//3*3+3]

        map(lambda x: x.remove(k) if k in x, [line, column, square])
        state[i][j] = {k}

        return state


    def result(self, state, action):
        """
        Calcule la configuration résultante à appliquer une action sur une
        configuration.

        Le nouvel état est une copie modifiée de l'état passé en argument.
        """
        new_state = numpify_state(state)
        map(lambda x:set(x), new_state)

        return tuple([frozenset(i) for i in self.normalise_state(_result(self,new_state,action))])

    def goal_test(self, state):
        """Vérifie si une grille est complète en supposant que l'état est valide"""
        return []

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



examples = load_examples('examples/100sudoku.txt')