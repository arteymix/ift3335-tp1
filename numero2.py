import sys

from aima.search import depth_first_graph_search
from sudoku import Sudoku, RandomizedSudoku

with open(sys.argv[1], 'r') as f:
    for line in f:
        example = tuple(map(int, line[:-1]))
        s = Sudoku(example)
        r = RandomizedSudoku(example)
        print depth_first_graph_search(s, bound=10000)
        print depth_first_graph_search(r, bound=10000)
