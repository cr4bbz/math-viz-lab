"""Native research lab for Basel weights on prime-height fibers.

The default command opens all four projections in one coupled Matplotlib
overview. ``--step`` opens one detailed view and ``--export`` regenerates the
deterministic SVG evidence.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import math
import sys

import matplotlib

if "--export" in sys.argv or "--check-layout" in sys.argv:
    matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.widgets import Button, Slider
import numpy as np

matplotlib.rcParams["svg.hashsalt"] = "math-viz-lab-weighted-prime-height-fibers"

EXPERIMENT_DIR = Path(__file__).resolve().parent
BASEL_LIMIT = math.pi**2 / 6

INK = "#10233f"
MUTED = "#66758a"
PAPER = "#f7f3ea"
SURFACE = "#fffdf8"
GRID = "#d8d5cd"
BLUE = "#2878a8"
ORANGE = "#d26535"
GREEN = "#24755d"
PURPLE = "#6c52a2"
GOLD = "#e8b44d"
PALE_ORANGE = "#fae3d5"

STEP_TITLES = {
    1: "1 · Höhenfaser: Ein Basel-Gewicht pro Gitterpunkt",
    2: "2 · Multiplikation: Faserkardinalität verändert den Abfall",
    3: "3 · Akkumulation: Konvergente Reihe wird divergent",
    4: "4 · Primfilter: Nur Primhöhen, weiterhin divergent",
}

STEP_NOTES = {
    1: "Die Projektion (a,b)↦n=a+b bündelt n−1 Gitterpunkte; jeder trägt dasselbe Gewicht 1/n².",
    2: "Der Einzelindex trägt 1/n², die ganze Faser dagegen (n−1)/n²≈1/n.",
    3: "Die Fasersumme ist exakt H_N−S_N. Die wachsende Multiplizität zerstört die Basel-Konvergenz.",
    4: "Der Primfilter verwirft zusammengesetzte Höhen, doch Σₚ(p−1)/p² ist nicht summierbar.",
}

STEP_LOGIC = {
    1: "Logik: H_n={(a,b)∈ℕ₊² | a+b=n}; |H_n|=n−1; μ(H_n)=Σ_{(a,b)∈H_n}1/n²",
    2: "Logik: μ(H_n)=(n−1)/n²=1/n−1/n²",
    3: "Logik: T_N=Σ_{n≤N}μ(H_n)=H_N−S_N",
    4: "Logik: Σ_{p prim} μ(H_p)=Σₚ(1/p−1/p²) divergiert",
}

STEP_LEAN = {
    1: "Lean: visibleFiberMass_of_complete",
    2: "Lean: fullFiberMass_eq_one_div_sub_one_div_sq",
    3: "Lean: fiberMassPartialSum_eq_reciprocal_sub_basel / fullFiberMass_not_summable",
    4: "Lean: prime_fullFiberMass_not_summable",
}


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    return all(n % divisor for divisor in range(3, math.isqrt(n) + 1, 2))


def basel_weight(n: int) -> float:
    if n < 1:
        raise ValueError("n must be positive")
    return 1.0 / (n * n)


def fiber_cardinality(n: int) -> int:
    if n < 1:
        raise ValueError("n must be positive")
    return max(0, n - 1)


def full_fiber_mass(n: int) -> float:
    return fiber_cardinality(n) * basel_weight(n)


def positive_height_fiber(n: int) -> list[tuple[int, int]]:
    if n < 2:
        return []
    return [(a, n - a) for a in range(1, n)]


@dataclass(frozen=True)
class SeriesData:
    indices: np.ndarray
    basel_terms: np.ndarray
    fiber_masses: np.ndarray
    prime_mask: np.ndarray
    basel_sums: np.ndarray
    harmonic_sums: np.ndarray
    fiber_sums: np.ndarray
    prime_fiber_sums: np.ndarray


def series_data(cutoff: int) -> SeriesData:
    if cutoff < 2:
        raise ValueError("cutoff must be at least 2")
    indices = np.arange(1, cutoff + 1, dtype=int)
    real_indices = indices.astype(float)
    basel_terms = 1.0 / real_indices**2
    fiber_masses = (real_indices - 1.0) * basel_terms
    prime_mask = np.fromiter((is_prime(int(n)) for n in indices), dtype=bool)
    basel_sums = np.cumsum(basel_terms)
    harmonic_sums = np.cumsum(1.0 / real_indices)
    fiber_sums = np.cumsum(fiber_masses)
    prime_fiber_sums = np.cumsum(np.where(prime_mask, fiber_masses, 0.0))
    return SeriesData(
        indices,
        basel_terms,
        fiber_masses,
        prime_mask,
        basel_sums,
        harmonic_sums,
        fiber_sums,
        prime_fiber_sums,
    )


def _style(ax: Axes, xlabel: str, ylabel: str) -> None:
    ax.set_xlabel(xlabel, color=INK, fontweight="bold")
    ax.set_ylabel(ylabel, color=INK, fontweight="bold")
    ax.grid(True, color=GRID, linewidth=0.7, alpha=0.8)
    ax.tick_params(colors=INK)
    for spine in ax.spines.values():
        spine.set_color(MUTED)


def _new_canvas(step: int) -> tuple[Figure, Axes, Axes]:
    fig = plt.figure(figsize=(14, 7.5), facecolor=PAPER)
    left = fig.add_axes((0.07, 0.19, 0.36, 0.672), facecolor=SURFACE)
    right = fig.add_axes((0.57, 0.19, 0.36, 0.672), facecolor=SURFACE)
    fig.text(0.07, 0.945, "MATH-VIZ-LAB · EXPERIMENT 04 · KOMPOSITION 002+003",
             color=ORANGE, fontsize=10, fontweight="bold")
    fig.text(0.07, 0.895, STEP_TITLES[step], color=INK, fontsize=18,
             fontweight="bold")
    fig.text(0.07, 0.115, STEP_NOTES[step], color=MUTED, fontsize=9.5)
    fig.text(0.07, 0.078, STEP_LOGIC[step], color=PURPLE, fontsize=9.3,
             fontweight="bold")
    fig.text(0.07, 0.042, STEP_LEAN[step], color=GREEN, fontsize=8.8,
             family="monospace")
    return fig, left, right


def _draw_step_1(left: Axes, right: Axes, selected: int,
                 *, compact: bool = False) -> None:
    fiber = positive_height_fiber(selected)
    a = np.array([point[0] for point in fiber])
    b = np.array([point[1] for point in fiber])
    left.plot([1, selected - 1], [selected - 1, 1], color=GOLD,
              linewidth=2.2, linestyle="--", label=f"Gerade a+b={selected}")
    left.scatter(a, b, color=PURPLE, edgecolor=INK,
                 s=32 if compact else 75, zorder=3,
                 label=f"H_{selected}: {selected-1} Punkte")
    left.set_xlim(0.5, selected - 0.5)
    left.set_ylim(0.5, selected - 0.5)
    left.set_aspect("equal", adjustable="box")
    left.set_xticks(np.arange(1, selected, max(1, (selected - 1) // 8)))
    left.set_yticks(np.arange(1, selected, max(1, (selected - 1) // 8)))
    _style(left, "erste Koordinate a", "zweite Koordinate b")
    left.set_title(f"Positive Höhenfaser H_{selected}", color=INK,
                   fontweight="bold")
    left.legend(loc="upper right", frameon=True, facecolor=SURFACE,
                fontsize=6.5 if compact else 9)

    term = basel_weight(selected)
    mass = full_fiber_mass(selected)
    right.bar(a, np.full_like(a, term, dtype=float), color=BLUE,
              edgecolor=INK, width=0.78, label="Punktgewicht 1/n²")
    right.axhline(term, color=ORANGE, linestyle="--", linewidth=1.8,
                  label=f"gleiches Gewicht: 1/{selected}²")
    right.set_xlim(0.3, selected - 0.3)
    right.set_ylim(0, term * 1.45)
    right.text(0.5, 0.88,
               f"Summe der {selected-1} Balken\nμ(H_{selected})={selected-1}/{selected**2}={mass:.6f}",
               transform=right.transAxes, ha="center", va="top", color=PURPLE,
               fontsize=7 if compact else 10, fontweight="bold")
    _style(right, "Faserkoordinate a", "Gewicht des Punkts (a,n−a)")
    right.set_title("Konstantes Gewicht entlang der Faser", color=INK,
                    fontweight="bold")
    right.legend(loc="lower center", frameon=True, facecolor=SURFACE,
                 fontsize=6.5 if compact else 9)


def _draw_step_2(left: Axes, right: Axes, data: SeriesData, selected: int,
                 *, compact: bool = False) -> None:
    n = data.indices[1:]
    base = data.basel_terms[1:]
    mass = data.fiber_masses[1:]
    left.loglog(n, base, color=BLUE, linewidth=2.2,
                label="Einzelgewicht 1/n²")
    left.loglog(n, mass, color=PURPLE, linewidth=2.4,
                label="Fasermasse (n−1)/n²")
    left.scatter([selected], [basel_weight(selected)], color=BLUE,
                 edgecolor=INK, s=30 if compact else 65, zorder=4)
    left.scatter([selected], [full_fiber_mass(selected)], color=PURPLE,
                 edgecolor=INK, s=30 if compact else 65, zorder=4)
    _style(left, "Höhenindex n (log)", "Gewicht (log)")
    left.set_title("Quadratischer gegen harmonischen Abfall", color=INK,
                   fontweight="bold")
    left.legend(loc="lower left", frameon=True, facecolor=SURFACE,
                fontsize=6.5 if compact else 9)

    ratio = n - 1
    right.plot(n, ratio, color=ORANGE, linewidth=2.3,
               label="μ(H_n)/(1/n²)=|H_n|=n−1")
    right.scatter([selected], [selected - 1], color=PURPLE, edgecolor=INK,
                  s=38 if compact else 80, zorder=4)
    right.annotate(f"n={selected}: Faktor {selected-1}",
                   (selected, selected - 1), xytext=(8, 10),
                   textcoords="offset points", color=PURPLE,
                   fontsize=7 if compact else 10, fontweight="bold")
    _style(right, "Höhenindex n", "Fasermultiplizität |H_n|")
    right.set_title("Verlorene Faserinformation wird zum Faktor", color=INK,
                    fontweight="bold")
    right.legend(loc="upper left", frameon=True, facecolor=SURFACE,
                 fontsize=6.5 if compact else 9)


def _draw_step_3(left: Axes, right: Axes, data: SeriesData,
                 *, compact: bool = False) -> None:
    n = data.indices
    left.semilogx(n, data.basel_sums, color=BLUE, linewidth=2.2,
                  label="Basel S_N=Σ1/n²")
    left.semilogx(n, data.fiber_sums, color=PURPLE, linewidth=2.5,
                  label="Fasersumme T_N=Σ(n−1)/n²")
    left.axhline(BASEL_LIMIT, color=ORANGE, linestyle="--", linewidth=1.8,
                 label="Basel-Grenzwert π²/6")
    _style(left, "Summengrenze N (log)", "Partialsumme")
    left.set_title("Konvergenz und Divergenz im selben Bild", color=INK,
                   fontweight="bold")
    left.legend(loc="upper left", frameon=True, facecolor=SURFACE,
                fontsize=6.5 if compact else 9)

    cutoff = int(data.indices[-1])
    values = [data.harmonic_sums[-1], data.basel_sums[-1], data.fiber_sums[-1]]
    labels = [f"H_{cutoff}\nharmonisch", f"S_{cutoff}\nBasel",
              f"T_{cutoff}\nFasern"]
    bars = right.bar(np.arange(3), values, color=[ORANGE, BLUE, PURPLE],
                     edgecolor=INK, width=0.62)
    right.set_xticks(np.arange(3), labels=labels)
    for bar, value in zip(bars, values):
        right.text(bar.get_x() + bar.get_width() / 2, value + max(values) * 0.025,
                   f"{value:.5f}", ha="center", color=INK,
                   fontsize=6.5 if compact else 9, fontweight="bold")
    right.text(0.5, 0.92, f"Exakt: T_{cutoff}=H_{cutoff}−S_{cutoff}",
               transform=right.transAxes, ha="center", color=GREEN,
               fontsize=7 if compact else 10, fontweight="bold")
    right.set_ylim(0, max(values) * 1.22)
    _style(right, "Summenart", f"Wert bei N={cutoff}")
    right.set_title("Endliche Identität erklärt den Unterschied", color=INK,
                    fontweight="bold")


def _draw_step_4(left: Axes, right: Axes, data: SeriesData,
                 *, compact: bool = False) -> None:
    mask = data.prime_mask & (data.indices >= 2)
    primes = data.indices[mask]
    prime_masses = data.fiber_masses[mask]
    left.loglog(data.indices[1:], data.fiber_masses[1:], color=MUTED,
                linewidth=1.4, alpha=0.75, label="alle Höhen μ(H_n)")
    left.scatter(primes, prime_masses, color=ORANGE, edgecolor=INK,
                 s=16 if compact else 36, zorder=3,
                 label="behaltene Primhöhen μ(H_p)")
    _style(left, "Höhenindex n (log)", "Fasermasse (log)")
    left.set_title("Primfilter auf dem Höhenbildraum", color=INK,
                   fontweight="bold")
    left.legend(loc="lower left", frameon=True, facecolor=SURFACE,
                fontsize=6.5 if compact else 9)

    right.semilogx(data.indices, data.fiber_sums, color=PURPLE, linewidth=2.2,
                   label="alle Fasern T_N")
    right.semilogx(data.indices, data.prime_fiber_sums, color=ORANGE,
                   linewidth=2.5, label="nur Primfasern P_N")
    right.semilogx(data.indices, data.basel_sums, color=BLUE, linestyle="--",
                   linewidth=1.6, label="Basel S_N (konvergent)")
    _style(right, "Filtergrenze N (log)", "gefilterte Partialsumme")
    right.set_title("Langsames Wachstum bleibt Divergenz", color=INK,
                    fontweight="bold")
    right.legend(loc="upper left", frameon=True, facecolor=SURFACE,
                 fontsize=6.5 if compact else 9)
    right.text(0.97, 0.08, "Lean: nicht summierbar",
               transform=right.transAxes, ha="right", color=GREEN,
               fontsize=7 if compact else 10, fontweight="bold")


def create_static_figure(step: int, *, cutoff: int = 500,
                         selected: int = 11) -> tuple[Figure, tuple[Axes, Axes]]:
    if step not in STEP_TITLES:
        raise ValueError("step must be between 1 and 4")
    if cutoff < 2:
        raise ValueError("cutoff must be at least 2")
    if not (2 <= selected <= cutoff):
        raise ValueError("selected must satisfy 2 <= selected <= cutoff")
    data = series_data(cutoff)
    fig, left, right = _new_canvas(step)
    if step == 1:
        _draw_step_1(left, right, selected)
    elif step == 2:
        _draw_step_2(left, right, data, selected)
    elif step == 3:
        _draw_step_3(left, right, data)
    else:
        _draw_step_4(left, right, data)
    return fig, (left, right)


def export_figures(output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for step in range(1, 5):
        fig, _ = create_static_figure(step)
        target = output_dir / f"experiment-04-step-{step}.svg"
        fig.savefig(target, format="svg", facecolor=fig.get_facecolor(),
                    metadata={"Date": None})
        normalized = "\n".join(
            line.rstrip() for line in target.read_text(encoding="utf-8").splitlines()
        ) + "\n"
        target.write_bytes(normalized.encode("utf-8"))
        plt.close(fig)
        print(f"exported {target}")


class InteractiveOverview:
    """All four coupled projections in one native dashboard."""

    def __init__(self, *, cutoff: int = 500, selected: int = 11) -> None:
        cutoff = max(50, min(2000, cutoff))
        cutoff = int(round(cutoff / 50) * 50)
        selected = max(2, min(50, selected))
        self.fig = plt.figure(figsize=(18, 10.5), facecolor=PAPER)
        self.fig.canvas.manager.set_window_title(
            "math-viz-lab · Gewichtete Primhöhenfasern"
        )
        self.fig.text(0.04, 0.974,
                      "GEWICHTETE PRIMHÖHENFASERN · EXPERIMENTE 002 + 003",
                      color=INK, fontsize=20, fontweight="bold", va="top")
        self.fig.text(
            0.04, 0.937,
            "Die Kardinalität einer Höhenfaser multipliziert das Basel-Gewicht und verändert die Summierbarkeit.",
            color=MUTED, fontsize=10.5, va="top",
        )
        specs = {
            1: (0.04, 0.265, 0.58, 0.895),
            2: (0.535, 0.76, 0.58, 0.895),
            3: (0.04, 0.265, 0.17, 0.485),
            4: (0.535, 0.76, 0.17, 0.485),
        }
        short_titles = {
            1: "Schritt 1 · Gewichtete Höhenfaser",
            2: "Schritt 2 · Multiplizität",
            3: "Schritt 3 · Partialsummen",
            4: "Schritt 4 · Primhöhenfilter",
        }
        self.panels: dict[int, tuple[Axes, Axes]] = {}
        for step, (left_x, right_x, bottom, title_y) in specs.items():
            left = self.fig.add_axes((left_x, bottom, 0.17, 0.29), facecolor=SURFACE)
            right = self.fig.add_axes((right_x, bottom, 0.17, 0.29), facecolor=SURFACE)
            self.panels[step] = (left, right)
            self.fig.text(left_x, title_y, short_titles[step], color=INK,
                          fontsize=12, fontweight="bold")

        self.cutoff_slider = Slider(
            self.fig.add_axes((0.12, 0.065, 0.27, 0.020), facecolor=SURFACE),
            "Summengrenze M", 50, 2000, valinit=cutoff, valstep=50,
            color=PALE_ORANGE,
        )
        self.selected_slider = Slider(
            self.fig.add_axes((0.53, 0.065, 0.22, 0.020), facecolor=SURFACE),
            "Höhenfaser n", 2, 50, valinit=selected, valstep=1,
            color=PALE_ORANGE,
        )
        self.export_button = Button(
            self.fig.add_axes((0.86, 0.048, 0.11, 0.05)), "SVG-Export",
            color=SURFACE, hovercolor=PALE_ORANGE,
        )
        self.status = self.fig.text(0.50, 0.515, "", ha="center", color=PURPLE,
                                    fontsize=9.2, fontweight="bold")
        self.cutoff_slider.on_changed(self._on_change)
        self.selected_slider.on_changed(self._on_change)
        self.export_button.on_clicked(self._on_export)
        self._redraw()

    def _on_change(self, _value: float) -> None:
        self._redraw()

    def _on_export(self, _event: object) -> None:
        export_figures(EXPERIMENT_DIR / "renders")
        self.status.set_text("Vier deterministische SVGs wurden neu erzeugt.")
        self.fig.canvas.draw_idle()

    def _redraw(self) -> None:
        cutoff = int(self.cutoff_slider.val)
        selected = int(self.selected_slider.val)
        data = series_data(cutoff)
        for left, right in self.panels.values():
            left.clear()
            right.clear()
        _draw_step_1(*self.panels[1], selected, compact=True)
        _draw_step_2(*self.panels[2], data, selected, compact=True)
        _draw_step_3(*self.panels[3], data, compact=True)
        _draw_step_4(*self.panels[4], data, compact=True)
        for left, right in self.panels.values():
            for axis in (left, right):
                axis.title.set_fontsize(9)
                axis.xaxis.label.set_fontsize(8)
                axis.yaxis.label.set_fontsize(8)
                axis.tick_params(labelsize=7)
        self.status.set_text(
            f"Aktiver Zustand: M={cutoff}, n={selected} · |H_n|={selected-1}, "
            f"μ(H_n)={full_fiber_mass(selected):.6f}, "
            f"Primfasersumme P_M={data.prime_fiber_sums[-1]:.6f}"
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
                        help="show only one detailed projection")
    parser.add_argument("--cutoff", type=int, default=500, help="summation cutoff M")
    parser.add_argument("--selected", type=int, default=11, help="selected height n")
    parser.add_argument("--output", type=Path, default=EXPERIMENT_DIR / "renders")
    args = parser.parse_args()
    if args.export:
        export_figures(args.output)
    elif args.check_layout:
        check_layout()
    elif args.step is None:
        InteractiveOverview(cutoff=args.cutoff, selected=args.selected).show()
    else:
        fig, _ = create_static_figure(args.step, cutoff=args.cutoff,
                                      selected=args.selected)
        fig.canvas.manager.set_window_title(
            "math-viz-lab · Gewichtete Primhöhenfasern"
        )
        plt.show()


if __name__ == "__main__":
    main()
