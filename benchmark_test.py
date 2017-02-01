import benchmark

def test_compute_retained_ratio():
  ratios = benchmark.compute_retained_ratio(
    lambda ls: ls[:len(ls)//2], max_size=15, iters=10)
  assert ratios ==  {
    10: .50,
    11: .4545454545454546,
    12: .50,
    13: .4615384615384615,
    14: .50,
    15: .4666666666666667,
  }

def test_compute_parameterized_retained_ratio():
  ratios = benchmark.compute_parameterized_retained_ratio(
    lambda ls, n, _: ls[:n], max_n=3, max_size=12, iters=10)
  assert ratios == {
    1: {10: 0.1,
        11: 0.09090909090909091,
        12: 0.08333333333333334
       },
    2: {10: 0.2,
        11: 0.18181818181818182,
        12: 0.16666666666666669
       },
    3: {10: 0.3,
        11: 0.2727272727272727,
        12: 0.25
       }
  }
