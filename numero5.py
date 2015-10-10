# -*- coding: utf-8 -*-

"""
Benchmarks

Les résultats sont écrits en CSV dans la sortie standard.
"""

from contextlib import contextmanager
import csv
import time
import sys

from aima.search import Node, depth_first_graph_search, hill_climbing, greedy_best_first_graph_search

from sudoku import Sudoku, FilledSudoku, NormalizedSudoku, RandomizedSudoku, SortedSudoku
from heuristics import most_constrained_cell
from utils import load_examples, compact


examples = load_examples(sys.argv[1])
results = csv.DictWriter(sys.stdout, fieldnames=('initial', 'algorithm', 'heuristic', 'bound', 'final', 'score','explored', 'time'))

results.writeheader()

def bench(algorithm, problem, *argv, **kwargs):
    """Benchmark an algorithm and write the results in the standard output."""
    # benchmark algorithm runtime
    a = time.clock()
    solution, explored = algorithm(problem, *argv, **kwargs)
    delta = time.clock() - a

    if isinstance(solution, Node):
        solution = solution.state

    # write results
    results.writerow({
        'initial': compact(problem.initial),
        'algorithm': algorithm.__name__,
        'heuristic': kwargs['f'].__name__ if 'f' in kwargs else '',
        'bound': kwargs['bound'] if 'bound' in kwargs else '',
        'final': compact(solution) if solution else '',
        'score' : problem.value(solution) if solution else '',
        'explored': explored,
        'time': delta})

for example in examples:
    sudoku = Sudoku(example)
    randomized = RandomizedSudoku(example)
    srt = SortedSudoku(example)
    filled = FilledSudoku(example)
    normalized = NormalizedSudoku(example)

    # profondeur d'abord
    bench(depth_first_graph_search, sudoku, bound=10000)

    # Hill-Climbing
    bench(hill_climbing, filled)

    # recherche heuristique
    bench(greedy_best_first_graph_search, sudoku, f=most_constrained_cell, bound=100)

    # bonus
    bench(greedy_best_first_graph_search, normalized, f=lambda node: normalized.value(node.state), bound=10000)

