
import sys

from aima.search import hill_climbing
from sudoku import FilledSudoku

from utils import load_examples

for example in load_examples(sys.argv[1]):
    s = FilledSudoku(example)
    solution, explored = hill_climbing(s)
    print ''.join(map(str, solution)), explored
