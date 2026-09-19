"""Native figures for prime-height geometry on the positive integer lattice.

Run without arguments to show one selected step in a Matplotlib window. Use
``--export`` to regenerate all four deterministic SVG research figures.
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

matplotlib.rcParams["svg.hashsalt"] = "math-viz-lab-prime-height"

EXPERIMENT_DIR = Path(__file__).resolve().parent

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
    1: "1 · Höhenprojektion: Gitterpunkte werden zu diagonalen Fasern",
    2: "2 · Primzahlfilter: Primzahlen wählen Höhenbänder aus",
    3: "3 · Primzahllücke: Indexabstand und euklidische Distanz",
    4: "4 · Endliches Fenster: vollständige und abgeschnittene Fasern",
}

STEP_NOTES = {
    1: "Die Projektion πₕ(a,b)=a+b verwirft die Lage entlang einer Diagonale; ihre Faser behält alle Zerlegungen n=a+b.",
    2: "Primalität verändert nicht die Form einer Faser. Sie entscheidet nur, welche Höhenindizes orange markiert werden.",
    3: "Für 11 und 13 ist die Primzahllücke 2; der senkrechte Abstand der Geraden beträgt dagegen 2/√2=√2.",
    4: "Ab n>N+1 ist die positive Faser nicht mehr vollständig sichtbar. Sinkende Punktzahlen sind dann Fensterartefakte.",
}

STEP_LOGIC = {
    1: "Logik: πₕ⁻¹(n) = {(a,b)∈ℕ₊² ∣ a+b=n}",
    2: "Logik: PrimeHeight(a,b) ↔ Nat.Prime(a+b)",
    3: "Logik: bandGap(p,q)=q−p;  separatorCount(p,q)=q−p−1",
    4: "Logik: C_N(n)=#{(a,b)∈[1,N]² ∣ a+b=n}",
}

STEP_LEAN = {
    1: "Lean: height / visibleHeightCardinality_of_complete",
    2: "Lean: PrimeHeight / primeHeight_of_sum_eq",
    3: "Lean: eleven_thirteen_prime_gap / bandNormalDistance_eleven_thirteen",
    4: "Lean: visibleHeightCardinality_of_complete / _of_truncated",
}


def is_prime(n: int) -> bool:
    """Return whether ``n`` is prime, by deterministic trial division."""

    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    divisor = 3
    while divisor * divisor <= n:
        if n % divisor == 0:
            return False
        divisor += 2
    return True


def primes_up_to(limit: int) -> list[int]:
    return [n for n in range(2, limit + 1) if is_prime(n)]


def visible_coordinates(window: int, height: int) -> list[tuple[int, int]]:
    """Positive lattice points ``(a,b)`` in the window with ``a+b=height``."""

    return [
        (a, height - a)
        for a in range(1, window + 1)
        if 1 <= height - a <= window
    ]


def full_positive_fiber(height: int) -> list[tuple[int, int]]:
    return [(a, height - a) for a in range(1, height)]


def visible_cardinality(window: int, height: int) -> int:
    return len(visible_coordinates(window, height))


def _new_canvas(step: int) -> tuple[Figure, Axes, Axes]:
    fig = plt.figure(figsize=(14, 7.5), facecolor=PAPER)
    # 0.36·14 in = 0.672·7.5 in: both panels are physically square and equal.
    left = fig.add_axes((0.07, 0.19, 0.36, 0.672), facecolor=SURFACE)
    right = fig.add_axes((0.57, 0.19, 0.36, 0.672), facecolor=SURFACE)
    fig.text(0.07, 0.945, "MATH-VIZ-LAB · EXPERIMENT 02", color=ORANGE,
             fontsize=10, fontweight="bold")
    fig.text(0.07, 0.895, STEP_TITLES[step], color=INK, fontsize=18,
             fontweight="bold")
    fig.text(0.07, 0.115, STEP_NOTES[step], color=MUTED, fontsize=9.5)
    fig.text(0.07, 0.078, STEP_LOGIC[step], color=PURPLE, fontsize=9.5,
             fontweight="bold")
    fig.text(0.07, 0.042, STEP_LEAN[step], color=GREEN, fontsize=8.8,
             family="monospace")
    return fig, left, right


def _style_grid(ax: Axes, limit: int) -> None:
    ax.set_xlim(0.3, limit + 0.7)
    ax.set_ylim(0.3, limit + 0.7)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("erste Koordinate a", color=INK, fontweight="bold")
    ax.set_ylabel("zweite Koordinate b", color=INK, fontweight="bold")
    ax.set_xticks(range(1, limit + 1, max(1, limit // 8)))
    ax.set_yticks(range(1, limit + 1, max(1, limit // 8)))
    ax.grid(True, color=GRID, linewidth=0.7, alpha=0.8)
    ax.tick_params(colors=INK)
    for spine in ax.spines.values():
        spine.set_color(MUTED)


def _draw_step_1(left: Axes, right: Axes, window: int, selected: int,
                 *, compact: bool = False) -> None:
    display = min(window, 16)
    selected_view = max(2, min(selected, 2 * display))
    marker_size = 600 * (10 / display) ** 2 * (0.32 if compact else 1.0)
    aa, bb = np.meshgrid(np.arange(1, display + 1), np.arange(1, display + 1))
    heights = aa + bb
    scatter = left.scatter(aa.ravel(), bb.ravel(), c=heights.ravel(), cmap="viridis",
                           marker="s", s=marker_size, edgecolor=SURFACE, linewidth=0.6)
    chosen = visible_coordinates(display, selected_view)
    if chosen:
        x, y = zip(*chosen)
        left.scatter(x, y, facecolors="none", edgecolors=ORANGE, marker="s",
                     s=marker_size * 1.18, linewidth=1.8,
                     label=f"Faser h={selected_view}")
    _style_grid(left, display)
    left.set_title("Höhenfeld h(a,b)=a+b", color=INK, fontweight="bold")
    left.legend(loc="upper left", frameon=True, facecolor=SURFACE,
                fontsize=7 if compact else 10)
    if compact:
        left.text(0.98, 0.03, "Farbe = Höhe h=a+b", transform=left.transAxes,
                  ha="right", color=INK, fontsize=6.5, fontweight="bold")
    else:
        color_axis = left.inset_axes([0.91, 0.08, 0.035, 0.40])
        colorbar = left.figure.colorbar(scatter, cax=color_axis)
        colorbar.set_label("Höhe h=a+b", color=INK)

    points_n: list[int] = []
    points_a: list[int] = []
    for a in range(1, display + 1):
        for b in range(1, display + 1):
            points_n.append(a + b)
            points_a.append(a)
    right.scatter(points_n, points_a, s=13 if compact else 34,
                  color=BLUE_SOFT, edgecolor=BLUE,
                  linewidth=0.7, label="transformierter Gitterpunkt")
    fiber_a = [a for a, _ in chosen]
    right.scatter([selected_view] * len(fiber_a), fiber_a,
                  s=38 if compact else 90, color=ORANGE, edgecolor=SURFACE, linewidth=1.5,
                  label="πₕ-Faser")
    right.axvline(selected_view, color=ORANGE, linestyle="--", linewidth=1.5)
    right.set_xlim(1, 2 * display + 1)
    right.set_ylim(0.3, display + 0.7)
    right.set_xlabel("projizierte Höhe n=a+b", color=INK, fontweight="bold")
    right.set_ylabel("verbleibende Faserkoordinate a", color=INK, fontweight="bold")
    right.set_title("Koordinatenwechsel (a,b) ↦ (n,a)", color=INK, fontweight="bold")
    right.grid(True, color=GRID, linewidth=0.7, alpha=0.8)
    right.legend(loc="upper right", frameon=True, facecolor=SURFACE,
                 fontsize=7 if compact else 10)


def _draw_step_2(left: Axes, right: Axes, window: int, *, compact: bool = False) -> None:
    values = range(1, window + 1)
    composite_x: list[int] = []
    composite_y: list[int] = []
    prime_x: list[int] = []
    prime_y: list[int] = []
    for a in values:
        for b in values:
            target = (prime_x, prime_y) if is_prime(a + b) else (composite_x, composite_y)
            target[0].append(a)
            target[1].append(b)
    marker_size = 42 if compact else 105
    left.scatter(composite_x, composite_y, marker="s", s=marker_size, color=BLUE_SOFT,
                 edgecolor=SURFACE, linewidth=0.4, label="zusammengesetzte Höhe")
    left.scatter(prime_x, prime_y, marker="s", s=marker_size, color=ORANGE,
                 edgecolor=SURFACE, linewidth=0.4, label="Primhöhe")
    _style_grid(left, window)
    left.set_title(f"Primhöhen im Fenster 1≤a,b≤{window}", color=INK, fontweight="bold")
    left.legend(loc="upper right", frameon=True, facecolor=SURFACE,
                fontsize=6.5 if compact else 10)

    heights = np.arange(2, 2 * window + 1)
    indicator = np.array([1 if is_prime(int(n)) else 0 for n in heights])
    colors = [ORANGE if value else BLUE_SOFT for value in indicator]
    right.vlines(heights, 0, indicator, colors=colors, linewidth=2.0)
    right.scatter(heights, indicator, c=colors, edgecolors=INK, linewidth=0.4, s=42)
    for prime in primes_up_to(2 * window):
        right.annotate(str(prime), (prime, 1), xytext=(0, 8), textcoords="offset points",
                       ha="center", color=ORANGE, fontsize=6 if compact else 8,
                       fontweight="bold")
    right.set_xlim(1, 2 * window + 1)
    right.set_ylim(-0.08, 1.22)
    right.set_yticks([0, 1], labels=["nein", "ja"])
    right.set_xlabel("Höhenindex n", color=INK, fontweight="bold")
    right.set_ylabel("Ist n prim?", color=INK, fontweight="bold")
    right.set_title("Projizierte Primzahlverteilung", color=INK, fontweight="bold")
    right.grid(True, axis="x", color=GRID, linewidth=0.7, alpha=0.8)
    right.legend(handles=[Patch(color=ORANGE, label="Primzahl n"),
                          Patch(color=BLUE_SOFT, label="zusammengesetztes n")],
                 loc="lower right", frameon=True, facecolor=SURFACE,
                 fontsize=6.5 if compact else 10)


def _draw_step_3(left: Axes, right: Axes, p: int, q: int,
                 *, compact: bool = False) -> None:
    upper = q + 2
    a = np.linspace(0, upper, 400)
    left.plot(a, p - a, color=ORANGE, linewidth=3, label=f"Primhöhenband a+b={p}")
    left.plot(a, q - a, color=PURPLE, linewidth=3, label=f"Primhöhenband a+b={q}")
    p_points = full_positive_fiber(p)
    q_points = full_positive_fiber(q)
    point_size = 25 if compact else 58
    left.scatter(*zip(*p_points), color=ORANGE, edgecolor=SURFACE, s=point_size, zorder=4)
    left.scatter(*zip(*q_points), color=PURPLE, edgecolor=SURFACE, s=point_size, zorder=4)
    midpoint_p = np.array([p / 2, p / 2])
    midpoint_q = np.array([q / 2, q / 2])
    left.annotate("", xy=midpoint_q, xytext=midpoint_p,
                  arrowprops=dict(arrowstyle="<->", color=INK, linewidth=2.0))
    distance = (q - p) / math.sqrt(2)
    label_point = (midpoint_p + midpoint_q) / 2
    left.annotate(f"senkrecht: (q−p)/√2 = {distance:.3f}", label_point,
                  xytext=(32, 16), textcoords="offset points", color=INK,
                  fontsize=7 if compact else 10, fontweight="bold",
                  arrowprops=dict(arrowstyle="-", color=INK))
    left.set_xlim(0, upper)
    left.set_ylim(0, upper)
    left.set_aspect("equal", adjustable="box")
    left.set_xlabel("erste Koordinate a", color=INK, fontweight="bold")
    left.set_ylabel("zweite Koordinate b", color=INK, fontweight="bold")
    left.set_title("Parallele Fasern im (a,b)-Raum", color=INK, fontweight="bold")
    left.grid(True, color=GRID, linewidth=0.7)
    left.legend(loc="upper right", frameon=True, facecolor=SURFACE,
                fontsize=6.5 if compact else 10)

    indices = list(range(p - 3, q + 4))
    prime_flags = [is_prime(n) for n in indices]
    right.axhline(0, color=INK, linewidth=1.2)
    right.scatter(indices, [0] * len(indices),
                  c=[ORANGE if flag else BLUE_SOFT for flag in prime_flags],
                  edgecolor=INK, s=100, zorder=3)
    for n, flag in zip(indices, prime_flags):
        right.annotate(str(n), (n, 0), xytext=(0, -24), textcoords="offset points",
                       ha="center", color=ORANGE if flag else MUTED,
                       fontweight="bold" if flag else "normal")
    right.annotate("", xy=(q, 0.48), xytext=(p, 0.48),
                   arrowprops=dict(arrowstyle="<->", color=PURPLE, linewidth=2.4))
    right.text((p + q) / 2, 0.58, f"bandGap({p},{q})={q-p}", ha="center",
               color=PURPLE, fontsize=7 if compact else 10, fontweight="bold")
    separators = max(0, q - p - 1)
    right.text((p + q) / 2, -0.58, f"{separators} Zwischenband: n={p+1}",
               ha="center", color=MUTED, fontsize=7 if compact else 10,
               fontweight="bold")
    right.set_xlim(indices[0] - 0.7, indices[-1] + 0.7)
    right.set_ylim(-0.85, 0.9)
    right.set_yticks([0], labels=["Höhenband"])
    right.set_xlabel("ganzzahliger Höhenindex n", color=INK, fontweight="bold")
    right.set_ylabel("Bandmarker", color=INK, fontweight="bold")
    right.set_title("Primzahllücke als Indexgeometrie", color=INK, fontweight="bold")
    right.grid(True, axis="x", color=GRID, linewidth=0.7)
    right.legend(handles=[Line2D([], [], marker="o", linestyle="", color=ORANGE,
                                 markeredgecolor=INK, label="Primhöhe"),
                          Line2D([], [], marker="o", linestyle="", color=BLUE_SOFT,
                                 markeredgecolor=INK, label="Zwischenband")],
                 loc="upper right", frameon=True, facecolor=SURFACE,
                 fontsize=6.5 if compact else 10)


def _draw_step_4(left: Axes, right: Axes, window: int, selected: int,
                 *, compact: bool = False) -> None:
    heights = np.arange(2, 2 * window + 1)
    counts = np.array([visible_cardinality(window, int(n)) for n in heights])
    left.plot(heights, counts, color=BLUE, linewidth=2.8, marker="o", markersize=3,
              label="sichtbare Fasergröße C_N(n)")
    left.axvspan(2, window + 1, color=GREEN, alpha=0.10,
                 label="vollständige Fasern")
    left.axvspan(window + 1, 2 * window, color=ORANGE, alpha=0.10,
                 label="abgeschnittene Fasern")
    left.axvline(window + 1, color=INK, linestyle="--", linewidth=1.5,
                 label=f"Schwelle N+1={window+1}")
    chosen_count = visible_cardinality(window, selected)
    left.scatter([selected], [chosen_count], color=PURPLE, s=100, zorder=5)
    left.annotate(f"C_{window}({selected})={chosen_count}", (selected, chosen_count),
                  xytext=(12, -25), textcoords="offset points", color=PURPLE,
                  fontweight="bold")
    left.set_xlim(1, 2 * window + 1)
    left.set_ylim(0, window + 1)
    left.set_xlabel("Höhenindex n", color=INK, fontweight="bold")
    left.set_ylabel("Anzahl sichtbarer Faserpunkte C_N(n)", color=INK, fontweight="bold")
    left.set_title("Fensterbedingte Dreiecksform", color=INK, fontweight="bold")
    left.grid(True, color=GRID, linewidth=0.7)
    left.legend(loc="upper right", frameon=True, facecolor=SURFACE,
                fontsize=6 if compact else 8)

    full = full_positive_fiber(selected)
    visible = set(visible_coordinates(window, selected))
    hidden = [point for point in full if point not in visible]
    right.add_patch(Rectangle((0.5, 0.5), window, window, facecolor=GREEN,
                              edgecolor=GREEN, alpha=0.08, linewidth=2,
                              label=f"Beobachtungsfenster N={window}"))
    if hidden:
        right.scatter(*zip(*hidden), facecolors="none", edgecolors=MUTED,
                      s=32 if compact else 70,
                      linewidth=1.5, label="außerhalb: nicht sichtbar")
    if visible:
        right.scatter(*zip(*sorted(visible)), color=PURPLE, edgecolor=SURFACE,
                      s=34 if compact else 75, linewidth=1.0,
                      label="sichtbare Faserpunkte")
    max_axis = max(window, selected - 1) + 1
    right.set_xlim(0, max_axis)
    right.set_ylim(0, max_axis)
    right.set_aspect("equal", adjustable="box")
    right.set_xlabel("erste Koordinate a", color=INK, fontweight="bold")
    right.set_ylabel("zweite Koordinate b", color=INK, fontweight="bold")
    right.set_title(f"Volle Faser a+b={selected} versus Fenster", color=INK,
                    fontweight="bold")
    right.grid(True, color=GRID, linewidth=0.7)
    right.legend(loc="upper right", frameon=True, facecolor=SURFACE,
                 fontsize=6 if compact else 8)


def create_static_figure(step: int, *, window: int = 16, selected: int = 19,
                         p: int = 11, q: int = 13) -> tuple[Figure, tuple[Axes, Axes]]:
    """Create one fully labelled two-panel research figure."""

    if step not in STEP_TITLES:
        raise ValueError("step must be between 1 and 4")
    if window < 3:
        raise ValueError("window must be at least 3")
    fig, left, right = _new_canvas(step)
    if step == 1:
        _draw_step_1(left, right, window, selected)
    elif step == 2:
        _draw_step_2(left, right, window)
    elif step == 3:
        _draw_step_3(left, right, p, q)
    else:
        _draw_step_4(left, right, window, selected)
    return fig, (left, right)


def export_figures(output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    settings = {
        1: {"selected": 11},
        2: {},
        3: {"p": 11, "q": 13},
        4: {"selected": 19},
    }
    for step in range(1, 5):
        fig, _ = create_static_figure(step, **settings[step])
        target = output_dir / f"experiment-02-step-{step}.svg"
        fig.savefig(target, format="svg", facecolor=fig.get_facecolor(),
                    metadata={"Date": None})
        # Matplotlib emits harmless trailing spaces inside SVG path data. Remove
        # them so generated artifacts also pass the repository whitespace check.
        normalized = "\n".join(
            line.rstrip() for line in target.read_text(encoding="utf-8").splitlines()
        ) + "\n"
        target.write_bytes(normalized.encode("utf-8"))
        plt.close(fig)
        print(f"exported {target}")


class InteractiveOverview:
    """One native window showing all projection steps with shared controls."""

    def __init__(self, *, window: int = 16, height: int = 19) -> None:
        window = max(8, min(30, window))
        height = max(2, min(2 * window, height))
        self.fig = plt.figure(figsize=(18, 10.5), facecolor=PAPER)
        self.fig.canvas.manager.set_window_title(
            "math-viz-lab · Interaktive Primhöhen-Geometrie"
        )
        self.fig.text(0.04, 0.974, "PRIMHÖHEN-GEOMETRIE · ALLE PROJEKTIONSSCHRITTE",
                      color=INK, fontsize=20, fontweight="bold", va="top")
        self.fig.text(
            0.04, 0.937,
            "Gemeinsame Regler koppeln Gitter, Primzahlfilter, Lückenmetrik und Fensterfaser.",
            color=MUTED, fontsize=10.5, va="top",
        )

        specs = {
            1: (0.04, 0.265, 0.58, 0.895),
            2: (0.535, 0.76, 0.58, 0.895),
            3: (0.04, 0.265, 0.17, 0.485),
            4: (0.535, 0.76, 0.17, 0.485),
        }
        short_titles = {
            1: "Schritt 1 · Höhenprojektion und Faser",
            2: "Schritt 2 · Primzahlfilter",
            3: "Schritt 3 · Primzahllücke und Distanz",
            4: "Schritt 4 · Endliches Fenster",
        }
        self.panels: dict[int, tuple[Axes, Axes]] = {}
        for step, (left_x, right_x, bottom, title_y) in specs.items():
            left = self.fig.add_axes((left_x, bottom, 0.17, 0.29), facecolor=SURFACE)
            right = self.fig.add_axes((right_x, bottom, 0.17, 0.29), facecolor=SURFACE)
            self.panels[step] = (left, right)
            self.fig.text(left_x, title_y, short_titles[step], color=INK,
                          fontsize=12, fontweight="bold")

        slider_color = ORANGE_SOFT
        self.window_slider = Slider(
            self.fig.add_axes((0.08, 0.065, 0.20, 0.020), facecolor=SURFACE),
            "Fenster N", 8, 30, valinit=window, valstep=1, color=slider_color,
        )
        self.height_slider = Slider(
            self.fig.add_axes((0.38, 0.065, 0.20, 0.020), facecolor=SURFACE),
            "Höhe n", 2, 2 * window, valinit=height, valstep=1, color=slider_color,
        )
        self.prime_pairs = list(zip(primes_up_to(100), primes_up_to(100)[1:]))
        self.pair_slider = Slider(
            self.fig.add_axes((0.68, 0.065, 0.16, 0.020), facecolor=SURFACE),
            "Primzahlpaar", 0, len(self.prime_pairs) - 1, valinit=4, valstep=1,
            valfmt="Index %0.0f", color=slider_color,
        )
        self.export_button = Button(
            self.fig.add_axes((0.88, 0.048, 0.09, 0.05)), "SVG-Export",
            color=SURFACE, hovercolor=ORANGE_SOFT,
        )
        self.status = self.fig.text(0.50, 0.515, "", ha="center", color=PURPLE,
                                    fontsize=9.5, fontweight="bold")

        self.window_slider.on_changed(self._on_change)
        self.height_slider.on_changed(self._on_change)
        self.pair_slider.on_changed(self._on_change)
        self.export_button.on_clicked(self._on_export)
        self._redraw()

    def _on_change(self, _value: float) -> None:
        window = int(self.window_slider.val)
        max_height = 2 * window
        self.height_slider.valmax = max_height
        self.height_slider.ax.set_xlim(self.height_slider.valmin, max_height)
        if self.height_slider.val > max_height:
            self.height_slider.set_val(max_height)
            return
        self._redraw()

    def _on_export(self, _event: object) -> None:
        export_figures(EXPERIMENT_DIR / "renders")
        self.status.set_text("Vier deterministische SVGs wurden neu erzeugt.")
        self.fig.canvas.draw_idle()

    def _redraw(self) -> None:
        window = int(self.window_slider.val)
        selected = int(self.height_slider.val)
        pair_index = int(self.pair_slider.val)
        p, q = self.prime_pairs[pair_index]
        for left, right in self.panels.values():
            left.clear()
            right.clear()

        _draw_step_1(*self.panels[1], window, selected, compact=True)
        _draw_step_2(*self.panels[2], window, compact=True)
        _draw_step_3(*self.panels[3], p, q, compact=True)
        _draw_step_4(*self.panels[4], window, selected, compact=True)

        for left, right in self.panels.values():
            for axis in (left, right):
                axis.title.set_fontsize(9)
                axis.xaxis.label.set_fontsize(8)
                axis.yaxis.label.set_fontsize(8)
                axis.tick_params(labelsize=7)
        self.status.set_text(
            f"Aktiver Zustand: N={window}, n={selected}, Primzahlpaar ({p},{q}) · "
            "Reglerzustand ist explorativ; YAML-Zustände bleiben maßgeblich."
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
                        help="show only one detailed step instead of the overview")
    parser.add_argument("--window", type=int, default=16, help="positive grid window size")
    parser.add_argument("--height", type=int, default=19,
                        help="selected height for a detailed view")
    parser.add_argument("--output", type=Path, default=EXPERIMENT_DIR / "renders")
    args = parser.parse_args()
    if args.export:
        export_figures(args.output)
    elif args.check_layout:
        check_layout()
    elif args.step is None:
        InteractiveOverview(window=args.window, height=args.height).show()
    else:
        fig, _ = create_static_figure(
            args.step,
            window=args.window,
            selected=args.height,
            p=11,
            q=13,
        )
        fig.canvas.manager.set_window_title("math-viz-lab · Primhöhen-Geometrie")
        plt.show()


if __name__ == "__main__":
    main()
