import sys

from aima.search import depth_first_graph_search
from sudoku import Sudoku, RandomizedSudoku, SortedSudoku

from utils import load_examples

for example in load_examples(sys.argv[1]):
    s = Sudoku(example)
    r = RandomizedSudoku(example)
    sorted_sudoku = SortedSudoku(example)
    print depth_first_graph_search(s, bound=10000)
    print depth_first_graph_search(r, bound=10000)
    print depth_first_graph_search(sorted_sudoku, bound=10000)
