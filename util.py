"""Helper functions for testing Dropsort implementations."""

import math, random

def full_shuffle(ls, randomness=True):
  """Real shuffle, for comparison with partial shuffles below."""
  if not randomness: return ls[:] # for compatiblitly with other shuffles
  return random.sample(ls, k=len(ls))

def partial_shuffle_orig(ls, randomness):
  """Approximate reimplementation of the algorithm in
  https://bitbucket.org/dimo414/dropsort/src/pristine/Research/DropsortTest/Dropsort.cs?t#Dropsort.cs-25

  Note that it does not necessarily preserve the contents of the original array
  (as it selects with replacement, introducing duplicate and dropped values).
  """
  copy = ls[:]
  for i in range(len(copy)):
    if random.random() < randomness:
      copy[i] = random.choice(ls)
  return copy

def partial_shuffle_sample(ls, randomness):
  """Partially shuffles a list by selecting a subset of indicies to shuffle,
  leaving other indicies alone. Note this means a low randomness value will
  effectively round-down to zero (a subset of size zero or one cannot be
  shuffled).
  """
  num_shuffle = int(math.ceil(randomness * len(ls)))
  #print(num_shuffle)
  indicies = random.sample(range(len(ls)), num_shuffle)
  #print(indicies)
  indicies_shuffled = indicies[:]
  random.shuffle(indicies_shuffled)
  #print(indicies_shuffled)
  copy = ls[:]
  for i in range(len(indicies)):
    copy[indicies_shuffled[i]] = ls[indicies[i]]
  return copy

def partial_shuffle(ls, randomness, reverse=True):
  """Partially shuffles a list by applying the Fisher-Yates shuffle with a
  given probability. By default also reverses the result 50% of the time to
  avoid directional bias."""
  copy = ls[:] if reverse and random.getrandbits(1) else ls[::-1]
  for i in range(len(copy)):
    if random.random() < randomness:
      j = random.choice(range(i, len(copy)))
      if i != j:
        tmp = copy[i]
        copy[i] = copy[j]
        copy[j] = tmp
  return copy

SHUFFLES = (
  full_shuffle,
  partial_shuffle_orig,
  partial_shuffle_sample,
  partial_shuffle,
)

def is_sorted(ls):
  """Returns true if the list is sorted"""
  return ls == sorted(ls)

def is_sublist(ls, subls):
  """Returns true if every element of subls exists, in order, in ls."""
  if len(ls) < len(subls):
    return False
  subls_i = 0
  for i, e in enumerate(ls):
    if subls_i >= len(subls):
      return True
    if e == subls[subls_i]:
      subls_i += 1
  return subls_i == len(subls)
