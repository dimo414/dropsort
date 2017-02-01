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
    lambda ls, n: ls[:n], max_n=12, max_size=12, iters=10)
  assert ratios == {
    10: {10: 1.0,
         11: 0.9090909090909092,
         12: 0.8333333333333334
        },
    11: {10: 1.0,
         11: 1.0,
         12: 0.9166666666666666
        },
    12: {10: 1.0,
         11: 1.0,
         12: 1.0
        }
  }

