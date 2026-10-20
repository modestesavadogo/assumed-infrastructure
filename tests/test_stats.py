"""Unit tests for the statistics helpers in src/analyze.py (run: python tests/test_stats.py)."""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
from analyze import boot_ci, holm  # noqa: E402

x = np.array([0.1, 0.4, -0.2, 0.3, 0.0, 0.5, 0.25, -0.1])

# the bootstrap interval is a pure function of its data: repeated and interleaved calls give identical results
a = boot_ci(x)
boot_ci(x[:5])
assert np.array_equal(a, boot_ci(x)), "bootstrap CI depends on call order"
assert a[0] < x.mean() < a[1], "mean outside its own 95% CI"
assert np.array_equal(boot_ci(np.append(x, np.nan)), a), "NaNs must be dropped before resampling"
assert not np.array_equal(boot_ci(x, seed=1), a), "seed must change the draws"

# Holm: textbook example (m = 4)
p = [0.01, 0.04, 0.03, 0.005]
assert np.allclose(holm(p), [0.03, 0.06, 0.06, 0.02]), holm(p)
assert (holm([0.5]) == 0.5).all()
assert (holm([0.4, 0.9]) <= 1).all()

print("all statistics tests passed")
