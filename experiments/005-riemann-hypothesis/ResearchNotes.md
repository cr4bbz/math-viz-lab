# Experiment 05: Die Riemannsche Vermutung

## 1. Gegenstand, Status und Forschungsfrage

Die Riemannsche Zetafunktion wird zunächst in der Halbebene `Re(s)>1` durch

\[
\zeta(s)=\sum_{n=1}^{\infty}\frac1{n^s}
\]

definiert und anschließend meromorph auf die komplexe Ebene fortgesetzt. Bei
`s=1` besitzt sie einen Pol. Die negativen geraden Zahlen sind triviale
Nullstellen. Die **Riemannsche Vermutung** lautet:

\[
\zeta(\rho)=0,\quad \rho\text{ nichttrivial}
\quad\Longrightarrow\quad
\operatorname{Re}(\rho)=\frac12.
\]

Diese Aussage ist offen. Weder eine Grafik noch eine endliche numerische Liste
noch die Lean-Definition `RiemannHypothesis` ist ein Beweis.

Die Forschungsfrage lautet:

> Wie lassen sich Definitionsbereich, analytische Fortsetzung, kritischer
> Streifen, kritische Gerade und endliche Nullstellenevidenz so projizieren,
> dass die offene universelle Aussage nicht mit einer Bildbeobachtung
> verwechselt wird?

## 2. Projektionsfolge

### Schritt 1: Dirichlet-Terme zu einem komplexen Summenpfad

Für `s=2+it` bilden die Partialsummen

\[
S_N(s)=\sum_{n=1}^{N}n^{-s}
\]

einen Pfad in der komplexen Ebene. Die linke Ansicht behält Real- und
Imaginärteil der Akkumulation. Die rechte projiziert denselben Vorgang auf den
skalaren Fehler `|S_N(s)−ζ(s)|`.

Diese Reihendarstellung ist nur für `Re(s)>1` legitim. Eine direkte Verwendung
derselben Reihe im kritischen Streifen wäre keine analytische Fortsetzung,
sondern eine divergente beziehungsweise unzulässige Berechnung. Mathlib beweist
die Übereinstimmung von Reihe und Zetafunktion unter genau dieser
Halbebenenbedingung.

### Schritt 2: Analytische Fortsetzung und Strukturkarte

Die analytische Fortsetzung fügt Werte außerhalb der ursprünglichen
Reihendomäne hinzu. Sichtbar werden:

- der Pol bei `s=1`,
- triviale Nullstellen bei `−2,−4,−6,…`,
- der kritische Streifen `0<Re(s)<1`,
- die kritische Gerade `Re(s)=1/2`,
- die nullstellenfreie rechte Halbebene `Re(s)≥1`, wobei `s=1` als Pol
  gesondert gelesen werden muss.

Die reelle Spur ist nur ein eindimensionaler Schnitt. Sie kann nicht zeigen,
wo komplexe nichttriviale Nullstellen liegen.

### Schritt 3: Komplexer Wert zu Betrag

Die Projektion

\[
\zeta(\sigma+it)\longmapsto
\log_{10}|\zeta(\sigma+it)|
\]

macht kleine Beträge als Täler sichtbar. Sie verwirft jedoch die komplexe
Phase. Ein endliches Raster kann eine Nullstelle außerdem verfehlen oder ein
kleines Minimum als Nullstelle erscheinen lassen.

Das versionierte Fenster verwendet `0≤σ≤1`, `0≤t≤35` und ein `61×141`-Raster.
Der horizontale Querschnitt bei `t=14.13` besitzt sein Rasterminimum nahe
`σ=1/2`. Das ist `numerical_evidence`, kein universeller Satz.

### Schritt 4: Einschränkung auf die kritische Gerade

Auf

\[
s(t)=\frac12+it
\]

kann die reellwertige Hardy-Funktion `Z(t)` verwendet werden. Ihre
Vorzeichenwechsel lokalisieren Nullstellen **auf dieser Geraden**. Die
Einschränkung ist didaktisch hilfreich, birgt aber eine logische Gefahr:

> Eine Suche auf der kritischen Geraden kann keine Nullstelle außerhalb der
> kritischen Geraden ausschließen.

Die mit `mpmath.zetazero` erzeugte Liste enumeriert kritische
Nullstellenhöhen. Sie ist deshalb keine unabhängige Vollsuche im Streifen.

### Schritt 5: Endliche Evidenz zu universeller Aussage

Die letzte Projektion trennt drei Ebenen:

1. **bewiesen:** triviale Nullstellen, Nullstellenfreiheit rechts des Streifens,
   Diskretheit und lokale Endlichkeit der Nullstellen;
2. **numerische Evidenz:** die ausgewählten gelisteten Nullstellen liegen auf
   `Re(s)=1/2`;
3. **offene Vermutung:** jede nichttriviale Nullstelle liegt dort.

Der entscheidende Informationsverlust ist der Quantorwechsel von „diese
endlich vielen“ zu „alle“. Er kann durch keine endliche Darstellung geschlossen
werden.

## 3. Versionierte Zustände

| Zustand | Evidenz | Kernaussage |
|---|---|---|
| `dirichlet-halfplane-2-plus-14i` | `lean_proved` | Reihendarstellung nur in `Re(s)>1` |
| `trivial-zero-minus-2` | `lean_proved` | `ζ(−2)=0` gehört zur trivialen Familie |
| `critical-strip-window-35` | `numerical_evidence` | endliche Betragslandschaft im Streifen |
| `first-five-critical-line-zeros` | `numerical_evidence` | fünf gelistete Höhen auf der Geraden |
| `riemann-hypothesis-open` | `conjecture` | universelle Aussage bleibt offen |

## 4. Lean-Spur

`MathVizLab/RiemannHypothesis.lean` formalisiert keine Lösung der Vermutung. Es
formalisiert stattdessen:

- `InCriticalStrip`, `OnCriticalLine` und `NontrivialZetaZero`,
- die Äquivalenz dieser didaktischen Formulierung mit mathlibs
  `RiemannHypothesis`,
- die Parametrisierung `1/2+it` der kritischen Geraden,
- die Spiegelinvarianz der kritischen Geraden unter `s↦1−s`,
- die trivialen Nullstellen,
- Nullstellenfreiheit für `Re(s)≥1`,
- Endlichkeit der Nullstellen in kompakten Fenstern,
- die Brücke `ζ(2)=π²/6` zum Basel-Experiment.

Das Vorhandensein eines Lean-Prädikats bedeutet nur, dass die Vermutung präzise
formuliert ist. Ein Beweis wäre ein Term dieses Typs; ein solcher wird nicht
konstruiert.

## 5. Kombinationslandkarte

Die Riemannsche Zetafunktion ist ein natürlicher Knoten zwischen den bisherigen
Experimenten.

| Kombination | verbindende Identität | mögliche Forschungsfrage |
|---|---|---|
| 003 Basel + 005 RH | `ζ(2)=π²/6` | Wie wird aus der reellen Potenzreihe eine komplexe Funktionsfamilie? |
| 002 Primhöhen + 005 RH | `ζ(s)=∏ₚ(1−p⁻ˢ)⁻¹` für `Re(s)>1` | Wie kodiert das Euler-Produkt die Primzahlen in ζ? |
| 004 gewichtete Fasern + 005 RH | `Σ(n−1)n⁻ˢ=ζ(s−1)−ζ(s)` für `Re(s)>2` | Wie verschieben Fasermultiplizitäten Pole und Konvergenzgrenzen? |
| 002 + 004 + 005 | logarithmische Ableitung `−ζ′/ζ` | Wie werden Primzahlpotenzen mit der Nullstellenstruktur gekoppelt? |

### Empfohlene nächste Kombination

Als Experiment 006 bietet sich die **Faser-Dirichlet-Reihe** an:

\[
D(s)=\sum_{n=1}^{\infty}\frac{n-1}{n^s}
    =\zeta(s-1)-\zeta(s),
\qquad \operatorname{Re}(s)>2.
\]

Sie verbindet Experiment 004 unmittelbar mit Experiment 005. Die
Fasermultiplizität verschiebt die Konvergenzhalbebene und den dominanten Pol um
eins. Danach kann das Euler-Produkt als zweite Kombination mit der
Primhöhen-Geometrie folgen.

## 6. Forschungsprotokoll

### 2026-09-19 — Aufbau des Riemann-Experiments

- **Standardzustand:** `critical-strip-window-35`
- **Frage:** Welche Projektionen erklären die Vermutung, ohne endliche Evidenz
  zum Beweis aufzuwerten?
- **Beobachtung:** Niedrige gelistete Nullstellen erscheinen als Täler auf der
  kritischen Geraden.
- **Evidenzklasse:** Raster und Nullstellenliste `numerical_evidence`;
  universelle Aussage `conjecture`; strukturelle Hintergrundsätze
  `lean_proved`
- **Begrenzung:** Das Raster endet bei `t=35`; `mpmath.zetazero` enumeriert
  Nullstellen auf der kritischen Geraden und schließt keine hypothetische
  Nullstelle außerhalb dieser Geraden aus.
- **Schluss:** Die letzte Ansicht muss Bestandteil jeder RH-Visualisierung
  bleiben, weil sie den unzulässigen Quantorwechsel sichtbar verhindert.
- **Nächste Projektion:** `D(s)=ζ(s−1)−ζ(s)` als erste konkrete
  Experiment-Kombination.
