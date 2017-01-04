import util

ls = list(range(100))

def check_shuffle(f):
  for r in (x * 0.1 for x in range(0, 11)):
    result = f(ls, r)
    assert ls == sorted(result)

# Not a valid shuffle
#def test_partial_shuffle_orig():
#  check_shuffle(util.partial_shuffle_orig)

def test_partial_shuffle_sample():
  check_shuffle(util.partial_shuffle_sample)

def test_partial_shuffle():
  check_shuffle(util.partial_shuffle)

def test_is_sorted():
  assert util.is_sorted(list(range(10)))
  assert not util.is_sorted(list(range(10))[::-1])
  assert not util.is_sorted([5,3,9,2,6,1])

def test_is_sublist():
  assert util.is_sublist(list(range(10)), list(range(5)))
  assert not util.is_sublist(list(range(5)), list(range(10)))

