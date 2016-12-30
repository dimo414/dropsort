"""Helper functions for testing Dropsort implementations."""

import random

def partial_shuffle_orig(ls, randomness):
  """Approximate reimplementation of the algorithm in
  https://bitbucket.org/dimo414/dropsort/src/pristine/Research/DropsortTest/Dropsort.cs?t#Dropsort.cs-25

  Note that it can introduce duplicates.
  """
  copy = ls[:]
  for i in range(len(copy)):
    if random.random() < randomness:
      copy[i] = random.choice(ls)
  return copy

def partial_shuffle(ls, randomness):
  """Partially shuffles a list by applying the Fisher-Yates shuffle with a
  given probability."""
  copy = ls[:] if random.getrandbits(1) else ls[::-1]
  for i in range(len(copy)):
    if random.random() < randomness:
      j = random.choice(range(i, len(copy)))
      if i != j:
        tmp = copy[i]
        copy[i] = copy[j]
        copy[j] = tmp
  return copy

def partial_shuffle_and_reverse(ls, randomness):
  """Invokes partial_shuffle() and, 50% of the time reverses the list, to
  avoid directional bias."""
  ls = partial_shuffle(ls, randomness)
  if random.getrandbits(1):
    reversed(ls)
  return ls

def is_sorted(ls):
  """Returns true if the list is sorted"""
  return ls == sorted(ls)

def verify(f, size=100):
  """Verifies that f returns a sorted list when passed a possibly-unsorted one.
  """
  def check_sorted(ls):
    if not is_sorted(f(ls)):
      raise AssertionError("%s didn't dropsort %s - returned %s" % (
          f.__name__, ls, f(ls)))
  ls = sorted(random.sample(range(size * 10), size))
  check_sorted(ls) # ordered
  check_sorted(ls[::-1]) # reversed
  for _ in range(100):
    random.shuffle(ls)
    check_sorted(ls)
    

