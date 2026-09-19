# Experiment 04: Basel-Gewichte auf Primhöhenfasern

## 1. Herkunft und neue Forschungsfrage

Dieses Experiment komponiert zwei vorhandene Forschungsobjekte:

- Experiment 02 liefert die Höhenprojektion
  `h(a,b)=a+b` und die positiven Fasern `H_n` mit `|H_n|=n−1`.
- Experiment 03 liefert das Basel-Gewicht `1/n²` und die konvergente Reihe
  `Σ 1/n²=π²/6`.

Jeder Gitterpunkt `(a,b)∈H_n` erhält nun das Gewicht `1/n²`. Die leitende Frage
lautet:

> Wie verändert die Fasermultiplizität `|H_n|=n−1` das konvergente
> Basel-Gewicht, und bleibt die resultierende Reihe nach einem Primhöhenfilter
> summierbar?

Die Antwort ist bemerkenswert: Schon die vollständigen Höhenfasern verwandeln
den quadratischen Abfall in einen harmonischen Hauptterm. Selbst der Filter auf
Primhöhen stellt die Konvergenz nicht wieder her.

## 2. Projektionsfolge

### Schritt 1: Vom Gitter zur gewichteten Faser

Für `n≥2` ist

\[
H_n=\{(a,b)\in\mathbb N_+^2\mid a+b=n\}
   =\{(1,n-1),\ldots,(n-1,1)\}.
\]

Die Höhenprojektion verwirft die Lage entlang der Diagonale. Ihre Faser besitzt
`n−1` Punkte. Weil jeder dieser Punkte dasselbe Gewicht `1/n²` trägt, ist die
gesamte Fasermasse

\[
\mu(H_n)=\sum_{(a,b)\in H_n}\frac1{n^2}
         =\frac{n-1}{n^2}.
\]

Im Standardzustand `n=11` werden zehn Gewichte `1/121` zur Masse `10/121`
zusammengefasst. Die Grafik zeigt die einzelnen Punkte und Balken weiterhin,
damit die Projektion ihre Multiplizität nicht unsichtbar macht.

### Schritt 2: Die Faserkardinalität als asymptotischer Faktor

Der Quotient aus Fasermasse und ursprünglichem Basel-Term ist exakt

\[
\frac{\mu(H_n)}{1/n^2}=n-1.
\]

Dadurch ändert sich die Größenordnung:

\[
\mu(H_n)=\frac{n-1}{n^2}
         =\frac1n-\frac1{n^2}
         \sim\frac1n.
\]

Die linke logarithmische Ansicht vergleicht beide Abfälle. Die rechte Ansicht
zeigt den verlorenen Faserparameter als wachsenden Multiplikationsfaktor. Das
ist der zentrale Mechanismus des Experiments: Eine Projektion kann bei einer
gewichteten Zählung nicht folgenlos durch nur einen Repräsentanten ersetzt
werden.

### Schritt 3: Partialsummen und Summierbarkeit

Wir bezeichnen mit

\[
S_N=\sum_{n=1}^N\frac1{n^2},\qquad
H_N=\sum_{n=1}^N\frac1n,
\]

die Basel- beziehungsweise harmonische Partialsumme. Für die Fasermassen gilt
endlich und exakt

\[
T_N=\sum_{n=1}^N\mu(H_n)=H_N-S_N.
\]

Da `S_N` konvergiert und `H_N` divergiert, ist auch die Faserreihe nicht
summierbar. Bei `N=500` lauten die numerischen Werte

\[
S_{500}\approx1{,}642936,quad
H_{500}\approx6{,}792823,quad
T_{500}\approx5{,}149887.
\]

Die konkreten Dezimalwerte sind numerische Evidenz. Die endliche Identität und
die Nicht-Summierbarkeit sind eigenständig in Lean bewiesen.

### Schritt 4: Der Primhöhenfilter

Nun werden nur Fasern mit primem Höhenindex behalten:

\[
P_N=\sum_{\substack{p\le N\\p\text{ prim}}}
     \frac{p-1}{p^2}.
\]

Die Projektion `n↦1_Prime(n)` verwirft alle zusammengesetzten Höhen. Sie behält
jedoch auf jeder Primhöhe den harmonischen Anteil

\[
\frac{p-1}{p^2}=\frac1p-\frac1{p^2}.
\]

Die Summe der Primzahlreziproken divergiert, während `Σ_p 1/p²` konvergiert.
Folglich ist auch die gewichtete Primhöhenreihe nicht summierbar. Ihre
Partialsumme wächst sehr langsam; ein endliches Diagramm allein könnte deshalb
fälschlich einen Grenzwert nahelegen. Gerade hier ist die Trennung zwischen
Visualisierung und Lean-Beweis entscheidend.

## 3. Was die Projektionen zeigen und verwerfen

| Projektion | sichtbar | verworfen | relevante Faser |
|---|---|---|---|
| `(a,b)↦a+b` | Höhenindex | Position auf der Diagonale | `H_n`, Größe `n−1` |
| Punktgewichte `↦μ(H_n)` | Gesamtmasse | einzelne Beiträge | alle `n−1` gleichen Gewichte |
| Termfolge `↦T_N` | Akkumulation | Herkunft eines Beitrags | Folgen mit gleicher endlicher Summe |
| `n↦1_Prime(n)` | Primhöhen | zusammengesetzte Höhen | alle Indizes mit gleichem Filterwert |

Die entscheidende Informationsgröße ist nicht nur der Wert auf dem Bildraum,
sondern die Multiplizität seiner Urbilder.

## 4. Versionierte Zustände und Evidenz

| Zustand | Evidenz | Kernaussage |
|---|---|---|
| `weighted-fiber-11` | `lean_proved` | zehn Punkte erzeugen die Masse `10/121` |
| `multiplicity-factor-11` | `lean_proved` | der Faktor ist `|H₁₁|=10` |
| `partial-sums-500` | `lean_proved` | `T_N=H_N−S_N`; die Reihe divergiert |
| `prime-filter-500` | `lean_proved` | der Primfilter beseitigt die Divergenz nicht |

Die in den Zuständen gespeicherten Dezimalwerte sind reproduzierbare endliche
Auswertungen. `lean_proved` bezieht sich jeweils auf die ausdrücklich benannten
allgemeinen Identitäten oder Nicht-Summierbarkeitssätze.

## 5. Lean-Spur

`MathVizLab/WeightedPrimeHeightFibers.lean` importiert bewusst die Module der
beiden Elternexperimente. Es formalisiert:

- `fullFiberMass` und `visibleFiberMass`,
- Gleichheit sichtbarer und voller Masse bei vollständiger Faser,
- die Zerlegung `(n−1)/n²=1/n−1/n²`,
- die endliche Summenidentität `T_N=H_N−S_N`,
- die Nicht-Summierbarkeit aller gewichteten Fasern,
- die Nicht-Summierbarkeit der gewichteten Primhöhenfasern mithilfe von
  `Nat.Primes.not_summable_one_div` aus mathlib.

## 6. Forschungsprotokoll

### 2026-09-19 — Komposition der Experimente 002 und 003

- **Ausgangszustände:** `prime-bands-window-16`, `partial-sum-20`
- **Neuer Standardzustand:** `weighted-fiber-11`
- **Frage:** Kann eine wachsende Fasergröße die Summierbarkeit eines Gewichts
  ändern, und überlebt dieser Effekt einen Primfilter?
- **Beobachtung:** Der Faktor `n−1` hebt einen Exponenten des quadratischen
  Abfalls auf.
- **Evidenzklasse:** allgemeine Identitäten und beide Divergenzaussagen
  `lean_proved`; dargestellte endliche Werte zusätzlich `numerical_evidence`
- **Begrenzung:** Die Grafik reicht nur bis zum einstellbaren Cutoff und zeigt
  keine asymptotische Geschwindigkeit der Primzahlreziprokensumme als Beweis.
- **Schluss:** Fasermultiplizität ist eine mathematisch wirksame Information.
  Sie darf bei Projektionen gewichteter Mengen nicht stillschweigend verloren
  gehen.
- **Nächste Projektion:** Ersetze `1/n²` durch `1/n^s` und untersuche die
  kritische Exponentverschiebung: Auf den Fasern verhält sich das Gewicht wie
  `n^{1-s}`, sodass die Konvergenzschwelle von `s>1` zu `s>2` wandert.
