import unittest
from pathlib import Path
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

EXPERIMENT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EXPERIMENT_DIR))

from render import create_static_figure, roots_for


class CubicFibersVisualizationTests(unittest.TestCase):
    def test_step_3_panels_have_identical_size(self) -> None:
        fig, (left, right) = create_static_figure(3, a=1.0)
        fig.canvas.draw()
        left_box = left.get_position()
        right_box = right.get_position()
        self.assertAlmostEqual(left_box.width, right_box.width, places=12)
        self.assertAlmostEqual(left_box.height, right_box.height, places=12)
        plt.close(fig)

    def test_real_root_cases(self) -> None:
        self.assertEqual(roots_for(-1.0), [0.0])
        self.assertEqual(roots_for(0.0), [0.0])
        self.assertEqual(roots_for(1.0), [-1.0, 0.0, 1.0])

    def test_every_step_renders(self) -> None:
        for step in range(1, 5):
            fig, panels = create_static_figure(step)
            fig.canvas.draw()
            self.assertEqual(len(panels), 2)
            plt.close(fig)


if __name__ == "__main__":
    unittest.main()
