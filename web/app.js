const NS = "http://www.w3.org/2000/svg";

const stages = {
  1: {
    kicker: "Schritt 1 · Ausgangsraum",
    title: "Das Vorzeichenfeld des Terms",
    caption: "Farben codieren das Vorzeichen von F(a,x); die noch unmarkierte Grenze ist die Nullstellenmenge.",
    explanation: `
      <p>Wir beginnen nicht mit einzelnen Graphen, sondern mit allen Paaren <span class="formula">(a,x)</span> zugleich. Jeder Bildpunkt steht für einen eingesetzten Parameter und Zustand.</p>
      <p class="observation"><strong>Beobachtung:</strong> Zwischen positiven und negativen Gebieten muss <span class="formula">F(a,x)=0</span> gelten. Diese Grenze wird im nächsten Schritt unser eigenes geometrisches Objekt.</p>`,
    formula: "F : ℝ² → ℝ, (a,x) ↦ x³ − a·x",
    reading: "Eine Funktion zweier Variablen ordnet jedem Parameter-Zustands-Paar genau einen Funktionswert zu.",
    lean: "def cubicFamily (a x : ℝ) : ℝ := x ^ 3 - a * x",
    leanReading: "Lean erhält zuerst exakt den Term, über den alle späteren Aussagen sprechen.",
    next: "Weiter: Nullstellenmenge →"
  },
  2: {
    kicker: "Schritt 2 · Niveauschnitt",
    title: "Die Nullstellenmenge wird zum Objekt",
    caption: "Orange: Parabel a = x². Grün: Linie x = 0. Ihre Vereinigung ist V.",
    explanation: `
      <p>Die Faktorisierung <span class="formula">x³ − a·x = x(x²−a)</span> zerlegt die Nullstellenmenge in zwei beschriftete Äste.</p>
      <p class="observation"><strong>Aufschlussreicher Ort:</strong> Bei <span class="formula">(a,x)=(0,0)</span> schneiden sich Linie und Parabel. Dort ändert sich später die Anzahl verschiedener Nullstellen.</p>`,
    formula: "(a,x) ∈ V ⇔ x = 0 ∨ x² = a",
    reading: "Das logische „oder“ entspricht geometrisch einer Vereinigung: Gerade oder Parabel.",
    lean: "theorem cubicFamily_eq_zero_iff (a x : ℝ) : F a x = 0 ↔ x = 0 ∨ x ^ 2 = a",
    leanReading: "Der zentrale Lean-Satz verbindet die algebraische Gleichung mit der sichtbaren Zerlegung.",
    next: "Weiter: auf a projizieren →"
  },
  3: {
    kicker: "Schritt 3 · Projektion πₐ",
    title: "Eine senkrechte Faser zählt Nullstellen",
    caption: "Die gestrichelte Gerade hält a fest. Ihre markierten Schnitte mit V sind die Nullstellen von x ↦ F(a,x).",
    explanation: "",
    formula: "Vₐ = πₐ⁻¹(a) = {x ∈ ℝ ∣ F(a,x)=0}",
    reading: "Eine Parameterfaser sammelt alle Zustände x, die zum gewählten a die Bedingung F=0 erfüllen.",
    lean: "theorem parameterFiber_of_pos {a : ℝ} (ha : 0 < a) : {x | F a x = 0} = {0, √a, -√a}",
    leanReading: "Lean beweist die drei Fälle a<0, a=0 und a>0 getrennt und exakt.",
    next: "Weiter: auf x projizieren →"
  },
  4: {
    kicker: "Schritt 4 · Projektion πₓ",
    title: "Die umgekehrte Faser entdeckt eine Ausnahme",
    caption: "Die gestrichelte Gerade hält x fest. Bei x=0 gehört jeder Parameter zur Faser; sonst nur a=x².",
    explanation: "",
    formula: "Vˣ = πₓ⁻¹(x) = {a ∈ ℝ ∣ F(a,x)=0}",
    reading: "Jetzt wird nicht nach Zuständen pro Parameter, sondern nach Parametern pro Zustand gefragt.",
    lean: "theorem stateFiber_of_ne_zero {x : ℝ} (hx : x ≠ 0) : {a | F a x = 0} = {x ^ 2}",
    leanReading: "Der Sonderfall x=0 wird separat als gesamte reelle Achse formalisiert.",
    next: "Forschungsweg abgeschlossen"
  }
};

let currentStep = 1;
let parameterA = 0;
let stateX = 0;

const main = document.getElementById("main-plot");
const fiber = document.getElementById("fiber-plot");
const slider = document.getElementById("fiber-slider");
const output = document.getElementById("slider-output");

const dims = { width: 720, height: 520, left: 72, right: 28, top: 26, bottom: 66 };
const domains = { a: [-2, 4], x: [-2.5, 2.5] };
const plotWidth = dims.width - dims.left - dims.right;
const plotHeight = dims.height - dims.top - dims.bottom;

function sx(a) {
  return dims.left + ((a - domains.a[0]) / (domains.a[1] - domains.a[0])) * plotWidth;
}

function sy(x) {
  return dims.top + ((domains.x[1] - x) / (domains.x[1] - domains.x[0])) * plotHeight;
}

function el(name, attrs = {}, text = "") {
  const node = document.createElementNS(NS, name);
  Object.entries(attrs).forEach(([key, value]) => node.setAttribute(key, String(value)));
  if (text) node.textContent = text;
  return node;
}

function clear(svg) {
  while (svg.firstChild) svg.removeChild(svg.firstChild);
}

function format(value) {
  return value.toLocaleString("de-DE", { minimumFractionDigits: 1, maximumFractionDigits: 1 });
}

function drawGrid(svg, xScale, yScale, xTicks, yTicks, labels) {
  xTicks.forEach(value => {
    const x = xScale(value);
    svg.appendChild(el("line", { x1: x, x2: x, y1: dims.top, y2: dims.height - dims.bottom, class: "grid-line" }));
    svg.appendChild(el("text", { x, y: dims.height - dims.bottom + 24, "text-anchor": "middle", class: "tick-label" }, String(value)));
  });
  yTicks.forEach(value => {
    const y = yScale(value);
    svg.appendChild(el("line", { x1: dims.left, x2: dims.width - dims.right, y1: y, y2: y, class: "grid-line" }));
    svg.appendChild(el("text", { x: dims.left - 14, y: y + 5, "text-anchor": "end", class: "tick-label" }, String(value)));
  });
  svg.appendChild(el("line", { x1: dims.left, x2: dims.width - dims.right, y1: yScale(0), y2: yScale(0), class: "axis" }));
  svg.appendChild(el("line", { x1: xScale(0), x2: xScale(0), y1: dims.top, y2: dims.height - dims.bottom, class: "axis" }));
  svg.appendChild(el("text", { x: dims.left + plotWidth / 2, y: dims.height - 16, "text-anchor": "middle", class: "axis-label" }, labels.x));
  const yLabel = el("text", { x: 18, y: dims.top + plotHeight / 2, "text-anchor": "middle", class: "axis-label", transform: `rotate(-90 18 ${dims.top + plotHeight / 2})` }, labels.y);
  svg.appendChild(yLabel);
}

function drawHeatmap() {
  const columns = 54;
  const rows = 46;
  const cellW = plotWidth / columns + 0.5;
  const cellH = plotHeight / rows + 0.5;
  for (let row = 0; row < rows; row += 1) {
    for (let col = 0; col < columns; col += 1) {
      const a = domains.a[0] + ((col + 0.5) / columns) * (domains.a[1] - domains.a[0]);
      const x = domains.x[1] - ((row + 0.5) / rows) * (domains.x[1] - domains.x[0]);
      const value = x ** 3 - a * x;
      main.appendChild(el("rect", {
        x: dims.left + col * (plotWidth / columns),
        y: dims.top + row * (plotHeight / rows),
        width: cellW,
        height: cellH,
        fill: value >= 0 ? "#d9edf6" : "#fae3d5",
        opacity: Math.min(0.9, 0.42 + Math.abs(value) / 18)
      }));
    }
  }
}

function drawLocus(svg, emphasize = true) {
  svg.appendChild(el("line", { x1: sx(domains.a[0]), x2: sx(domains.a[1]), y1: sy(0), y2: sy(0), class: "zero-axis", opacity: emphasize ? 1 : .45 }));
  const points = [];
  for (let x = domains.x[0]; x <= domains.x[1] + .001; x += .025) {
    const a = x * x;
    if (a >= domains.a[0] && a <= domains.a[1]) points.push(`${sx(a)},${sy(x)}`);
  }
  svg.appendChild(el("polyline", { points: points.join(" "), class: "zero-locus", opacity: emphasize ? 1 : .45 }));
  if (emphasize) {
    svg.appendChild(el("text", { x: sx(2.65), y: sy(1.72) - 10, class: "plot-label" }, "a = x²"));
    if (currentStep !== 4) {
      svg.appendChild(el("text", { x: sx(-1.65), y: sy(0) - 12, class: "plot-label" }, "x = 0"));
    }
    svg.appendChild(el("circle", { cx: sx(0), cy: sy(0), r: 7, fill: "#10233f" }));
    svg.appendChild(el("text", { x: sx(0) + 12, y: sy(0) + 24, class: "plot-label" }, "kritischer Punkt (0,0)"));
  }
}

function rootsFor(a) {
  if (a > 1e-9) return [-Math.sqrt(a), 0, Math.sqrt(a)];
  return [0];
}

function drawParameterFiber() {
  const px = sx(parameterA);
  main.appendChild(el("line", { x1: px, x2: px, y1: dims.top, y2: dims.height - dims.bottom, class: "fiber-line" }));
  rootsFor(parameterA).forEach(root => {
    main.appendChild(el("circle", { cx: px, cy: sy(root), r: 9, class: "fiber-point" }));
  });
  main.appendChild(el("text", { x: px + 10, y: dims.top + 22, class: "plot-label" }, `a = ${format(parameterA)}`));
}

function drawStateFiber() {
  const py = sy(stateX);
  main.appendChild(el("line", { x1: dims.left, x2: dims.width - dims.right, y1: py, y2: py, class: "fiber-line" }));
  if (Math.abs(stateX) < 1e-9) {
    for (let i = 0; i < 7; i += 1) {
      const a = domains.a[0] + (i / 6) * (domains.a[1] - domains.a[0]);
      main.appendChild(el("circle", { cx: sx(a), cy: py, r: 6, class: "fiber-point" }));
    }
    main.appendChild(el("text", { x: sx(-1.7), y: py - 16, class: "plot-label" }, "alle a ∈ ℝ"));
  } else {
    const a = stateX ** 2;
    if (a <= domains.a[1]) main.appendChild(el("circle", { cx: sx(a), cy: py, r: 9, class: "fiber-point" }));
    main.appendChild(el("text", { x: Math.min(sx(a) + 12, dims.width - 150), y: py - 14, class: "plot-label" }, `a = x² = ${format(a)}`));
  }
  main.appendChild(el("text", { x: dims.left + 10, y: py + (stateX > 1.9 ? 22 : -12), class: "plot-label" }, `x = ${format(stateX)}`));
}

function drawMain() {
  clear(main);
  main.appendChild(el("title", { id: "main-plot-title" }, "Parameter-Zustands-Diagramm"));
  main.appendChild(el("desc", { id: "main-plot-desc" }, "Horizontale Achse Parameter a, vertikale Achse Zustand x; visualisiert werden Vorzeichen, Nullstellenmenge oder Fasern."));
  if (currentStep === 1) drawHeatmap();
  drawGrid(main, sx, sy, [-2, -1, 0, 1, 2, 3, 4], [-2, -1, 0, 1, 2], { x: "Parameter a", y: "Zustand x" });
  if (currentStep >= 2) drawLocus(main, true);
  if (currentStep === 1) {
    main.appendChild(el("text", { x: sx(2.7), y: sy(2.05), class: "plot-label" }, "F(a,x) > 0"));
    main.appendChild(el("text", { x: sx(2.7), y: sy(1.15), class: "plot-label" }, "F(a,x) < 0"));
  }
  if (currentStep === 3) drawParameterFiber();
  if (currentStep === 4) drawStateFiber();
}

function drawFiberGraph() {
  clear(fiber);
  fiber.appendChild(el("title", { id: "fiber-plot-title" }, "Funktionsgraph einer Parameterfaser"));
  fiber.appendChild(el("desc", { id: "fiber-plot-desc" }, `Graph von x ↦ F(a,x) für a = ${format(parameterA)} mit markierten Nullstellen.`));
  const d = { width: 470, height: 360, left: 58, right: 20, top: 24, bottom: 54 };
  const xMin = -2.5, xMax = 2.5, yMin = -12, yMax = 12;
  const fx = x => d.left + ((x - xMin) / (xMax - xMin)) * (d.width - d.left - d.right);
  const fy = y => d.top + ((yMax - y) / (yMax - yMin)) * (d.height - d.top - d.bottom);
  [-2, -1, 0, 1, 2].forEach(value => {
    fiber.appendChild(el("line", { x1: fx(value), x2: fx(value), y1: d.top, y2: d.height - d.bottom, class: "grid-line" }));
    fiber.appendChild(el("text", { x: fx(value), y: d.height - d.bottom + 22, "text-anchor": "middle", class: "tick-label" }, String(value)));
  });
  [-10, -5, 0, 5, 10].forEach(value => {
    fiber.appendChild(el("line", { x1: d.left, x2: d.width - d.right, y1: fy(value), y2: fy(value), class: "grid-line" }));
    fiber.appendChild(el("text", { x: d.left - 10, y: fy(value) + 5, "text-anchor": "end", class: "tick-label" }, String(value)));
  });
  fiber.appendChild(el("line", { x1: d.left, x2: d.width - d.right, y1: fy(0), y2: fy(0), class: "zero-reference" }));
  fiber.appendChild(el("line", { x1: fx(0), x2: fx(0), y1: d.top, y2: d.height - d.bottom, class: "axis" }));
  const points = [];
  for (let x = xMin; x <= xMax + .001; x += .025) {
    const y = x ** 3 - parameterA * x;
    points.push(`${fx(x)},${fy(Math.max(yMin, Math.min(yMax, y)))}`);
  }
  fiber.appendChild(el("polyline", { points: points.join(" "), class: "function-path" }));
  rootsFor(parameterA).forEach(root => fiber.appendChild(el("circle", { cx: fx(root), cy: fy(0), r: 8, class: "fiber-point" })));
  fiber.appendChild(el("text", { x: d.left + (d.width - d.left - d.right) / 2, y: d.height - 12, "text-anchor": "middle", class: "axis-label" }, "Zustand x"));
  const yLabel = el("text", { x: 16, y: d.top + (d.height - d.top - d.bottom) / 2, "text-anchor": "middle", class: "axis-label", transform: `rotate(-90 16 ${d.top + (d.height - d.top - d.bottom) / 2})` }, "Funktionswert F(a,x)");
  fiber.appendChild(yLabel);
}

function parameterExplanation() {
  const count = parameterA > 0 ? 3 : 1;
  const caseText = parameterA < 0
    ? "Für a<0 ist x²=a unmöglich, weil ein Quadrat nie negativ ist."
    : parameterA > 0
      ? "Für a>0 liefert x²=a zwei zusätzliche Lösungen: ±√a."
      : "Bei a=0 fallen die drei algebraischen Äste in x=0 zusammen.";
  const roots = rootsFor(parameterA).map(format).join("; ");
  const countText = count === 1 ? "genau einem Punkt" : "drei verschiedenen Punkten";
  return `<p>Die senkrechte Linie schneidet <span class="formula">V</span> in <strong>${countText}</strong>: <span class="formula">{${roots}}</span>.</p><p class="observation"><strong>Warum?</strong> ${caseText} Der Wert <span class="formula">a=0</span> ist daher ein Bifurkationswert.</p>`;
}

function stateExplanation() {
  if (Math.abs(stateX) < 1e-9) {
    return `<p>Für <span class="formula">x=0</span> gilt <span class="formula">F(a,0)=0</span> für <strong>jedes</strong> reelle a. Die Faser ist eine ganze Gerade.</p><p class="observation"><strong>Forschungsfund:</strong> Dieselbe Menge V besitzt unter der zweiten Projektion eine außergewöhnliche Faser. Projektionen bewahren also unterschiedliche Informationen.</p>`;
  }
  return `<p>Für <span class="formula">x=${format(stateX)}</span> bleibt nach Division durch x die Gleichung <span class="formula">a=x²=${format(stateX ** 2)}</span>. Die Faser enthält genau einen Parameter.</p><p class="observation"><strong>Vergleich mit x=0:</strong> Bewege den Regler auf 0. Dort darf man nicht durch x teilen – und die Faser springt von einem Punkt zu einer ganzen Geraden.</p>`;
}

function legendItems() {
  if (currentStep === 1) return [
    ["#d9edf6", "F(a,x) > 0"],
    ["#fae3d5", "F(a,x) < 0"],
    ["#526274", "Achsen / Grenze F=0", true]
  ];
  const base = [["#d26535", "Ast a=x²", true], ["#24755d", "Ast x=0", true]];
  if (currentStep >= 3) base.push(["#6c52a2", currentStep === 3 ? "gewählte a-Faser und Nullstellen" : "gewählte x-Faser und Parameter", true]);
  return base;
}

function renderLegend() {
  const legend = document.getElementById("legend");
  legend.innerHTML = legendItems().map(([color, label, line]) => `<span class="legend-item"><i class="swatch${line ? " line" : ""}" style="background:${color}" aria-hidden="true"></i>${label}</span>`).join("");
}

function renderStage() {
  const stage = stages[currentStep];
  document.getElementById("stage-kicker").textContent = stage.kicker;
  document.getElementById("stage-title").textContent = stage.title;
  document.getElementById("main-caption").textContent = stage.caption;
  document.getElementById("logic-formula").textContent = stage.formula;
  document.getElementById("logic-reading").textContent = stage.reading;
  document.getElementById("lean-theorem").textContent = stage.lean;
  document.getElementById("lean-reading").textContent = stage.leanReading;
  document.getElementById("explanation").innerHTML = currentStep === 3 ? parameterExplanation() : currentStep === 4 ? stateExplanation() : stage.explanation;

  document.querySelectorAll(".step").forEach(button => {
    const active = Number(button.dataset.step) === currentStep;
    button.classList.toggle("active", active);
    if (active) button.setAttribute("aria-current", "step"); else button.removeAttribute("aria-current");
  });

  const controls = document.getElementById("control-wrap");
  const fiberFigure = document.getElementById("fiber-figure");
  controls.hidden = currentStep < 3;
  fiberFigure.hidden = currentStep !== 3;
  if (currentStep === 3) {
    document.getElementById("slider-label").textContent = "Parameter a";
    slider.min = "-2"; slider.max = "4"; slider.step = ".1"; slider.value = String(parameterA);
    output.textContent = format(parameterA);
    drawFiberGraph();
  } else if (currentStep === 4) {
    document.getElementById("slider-label").textContent = "Zustand x";
    slider.min = "-2"; slider.max = "2"; slider.step = ".1"; slider.value = String(stateX);
    output.textContent = format(stateX);
  }

  const prev = document.getElementById("prev-step");
  const next = document.getElementById("next-step");
  prev.disabled = currentStep === 1;
  next.disabled = currentStep === 4;
  next.textContent = stage.next;
  drawMain();
  renderLegend();
}

document.querySelectorAll(".step").forEach(button => button.addEventListener("click", () => {
  currentStep = Number(button.dataset.step);
  renderStage();
}));

document.getElementById("prev-step").addEventListener("click", () => {
  if (currentStep > 1) { currentStep -= 1; renderStage(); }
});

document.getElementById("next-step").addEventListener("click", () => {
  if (currentStep < 4) { currentStep += 1; renderStage(); }
});

slider.addEventListener("input", () => {
  const value = Number(slider.value);
  if (currentStep === 3) parameterA = value;
  if (currentStep === 4) stateX = value;
  output.textContent = format(value);
  renderStage();
});

renderStage();
