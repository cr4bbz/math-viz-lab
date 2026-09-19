# Experiment 02: Primhöhen als diagonale Fasern

## Herkunft und Abgrenzung

Dieses Experiment adaptiert die Primhöhen-Geometrie aus dem Schwesterprojekt
[`math-lab`](https://github.com/cr4bbz/math-lab), Stand `e365a0d`. Mathematische
Ausgangspunkte sind dort insbesondere `MathLab/PrimeHeightGrid.lean`,
`MathLab/PrimeBandGeometry.lean` und die Beobachtung O1 in `OBSERVATIONS.md`.
Die vorhandenen Browseransichten werden nicht übernommen. `math-viz-lab`
erzeugt stattdessen feste, reproduzierbare SVG-Abbildungen mit Matplotlib und
eine eigenständig geprüfte Lean-Datei.

## 1. Forschungsfrage

Auf dem positiven ganzzahligen Gitter betrachten wir die additive Höhe

\[
h(a,b)=a+b,\qquad (a,b)\in\mathbb N_+^2.
\]

Die leitende Frage lautet:

> Wie werden Primzahlverteilung und Primzahllücken zu einer Geometrie
> diagonaler Fasern, und welche sichtbaren Muster entstehen lediglich durch
> das endliche Beobachtungsfenster?

Die Frage verbindet drei Begriffe, die auseinandergehalten werden müssen:

- Die **Höhenfaser** ist die Menge aller Gitterpunkte mit festem Wert `a+b=n`.
- Der **Primzahlfilter** wählt diejenigen Fasern aus, deren Index `n` prim ist.
- Ein **endliches Fenster** schneidet Fasern ab und kann dadurch eine scheinbare
  Größenänderung erzeugen, die keine Eigenschaft der Primzahlen ist.

## 2. Projektionsfolge

### Schritt 1: Vom Gitter zur Höhenfaser

Die Projektion

\[
\pi_h:\mathbb N_+^2\to\mathbb N,\qquad (a,b)\mapsto a+b
\]

verwirft, wo ein Punkt entlang seiner Diagonale liegt. Ihre Faser über `n` ist

\[
H_n=\pi_h^{-1}(n)=\{(a,b)\in\mathbb N_+^2\mid a+b=n\}.
\]

Durch den Koordinatenwechsel `(a,b) ↦ (n,a)` wird eine Diagonale zu einer
senkrechten Punktspalte. Für `n≥2` besitzt die volle positive Faser genau
`n−1` Punkte: `(1,n−1), …, (n−1,1)`.

Was die Projektion zeigt: die gemeinsame Höhe und die Anzahl ihrer
Zerlegungen. Was sie unterdrückt: die ursprüngliche zweidimensionale Lage sowie
die Symmetrie `(a,b) ↔ (b,a)`, sofern die Faserkoordinate nicht mitgeführt wird.

### Schritt 2: Primzahlen als Auswahl von Fasern

Wir definieren

\[
\operatorname{PrimeHeight}(a,b)\iff a+b\text{ ist prim}.
\]

Primalität ändert also nicht die Form der Diagonalen. Sie ist ein Filter auf
dem eindimensionalen Bildraum der Höhenprojektion. Im `16×16`-Fenster treten
die Primhöhen

\[
2,3,5,7,11,13,17,19,23,29,31
\]

als orange parallele Bänder auf. Diese endliche Liste ist
`numerical_evidence`; der Lean-Satz `primeHeight_of_sum_eq` prüft dagegen die
allgemeine logische Verbindung zwischen Primindex und Gitterzelle.

### Schritt 3: Zwei verschiedene Abstandsbegriffe

Für Primhöhen `p<q` ist die Primzahllücke

\[
g=q-p
\]

der Abstand ihrer ganzzahligen Höhenindizes. Im ursprünglichen euklidischen
Koordinatensystem sind die Fasern die parallelen Geraden
`a+b=p` und `a+b=q`. Da ihr Normalenvektor `(1,1)` die Länge `√2` besitzt, ist
ihr senkrechter Abstand

\[
d_\perp=\frac{q-p}{\sqrt2}.
\]

Für `p=11` und `q=13` gilt daher `g=2`, zwischen ihnen liegt genau das Band
`n=12`, und der euklidische Abstand ist `√2`. Diese Unterscheidung verhindert,
dass eine arithmetische Indexmetrik unbemerkt als euklidische Länge gelesen
wird. Beide Aussagen sind in Lean für das gewählte Beispiel geprüft.

### Schritt 4: Das Fenster als eigener mathematischer Operator

Im Fenster

\[
W_N=\{1,\ldots,N\}^2
\]

beobachten wir nicht `H_n`, sondern `H_n∩W_N`. Seine Kardinalität ist

\[
C_N(n)=
\begin{cases}
n-1,&2\le n\le N+1,\\
2N-n+1,&N+1<n\le2N,\\
0,&n>2N.
\end{cases}
\]

Für `N=16` ist `H_11` vollständig sichtbar und hat 10 Punkte. Die volle Faser
`H_19` hat 18 Punkte, aber nur 14 davon liegen im Fenster. Das Absinken der
sichtbaren Kurve nach `n=17` ist deshalb ein **Darstellungsartefakt**, keine
Aussage über eine abnehmende Häufigkeit oder Größe von Primzahlen.

## 3. Versionierte Zustände

| Zustand | Projektion | Evidenz | Kernaussage |
|---|---|---|---|
| `height-fiber-11` | Höhe | `lean_proved` | vollständige Faser mit 10 Punkten |
| `prime-bands-window-16` | Primzahlfilter | `numerical_evidence` | sichtbare Primhöhen bis 32 |
| `gap-11-13` | Primhöhenpaar | `lean_proved` | Lücke 2, ein Zwischenband, Distanz √2 |
| `truncated-fiber-19` | Fensterfaser | `lean_proved` | 14 von 18 Punkten sichtbar |

## 4. Lean-Spur

`MathVizLab/PrimeHeightGeometry.lean` formalisiert:

- `height` und `PrimeHeight`,
- die Symmetrie der Höhe und des Primhöhenprädikats,
- die exakte Kardinalität vollständiger und abgeschnittener Fensterfasern,
- die Geradheit später Primhöhenlücken,
- die Lücke und Zwischenbandzahl für `11,13`,
- die euklidische Distanz `√2` der beiden zugehörigen Geraden.

Die Aussagen zur Fensterkardinalität und zu Primhöhenlücken sind aus den
gleichnamigen Konstruktionen in `math-lab` adaptiert. Die explizite Trennung von
Indexabstand und euklidischer Distanz ist die zusätzliche geometrische
Didaktisierung dieses Experiments.

## 5. Forschungsprotokoll

### 2026-09-19 — Aufbau des Experiments

- **Zustände:** alle vier oben genannten Zustände
- **Frage:** Wie verhält sich die Primzahlfolge unter der Höhenprojektion?
- **Beobachtung:** Primzahlen werden als parallele diagonale Bänder sichtbar.
- **Evidenzklasse:** endliche Bandliste `numerical_evidence`; Faser- und
  Abstandsformeln `lean_proved`
- **Begrenzung:** Das Fenster zeigt nur `2≤n≤32`; ab `n=18` sind die Fasern
  abgeschnitten.
- **Schluss:** Die Projektion geometrisiert Primzahllücken, erzeugt aber keine
  neue Verteilungsaussage. Fenstergeometrie muss vor jeder statistischen
  Interpretation herausgerechnet werden.
- **Nächste Projektion:** Quotientiere eine endliche Folge aufeinanderfolgender
  Primhöhen nach Translation und behalte nur ihr Lückenwort. Danach kann geprüft
  werden, welche geometrischen Muster wiederkehren und welche Information über
  den absoluten Ort verloren geht.
