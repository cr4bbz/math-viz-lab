import unittest
from pathlib import Path
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

EXPERIMENT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EXPERIMENT_DIR))

from render import (
    BASEL_LIMIT,
    InteractiveOverview,
    basel_term,
    create_static_figure,
    partial_sum,
    tail_error,
)


class BaselVisualizationTests(unittest.TestCase):
    def test_terms_and_first_partial_sums(self) -> None:
        self.assertEqual(basel_term(1), 1.0)
        self.assertEqual(basel_term(2), 0.25)
        self.assertEqual(partial_sum(1), 1.0)
        self.assertEqual(partial_sum(2), 1.25)
        with self.assertRaises(ValueError):
            basel_term(0)

    def test_numerical_tail_lies_in_integral_corridor(self) -> None:
        for n in (1, 2, 5, 20, 100):
            remainder = tail_error(n)
            self.assertLessEqual(1.0 / (n + 1), remainder)
            self.assertLessEqual(remainder, 1.0 / n)

    def test_partial_sums_approach_basel_limit_from_below(self) -> None:
        self.assertLess(partial_sum(20), BASEL_LIMIT)
        self.assertLess(tail_error(200), tail_error(20))

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
        overview.cutoff_slider.set_val(100)
        overview.selected_slider.set_val(12)
        overview.visible_slider.set_val(8)
        self.assertIn("M=100", overview.status.get_text())
        self.assertIn("N=12", overview.status.get_text())
        self.assertIn("K=8", overview.status.get_text())
        plt.close(overview.fig)


if __name__ == "__main__":
    unittest.main()
