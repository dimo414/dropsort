"""Dropsort implementations.

Linear-time "sorting" algorithms that work by eliminating elements which appear
out of order."""

import util

from heapq import merge

def dropsort(ls):
  """The original algorithm, per
  http://www.dangermouse.net/esoteric/dropsort.html"""
  if len(ls) <= 1:
    return ls[:]
  result = ls[:1]
  for i in range(1, len(ls)):
    if result[-1] <= ls[i]:
      result.append(ls[i])
  return result

def drop_merge_sort(ls):
  """Standard (lossless) sorting algorithm that uses dropsort internally.
  Described on DangerMouse's site."""
  if len(ls) <= 1:
    return ls[:]
  if len(ls) == 2:
    return merge(ls[:1], ls[1:])

  ordered = ls[:1]
  unordered = []
  for i in range(1, len(ls)):
    if ordered[-1] <= ls[i]:
      ordered.append(ls[i])
    else:
      unordered.append(ls[i])
  return list(merge(ordered, drop_merge_sort(unordered[::-1])))

def dropsort_between(ls):
  """Double Comparison improvement. Based on
  https://bitbucket.org/dimo414/dropsort/src/pristine/Research/DropsortTest/Dropsort.cs#Dropsort.cs-98

  Essentially this only adds an element if it's between its siblings
  (l <= e <= r), rather than dropsort which only considers the previous
  element (l <= e). This avoids selecting an element which is out of place
  (assuming its siblings are roughly in-place).
  """
  if len(ls) <= 1:
    return ls[:]
  result = ls[:1]
  for i in range(1, len(ls)):
    if result[-1] <= ls[i] and (i+1 == len(ls) or ls[i] <= ls[i+1]):
      result.append(ls[i])
  return result

def dropsort_consecutive(ls, n=3):
  """Recent Memory improvement. Based on
  https://bitbucket.org/dimo414/dropsort/src/pristine/Research/DropsortTest/Dropsort.cs#Dropsort.cs-120
  
  Avoids dropping more than n elements in a row by counting how many
  consecutive elements have been dropped, and revoking the last-added element
  (and adding the n-th element in its place instead) if it reaches the
  threshold.
  """
  if len(ls) <= 1:
    return ls[:]
  result = ls[:1]
  consecutive_drops = 0
  for i in range(1, len(ls)):
    if result[-1] <= ls[i]:
      result.append(ls[i])
      consecutive_drops = 0 # paper's implementation didn't have this line
    else:
      consecutive_drops += 1
      # paper's implementation also requires len(result) > 1
      # need to also confirm the prior element is also less than the value to
      # be added - otherwise the result will not be sorted
      if consecutive_drops >= n and (len(result) < 2 or result[-2] <= ls[i]):
        result[-1] = ls[i] # overwrite
        consecutive_drops = 0
  return result

def dropsort_between_consecutive(ls, n=3):
  """Double Comparison + Recent Memory improvement. Based on
  https://bitbucket.org/dimo414/dropsort/src/pristine/Research/DropsortTest/Dropsort.cs#Dropsort.cs-153

  Applies both prior optimizations.
  """
  if len(ls) <= 1:
    return ls[:]
  result = ls[:1]
  consecutive_drops = 0
  for i in range(1, len(ls)):
    if result[-1] <= ls[i] and (i+1 == len(ls) or ls[i] <= ls[i+1]):
      result.append(ls[i])
      consecutive_drops = 0
    else:
      consecutive_drops += 1
      if consecutive_drops >= n and (len(result) < 2 or result[-2] <= ls[i]):
        result[-1] = ls[i]
        consecutive_drops = 0
  return result

def dropsort_minmax(ls, key=lambda k: k):
  """Precomputes the min/max values and uses that as a heuristic to determine
  which element to remove.
  """
  low = key(min(ls))
  high = key(max(ls))
  result = ls[:1]
  for i in range(1, len(ls)):
    if result[-1] <= ls[i]:
      result.append(ls[i])
    else:
      expected = low + i/len(ls) * (high-low)
      left = key(result[-1])
      right = key(ls[i])
      # if left is "more" out-of-place than right
      if abs(left - expected) > abs(right - expected):
        if len(result) < 2 or result[-2] <= ls[i]:
          result[-1] = ls[i]
  return result


# basic verify
if __name__ == '__main__':
  for f in (dropsort, drop_merge_sort, dropsort_between, dropsort_consecutive,
      dropsort_between_consecutive, dropsort_minmax):  
    util.verify(f)
