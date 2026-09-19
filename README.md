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

## Nachhaltiger Forschungsablauf

Das Repository enthält einen lokalen Codex-Skill unter
`.agents/skills/graphical-math-research` und verbindliche Projektregeln in
`AGENTS.md`. Ein Experiment wird nicht durch einen flüchtigen GUI-Zustand,
sondern durch `experiment.yaml` und benannte Zustände unter `states/`
repräsentiert.

Für Forschungsbeiträge kann der Skill explizit aufgerufen werden:

```text
$graphical-math-research Untersuche die Parameterfaser nahe a=0.
```

Der Skill kann bei passenden Aufgaben auch automatisch ausgewählt werden.

## Natives Forschungslabor starten

Die Visualisierung ist bewusst **keine Webseite**. Sie läuft als lokales
Matplotlib-Fenster mit festen Zeichenflächen; Browserbreite, CSS und responsive
Layouts beeinflussen die Mathematik daher nicht.

Im Repository:

```powershell
python -m pip install -r requirements.txt
python experiments/001-cubic-fibers/render.py
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

Vier vollständig beschriftete SVG-Dateien werden unter
`experiments/001-cubic-fibers/renders/` versioniert.
Sie lassen sich jederzeit deterministisch neu erzeugen:

```powershell
python .agents/skills/graphical-math-research/scripts/validate_experiment.py --all
python .agents/skills/graphical-math-research/scripts/render_experiment.py experiments/001-cubic-fibers/experiment.yaml
python experiments/001-cubic-fibers/render.py --check-layout
python -m unittest discover -s experiments/001-cubic-fibers/tests -v
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

## Experiment 02: Primhöhen-Geometrie

Das zweite Experiment adaptiert die Primhöhen-Forschung aus dem Schwesterprojekt
[`math-lab`](https://github.com/cr4bbz/math-lab). Auf dem positiven Gitter wird
die Projektion

\[
\pi_h(a,b)=a+b
\]

untersucht. Ihre Fasern sind Diagonalen; Primzahlen wählen bestimmte
Höhenbänder aus, und Primzahllücken werden zu Abständen ihrer Höhenindizes. Die
Abbildungen unterscheiden ausdrücklich zwischen diesem Indexabstand, dem
euklidischen Abstand paralleler Geraden und Artefakten eines endlichen Fensters.

```powershell
python experiments/002-prime-height-geometry/render.py
python .agents/skills/graphical-math-research/scripts/render_experiment.py experiments/002-prime-height-geometry/experiment.yaml
python -m unittest discover -s experiments/002-prime-height-geometry/tests -v
lake build
```

Der erste Befehl öffnet eine native interaktive Übersicht mit allen vier
Projektionsschritten gleichzeitig. Regler koppeln Fenstergröße `N`, ausgewählte
Höhe `n` und das betrachtete aufeinanderfolgende Primzahlpaar. Eine einzelne
Detailansicht bleibt beispielsweise mit `--step 3` verfügbar.

Die Herleitung und Evidenzklassifikation stehen in
[`experiments/002-prime-height-geometry/ResearchNotes.md`](experiments/002-prime-height-geometry/ResearchNotes.md).

## Experiment 03: Das Basel-Problem

Das dritte Experiment untersucht die Reihe

\[
\sum_{n=1}^{\infty}\frac1{n^2}=\frac{\pi^2}{6}
\]

als Folge von vier Projektionen: vom Index zum Quadratreziproken, von den
Einzeltermen zur Partialsumme, von der Partialsumme zum Restfehler und von
positiven Indizes zur symmetrischen Domäne `ℤ∖{0}`. Der letzte Schritt klärt,
dass die ganzzahlige Variante wegen der Paare `±n` den Wert `π²/3` besitzt.

```powershell
python experiments/003-basel-problem/render.py
python experiments/003-basel-problem/render.py --step 3
python experiments/003-basel-problem/render.py --export
python -m unittest discover -s experiments/003-basel-problem/tests -v
lake build
```

Der erste Befehl öffnet alle vier Schritte gleichzeitig. Die Regler steuern
Kurvenende `M`, ausgewählte Partialsumme `N` und den sichtbaren Indexradius `K`.
Der zweite Befehl öffnet eine große Detailansicht der Restschranken.

## Experiment 04: Gewichtete Primhöhenfasern

Das vierte Experiment komponiert die Primhöhen-Geometrie aus Experiment 02 mit
den Quadratreziproken aus Experiment 03. Jeder Punkt der Höhenfaser

\[
H_n=\{(a,b)\in\mathbb N_+^2\mid a+b=n\}
\]

erhält das Gewicht `1/n²`. Weil `|H_n|=n−1`, besitzt die ganze Faser die Masse

\[
\mu(H_n)=\frac{n-1}{n^2}=\frac1n-\frac1{n^2}.
\]

Die resultierende Reihe divergiert; selbst die Einschränkung auf Primhöhen ist
nicht summierbar. Beide Aussagen sind in Lean geprüft.

```powershell
python experiments/004-weighted-prime-height-fibers/render.py
python experiments/004-weighted-prime-height-fibers/render.py --step 4
python experiments/004-weighted-prime-height-fibers/render.py --export
python -m unittest discover -s experiments/004-weighted-prime-height-fibers/tests -v
lake build
```

Der Standardstart zeigt alle vier Projektionen gleichzeitig. Die Regler koppeln
Summengrenze `M` und ausgewählte Höhenfaser `n` über sämtliche Ansichten.

## Forschungsprotokolle

Die ausführlichen didaktischen und mathematischen Herleitungen stehen in den
jeweiligen `ResearchNotes.md`-Dateien:

- [`Experiment 01: kubische Fasern`](experiments/001-cubic-fibers/ResearchNotes.md)
- [`Experiment 02: Primhöhen-Geometrie`](experiments/002-prime-height-geometry/ResearchNotes.md)
- [`Experiment 03: Basel-Problem`](experiments/003-basel-problem/ResearchNotes.md)
- [`Experiment 04: gewichtete Primhöhenfasern`](experiments/004-weighted-prime-height-fibers/ResearchNotes.md)

Dort werden auch die Evidenzklassen und nächsten visualisierbaren
Forschungsfragen festgehalten.

## Struktur

```text
.
├── AGENTS.md                        Verbindlicher Forschungsvertrag
├── .agents/skills/
│   └── graphical-math-research/     Wiederverwendbarer Forschungsablauf
├── experiments/
│   ├── 001-cubic-fibers/
│   │   ├── experiment.yaml          Gemeinsamer Forschungszustand
│   │   ├── states/                  Benannte, erhaltende Zustände
│   │   ├── render.py                Natives Labor und SVG-Export
│   │   ├── renders/                 Reproduzierbare Abbildungen
│   │   ├── tests/                   Layout- und Renderprüfungen
│   │   └── ResearchNotes.md         Didaktisches Forschungsprotokoll
│   ├── 002-prime-height-geometry/    Geometrie der Primhöhen
│   │   ├── experiment.yaml
│   │   ├── states/
│   │   ├── render.py
│   │   ├── renders/
│   │   ├── tests/
│   │   └── ResearchNotes.md
│   ├── 003-basel-problem/            Reziproke Quadratsumme
│   │   ├── experiment.yaml
│   │   ├── states/
│   │   ├── render.py
│   │   ├── renders/
│   │   ├── tests/
│   │   └── ResearchNotes.md
│   └── 004-weighted-prime-height-fibers/
│       ├── experiment.yaml          Kompositions- und Evidenzmanifest
│       ├── states/
│       ├── render.py                Gekoppelte native Übersicht
│       ├── renders/
│       ├── tests/
│       └── ResearchNotes.md
├── MathVizLab/
│   ├── CubicFamily.lean             Geprüfte mathematische Aussagen
│   ├── PrimeHeightGeometry.lean      Geprüfte Primhöhen-Geometrie
│   ├── BaselProblem.lean             Geprüfte Basel-Reihe
│   └── WeightedPrimeHeightFibers.lean
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
