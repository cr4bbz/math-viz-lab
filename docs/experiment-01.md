# Experiment 01: Kubische Fasern und ein Bifurkationswert

## 1. Die Forschungsfrage

Für jeden reellen Parameter \(a\) betrachten wir die Funktion

\[
f_a(x)=x^3-a x.
\]

Die gewöhnliche Schulbuchfrage lautet: „Welche Nullstellen hat \(f_a\)?“ Das
Labor stellt zunächst eine größere Frage: **Wie hängen alle Nullstellen aller
Parameter geometrisch zusammen?** Erst danach projizieren wir diese Gesamtform
wieder auf einzelne Koordinaten. Diese Reihenfolge ist wichtig, weil sie die
Stellen sichtbar macht, an denen sich Fasern qualitativ ändern.

## 2. Drei Darstellungsebenen

Das Experiment hält drei Repräsentationen synchron:

| Ebene | Gegenstand | Erkenntnisfunktion |
|---|---|---|
| symbolisch | \(x^3-a x=x(x^2-a)\) | Faktorisierung erzeugt eine Fallunterscheidung |
| geometrisch | Gerade \(x=0\) vereinigt mit Parabel \(a=x^2\) | Schnittzahlen und außergewöhnliche Punkte werden sichtbar |
| logisch / Lean | `x = 0 ∨ x ^ 2 = a` | Das geometrische „Vereinigen“ wird zu einem präzisen Oder |

Keine Ebene soll die anderen ersetzen. Das Bild schlägt Vermutungen vor, die
Algebra erklärt den Mechanismus und Lean prüft, ob die Formulierung alle Fälle
korrekt umfasst.

## 3. Schrittweise Projektion

### Schritt 1: Vom Term zum Vorzeichenfeld

Wir interpretieren \(F(a,x)=x^3-a x\) als eine Funktion
\(F:\mathbb R^2\to\mathbb R\). Ein Punkt \((a,x)\) ist jetzt keine Lösung,
sondern zunächst nur eine Eingabe. Das Vorzeichenfeld zeigt, wo der Wert positiv
oder negativ ist.

Didaktischer Zweck: Eine Nullstellenmenge ist die Grenze zwischen
Vorzeichenbereichen. So erscheint die Gleichung \(F=0\) nicht als isolierte
Rechenaufgabe, sondern als Niveauschnitt eines größeren Feldes.

### Schritt 2: Vom Feld zur Niveaumenge

Die Faktorisierung

\[
F(a,x)=x(x^2-a)
\]

liefert

\[
F(a,x)=0 \iff x=0\ \lor\ x^2=a.
\]

Darum ist

\[
V=\{x=0\}\cup\{a=x^2\}.
\]

Die Linie und die Parabel treffen sich in \((0,0)\). Dieser Punkt ist ein guter
Forschungskandidat, weil dort zwei Komponenten der Nullstellenmenge
zusammenfallen. Die Visualisierung markiert ihn deshalb ausdrücklich.

### Schritt 3: Projektion auf den Parameter

Die Projektion

\[
\pi_a:V\to\mathbb R,\qquad (a,x)\mapsto a
\]

hat über einem Parameter \(a\) die Faser

\[
V_a=\pi_a^{-1}(a)=\{x\in\mathbb R\mid F(a,x)=0\}.
\]

Im \((a,x)\)-Diagramm ist das ein senkrechter Schnitt. Es entstehen drei Fälle:

1. **\(a<0\):** Die Gleichung \(x^2=a\) hat keine reelle Lösung. Die Faser ist
   \(\{0\}\).
2. **\(a=0\):** Formal treffen die Äste \(x=0\), \(x=\sqrt a\) und
   \(x=-\sqrt a\) zusammen. Als Menge bleibt wieder \(\{0\}\); algebraisch ist
   die Nullstelle dreifach.
3. **\(a>0\):** Die Faser ist \(\{0,\sqrt a,-\sqrt a\}\), also drei
   verschiedene Punkte.

Der Wert \(a=0\) ist ein **Bifurkationswert** für die Menge der verschiedenen
reellen Nullstellen. Das Bild zählt Schnittpunkte; der Lean-Beweis zeigt, dass
dabei kein Punkt übersehen wird.

### Schritt 4: Projektion auf den Zustand

Wir wechseln die Blickrichtung:

\[
\pi_x:V\to\mathbb R,\qquad (a,x)\mapsto x.
\]

Die Faser

\[
V^x=\{a\in\mathbb R\mid F(a,x)=0\}
\]

ist im selben Diagramm ein waagerechter Schnitt. Für \(x\ne0\) darf die
Gleichung durch \(x\) geteilt werden, sodass genau \(a=x^2\) bleibt. Für
\(x=0\) wäre diese Division unzulässig; tatsächlich gilt \(F(a,0)=0\) für jedes
\(a\). Die Faser springt von einem Punkt zu einer ganzen Geraden.

Didaktisch ist das ein nützliches Warnsignal: **Eine algebraische Operation kann
genau die außergewöhnliche Faser vernichten, die geometrisch am
aufschlussreichsten ist.**

## 4. Was Lean genau absichert

Die Datei `MathVizLab/CubicFamily.lean` trennt Definition und Behauptungen:

- `cubicFamily` definiert den untersuchten Term.
- `cubicFamily_eq_zero_iff` beweist die Vereinigung von Linie und Parabel.
- `parameterFiber_of_neg`, `parameterFiber_at_zero` und
  `parameterFiber_of_pos` klassifizieren alle Parameterfasern.
- `stateFiber_at_zero` und `stateFiber_of_ne_zero` klassifizieren die Fasern der
  zweiten Projektion.
- `positive_roots_are_distinct` verhindert, dass „drei dargestellte Punkte“ mit
  „drei verschiedenen Punkten“ verwechselt wird.

Die Visualisierung selbst ist kein Beweis: Sie zeichnet nur einen endlichen
Ausschnitt mit endlicher Auflösung. Die Lean-Sätze quantifizieren dagegen über
alle reellen Parameter und Zustände.

## 5. Anschlussfragen für weitere Experimente

### A. Vielfachheit statt bloßer Punktzahl

Bei \(a=0\) hat \(f_0(x)=x^3\) nur eine verschiedene Nullstelle, aber
Vielfachheit drei. Eine nächste Visualisierung kann zusätzlich die Ableitung
\(\partial F/\partial x=3x^2-a\) einblenden. Gemeinsame Nullstellen von \(F\)
und dieser Ableitung kennzeichnen mehrfach auftretende Wurzeln.

### B. Diskriminante einer allgemeineren kubischen Familie

Für \(x^3+p x+q\) lebt die Nullstellenmenge im dreidimensionalen Raum
\((p,q,x)\). Die Projektion auf die \((p,q)\)-Ebene führt zur
Diskriminantenkurve \(4p^3+27q^2=0\). Das ist die direkte zweiparametrige
Fortsetzung des aktuellen Experiments.

### C. Komplexe statt reelle Fasern

Über \(\mathbb C\) verschwinden die beiden zusätzlichen Wurzeln für \(a<0\)
nicht; sie verlassen nur die reelle Achse. Eine Darstellung von Real- und
Imaginärteil würde erklären, warum die reelle Faserzahl springt, obwohl der
Fundamentalsatz der Algebra stets drei komplexe Wurzeln mit Vielfachheit zählt.

### D. Stabilität der Projektion

Man kann untersuchen, welche kleinen Störungen des Terms den Bifurkationswert
verschieben oder aufspalten. So führt die elementare Nullstellenfrage zu
Singularitätentheorie und qualitativer Dynamik.
