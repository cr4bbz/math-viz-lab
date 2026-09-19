"""Native visual research lab for the family F(a, x) = x³ - a·x.

Run without arguments to open the Matplotlib desktop lab.  Use ``--export``
to regenerate the reproducible SVG figures in ``figures/``.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

import matplotlib

if "--export" in sys.argv or "--check-layout" in sys.argv:
    matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.patches import FancyBboxPatch, Patch
from matplotlib.widgets import Button, Slider
import numpy as np

matplotlib.rcParams["svg.hashsalt"] = "math-viz-lab"

INK = "#10233f"
MUTED = "#5f6f82"
PAPER = "#f7f3ea"
SURFACE = "#fffdf8"
GRID = "#d8d5cd"
BLUE = "#2878a8"
BLUE_SOFT = "#d9edf6"
ORANGE = "#d26535"
ORANGE_SOFT = "#fae3d5"
GREEN = "#24755d"
PURPLE = "#6c52a2"
GOLD = "#e8b44d"

A_DOMAIN = (-2.0, 4.0)
X_DOMAIN = (-2.5, 2.5)

STEP_TITLES = {
    1: "1 · Termfeld: Wo kann F(a,x)=0 liegen?",
    2: "2 · Niveauschnitt: Die Nullstellenmenge wird zum Objekt",
    3: "3 · Projektion πₐ: Eine senkrechte Faser zählt Nullstellen",
    4: "4 · Projektion πₓ: Die umgekehrte Faser entdeckt eine Ausnahme",
}

STEP_NOTES = {
    1: "Farben zeigen das Vorzeichen. Die Grenze zwischen ihnen motiviert den Schnitt F=0.",
    2: "Das logische Oder entspricht einer Vereinigung: V = {x=0} ∪ {a=x²}.",
    3: "Links und rechts besitzen exakt dieselbe Zeichenfläche. Schnittpunkte links sind Nullstellen rechts.",
    4: "Bei x=0 ist die Faser die ganze a-Achse; für x≠0 bleibt genau der Punkt a=x².",
}

STEP_LOGIC = {
    1: "Logik: F : ℝ² → ℝ,  (a,x) ↦ x³−a·x",
    2: "Logik: F(a,x)=0  ↔  x=0 ∨ x²=a",
    3: "Logik: Vₐ = πₐ⁻¹(a) = {x∈ℝ ∣ F(a,x)=0}",
    4: "Logik: Vˣ = πₓ⁻¹(x) = {a∈ℝ ∣ F(a,x)=0}",
}

STEP_LEAN = {
    1: "Lean: def cubicFamily (a x : ℝ) : ℝ := x ^ 3 - a * x",
    2: "Lean: theorem cubicFamily_eq_zero_iff",
    3: "Lean: parameterFiber_of_neg / parameterFiber_at_zero / parameterFiber_of_pos",
    4: "Lean: stateFiber_at_zero / stateFiber_of_ne_zero",
}


def cubic_family(a: np.ndarray | float, x: np.ndarray | float) -> np.ndarray | float:
    """Evaluate F(a, x) = x³ - a·x."""

    return x**3 - a * x


def roots_for(a: float) -> list[float]:
    """Return the distinct real roots for a parameter value."""

    if a > 0:
        return [-float(np.sqrt(a)), 0.0, float(np.sqrt(a))]
    return [0.0]


def _new_canvas(step: int) -> tuple[Figure, Axes, Axes]:
    """Create two panels with deliberately identical physical dimensions."""

    fig = plt.figure(figsize=(14, 7.5), facecolor=PAPER)
    # Fixed rectangles avoid layout-engine changes caused by different tick-label
    # widths. This equality is asserted in tests/test_visualization.py.
    left = fig.add_axes((0.07, 0.19, 0.39, 0.67), facecolor=SURFACE)
    right = fig.add_axes((0.56, 0.19, 0.39, 0.67), facecolor=SURFACE)
    fig.text(0.07, 0.945, "MATH-VIZ-LAB · EXPERIMENT 01", color=ORANGE,
             fontsize=10, fontweight="bold")
    fig.text(0.07, 0.895, STEP_TITLES[step], color=INK, fontsize=19,
             fontweight="bold")
    fig.text(0.07, 0.115, STEP_NOTES[step], color=MUTED, fontsize=10)
    fig.text(0.07, 0.078, STEP_LOGIC[step], color=PURPLE, fontsize=9.5,
             fontweight="bold")
    fig.text(0.07, 0.042, STEP_LEAN[step], color=GREEN, fontsize=8.8,
             family="monospace")
    return fig, left, right


def _style_cartesian(ax: Axes, xlabel: str, ylabel: str) -> None:
    ax.set_xlabel(xlabel, color=INK, fontweight="bold")
    ax.set_ylabel(ylabel, color=INK, fontweight="bold")
    ax.tick_params(colors=INK)
    ax.grid(True, color=GRID, linewidth=0.8, alpha=0.8)
    for spine in ax.spines.values():
        spine.set_color(MUTED)
        spine.set_linewidth(0.8)


def _draw_locus(ax: Axes, *, label_branches: bool = True) -> None:
    ax.set_xlim(*A_DOMAIN)
    ax.set_ylim(*X_DOMAIN)
    _style_cartesian(ax, "Parameter a", "Zustand x")

    a_line = np.linspace(*A_DOMAIN, 300)
    ax.plot(a_line, np.zeros_like(a_line), color=GREEN, linewidth=3.2,
            label="Ast x=0", zorder=3)
    x_curve = np.linspace(-2.0, 2.0, 400)
    ax.plot(x_curve**2, x_curve, color=ORANGE, linewidth=3.2,
            label="Ast a=x²", zorder=4)
    ax.scatter([0], [0], s=65, color=INK, zorder=6)
    ax.annotate("kritischer Punkt (0,0)", (0, 0), xytext=(10, -25),
                textcoords="offset points", color=INK, fontweight="bold")
    if label_branches:
        ax.text(2.55, 1.68, "a=x²", color=ORANGE, fontweight="bold")
        ax.text(-1.65, 0.14, "x=0", color=GREEN, fontweight="bold")


def _draw_step_1(left: Axes, right: Axes) -> None:
    a = np.linspace(*A_DOMAIN, 320)
    x = np.linspace(*X_DOMAIN, 280)
    aa, xx = np.meshgrid(a, x)
    values = cubic_family(aa, xx)
    left.contourf(aa, xx, values, levels=[-100, 0, 100],
                  colors=[ORANGE_SOFT, BLUE_SOFT], alpha=0.94)
    left.contour(aa, xx, values, levels=[0], colors=[INK], linewidths=1.5)
    left.set_xlim(*A_DOMAIN)
    left.set_ylim(*X_DOMAIN)
    _style_cartesian(left, "Parameter a", "Zustand x")
    left.set_title("Vorzeichenfeld im (a,x)-Raum", color=INK, fontweight="bold")
    left.text(2.7, 2.0, "F>0", color=BLUE, fontweight="bold")
    left.text(2.7, 1.05, "F<0", color=ORANGE, fontweight="bold")
    left.legend(handles=[Patch(color=BLUE_SOFT, label="F(a,x)>0"),
                         Patch(color=ORANGE_SOFT, label="F(a,x)<0"),
                         Line2D([], [], color=INK, label="Grenze F(a,x)=0")],
                loc="lower left", frameon=True, facecolor=SURFACE)

    sample_x = np.linspace(*X_DOMAIN, 500)
    for value, color, style in [(-1.0, PURPLE, "--"), (0.0, GREEN, "-"), (1.0, BLUE, "-.")]:
        right.plot(sample_x, cubic_family(value, sample_x), color=color,
                   linestyle=style, linewidth=2.6, label=f"a={value:g}")
    right.axhline(0, color=ORANGE, linewidth=1.6, label="Niveau F=0")
    right.set_xlim(*X_DOMAIN)
    right.set_ylim(-12, 12)
    _style_cartesian(right, "Zustand x", "Funktionswert F(a,x)")
    right.set_title("Drei eindimensionale Schnitte", color=INK, fontweight="bold")
    right.legend(loc="upper left", frameon=True, facecolor=SURFACE)


def _logic_box(ax: Axes, xy: tuple[float, float], width: float, height: float,
               title: str, detail: str, color: str) -> None:
    box = FancyBboxPatch(xy, width, height, boxstyle="round,pad=0.02",
                         transform=ax.transAxes, facecolor=SURFACE,
                         edgecolor=color, linewidth=2)
    ax.add_patch(box)
    ax.text(xy[0] + width / 2, xy[1] + height * 0.62, title,
            transform=ax.transAxes, ha="center", va="center", color=INK,
            fontsize=15, fontweight="bold")
    ax.text(xy[0] + width / 2, xy[1] + height * 0.28, detail,
            transform=ax.transAxes, ha="center", va="center", color=MUTED,
            fontsize=10)


def _draw_step_2(left: Axes, right: Axes) -> None:
    _draw_locus(left)
    left.set_title("V = {(a,x) ∣ F(a,x)=0}", color=INK, fontweight="bold")
    left.legend(loc="upper left", frameon=True, facecolor=SURFACE)

    right.set_axis_off()
    right.set_title("Algebra → Logik → Geometrie", color=INK, fontweight="bold")
    _logic_box(right, (0.19, 0.72), 0.62, 0.15, "x(x²−a)=0", "faktorisierter Term", INK)
    _logic_box(right, (0.05, 0.38), 0.38, 0.17, "x=0", "Gerade", GREEN)
    _logic_box(right, (0.57, 0.38), 0.38, 0.17, "x²=a", "Parabel", ORANGE)
    _logic_box(right, (0.19, 0.06), 0.62, 0.15, "V = Gerade ∪ Parabel", "„oder“ wird Vereinigung", PURPLE)
    arrow = dict(arrowstyle="->", color=MUTED, linewidth=1.8)
    right.annotate("", xy=(0.24, 0.55), xytext=(0.43, 0.72),
                   xycoords="axes fraction", arrowprops=arrow)
    right.annotate("", xy=(0.76, 0.55), xytext=(0.57, 0.72),
                   xycoords="axes fraction", arrowprops=arrow)
    right.annotate("", xy=(0.37, 0.21), xytext=(0.24, 0.38),
                   xycoords="axes fraction", arrowprops=arrow)
    right.annotate("", xy=(0.63, 0.21), xytext=(0.76, 0.38),
                   xycoords="axes fraction", arrowprops=arrow)


def _draw_step_3(left: Axes, right: Axes, a: float) -> None:
    _draw_locus(left)
    left.set_title("Senkrechter Schnitt bei festem a", color=INK, fontweight="bold")
    left.axvline(a, color=PURPLE, linewidth=2.4, linestyle="--",
                 label=f"Faser a={a:.1f}")
    roots = roots_for(a)
    left.scatter([a] * len(roots), roots, s=95, color=PURPLE,
                 edgecolor=SURFACE, linewidth=2, zorder=8,
                 label="Elemente der Faser")
    left.legend(loc="upper left", frameon=True, facecolor=SURFACE)

    sample_x = np.linspace(*X_DOMAIN, 600)
    right.plot(sample_x, cubic_family(a, sample_x), color=BLUE, linewidth=3,
               label=f"x ↦ F({a:.1f},x)")
    right.axhline(0, color=ORANGE, linewidth=1.8, label="Niveau F=0")
    right.scatter(roots, np.zeros(len(roots)), s=95, color=PURPLE,
                  edgecolor=SURFACE, linewidth=2, zorder=8,
                  label="Nullstellen")
    right.set_xlim(*X_DOMAIN)
    right.set_ylim(-12, 12)
    _style_cartesian(right, "Zustand x", "Funktionswert F(a,x)")
    right.set_title("Dieselbe Faser als Funktionsgraph", color=INK, fontweight="bold")
    right.legend(loc="upper left", frameon=True, facecolor=SURFACE)

    count = "eine verschiedene Nullstelle" if len(roots) == 1 else "drei verschiedene Nullstellen"
    right.text(0.98, 0.04, count, transform=right.transAxes, ha="right",
               color=PURPLE, fontweight="bold",
               bbox=dict(facecolor=SURFACE, edgecolor=PURPLE, boxstyle="round,pad=0.35"))


def _draw_step_4(left: Axes, right: Axes, x: float) -> None:
    _draw_locus(left, label_branches=False)
    left.set_title("Waagerechter Schnitt bei festem x", color=INK, fontweight="bold")
    left.axhline(x, color=PURPLE, linewidth=2.4, linestyle="--",
                 label=f"Faser x={x:.1f}")
    if abs(x) < 1e-12:
        sample_a = np.linspace(*A_DOMAIN, 9)
        left.scatter(sample_a, np.zeros_like(sample_a), s=58, color=PURPLE,
                     edgecolor=SURFACE, linewidth=1.5, zorder=8)
        fiber_label = "alle a∈ℝ"
    else:
        left.scatter([x**2], [x], s=95, color=PURPLE,
                     edgecolor=SURFACE, linewidth=2, zorder=8)
        fiber_label = f"genau a=x²={x**2:.2f}"
    left.legend(handles=[Line2D([], [], color=ORANGE, linewidth=3, label="Ast a=x²"),
                         Line2D([], [], color=GREEN, linewidth=3, label="Ast x=0"),
                         Line2D([], [], color=PURPLE, linestyle="--", label=f"Faser x={x:.1f}")],
                loc="upper left", frameon=True, facecolor=SURFACE)

    right.set_xlim(*A_DOMAIN)
    right.set_ylim(-1, 1)
    right.set_yticks([])
    right.axhline(0, color=INK, linewidth=1.4)
    right.set_xlabel("Parameter a", color=INK, fontweight="bold")
    right.set_title("Parameter in der x-Faser", color=INK, fontweight="bold")
    right.grid(True, axis="x", color=GRID, linewidth=0.8)
    right.tick_params(colors=INK)
    for spine in right.spines.values():
        spine.set_color(MUTED)
        spine.set_linewidth(0.8)
    if abs(x) < 1e-12:
        right.plot(A_DOMAIN, [0, 0], color=PURPLE, linewidth=8,
                   solid_capstyle="round", label="gesamte reelle Parameterachse")
        right.scatter(np.linspace(*A_DOMAIN, 9), np.zeros(9), color=SURFACE,
                      edgecolor=PURPLE, linewidth=2, s=60, zorder=4)
    else:
        right.scatter([x**2], [0], color=PURPLE, edgecolor=SURFACE,
                      linewidth=2, s=140, zorder=4, label="einziger Parameter")
        right.annotate(f"a={x**2:.2f}", (x**2, 0), xytext=(0, 28),
                       textcoords="offset points", ha="center", color=PURPLE,
                       fontweight="bold")
    right.text(0.5, 0.17, fiber_label, transform=right.transAxes, ha="center",
               color=PURPLE, fontsize=14, fontweight="bold")
    right.legend(loc="upper left", frameon=True, facecolor=SURFACE)


def create_static_figure(step: int, *, a: float = 1.0, x: float = 0.0) -> tuple[Figure, tuple[Axes, Axes]]:
    """Create one fully labelled, deterministic two-panel research figure."""

    if step not in STEP_TITLES:
        raise ValueError("step must be between 1 and 4")
    fig, left, right = _new_canvas(step)
    if step == 1:
        _draw_step_1(left, right)
    elif step == 2:
        _draw_step_2(left, right)
    elif step == 3:
        _draw_step_3(left, right, a)
    else:
        _draw_step_4(left, right, x)
    return fig, (left, right)


def export_figures(output_dir: Path) -> None:
    """Regenerate the four version-controlled SVG research figures."""

    output_dir.mkdir(parents=True, exist_ok=True)
    settings = {1: {}, 2: {}, 3: {"a": 1.0}, 4: {"x": 0.0}}
    for step in range(1, 5):
        fig, _ = create_static_figure(step, **settings[step])
        target = output_dir / f"experiment-01-step-{step}.svg"
        fig.savefig(target, format="svg", facecolor=fig.get_facecolor(),
                    metadata={"Date": None})
        plt.close(fig)
        print(f"exported {target}")


class NativeLab:
    """Small native Matplotlib application; no browser or HTML is involved."""

    def __init__(self) -> None:
        self.step = 1
        self.a = 1.0
        self.x = 0.0
        self.fig = plt.figure(figsize=(14, 8.5), facecolor=PAPER)
        self.fig.canvas.manager.set_window_title("math-viz-lab · Kubische Fasern")
        self.left = self.fig.add_axes((0.07, 0.27, 0.39, 0.58), facecolor=SURFACE)
        self.right = self.fig.add_axes((0.56, 0.27, 0.39, 0.58), facecolor=SURFACE)
        self.title = self.fig.text(0.07, 0.93, "", color=INK, fontsize=19,
                                   fontweight="bold")
        self.note = self.fig.text(0.07, 0.225, "", color=MUTED, fontsize=9.5)
        self.logic = self.fig.text(0.07, 0.197, "", color=PURPLE,
                                   fontsize=9, fontweight="bold")
        self.lean = self.fig.text(0.07, 0.171, "", color=GREEN,
                                  fontsize=8.5, family="monospace")
        self.slider_axis = self.fig.add_axes((0.22, 0.125, 0.56, 0.035), facecolor=SURFACE)
        self.slider = Slider(self.slider_axis, "Parameter a", -2.0, 4.0,
                             valinit=self.a, valstep=0.1, color=ORANGE)
        self.slider.on_changed(self._on_slider)
        self.buttons: list[Button] = []
        for index in range(4):
            axis = self.fig.add_axes((0.14 + index * 0.19, 0.035, 0.16, 0.055))
            button = Button(axis, f"Schritt {index + 1}", color=SURFACE,
                            hovercolor=ORANGE_SOFT)
            button.on_clicked(lambda _event, value=index + 1: self._set_step(value))
            self.buttons.append(button)
        self.fig.canvas.mpl_connect("key_press_event", self._on_key)
        self._redraw()

    def _set_step(self, step: int) -> None:
        self.step = step
        self.slider.label.set_text("Zustand x" if step == 4 else "Parameter a")
        self.slider.valmin, self.slider.valmax = (-2.0, 2.0) if step == 4 else (-2.0, 4.0)
        self.slider.ax.set_xlim(self.slider.valmin, self.slider.valmax)
        self.slider.set_val(self.x if step == 4 else self.a)
        self._redraw()

    def _on_slider(self, value: float) -> None:
        if self.step == 4:
            self.x = value
        else:
            self.a = value
        self._redraw()

    def _on_key(self, event: object) -> None:
        key = getattr(event, "key", None)
        if key == "right":
            self._set_step(min(4, self.step + 1))
        elif key == "left":
            self._set_step(max(1, self.step - 1))

    def _redraw(self) -> None:
        self.left.clear()
        self.right.clear()
        self.title.set_text(STEP_TITLES[self.step])
        self.note.set_text(STEP_NOTES[self.step])
        self.logic.set_text(STEP_LOGIC[self.step])
        self.lean.set_text(STEP_LEAN[self.step])
        for index, button in enumerate(self.buttons, start=1):
            button.ax.set_facecolor(ORANGE_SOFT if index == self.step else SURFACE)
        if self.step == 1:
            _draw_step_1(self.left, self.right)
        elif self.step == 2:
            _draw_step_2(self.left, self.right)
        elif self.step == 3:
            _draw_step_3(self.left, self.right, self.a)
        else:
            _draw_step_4(self.left, self.right, self.x)
        self.fig.canvas.draw_idle()

    def show(self) -> None:
        plt.show()


def check_step_3_layout() -> None:
    fig, (left, right) = create_static_figure(3, a=1.0)
    fig.canvas.draw()
    lp, rp = left.get_position(), right.get_position()
    equal = np.isclose(lp.width, rp.width) and np.isclose(lp.height, rp.height)
    print(f"left={lp.width:.6f} x {lp.height:.6f}")
    print(f"right={rp.width:.6f} x {rp.height:.6f}")
    plt.close(fig)
    if not equal:
        raise SystemExit("step 3 panels are not equal")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--export", action="store_true", help="regenerate SVG figures")
    parser.add_argument("--check-layout", action="store_true", help="verify equal step-3 panels")
    parser.add_argument("--output", type=Path, default=Path("figures"), help="export directory")
    args = parser.parse_args()
    if args.export:
        export_figures(args.output)
    elif args.check_layout:
        check_step_3_layout()
    else:
        NativeLab().show()


if __name__ == "__main__":
    main()
