# Experiment 03: Das Basel-Problem

## 1. Gegenstand und Domänenklärung

Wir untersuchen die Reihe

\[
\sum_{n=1}^{\infty}\frac1{n^2}=\frac{\pi^2}{6}.
\]

Das ist die klassische Form des **Basel-Problems**. Die Formulierung
`n ∈ ℤ` benötigt eine wichtige Präzisierung: Für `n=0` ist der reelle Ausdruck
`1/n²` nicht definiert. Wird stattdessen über alle von null verschiedenen
ganzen Zahlen summiert, erscheinen die Indizes paarweise als `−n` und `n`:

\[
\sum_{n\in\mathbb Z\setminus\{0\}}\frac1{n^2}
=2\sum_{n=1}^{\infty}\frac1{n^2}
=\frac{\pi^2}{3}.
\]

Das Experiment stellt beide Domänen nebeneinander. So wird eine scheinbar
kleine Änderung der Indexmenge als mathematisch relevante Verdopplung sichtbar.

## 2. Forschungsfrage

> Wie machen geometrische Flächen, Partialsummen, Restschranken und die
> Faser `{−n,n}` den Wert und die Domänenabhängigkeit der Basel-Reihe sichtbar?

Die Visualisierung soll nicht nur den bekannten Grenzwert wiedergeben. Sie
untersucht, welche Information bei jeder Projektion erhalten bleibt und welche
verloren geht.

## 3. Projektionsfolge

### Schritt 1: Index zu Summand und Quadratfläche

Die Abbildung

\[
n\longmapsto a_n=\frac1{n^2},\qquad n\in\mathbb N_+,
\]

macht aus einem diskreten Index eine positive Größe. Geometrisch ist `1/n²`
die Fläche eines Teilquadrats, wenn das Einheitsquadrat in ein `n×n`-Gitter
zerlegt wird. Die linke Ansicht zeigt den quadratischen Abfall der Termfolge,
die rechte dieselbe Zahl als Fläche.

Erhalten bleiben Index und Größe. Noch unsichtbar ist, wie sich die unendlich
vielen Flächen akkumulieren.

### Schritt 2: Endliche Folge zu Partialsumme

Für einen Abschneideindex `N` wird die ganze endliche Termfolge auf eine Zahl
projiziert:

\[
(a_1,\ldots,a_N)\longmapsto
S_N=\sum_{n=1}^{N}\frac1{n^2}.
\]

Diese Projektion verliert die Reihenfolge und die Identität der einzelnen
Beiträge. Sie zeigt dafür unmittelbar die monotone Annäherung an `π²/6`.
Die logarithmische Restdarstellung rechts verhindert, dass kleine Unterschiede
nahe dem Grenzwert optisch verschwinden.

Für den versionierten Zustand `N=20` gilt numerisch

\[
S_{20}\approx1{,}596163244,
\qquad
\frac{\pi^2}{6}-S_{20}\approx0{,}048770823.
\]

Die Dezimalwerte sind `numerical_evidence`. Der unendliche Grenzwert selbst ist
in Lean bewiesen.

### Schritt 3: Partialsumme zu Restterm

Wir wechseln von der bereits gesammelten Größe zur noch fehlenden Größe:

\[
R_N=\frac{\pi^2}{6}-S_N.
\]

Für die fallende Funktion `x↦1/x²` liefert der Integralvergleich den Korridor

\[
\frac1{N+1}\le R_N\le\frac1N.
\]

Die linke Ansicht zeigt alle drei Größen logarithmisch; die rechte vergrößert
den lokalen Ausschnitt für das ausgewählte `N`. Die Schranken werden hier über
endlich viele numerische Stichproben geprüft und deshalb ausdrücklich als
`numerical_evidence`, nicht als Lean-Beweis, geführt.

Diese Projektion ist für Forschung aufschlussreich, weil sie die Frage vom
Wert der Summe zur **Konvergenzgeschwindigkeit** verschiebt. Sichtbar wird
`R_N=Θ(1/N)`; aus der Grafik allein folgt diese asymptotische Aussage jedoch
nicht als Beweis.

### Schritt 4: Positive Indizes zu ganzzahligen Vorzeichenfasern

Die Betragsprojektion

\[
q:\mathbb Z\setminus\{0\}\to\mathbb N_+,
\qquad q(n)=|n|
\]

hat über jedem positiven Index die zweielementige Faser

\[
q^{-1}(n)=\{-n,n\}.
\]

Da `1/(−n)²=1/n²`, tragen beide Faserpunkte gleich viel bei. Die linke Ansicht
zeigt diese Spiegelsymmetrie und markiert die ausgeschlossene Null. Die rechte
zeigt, dass die symmetrische Partialsumme exakt `2S_N` ist. Damit wird aus dem
Basel-Wert `π²/6` der bilaterale Wert `π²/3`.

## 4. Versionierte Zustände und Evidenz

| Zustand | Projektion | Evidenz | Kernaussage |
|---|---|---|---|
| `positive-terms-10` | Index zu Term/Fläche | `lean_proved` | für `n>0` ist der Term `1/n²` |
| `partial-sum-20` | endliche Folge zu Summe | `numerical_evidence` | Wert und Rest bei `N=20` |
| `tail-bound-20` | Partialsumme zu Rest | `numerical_evidence` | der berechnete Rest liegt im Korridor |
| `bilateral-integers-20` | Betrag und Vorzeichenfaser | `lean_proved` | ±n verdoppelt Partialsumme und Grenzwert |

## 5. Lean-Spur

`MathVizLab/BaselProblem.lean` formalisiert:

- einen bei `n=0` explizit auf null gesetzten Summanden `baselTerm`,
- positive Terme und die ersten beiden Partialsummen,
- den Grenzwert `π²/6` mithilfe des mathlib-Satzes `hasSum_zeta_two`,
- die endliche Verdopplung durch die Paare `−n,n`,
- die daraus folgende bilaterale Summe `π²/3`.

Lean definiert Division durch null in Körpern total und wertet `1/0` zu `0`
aus. Das ersetzt keine mathematische Domänenentscheidung. Die Fallunterscheidung
in `baselTerm` sowie die sichtbare Markierung von `0` dokumentieren deshalb
bewusst, dass die klassische Reihe nur positive Indizes besitzt.

## 6. Forschungsprotokoll

### 2026-09-19 — Aufbau des Experiments

- **Zustände:** die vier oben beschriebenen Zustände
- **Frage:** Welche Sicht auf Summand, Summe, Fehler und Indexdomäne ist jeweils
  erkenntnisreich?
- **Beobachtung:** Die Einzelterme fallen quadratisch, der Rest dagegen nur in
  der Größenordnung `1/N`.
- **Evidenzklasse:** Grenzwert und symmetrische Verdopplung `lean_proved`;
  Dezimalwerte und dargestellte Restschranken `numerical_evidence`;
  Flächenmodell `visual_observation`
- **Begrenzung:** Die Visualisierung erklärt noch nicht, warum gerade `π`
  erscheint. Dafür wäre eine weitere geometrische oder analytische Darstellung
  nötig.
- **Schluss:** Die Faser `{−n,n}` erklärt vollständig den Faktor zwei beim
  Wechsel von positiven zu ganzzahligen Indizes, nicht jedoch den Wert `π²/6`.
- **Nächste Projektion:** Über die Euler-Produktdarstellung
  `ζ(2)=∏ₚ(1−p⁻²)⁻¹` kann die Reihe auf Primfaktoren projiziert und mit der
  Primhöhen-Geometrie aus Experiment 02 verbunden werden.
