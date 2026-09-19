import unittest
from pathlib import Path
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

EXPERIMENT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EXPERIMENT_DIR))

from render import (
    InteractiveOverview,
    basel_weight,
    create_static_figure,
    fiber_cardinality,
    full_fiber_mass,
    is_prime,
    positive_height_fiber,
    series_data,
)


class WeightedPrimeHeightFiberTests(unittest.TestCase):
    def test_height_fiber_and_mass_at_eleven(self) -> None:
        fiber = positive_height_fiber(11)
        self.assertEqual(len(fiber), 10)
        self.assertEqual(fiber[0], (1, 10))
        self.assertEqual(fiber[-1], (10, 1))
        self.assertEqual(fiber_cardinality(11), 10)
        self.assertAlmostEqual(basel_weight(11), 1 / 121)
        self.assertAlmostEqual(full_fiber_mass(11), 10 / 121)

    def test_prime_classifier(self) -> None:
        self.assertEqual(
            [n for n in range(2, 30) if is_prime(n)],
            [2, 3, 5, 7, 11, 13, 17, 19, 23, 29],
        )

    def test_finite_sum_identity(self) -> None:
        data = series_data(500)
        np.testing.assert_allclose(
            data.fiber_sums,
            data.harmonic_sums - data.basel_sums,
            rtol=0,
            atol=2e-14,
        )
        self.assertAlmostEqual(data.fiber_sums[-1], 5.149887364475631)
        self.assertAlmostEqual(data.prime_fiber_sums[-1], 1.6447353612407805)

    def test_every_step_has_equal_comparison_panels(self) -> None:
        for step in range(1, 5):
            fig, (left, right) = create_static_figure(step)
            fig.canvas.draw()
            left_box = left.get_position()
            right_box = right.get_position()
            self.assertAlmostEqual(left_box.width, right_box.width, places=12)
            self.assertAlmostEqual(left_box.height, right_box.height, places=12)
            plt.close(fig)

    def test_interactive_overview_contains_and_updates_all_steps(self) -> None:
        overview = InteractiveOverview()
        self.assertEqual(set(overview.panels), {1, 2, 3, 4})
        self.assertTrue(all(len(pair) == 2 for pair in overview.panels.values()))
        overview.cutoff_slider.set_val(1000)
        overview.selected_slider.set_val(17)
        self.assertIn("M=1000", overview.status.get_text())
        self.assertIn("n=17", overview.status.get_text())
        self.assertIn("|H_n|=16", overview.status.get_text())
        plt.close(overview.fig)


if __name__ == "__main__":
    unittest.main()
