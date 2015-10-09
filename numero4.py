#!/usr/bin/env python

import sys

from sudoku import Sudoku, FilledSudoku
from heuristics import most_constrained_cell,  non_inferable_cells, conflicts

from aima.search import greedy_best_first_graph_search

with open(sys.argv[1], 'r') as f:
    for line in f:
        example = tuple(map(int, line[:-1]))

        s = Sudoku(example)
        f = FilledSudoku(example)

        print greedy_best_first_graph_search(s, most_constrained_cell, bound=100)
        print greedy_best_first_graph_search(s, non_inferable_cells, bound=100)
        print greedy_best_first_graph_search(f, conflicts, bound=100)
