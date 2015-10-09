
import sys

from aima.search import hill_climbing
from sudoku import FilledSudoku

with open(sys.argv[1], 'r') as f:
    for line in f:
        example = tuple(map(int, line[:-1]))
        s = FilledSudoku(example)
        print hill_climbing(s)
