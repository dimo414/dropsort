import random
import pytest
import dropsort, util

def assert_sorted(ls):
  __tracebackhide__ = True
  if not util.is_sorted(ls):
    pytest.fail("%s is not sorted" % ls)

def assert_sublist(ls, subls):
  __tracebackhide__ = True
  if not util.is_sublist(ls, subls):
    pytest.fail("%s is not a sublist of %s" % (subls, ls))

@pytest.mark.parametrize("f", [
    (dropsort.dropsort),
    (dropsort.dropsort_between),
    (dropsort.dropsort_consecutive),
    (dropsort.dropsort_between_consecutive),
    (dropsort.dropsort_minmax),
    (dropsort.dropsort_window),
])
def test_dropsort(f, size=100):
  """Verifies that f returns a sorted list when passed a possibly-unsorted one.
  """
  def check_sorted(ls):
    result = f(ls)
    assert_sorted(result)
    assert_sublist(ls, result)

  ls = sorted(random.sample(range(size * 10), size))
  check_sorted(ls) # ordered
  check_sorted(ls[::-1]) # reversed
  for _ in range(100):
    random.shuffle(ls) # randomized
    check_sorted(ls)

def test_drop_merge_sort(size=100):
  ls = list(range(size * 10))
  for _ in range(10):
    sample = random.sample(ls, size)
    result = dropsort.drop_merge_sort(sample)
    assert_sorted(result)
    assert sorted(sample) == result
