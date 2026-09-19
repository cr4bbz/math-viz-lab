import unittest
from pathlib import Path
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

EXPERIMENT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EXPERIMENT_DIR))

from render import (
    InteractiveOverview,
    create_static_figure,
    full_positive_fiber,
    is_prime,
    visible_cardinality,
    visible_coordinates,
)


class PrimeHeightVisualizationTests(unittest.TestCase):
    def test_prime_classifier_on_displayed_domain(self) -> None:
        primes = [n for n in range(2, 33) if is_prime(n)]
        self.assertEqual(primes, [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31])

    def test_complete_and_truncated_fibers(self) -> None:
        self.assertEqual(len(full_positive_fiber(11)), 10)
        self.assertEqual(visible_cardinality(16, 11), 10)
        self.assertEqual(visible_cardinality(16, 19), 14)
        self.assertEqual(visible_coordinates(16, 19)[0], (3, 16))
        self.assertEqual(visible_coordinates(16, 19)[-1], (16, 3))

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
        overview.window_slider.set_val(12)
        overview.height_slider.set_val(17)
        overview.pair_slider.set_val(5)
        self.assertIn("N=12", overview.status.get_text())
        self.assertIn("n=17", overview.status.get_text())
        self.assertIn("(13,17)", overview.status.get_text())
        plt.close(overview.fig)


if __name__ == "__main__":
    unittest.main()
