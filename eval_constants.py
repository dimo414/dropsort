#!/usr/bin/env python3
"""Prints a table showing the retained ratio of a given function over several
values of n."""

import random, sys

import benchmark, dropsort, util

if __name__ == '__main__':
  # TODO use argparse to make more user-friendly
  f = dropsort.PARAMETERIZED_DROPSORTS[int(sys.argv[1]) if len(sys.argv) > 1 else 0]
  s = util.SHUFFLES[int(sys.argv[2]) if len(sys.argv) > 2 else 0]
  print('Results for %s using %s:' % (f.__name__, s.__name__))
  max_n=10
  ratios = benchmark.compute_parameterized_retained_ratio(
    f, max_size=50, max_n=max_n, iters=100, shuffle=s)

  ns = sorted(ratios.keys())
  sizes = sorted(next(iter(ratios.values())).keys())
  print('\t' + '\t'.join(map(str, range(1, max_n+1))))

  for size in sizes:
    print('%s\t%s' % (size, '  '.join('%5.2f%%' % ratios[n][size] for n in ns)))
