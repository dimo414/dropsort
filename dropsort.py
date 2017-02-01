"""Dropsort implementations.

Linear-time "sorting" algorithms that work by eliminating elements which appear
out of order."""

import util

from collections import deque
from heapq import merge

def _keyify(ls, key):
  return [(key(v), v) for v in ls]

def _unkeyify(key_ls):
  return [e[1] for e in key_ls]

def _curry(f, n):
  def curried(ls, key=lambda k: k):
    return f(ls, n, key)
  curried.__name__ = f.__name__
  return curried

def dropsort(ls, key=lambda k: k):
  """The original algorithm, per
  http://www.dangermouse.net/esoteric/dropsort.html"""
  if len(ls) <= 1:
    return ls[:]
  key_ls = _keyify(ls, key)
  result = key_ls[:1]
  for i in range(1, len(key_ls)):
    if result[-1] <= key_ls[i]:
      result.append(key_ls[i])
  return _unkeyify(result)

def drop_merge_sort(ls, key=lambda k: k):
  """Standard (lossless) sorting algorithm that uses dropsort internally.
  Described on DangerMouse's site."""
  if len(ls) <= 1:
    return ls[:]
  if len(ls) == 2:
    return ls if key(ls[0]) < key(ls[1]) else ls[::-1]

  return _unkeyify(_raw_drop_merge_sort(_keyify(ls, key)))

def _raw_drop_merge_sort(key_ls):
  ordered = key_ls[:1]
  unordered = []
  for i in range(1, len(key_ls)):
    if ordered[-1] <= key_ls[i]:
      ordered.append(key_ls[i])
    else:
      unordered.append(key_ls[i])
  return list(merge(ordered, drop_merge_sort(unordered[::-1])))

def dropsort_between(ls, key=lambda k: k):
  """Double Comparison improvement. Based on
  https://bitbucket.org/dimo414/dropsort/src/pristine/Research/DropsortTest/Dropsort.cs#Dropsort.cs-98

  Essentially this only adds an element if it's between its siblings
  (l <= e <= r), rather than dropsort which only considers the previous
  element (l <= e). This avoids selecting an element which is out of place
  (assuming its siblings are roughly in-place).
  """
  if len(ls) <= 1:
    return ls[:]

  key_ls = _keyify(ls, key)
  result = key_ls[:1]
  for i in range(1, len(key_ls)):
    if result[-1] <= key_ls[i] and (i+1 == len(key_ls) or key_ls[i] <= key_ls[i+1]):
      result.append(key_ls[i])
  return _unkeyify(result)

def dropsort_consecutive(ls, n=3, key=lambda k: k):
  """Recent Memory improvement. Based on
  https://bitbucket.org/dimo414/dropsort/src/pristine/Research/DropsortTest/Dropsort.cs#Dropsort.cs-120

  Avoids dropping more than n elements in a row by counting how many
  consecutive elements have been dropped, and revoking the last-added element
  (and adding the n-th element in its place instead) if it reaches the
  threshold.
  """
  if len(ls) <= 1:
    return ls[:]

  key_ls = _keyify(ls, key)
  result = key_ls[:1]
  consecutive_drops = 0
  for i in range(1, len(key_ls)):
    if key(result[-1]) <= key(key_ls[i]):
      result.append(key_ls[i])
      consecutive_drops = 0 # paper's implementation didn't have this line
    else:
      consecutive_drops += 1
      # paper's implementation also requires len(result) > 1
      # need to also confirm the prior element is also less than the value to
      # be added - otherwise the result will not be sorted
      if consecutive_drops >= n and (len(result) < 2 or result[-2] <= key_ls[i]):
        result[-1] = key_ls[i] # overwrite
        consecutive_drops = 0
  return _unkeyify(result)

def dropsort_between_consecutive(ls, n=3, key=lambda k: k):
  """Double Comparison + Recent Memory improvement. Based on
  https://bitbucket.org/dimo414/dropsort/src/pristine/Research/DropsortTest/Dropsort.cs#Dropsort.cs-153

  Applies both prior optimizations.
  """
  if len(ls) <= 1:
    return ls[:]

  key_ls = _keyify(ls, key)
  result = key_ls[:1]
  consecutive_drops = 0
  for i in range(1, len(key_ls)):
    if result[-1] <= key_ls[i] and (i+1 == len(key_ls) or key_ls[i] <= key_ls[i+1]):
      result.append(key_ls[i])
      consecutive_drops = 0
    else:
      consecutive_drops += 1
      if consecutive_drops >= n and (len(result) < 2 or result[-2] <= key_ls[i]):
        result[-1] = key_ls[i]
        consecutive_drops = 0
  return _unkeyify(result)

def dropsort_minmax(ls, key=lambda k: k):
  """Precomputes the min/max values and uses that as a heuristic to determine
  which element to remove.

  Note this computes the distance between elements, so the key function must
  return an arithmetic type (+-*/, can be cast to an int).
  """
  if len(ls) <= 1:
    return ls[:]

  key_ls = _keyify(ls, key)
  low = min(key_ls)
  high = max(key_ls)
  result = key_ls[:1]
  for i in range(1, len(key_ls)):
    if result[-1] <= key_ls[i]:
      result.append(key_ls[i])
    else:
      expected = int(low[0] + i/len(key_ls) * (high[0]-low[0]))
      left = result[-1]
      right = key_ls[i]
      # if left is "more" out-of-place than right
      if abs(left[0] - expected) > abs(right[0] - expected):
        if len(result) < 2 or result[-2] <= key_ls[i]:
          result[-1] = key_ls[i]
  return _unkeyify(result)


def dropsort_window(ls, window_size=10, key=lambda k: k):
  """Uses a fixed-size moving buffer to improve retention.

  For each element in the input it is added to the end of the buffer. Then the
  head of the buffer is considered for addition to the result list. If it's a
  valid addition (greater-than or equal-to the previously accepted result) the
  window is traversed once to determine whether adding the element would
  cause more elements in the window to be excluded.

  This means the runtime of this function is technically O(n*k), however the
  window size can be treated as a constant, making it effectively linear.
  """
  if len(ls) <= 1:
    return ls[:]

  key_ls = _keyify(ls, key)
  result = []
  window = deque()

  def should_accept(value):
    accept, reject = 1, 0
    accept_max, reject_max = value, result[-1] if result else None
    for e in window:
      if e >= accept_max:
        accept += 1
        accept_max = e
      if not reject_max or e >= reject_max:
        reject += 1
        reject_max = e
    return accept >= reject

  def decide():
    value = window.popleft()
    if ((not result or result[-1] <= value) and
        should_accept(value)):
      result.append(value)

  for e in key_ls:
    window.append(e)
    # always ensure the buffer is full
    if len(window) < window_size:
      continue

    decide()

  # drain the window
  while window:
    decide()
  return _unkeyify(result)

DROPSORTS = (
  dropsort,
  dropsort_between,
  _curry(dropsort_consecutive, 10), # TODO pick ideal n
  _curry(dropsort_between_consecutive, 10), # TODO pick ideal n
  dropsort_minmax,
  _curry(dropsort_window, 10), # TODO pick ideal n
)

PARAMETERIZED_DROPSORTS = (
  dropsort_consecutive,
  dropsort_between_consecutive,
  dropsort_window
)

# basic verify
if __name__ == '__main__':
  for f in (dropsort, drop_merge_sort, dropsort_between, dropsort_consecutive,
      dropsort_between_consecutive, dropsort_minmax, dropsort_window):
    util.verify(f)
