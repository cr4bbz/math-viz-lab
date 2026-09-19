"""Native visual research lab for the Riemann hypothesis.

The default command opens five coupled projections. Static SVGs are generated
with ``--export``. Numerical plots are finite evidence, never a proof of RH.
"""

from __future__ import annotations

import argparse
from functools import lru_cache
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
import mpmath as mp
import numpy as np

mp.mp.dps = 30
matplotlib.rcParams["svg.hashsalt"] = "math-viz-lab-riemann-hypothesis"

EXPERIMENT_DIR = Path(__file__).resolve().parent

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
RED = "#a9473b"
PALE_ORANGE = "#fae3d5"
PALE_GREEN = "#d8eee5"
PALE_PURPLE = "#e8e0f5"

STEP_TITLES = {
    1: "1 · Dirichlet-Reihe: Sichere Halbebene Re(s)>1",
    2: "2 · Analytische Fortsetzung: Pole, triviale Nullstellen, Streifen",
    3: "3 · Betragsprojektion: Täler von log₁₀|ζ(σ+it)|",
    4: "4 · Kritische Gerade: Hardy-Z-Funktion und Nullstellenhöhen",
    5: "5 · Evidenzgrenze: Endliche Treffer sind kein universeller Beweis",
}

STEP_NOTES = {
    1: "Nur für Re(s)>1 stimmt ζ(s) mit der naiven Reihe Σn⁻ˢ überein; gezeigt wird s=2+it.",
    2: "Analytische Fortsetzung erweitert ζ über die Reihendomäne hinaus; s=1 bleibt ein Pol.",
    3: "Die Betragsprojektion macht Nullstellen als dunkle Täler sichtbar, verwirft aber die komplexe Phase.",
    4: "Auf Re(s)=1/2 ist Hardy Z(t) reell; Vorzeichenwechsel lokalisieren Nullstellen auf dieser Geraden.",
    5: "Die aufgeführten Nullstellen liegen numerisch auf Re(s)=1/2; RH quantifiziert über alle nichttrivialen Nullstellen.",
}

STEP_LOGIC = {
    1: "Logik: Re(s)>1 ⇒ ζ(s)=Σ_{n≥1}n⁻ˢ",
    2: "Logik: ζ(−2m)=0; Re(s)≥1 ⇒ ζ(s)≠0; s=1 ist Pol",
    3: "Logik: ζ(s)=0 ⇒ |ζ(s)|=0; Umkehrung gilt, aber die Phase geht verloren",
    4: "Logik: s(t)=1/2+it liegt auf der kritischen Geraden",
    5: "Offene Vermutung: jede nichttriviale Nullstelle ρ erfüllt Re(ρ)=1/2",
}

STEP_LEAN = {
    1: "Lean/mathlib: zeta_eq_tsum_one_div_nat_add_one_cpow",
    2: "Lean: negative_even_is_zeta_zero / zeta_nonzero_of_one_le_re",
    3: "Lean: compact_inter_zetaZeros_finite; Grafik = numerical_evidence",
    4: "Lean: criticalLinePoint_on_line; Nullstellenwerte numerisch",
    5: "Lean: riemannHypothesis_iff_nontrivial_zeros_on_line; Status = open conjecture",
}


def zeta_value(sigma: float, height: float) -> complex:
    return complex(mp.zeta(mp.mpc(sigma, height)))


def dirichlet_partial_sums(cutoff: int, height: float,
                           sigma: float = 2.0) -> np.ndarray:
    if cutoff < 1:
        raise ValueError("cutoff must be positive")
    n = np.arange(1, cutoff + 1, dtype=float)
    terms = np.exp(-(sigma + 1j * height) * np.log(n))
    return np.cumsum(terms)


@lru_cache(maxsize=8)
def known_zero_heights(count: int) -> tuple[float, ...]:
    if count < 1:
        raise ValueError("count must be positive")
    return tuple(float(mp.im(mp.zetazero(k))) for k in range(1, count + 1))


@lru_cache(maxsize=1)
def critical_strip_grid() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    sigmas = np.linspace(0.0, 1.0, 61)
    heights = np.linspace(0.0, 35.0, 141)
    values = np.empty((len(heights), len(sigmas)), dtype=float)
    for row, height in enumerate(heights):
        for col, sigma in enumerate(sigmas):
            try:
                magnitude = abs(mp.zeta(mp.mpc(float(sigma), float(height))))
                values[row, col] = math.log10(max(float(magnitude), 1e-5))
            except ValueError:
                values[row, col] = 2.0
    return sigmas, heights, np.clip(values, -3.0, 2.0)


@lru_cache(maxsize=1)
def hardy_curve() -> tuple[np.ndarray, np.ndarray]:
    heights = np.linspace(0.0, 35.0, 501)
    values = np.array([float(mp.siegelz(float(t))) for t in heights])
    return heights, values


@lru_cache(maxsize=1)
def real_axis_zeta() -> tuple[np.ndarray, np.ndarray]:
    left = np.linspace(-8.0, 0.96, 360)
    right = np.linspace(1.04, 3.0, 120)
    x = np.concatenate([left, [np.nan], right])
    y = []
    for value in x:
        if np.isnan(value):
            y.append(np.nan)
        else:
            y.append(float(mp.re(mp.zeta(float(value)))))
    return x, np.clip(np.array(y), -6.0, 6.0)


def _style(ax: Axes, xlabel: str, ylabel: str) -> None:
    ax.set_xlabel(xlabel, color=INK, fontweight="bold")
    ax.set_ylabel(ylabel, color=INK, fontweight="bold")
    ax.grid(True, color=GRID, linewidth=0.7, alpha=0.7)
    ax.tick_params(colors=INK)
    for spine in ax.spines.values():
        spine.set_color(MUTED)


def _new_canvas(step: int) -> tuple[Figure, Axes, Axes]:
    fig = plt.figure(figsize=(14, 7.5), facecolor=PAPER)
    left = fig.add_axes((0.07, 0.19, 0.36, 0.672), facecolor=SURFACE)
    right = fig.add_axes((0.57, 0.19, 0.36, 0.672), facecolor=SURFACE)
    fig.text(0.07, 0.945, "MATH-VIZ-LAB · EXPERIMENT 05",
             color=ORANGE, fontsize=10, fontweight="bold")
    fig.text(0.07, 0.895, STEP_TITLES[step], color=INK, fontsize=18,
             fontweight="bold")
    fig.text(0.07, 0.115, STEP_NOTES[step], color=MUTED, fontsize=9.2)
    fig.text(0.07, 0.078, STEP_LOGIC[step], color=PURPLE, fontsize=9.2,
             fontweight="bold")
    fig.text(0.07, 0.042, STEP_LEAN[step], color=GREEN, fontsize=8.5,
             family="monospace")
    return fig, left, right


def _draw_step_1(left: Axes, right: Axes, cutoff: int, height: float,
                 *, compact: bool = False) -> None:
    sums = dirichlet_partial_sums(cutoff, height)
    target = zeta_value(2.0, height)
    left.plot(sums.real, sums.imag, color=BLUE, linewidth=1.8,
              label="Pfad der Partialsummen")
    left.scatter([sums[0].real], [sums[0].imag], color=ORANGE,
                 edgecolor=INK, s=30 if compact else 65, label="Start n=1")
    left.scatter([sums[-1].real], [sums[-1].imag], color=PURPLE,
                 edgecolor=INK, s=35 if compact else 80, label=f"S_{cutoff}")
    left.scatter([target.real], [target.imag], marker="*", color=GREEN,
                 edgecolor=INK, s=70 if compact else 150, label="ζ(2+it)")
    _style(left, "Realteil der Partialsumme", "Imaginärteil der Partialsumme")
    left.set_title(f"Komplexer Summenpfad bei s=2+{height:.2f}i",
                   color=INK, fontweight="bold")
    left.legend(loc="best", frameon=True, facecolor=SURFACE,
                fontsize=6 if compact else 8.5)

    indices = np.arange(1, cutoff + 1)
    errors = np.abs(sums - target)
    right.loglog(indices, errors, color=PURPLE, linewidth=2.2,
                 label="|S_N−ζ(2+it)|")
    right.loglog(indices, 1.0 / indices, color=ORANGE, linestyle="--",
                 linewidth=1.6, label="Vergleich 1/N")
    _style(right, "Summengrenze N (log)", "Näherungsfehler (log)")
    right.set_title("Konvergenz in der sicheren Halbebene", color=INK,
                    fontweight="bold")
    right.legend(loc="lower left", frameon=True, facecolor=SURFACE,
                 fontsize=6.5 if compact else 9)


def _draw_step_2(left: Axes, right: Axes, *, compact: bool = False) -> None:
    x, y = real_axis_zeta()
    left.plot(x, y, color=BLUE, linewidth=2.0, label="analytisch fortgesetztes ζ(x)")
    trivial = np.array([-2, -4, -6, -8])
    left.scatter(trivial, np.zeros_like(trivial), color=ORANGE, edgecolor=INK,
                 s=28 if compact else 65, zorder=4, label="triviale Nullstellen −2m")
    left.axvline(1, color=RED, linestyle="--", linewidth=2,
                 label="Pol bei s=1")
    left.axhline(0, color=INK, linewidth=1)
    left.set_xlim(-8.2, 3.1)
    left.set_ylim(-6.2, 6.2)
    _style(left, "reelles Argument x", "ζ(x), auf [−6,6] beschnitten")
    left.set_title("Reelle Spur der analytischen Fortsetzung", color=INK,
                   fontweight="bold")
    left.legend(loc="lower right", frameon=True, facecolor=SURFACE,
                fontsize=6 if compact else 8.5)

    right.axvspan(0, 1, color=PALE_PURPLE, alpha=0.9,
                  label="kritischer Streifen 0<σ<1")
    right.axvspan(1, 3, color=PALE_GREEN, alpha=0.75,
                  label="nullstellenfrei: σ≥1")
    right.axvline(0.5, color=PURPLE, linewidth=2.4,
                  label="kritische Gerade σ=1/2")
    right.axvline(1, color=RED, linestyle="--", linewidth=1.8,
                  label="Pol s=1")
    right.scatter(trivial, np.zeros_like(trivial), color=ORANGE, edgecolor=INK,
                  s=25 if compact else 55, zorder=4, label="triviale Nullstellen")
    right.set_xlim(-8.2, 3.0)
    right.set_ylim(-8, 8)
    _style(right, "σ=Re(s)", "t=Im(s)")
    right.set_title("Strukturkarte der komplexen Ebene", color=INK,
                    fontweight="bold")
    right.legend(loc="upper left", frameon=True, facecolor=SURFACE,
                 fontsize=5.5 if compact else 8)


def _draw_step_3(left: Axes, right: Axes, height: float,
                 *, compact: bool = False) -> None:
    sigmas, heights, values = critical_strip_grid()
    levels = np.array([-3, -2, -1, 0, 1, 2], dtype=float)
    left.contourf(sigmas, heights, values, levels=levels, cmap="magma")
    lines = left.contour(sigmas, heights, values, levels=levels[:-1],
                         colors="white", linewidths=0.35, alpha=0.65)
    left.clabel(lines, inline=True, fontsize=4.5 if compact else 7,
                fmt=lambda level: f"{level:g}")
    left.axvline(0.5, color=GREEN, linewidth=2.0,
                 label="kritische Gerade σ=1/2")
    left.axhline(height, color=BLUE, linestyle="--", linewidth=1.4,
                 label=f"Querschnitt t={height:.2f}")
    _style(left, "σ=Re(s)", "t=Im(s)")
    left.set_title("Konturen von log₁₀|ζ(σ+it)|", color=INK,
                   fontweight="bold")
    left.legend(loc="upper right", frameon=True, facecolor=SURFACE,
                fontsize=5.5 if compact else 8)

    scan_sigma = np.linspace(0.0, 1.0, 161)
    scan = np.array([
        math.log10(max(abs(zeta_value(float(sigma), height)), 1e-8))
        for sigma in scan_sigma
    ])
    minimum_index = int(np.argmin(scan))
    minimum_sigma = float(scan_sigma[minimum_index])
    right.plot(scan_sigma, scan, color=BLUE, linewidth=2.2,
               label=f"log₁₀|ζ(σ+{height:.2f}i)|")
    right.axvline(0.5, color=PURPLE, linestyle="--", linewidth=1.8,
                  label="σ=1/2")
    right.scatter([minimum_sigma], [scan[minimum_index]], color=ORANGE,
                  edgecolor=INK, s=35 if compact else 75, zorder=4,
                  label=f"Rasterminimum σ≈{minimum_sigma:.3f}")
    _style(right, "σ=Re(s)", "log₁₀|ζ(σ+it)|")
    right.set_title("Horizontaler Querschnitt durch den Streifen", color=INK,
                    fontweight="bold")
    right.legend(loc="best", frameon=True, facecolor=SURFACE,
                 fontsize=5.5 if compact else 8)


def _draw_step_4(left: Axes, right: Axes, zero_count: int,
                 *, compact: bool = False) -> None:
    heights, values = hardy_curve()
    zeros = np.array(known_zero_heights(zero_count))
    left.plot(heights, values, color=BLUE, linewidth=1.8, label="Hardy Z(t)")
    left.axhline(0, color=INK, linewidth=1)
    for index, zero in enumerate(zeros):
        left.axvline(zero, color=ORANGE, alpha=0.55, linewidth=1.1,
                     label="aufgelistete Nullstellen" if index == 0 else None)
    left.set_xlim(0, 35)
    _style(left, "Höhe t auf s=1/2+it", "Hardy Z(t), reell")
    left.set_title("Vorzeichenwechsel auf der kritischen Geraden", color=INK,
                   fontweight="bold")
    left.legend(loc="upper left", frameon=True, facecolor=SURFACE,
                fontsize=6 if compact else 8.5)

    indices = np.arange(1, zero_count + 1)
    right.plot(indices, zeros, color=PURPLE, marker="o", markerfacecolor=ORANGE,
               markeredgecolor=INK, linewidth=1.8, label="γ_k mit ρ_k=1/2+iγ_k")
    for index, zero in zip(indices, zeros):
        right.text(index, zero + 0.4, f"{zero:.3f}", ha="center", color=INK,
                   fontsize=5 if compact else 7)
    right.set_xticks(indices)
    _style(right, "Nullstellenindex k", "Höhe γ_k")
    right.set_title(f"Die ersten {zero_count} aufgelisteten Höhen", color=INK,
                    fontweight="bold")
    right.legend(loc="upper left", frameon=True, facecolor=SURFACE,
                 fontsize=6 if compact else 8.5)


def _draw_step_5(left: Axes, right: Axes, zero_count: int,
                 *, compact: bool = False) -> None:
    zeros = np.array(known_zero_heights(zero_count))
    signed = np.concatenate([-zeros[::-1], zeros])
    sigma = np.full_like(signed, 0.5)
    left.axvspan(0, 1, color=PALE_PURPLE, alpha=0.85,
                 label="kritischer Streifen")
    left.axvline(0.5, color=PURPLE, linewidth=2.2,
                 label="kritische Gerade")
    left.scatter(sigma, signed, color=ORANGE, edgecolor=INK,
                 s=28 if compact else 65, zorder=4,
                 label=f"± erste {zero_count} gelistete Nullstellen")
    left.set_xlim(-0.05, 1.05)
    bound = max(18.0, float(zeros[-1]) + 2)
    left.set_ylim(-bound, bound)
    _style(left, "σ=Re(ρ)", "t=Im(ρ)")
    left.set_title("Endliche numerische Auswahl", color=INK,
                   fontweight="bold")
    left.legend(loc="upper right", frameon=True, facecolor=SURFACE,
                fontsize=5.5 if compact else 8)
    left.text(0.03, 0.03, "Keine Suche nach allen Nullstellen im Streifen",
              transform=left.transAxes, color=RED,
              fontsize=6 if compact else 8.5, fontweight="bold")

    right.set_axis_off()
    boxes = [
        (0.08, 0.68, 0.84, 0.20, PALE_GREEN,
         "Bewiesen", "ζ hat triviale Nullstellen; rechts von σ=1 keine Nullstellen"),
        (0.08, 0.39, 0.84, 0.20, PALE_ORANGE,
         "Numerische Evidenz", f"Die {zero_count} gelisteten Nullstellen liegen auf σ=1/2"),
        (0.08, 0.10, 0.84, 0.20, PALE_PURPLE,
         "Offene Vermutung", "ALLE nichttrivialen Nullstellen liegen auf σ=1/2"),
    ]
    for x0, y0, width, height_box, color, heading, text in boxes:
        right.add_patch(Rectangle((x0, y0), width, height_box,
                                  transform=right.transAxes, facecolor=color,
                                  edgecolor=INK, linewidth=1.4))
        right.text(x0 + 0.03, y0 + height_box * 0.68, heading,
                   transform=right.transAxes, color=INK,
                   fontsize=7 if compact else 10, fontweight="bold")
        right.text(x0 + 0.03, y0 + height_box * 0.30, text,
                   transform=right.transAxes, color=MUTED,
                   fontsize=5.5 if compact else 8.2)
    right.annotate("Quantorwechsel: endlich → alle", xy=(0.5, 0.305),
                   xytext=(0.5, 0.335), xycoords="axes fraction",
                   textcoords="axes fraction", ha="center", color=RED,
                   fontsize=5 if compact else 8, fontweight="bold",
                   arrowprops=dict(arrowstyle="->", color=RED, linewidth=1.5))
    right.set_title("Beweisstatus statt Bildüberdehnung", color=INK,
                    fontweight="bold")


def create_static_figure(step: int, *, cutoff: int = 120,
                         height: float = 14.13, zero_count: int = 5
                         ) -> tuple[Figure, tuple[Axes, Axes]]:
    if step not in STEP_TITLES:
        raise ValueError("step must be between 1 and 5")
    if cutoff < 2:
        raise ValueError("cutoff must be at least 2")
    if not (0 <= height <= 35):
        raise ValueError("height must satisfy 0 <= t <= 35")
    if not (1 <= zero_count <= 10):
        raise ValueError("zero_count must satisfy 1 <= K <= 10")
    fig, left, right = _new_canvas(step)
    if step == 1:
        _draw_step_1(left, right, cutoff, height)
    elif step == 2:
        _draw_step_2(left, right)
    elif step == 3:
        _draw_step_3(left, right, height)
    elif step == 4:
        _draw_step_4(left, right, zero_count)
    else:
        _draw_step_5(left, right, zero_count)
    return fig, (left, right)


def export_figures(output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for step in range(1, 6):
        fig, _ = create_static_figure(step)
        target = output_dir / f"experiment-05-step-{step}.svg"
        fig.savefig(target, format="svg", facecolor=fig.get_facecolor(),
                    metadata={"Date": None})
        normalized = "\n".join(
            line.rstrip() for line in target.read_text(encoding="utf-8").splitlines()
        ) + "\n"
        target.write_bytes(normalized.encode("utf-8"))
        plt.close(fig)
        print(f"exported {target}")


class InteractiveOverview:
    """All five Riemann-zeta projections in one native dashboard."""

    def __init__(self, *, cutoff: int = 120, height: float = 14.13,
                 zero_count: int = 5) -> None:
        cutoff = max(20, min(300, cutoff))
        height = max(0.0, min(35.0, height))
        zero_count = max(1, min(10, zero_count))
        self.fig = plt.figure(figsize=(18, 13.5), facecolor=PAPER)
        self.fig.canvas.manager.set_window_title(
            "math-viz-lab · Riemannsche Vermutung"
        )
        self.fig.text(0.04, 0.982,
                      "RIEMANNSCHE VERMUTUNG · STRUKTUR, NULLSTELLEN, EVIDENZGRENZE",
                      color=INK, fontsize=20, fontweight="bold", va="top")
        self.fig.text(
            0.04, 0.954,
            "Alle Ansichten trennen bewiesene Zeta-Struktur, endliche Numerik und die offene universelle Behauptung.",
            color=MUTED, fontsize=10.5, va="top",
        )
        specs = {
            1: (0.04, 0.265, 0.69, 0.915),
            2: (0.535, 0.76, 0.69, 0.915),
            3: (0.04, 0.265, 0.405, 0.63),
            4: (0.535, 0.76, 0.405, 0.63),
            5: (0.2875, 0.5125, 0.12, 0.345),
        }
        short_titles = {
            1: "Schritt 1 · Dirichlet-Reihe",
            2: "Schritt 2 · Fortsetzung und Streifen",
            3: "Schritt 3 · Betragslandschaft",
            4: "Schritt 4 · Kritische Gerade",
            5: "Schritt 5 · Evidenz und Vermutung",
        }
        self.panels: dict[int, tuple[Axes, Axes]] = {}
        for step, (left_x, right_x, bottom, title_y) in specs.items():
            left = self.fig.add_axes((left_x, bottom, 0.17, 0.19), facecolor=SURFACE)
            right = self.fig.add_axes((right_x, bottom, 0.17, 0.19), facecolor=SURFACE)
            self.panels[step] = (left, right)
            self.fig.text(left_x, title_y, short_titles[step], color=INK,
                          fontsize=12, fontweight="bold")

        self.cutoff_slider = Slider(
            self.fig.add_axes((0.12, 0.035, 0.16, 0.015), facecolor=SURFACE),
            "Reihencutoff N", 20, 300, valinit=cutoff, valstep=10,
            color=PALE_ORANGE,
        )
        self.height_slider = Slider(
            self.fig.add_axes((0.39, 0.035, 0.16, 0.015), facecolor=SURFACE),
            "Höhe t", 0.0, 35.0, valinit=height, valstep=0.01,
            color=PALE_ORANGE,
        )
        self.zero_slider = Slider(
            self.fig.add_axes((0.66, 0.035, 0.12, 0.015), facecolor=SURFACE),
            "Nullstellen K", 1, 10, valinit=zero_count, valstep=1,
            color=PALE_ORANGE,
        )
        self.export_button = Button(
            self.fig.add_axes((0.86, 0.019, 0.11, 0.045)), "SVG-Export",
            color=SURFACE, hovercolor=PALE_ORANGE,
        )
        self.status = self.fig.text(0.50, 0.365, "", ha="center", color=PURPLE,
                                    fontsize=9.2, fontweight="bold")
        self.cutoff_slider.on_changed(self._on_change)
        self.height_slider.on_changed(self._on_change)
        self.zero_slider.on_changed(self._on_change)
        self.export_button.on_clicked(self._on_export)
        self._redraw()

    def _on_change(self, _value: float) -> None:
        self._redraw()

    def _on_export(self, _event: object) -> None:
        export_figures(EXPERIMENT_DIR / "renders")
        self.status.set_text("Fünf deterministische SVGs wurden neu erzeugt.")
        self.fig.canvas.draw_idle()

    def _redraw(self) -> None:
        cutoff = int(self.cutoff_slider.val)
        height = float(self.height_slider.val)
        zero_count = int(self.zero_slider.val)
        for left, right in self.panels.values():
            left.clear()
            right.clear()
        _draw_step_1(*self.panels[1], cutoff, height, compact=True)
        _draw_step_2(*self.panels[2], compact=True)
        _draw_step_3(*self.panels[3], height, compact=True)
        _draw_step_4(*self.panels[4], zero_count, compact=True)
        _draw_step_5(*self.panels[5], zero_count, compact=True)
        for left, right in self.panels.values():
            for axis in (left, right):
                axis.title.set_fontsize(9)
                axis.xaxis.label.set_fontsize(8)
                axis.yaxis.label.set_fontsize(8)
                axis.tick_params(labelsize=7)
        magnitude = abs(zeta_value(0.5, height))
        self.status.set_text(
            f"Aktiver Zustand: N={cutoff}, t={height:.2f}, K={zero_count} · "
            f"|ζ(1/2+it)|={magnitude:.3e} · RH bleibt offene Vermutung"
        )
        self.fig.canvas.draw_idle()

    def show(self) -> None:
        plt.show()


def check_layout() -> None:
    for step in range(1, 6):
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
    parser.add_argument("--step", type=int, choices=range(1, 6),
                        help="show only one detailed projection")
    parser.add_argument("--cutoff", type=int, default=120, help="Dirichlet cutoff N")
    parser.add_argument("--height", type=float, default=14.13, help="selected height t")
    parser.add_argument("--zeros", type=int, default=5, help="listed zero count K")
    parser.add_argument("--output", type=Path, default=EXPERIMENT_DIR / "renders")
    args = parser.parse_args()
    if args.export:
        export_figures(args.output)
    elif args.check_layout:
        check_layout()
    elif args.step is None:
        InteractiveOverview(cutoff=args.cutoff, height=args.height,
                            zero_count=args.zeros).show()
    else:
        fig, _ = create_static_figure(args.step, cutoff=args.cutoff,
                                      height=args.height, zero_count=args.zeros)
        fig.canvas.manager.set_window_title(
            "math-viz-lab · Riemannsche Vermutung"
        )
        plt.show()


if __name__ == "__main__":
    main()
