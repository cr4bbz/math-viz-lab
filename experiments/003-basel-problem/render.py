"""Native interactive visualization of the Basel problem.

The default command opens all four projection steps in one coupled Matplotlib
overview. ``--step`` opens a detailed view; ``--export`` regenerates SVGs.
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path
import sys

import matplotlib

if "--export" in sys.argv or "--check-layout" in sys.argv:
    matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.patches import Patch, Rectangle
from matplotlib.widgets import Button, Slider
import numpy as np

matplotlib.rcParams["svg.hashsalt"] = "math-viz-lab-basel"

EXPERIMENT_DIR = Path(__file__).resolve().parent
BASEL_LIMIT = math.pi**2 / 6
BILATERAL_LIMIT = math.pi**2 / 3

INK = "#10233f"
MUTED = "#66758a"
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

STEP_TITLES = {
    1: "1 · Summand: Das Reziproke eines Quadrats",
    2: "2 · Akkumulation: Partialsummen nähern sich π²/6",
    3: "3 · Restterm: Wie viel Fläche fehlt nach N Summanden?",
    4: "4 · Domänenwechsel: ℕ₊ gegenüber ℤ∖{0}",
}

STEP_NOTES = {
    1: "Jeder Summand 1/n² ist die Fläche eines Quadrats mit Seitenlänge 1/n.",
    2: "Die Projektion von der ganzen Termfolge auf S_N behält nur die akkumulierte Summe und verwirft die Einzelbeiträge.",
    3: "Der Rest R_N=π²/6−S_N liegt numerisch zwischen den Integralvergleichsgrenzen 1/(N+1) und 1/N.",
    4: "Bei ganzzahligen Indizes muss 0 ausgeschlossen werden; ±n liefern gleiche Werte und verdoppeln die Summe.",
}

STEP_LOGIC = {
    1: "Logik: a_n=1/n², n∈ℕ₊; geometrisch: Fläche Q_n=(1/n)²",
    2: "Logik: S_N=Σ_{n=1}^N 1/n²  →  π²/6",
    3: "Logik: R_N=π²/6−S_N;  1/(N+1) ≤ R_N ≤ 1/N",
    4: "Logik: Σ_{n∈ℤ∖{0}}1/n² = 2·Σ_{n≥1}1/n² = π²/3",
}

STEP_LEAN = {
    1: "Lean: baselTerm / baselTerm_of_pos",
    2: "Lean: basel_hasSum / basel_tsum (via mathlib.hasSum_zeta_two)",
    3: "Lean: Grenzwert bewiesen; Restschranken in diesem Experiment numerische Evidenz",
    4: "Lean: bilateralPartialSum_eq_two_mul / bilateral_hasSum",
}


def basel_term(n: int) -> float:
    if n <= 0:
        raise ValueError("the classical Basel term requires n >= 1")
    return 1.0 / (n * n)


def partial_sums(cutoff: int) -> np.ndarray:
    if cutoff < 1:
        raise ValueError("cutoff must be positive")
    n = np.arange(1, cutoff + 1, dtype=float)
    return np.cumsum(1.0 / n**2)


def partial_sum(n: int) -> float:
    return float(partial_sums(n)[-1])


def tail_error(n: int) -> float:
    return BASEL_LIMIT - partial_sum(n)


def _new_canvas(step: int) -> tuple[Figure, Axes, Axes]:
    fig = plt.figure(figsize=(14, 7.5), facecolor=PAPER)
    left = fig.add_axes((0.07, 0.19, 0.36, 0.672), facecolor=SURFACE)
    right = fig.add_axes((0.57, 0.19, 0.36, 0.672), facecolor=SURFACE)
    fig.text(0.07, 0.945, "MATH-VIZ-LAB · EXPERIMENT 03", color=ORANGE,
             fontsize=10, fontweight="bold")
    fig.text(0.07, 0.895, STEP_TITLES[step], color=INK, fontsize=18,
             fontweight="bold")
    fig.text(0.07, 0.115, STEP_NOTES[step], color=MUTED, fontsize=9.5)
    fig.text(0.07, 0.078, STEP_LOGIC[step], color=PURPLE, fontsize=9.5,
             fontweight="bold")
    fig.text(0.07, 0.042, STEP_LEAN[step], color=GREEN, fontsize=8.8,
             family="monospace")
    return fig, left, right


def _style(ax: Axes, xlabel: str, ylabel: str) -> None:
    ax.set_xlabel(xlabel, color=INK, fontweight="bold")
    ax.set_ylabel(ylabel, color=INK, fontweight="bold")
    ax.grid(True, color=GRID, linewidth=0.7, alpha=0.8)
    ax.tick_params(colors=INK)
    for spine in ax.spines.values():
        spine.set_color(MUTED)


def _draw_square_diagram(ax: Axes, *, compact: bool) -> None:
    ax.set_axis_off()
    positions = [(0.08, 0.56), (0.56, 0.56), (0.08, 0.08), (0.56, 0.08)]
    box = 0.34
    for n, (x0, y0) in enumerate(positions, start=1):
        ax.add_patch(Rectangle((x0, y0), box, box, transform=ax.transAxes,
                               facecolor=SURFACE, edgecolor=INK, linewidth=1.6))
        cell = box / n
        for k in range(1, n):
            ax.plot([x0 + k * cell, x0 + k * cell], [y0, y0 + box],
                    transform=ax.transAxes, color=GRID, linewidth=0.8)
            ax.plot([x0, x0 + box], [y0 + k * cell, y0 + k * cell],
                    transform=ax.transAxes, color=GRID, linewidth=0.8)
        ax.add_patch(Rectangle((x0, y0), cell, cell, transform=ax.transAxes,
                               facecolor=ORANGE, edgecolor=ORANGE, alpha=0.9))
        ax.text(x0 + box / 2, y0 - 0.045, f"n={n}: Fläche 1/{n*n}",
                transform=ax.transAxes, ha="center", va="top", color=INK,
                fontsize=6.5 if compact else 9, fontweight="bold")
    ax.set_title("Ein markiertes Teilquadrat hat Fläche 1/n²", color=INK,
                 fontweight="bold")


def _draw_step_1(left: Axes, right: Axes, visible: int,
                 *, compact: bool = False) -> None:
    indices = np.arange(1, visible + 1)
    values = 1.0 / indices.astype(float) ** 2
    left.vlines(indices, 0, values, color=BLUE, linewidth=1.8)
    left.scatter(indices, values, color=ORANGE, edgecolor=INK,
                 s=22 if compact else 48, zorder=3, label="aₙ=1/n²")
    left.set_xlim(0.3, visible + 0.7)
    left.set_ylim(0, 1.08)
    _style(left, "Index n∈ℕ₊", "Summand aₙ=1/n²")
    left.set_title(f"Die ersten {visible} Summanden", color=INK, fontweight="bold")
    left.legend(loc="upper right", frameon=True, facecolor=SURFACE,
                fontsize=7 if compact else 10)
    _draw_square_diagram(right, compact=compact)


def _draw_step_2(left: Axes, right: Axes, cutoff: int, selected: int,
                 *, compact: bool = False) -> None:
    sums = partial_sums(cutoff)
    indices = np.arange(1, cutoff + 1)
    left.plot(indices, sums, color=BLUE, linewidth=2.4, label="Partialsumme S_N")
    left.axhline(BASEL_LIMIT, color=ORANGE, linestyle="--", linewidth=2,
                 label="Grenzwert π²/6")
    selected = min(selected, cutoff)
    left.scatter([selected], [sums[selected - 1]], color=PURPLE,
                 s=45 if compact else 90, zorder=4)
    left.annotate(f"S_{selected}={sums[selected-1]:.8f}",
                  (selected, sums[selected - 1]), xytext=(8, -24),
                  textcoords="offset points", color=PURPLE,
                  fontsize=7 if compact else 10, fontweight="bold")
    left.set_xlim(1, cutoff)
    left.set_ylim(0.9, BASEL_LIMIT + 0.06)
    _style(left, "Summengrenze N", "Partialsumme S_N")
    left.set_title("Akkumulation der Summanden", color=INK, fontweight="bold")
    left.legend(loc="lower right", frameon=True, facecolor=SURFACE,
                fontsize=7 if compact else 10)

    errors = BASEL_LIMIT - sums
    right.loglog(indices, errors, color=PURPLE, linewidth=2.2,
                 label="Rest R_N=π²/6−S_N")
    right.loglog(indices, 1.0 / indices, color=GREEN, linestyle="--",
                 linewidth=1.6, label="Vergleich 1/N")
    right.scatter([selected], [errors[selected - 1]], color=ORANGE,
                  s=38 if compact else 80, zorder=4)
    _style(right, "Summengrenze N (log)", "Restfehler R_N (log)")
    right.set_title("Konvergenzgeschwindigkeit", color=INK, fontweight="bold")
    right.legend(loc="lower left", frameon=True, facecolor=SURFACE,
                 fontsize=7 if compact else 10)


def _draw_step_3(left: Axes, right: Axes, cutoff: int, selected: int,
                 *, compact: bool = False) -> None:
    selected = min(selected, cutoff)
    indices = np.arange(1, cutoff + 1)
    errors = BASEL_LIMIT - partial_sums(cutoff)
    lower = 1.0 / (indices + 1)
    upper = 1.0 / indices
    left.loglog(indices, upper, color=GREEN, linestyle="--", linewidth=1.6,
                label="obere Schranke 1/N")
    left.loglog(indices, errors, color=PURPLE, linewidth=2.5,
                label="Rest R_N")
    left.loglog(indices, lower, color=ORANGE, linestyle=":", linewidth=2,
                label="untere Schranke 1/(N+1)")
    left.fill_between(indices, lower, upper, color=GOLD, alpha=0.13,
                      label="Integralvergleichs-Korridor")
    left.scatter([selected], [errors[selected - 1]], color=INK,
                 s=35 if compact else 75, zorder=5)
    _style(left, "Summengrenze N (log)", "Wert (log)")
    left.set_title("Restterm zwischen zwei Schranken", color=INK, fontweight="bold")
    left.legend(loc="lower left", frameon=True, facecolor=SURFACE,
                fontsize=6 if compact else 9)

    lo = 1.0 / (selected + 1)
    err = errors[selected - 1]
    hi = 1.0 / selected
    right.axhline(0, color=INK, linewidth=1.2)
    right.scatter([lo, err, hi], [0, 0, 0],
                  color=[ORANGE, PURPLE, GREEN], edgecolor=INK,
                  s=75 if compact else 140, zorder=4)
    right.annotate("", xy=(hi, 0.28), xytext=(lo, 0.28),
                   arrowprops=dict(arrowstyle="<->", color=GOLD, linewidth=2.4))
    labels = [(lo, "1/(N+1)"), (err, "R_N"), (hi, "1/N")]
    for value, label in labels:
        right.annotate(f"{label}\n{value:.7f}", (value, 0), xytext=(0, -28),
                       textcoords="offset points", ha="center", color=INK,
                       fontsize=6.5 if compact else 9)
    pad = max((hi - lo) * 0.35, hi * 0.02)
    right.set_xlim(lo - pad, hi + pad)
    right.set_ylim(-0.55, 0.65)
    right.set_yticks([0], labels=[f"N={selected}"])
    _style(right, "Restgröße", "ausgewählter Index")
    right.set_title("Lokaler Schrankenvergleich", color=INK, fontweight="bold")
    right.legend(handles=[Line2D([], [], marker="o", linestyle="", color=PURPLE,
                                 markeredgecolor=INK, label="numerisch berechneter Rest")],
                 loc="upper right", frameon=True, facecolor=SURFACE,
                 fontsize=6.5 if compact else 9)


def _draw_step_4(left: Axes, right: Axes, visible: int, selected: int,
                 *, compact: bool = False) -> None:
    signed = np.array([z for z in range(-visible, visible + 1) if z != 0])
    values = 1.0 / signed.astype(float) ** 2
    colors = [ORANGE if z < 0 else BLUE for z in signed]
    left.vlines(signed, 0, values, colors=colors, linewidth=1.6)
    left.scatter(signed, values, c=colors, edgecolor=INK,
                 s=18 if compact else 42, zorder=3)
    left.scatter([0], [0], marker="x", color=INK, s=60 if compact else 110,
                 linewidth=2.2, label="n=0 ausgeschlossen")
    left.set_xlim(-visible - 0.8, visible + 0.8)
    left.set_ylim(-0.03, 1.08)
    _style(left, "Ganzzahlindex n∈ℤ", "1/n² für n≠0")
    left.set_title("Spiegelsymmetrie n↔−n", color=INK, fontweight="bold")
    left.legend(handles=[Patch(color=ORANGE, label="negative Indizes"),
                         Patch(color=BLUE, label="positive Indizes"),
                         Line2D([], [], marker="x", linestyle="", color=INK,
                                label="0 ausgeschlossen")],
                loc="upper center", frameon=True, facecolor=SURFACE,
                fontsize=6 if compact else 9)

    one_sided = partial_sum(selected)
    bilateral = 2 * one_sided
    x = np.array([0, 1])
    right.bar(x, [one_sided, bilateral], color=[BLUE, PURPLE], width=0.55,
              edgecolor=INK)
    right.axhline(BASEL_LIMIT, color=ORANGE, linestyle="--", linewidth=1.7,
                  label="π²/6")
    right.axhline(BILATERAL_LIMIT, color=GREEN, linestyle=":", linewidth=2,
                  label="π²/3")
    right.set_xticks(x, labels=[f"positiv\nS_{selected}",
                                f"beidseitig\n2S_{selected}"])
    for xpos, value in zip(x, [one_sided, bilateral]):
        right.text(xpos, value + 0.05, f"{value:.6f}", ha="center", color=INK,
                   fontsize=7 if compact else 10, fontweight="bold")
    right.set_xlim(-0.6, 1.6)
    right.set_ylim(0, BILATERAL_LIMIT + 0.28)
    _style(right, "Indexdomäne", "symmetrische Partialsumme")
    right.set_title("Verdopplung durch ±n-Paare", color=INK, fontweight="bold")
    right.legend(loc="lower right", frameon=True, facecolor=SURFACE,
                 fontsize=7 if compact else 10)


def create_static_figure(step: int, *, cutoff: int = 200, selected: int = 20,
                         visible: int = 10) -> tuple[Figure, tuple[Axes, Axes]]:
    if step not in STEP_TITLES:
        raise ValueError("step must be between 1 and 4")
    if not (1 <= selected <= cutoff):
        raise ValueError("selected must satisfy 1 <= selected <= cutoff")
    fig, left, right = _new_canvas(step)
    if step == 1:
        _draw_step_1(left, right, visible)
    elif step == 2:
        _draw_step_2(left, right, cutoff, selected)
    elif step == 3:
        _draw_step_3(left, right, cutoff, selected)
    else:
        _draw_step_4(left, right, visible, selected)
    return fig, (left, right)


def export_figures(output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for step in range(1, 5):
        fig, _ = create_static_figure(step)
        target = output_dir / f"experiment-03-step-{step}.svg"
        fig.savefig(target, format="svg", facecolor=fig.get_facecolor(),
                    metadata={"Date": None})
        normalized = "\n".join(
            line.rstrip() for line in target.read_text(encoding="utf-8").splitlines()
        ) + "\n"
        target.write_bytes(normalized.encode("utf-8"))
        plt.close(fig)
        print(f"exported {target}")


class InteractiveOverview:
    """All Basel projections in one native, coupled dashboard."""

    def __init__(self, *, cutoff: int = 200, selected: int = 20,
                 visible: int = 10) -> None:
        cutoff = max(20, min(500, cutoff))
        selected = max(1, min(cutoff, selected))
        visible = max(4, min(30, visible))
        self.fig = plt.figure(figsize=(18, 10.5), facecolor=PAPER)
        self.fig.canvas.manager.set_window_title(
            "math-viz-lab · Interaktives Basel-Problem"
        )
        self.fig.text(0.04, 0.974, "BASEL-PROBLEM · ALLE PROJEKTIONSSCHRITTE",
                      color=INK, fontsize=20, fontweight="bold", va="top")
        self.fig.text(
            0.04, 0.937,
            "Terme, Partialsummen, Restschranken und die symmetrische Ganzzahldomäne reagieren gemeinsam.",
            color=MUTED, fontsize=10.5, va="top",
        )
        specs = {
            1: (0.04, 0.265, 0.58, 0.895),
            2: (0.535, 0.76, 0.58, 0.895),
            3: (0.04, 0.265, 0.17, 0.485),
            4: (0.535, 0.76, 0.17, 0.485),
        }
        short_titles = {
            1: "Schritt 1 · Summand und Quadratfläche",
            2: "Schritt 2 · Partialsummen",
            3: "Schritt 3 · Restterm",
            4: "Schritt 4 · Ganzzahldomäne",
        }
        self.panels: dict[int, tuple[Axes, Axes]] = {}
        for step, (left_x, right_x, bottom, title_y) in specs.items():
            left = self.fig.add_axes((left_x, bottom, 0.17, 0.29), facecolor=SURFACE)
            right = self.fig.add_axes((right_x, bottom, 0.17, 0.29), facecolor=SURFACE)
            self.panels[step] = (left, right)
            self.fig.text(left_x, title_y, short_titles[step], color=INK,
                          fontsize=12, fontweight="bold")

        slider_color = ORANGE_SOFT
        self.cutoff_slider = Slider(
            self.fig.add_axes((0.08, 0.065, 0.20, 0.020), facecolor=SURFACE),
            "Kurvenende M", 20, 500, valinit=cutoff, valstep=10,
            color=slider_color,
        )
        self.selected_slider = Slider(
            self.fig.add_axes((0.38, 0.065, 0.20, 0.020), facecolor=SURFACE),
            "Partialsumme N", 1, cutoff, valinit=selected, valstep=1,
            color=slider_color,
        )
        self.visible_slider = Slider(
            self.fig.add_axes((0.68, 0.065, 0.16, 0.020), facecolor=SURFACE),
            "sichtbare Terme K", 4, 30, valinit=visible, valstep=1,
            color=slider_color,
        )
        self.export_button = Button(
            self.fig.add_axes((0.88, 0.048, 0.09, 0.05)), "SVG-Export",
            color=SURFACE, hovercolor=ORANGE_SOFT,
        )
        self.status = self.fig.text(0.50, 0.515, "", ha="center", color=PURPLE,
                                    fontsize=9.5, fontweight="bold")
        self.cutoff_slider.on_changed(self._on_change)
        self.selected_slider.on_changed(self._on_change)
        self.visible_slider.on_changed(self._on_change)
        self.export_button.on_clicked(self._on_export)
        self._redraw()

    def _on_change(self, _value: float) -> None:
        cutoff = int(self.cutoff_slider.val)
        self.selected_slider.valmax = cutoff
        self.selected_slider.ax.set_xlim(1, cutoff)
        if self.selected_slider.val > cutoff:
            self.selected_slider.set_val(cutoff)
            return
        self._redraw()

    def _on_export(self, _event: object) -> None:
        export_figures(EXPERIMENT_DIR / "renders")
        self.status.set_text("Vier deterministische SVGs wurden neu erzeugt.")
        self.fig.canvas.draw_idle()

    def _redraw(self) -> None:
        cutoff = int(self.cutoff_slider.val)
        selected = int(self.selected_slider.val)
        visible = int(self.visible_slider.val)
        for left, right in self.panels.values():
            left.clear()
            right.clear()
        _draw_step_1(*self.panels[1], visible, compact=True)
        _draw_step_2(*self.panels[2], cutoff, selected, compact=True)
        _draw_step_3(*self.panels[3], cutoff, selected, compact=True)
        _draw_step_4(*self.panels[4], visible, selected, compact=True)
        for left, right in self.panels.values():
            for axis in (left, right):
                axis.title.set_fontsize(9)
                axis.xaxis.label.set_fontsize(8)
                axis.yaxis.label.set_fontsize(8)
                axis.tick_params(labelsize=7)
        self.status.set_text(
            f"Aktiver Zustand: M={cutoff}, N={selected}, K={visible} · "
            f"S_N={partial_sum(selected):.9f}, Rest={tail_error(selected):.3e}"
        )
        self.fig.canvas.draw_idle()

    def show(self) -> None:
        plt.show()


def check_layout() -> None:
    for step in range(1, 5):
        fig, (left, right) = create_static_figure(step)
        fig.canvas.draw()
        lp, rp = left.get_position(), right.get_position()
        if not (np.isclose(lp.width, rp.width) and np.isclose(lp.height, rp.height)):
            raise SystemExit(f"step {step} panels are not equal")
        plt.close(fig)
    print("all comparison panels have equal physical dimensions")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--export", action="store_true", help="regenerate SVG figures")
    parser.add_argument("--check-layout", action="store_true", help="verify panel dimensions")
    parser.add_argument("--step", type=int, choices=range(1, 5),
                        help="show only one detailed step")
    parser.add_argument("--cutoff", type=int, default=200, help="curve cutoff M")
    parser.add_argument("--selected", type=int, default=20, help="selected partial sum N")
    parser.add_argument("--visible", type=int, default=10, help="visible signed radius K")
    parser.add_argument("--output", type=Path, default=EXPERIMENT_DIR / "renders")
    args = parser.parse_args()
    if args.export:
        export_figures(args.output)
    elif args.check_layout:
        check_layout()
    elif args.step is None:
        InteractiveOverview(cutoff=args.cutoff, selected=args.selected,
                            visible=args.visible).show()
    else:
        fig, _ = create_static_figure(args.step, cutoff=args.cutoff,
                                      selected=args.selected, visible=args.visible)
        fig.canvas.manager.set_window_title("math-viz-lab · Basel-Problem")
        plt.show()


if __name__ == "__main__":
    main()
