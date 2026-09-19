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
    create_static_figure,
    critical_strip_grid,
    dirichlet_partial_sums,
    known_zero_heights,
    zeta_value,
)


class RiemannHypothesisVisualizationTests(unittest.TestCase):
    def test_first_five_listed_zero_heights(self) -> None:
        zeros = known_zero_heights(5)
        expected = (
            14.134725141734695,
            21.022039638771556,
            25.01085758014569,
            30.424876125859512,
            32.93506158773919,
        )
        np.testing.assert_allclose(zeros, expected, rtol=0, atol=1e-12)

    def test_dirichlet_approximation_improves(self) -> None:
        sums = dirichlet_partial_sums(120, 14.13)
        target = zeta_value(2.0, 14.13)
        self.assertLess(abs(sums[-1] - target), abs(sums[1] - target))

    def test_critical_strip_grid_and_first_cross_section(self) -> None:
        sigmas, heights, values = critical_strip_grid()
        self.assertEqual(values.shape, (len(heights), len(sigmas)))
        zero_height = known_zero_heights(1)[0]
        scan = np.array([abs(zeta_value(float(sigma), zero_height)) for sigma in sigmas])
        minimum_sigma = float(sigmas[int(np.argmin(scan))])
        self.assertAlmostEqual(minimum_sigma, 0.5, places=2)

    def test_every_step_has_equal_comparison_panels(self) -> None:
        for step in range(1, 6):
            fig, (left, right) = create_static_figure(step)
            fig.canvas.draw()
            left_box = left.get_position()
            right_box = right.get_position()
            self.assertAlmostEqual(left_box.width, right_box.width, places=12)
            self.assertAlmostEqual(left_box.height, right_box.height, places=12)
            plt.close(fig)

    def test_interactive_overview_contains_and_updates_all_steps(self) -> None:
        overview = InteractiveOverview()
        self.assertEqual(set(overview.panels), {1, 2, 3, 4, 5})
        overview.cutoff_slider.set_val(200)
        overview.height_slider.set_val(21.02)
        overview.zero_slider.set_val(4)
        self.assertIn("N=200", overview.status.get_text())
        self.assertIn("t=21.02", overview.status.get_text())
        self.assertIn("K=4", overview.status.get_text())
        self.assertIn("offene Vermutung", overview.status.get_text())
        plt.close(overview.fig)


if __name__ == "__main__":
    unittest.main()
