# math-viz-lab

Ein Labor für **grafische Matheforschung**, **mathematik-didaktische Begleitung**
und **maschinell geprüfte Formulierungen in Lean**.

## Experiment 01: Projektionen und Fasern der kubischen Familie

Wir untersuchen

\[
F(a,x)=x^3-a x=x(x^2-a)
\]

als Funktion auf dem Parameter-Zustands-Raum \(\mathbb R^2\). Das Experiment
führt in vier aufeinander aufbauenden Ansichten vom Vorzeichenfeld zur
Nullstellenmenge

\[
V=\{(a,x)\in\mathbb R^2\mid F(a,x)=0\}
\]

und anschließend zu zwei verschiedenen Koordinatenprojektionen:

- \(\pi_a(a,x)=a\): Die Faser enthält die Nullstellen für einen festen Parameter.
- \(\pi_x(a,x)=x\): Die Faser enthält die Parameter für einen festen Zustand.

Die erste Projektion entdeckt den Bifurkationswert \(a=0\): Für \(a\le 0\)
gibt es eine verschiedene reelle Nullstelle, für \(a>0\) drei. Die zweite
Projektion entdeckt eine andere Besonderheit: Über \(x=0\) liegt die ganze
Parameterachse, während jede Faser über \(x\ne0\) genau einen Punkt enthält.

## Natives Forschungslabor starten

Die Visualisierung ist bewusst **keine Webseite**. Sie läuft als lokales
Matplotlib-Fenster mit festen Zeichenflächen; Browserbreite, CSS und responsive
Layouts beeinflussen die Mathematik daher nicht.

Im Repository:

```powershell
python -m pip install -r requirements.txt
python cubic_fibers_lab.py
```

Die vier nummerierten Schritte sind direkt anwählbar. In Schritt 3 und 4
steuert ein Regler die untersuchte Faser. Jede Ansicht enthält:

- beschriftete Achsen und eine bedeutungstragende Legende,
- die jeweilige logische Formulierung,
- eine didaktische Lesart,
- den zugehörigen Lean-Satz.

Die beiden Diagramme in Schritt 3 besitzen per Konstruktion exakt dieselbe
Breite und Höhe. Das wird zusätzlich automatisiert getestet.

## Reproduzierbare Abbildungen erzeugen

Vier vollständig beschriftete SVG-Dateien werden unter `figures/` versioniert.
Sie lassen sich jederzeit deterministisch neu erzeugen:

```powershell
python cubic_fibers_lab.py --export
python cubic_fibers_lab.py --check-layout
python -m unittest discover -s tests -v
```

## Lean-Formalisierung prüfen

Voraussetzung: [elan](https://github.com/leanprover/elan). Das Repository legt
Lean `v4.34.0` und mathlib `v4.34.0` fest.

```powershell
lake update
lake build
lake exe mathVizLabCheck
```

Die Beweise stehen in [`MathVizLab/CubicFamily.lean`](MathVizLab/CubicFamily.lean).
Formalisiert sind:

1. die Zerlegung `F a x = 0 ↔ x = 0 ∨ x² = a`,
2. die Parameterfasern für `a < 0`, `a = 0` und `a > 0`,
3. die Zustandsfaser über `x = 0` sowie über `x ≠ 0`,
4. die paarweise Verschiedenheit der drei positiven Wurzeln.

## Forschungsprotokoll

Die ausführliche didaktische und mathematische Herleitung steht in
[`docs/experiment-01.md`](docs/experiment-01.md). Dort werden auch nächste
visualisierbare Forschungsfragen formuliert.

## Struktur

```text
.
├── cubic_fibers_lab.py              Natives Labor und SVG-Export
├── figures/                         Reproduzierbare Forschungsabbildungen
├── tests/
│   └── test_visualization.py        Größen- und Renderprüfungen
├── MathVizLab/
│   └── CubicFamily.lean             Geprüfte mathematische Aussagen
├── docs/
│   └── experiment-01.md             Didaktisches Forschungsprotokoll
├── lakefile.lean
├── lean-toolchain
├── requirements.txt
└── Main.lean
```

## Arbeitsprinzip für weitere Beiträge

Jeder Beitrag soll dieselben vier Ebenen miteinander verbinden:

1. **Gegenstand:** Ein mathematisches Objekt mit klarer Forschungsfrage.
2. **Projektionsfolge:** Jede Informationsreduktion erzeugt eine neue,
   beschriftete Visualisierung und eine neue Faserfrage.
3. **Didaktische Spur:** Symbolische, geometrische und sprachliche Darstellung
   erklären einander.
4. **Lean-Spur:** Sichtbare Behauptungen werden als prüfbare Sätze formuliert;
   numerische Bilder gelten nicht als Beweise.
