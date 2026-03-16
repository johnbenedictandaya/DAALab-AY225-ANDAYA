/* ═══════════════════════════════════════════════════════════════
   Travelling Salesman Problem – Node Map & Shortest Path
   Algorithm: Dijkstra's (for distance / time / fuel)
   ═══════════════════════════════════════════════════════════════ */

// ── 1. Raw Edge Data ──────────────────────────────────────────
const RAW_EDGES = [
  { from: "IMUS",     to: "BACOOR",   distance: 10, time: 15, fuel: 1.2 },
  { from: "BACOOR",   to: "DASMA",    distance: 12, time: 25, fuel: 1.5 },
  { from: "DASMA",    to: "KAWIT",    distance: 12, time: 25, fuel: 1.5 },
  { from: "KAWIT",    to: "INDANG",   distance: 12, time: 25, fuel: 1.2 },
  { from: "INDANG",   to: "SILANG",   distance: 14, time: 25, fuel: 1.5 },
  { from: "SILANG",   to: "GENTRI",   distance: 10, time: 25, fuel: 1.3 },
  { from: "GENTRI",   to: "NOVELETA", distance: 10, time: 25, fuel: 1.5 },
  { from: "NOVELETA", to: "IMUS",     distance: 10, time: 15, fuel: 1.2 },
  { from: "BACOOR",   to: "SILANG",   distance: 10, time: 25, fuel: 1.3 },
  { from: "DASMA",    to: "SILANG",   distance: 12, time: 25, fuel: 1.5 },
  { from: "SILANG",   to: "BACOOR",   distance: 10, time: 25, fuel: 1.3 },
  { from: "NOVELETA", to: "BACOOR",   distance: 10, time: 15, fuel: 1.2 },
  { from: "SILANG",   to: "KAWIT",    distance: 14, time: 25, fuel: 1.2 },
  { from: "IMUS",     to: "NOVELETA", distance: 10, time: 15, fuel: 1.2 },
];

// ── 2. Build Graph ────────────────────────────────────────────
const NODES = [...new Set(RAW_EDGES.flatMap(e => [e.from, e.to]))].sort();

// Adjacency list: graph[node] = [ {to, distance, time, fuel}, ... ]
const graph = {};
NODES.forEach(n => (graph[n] = []));
RAW_EDGES.forEach(e => {
  graph[e.from].push({ to: e.to,   distance: e.distance, time: e.time, fuel: e.fuel });
});

// ── 3. Dijkstra's Algorithm ───────────────────────────────────
/**
 * Returns { path: [...nodes], cost, steps: [...edge objects] }
 * or null if no path.
 */
function dijkstra(start, end, criteria) {
  const dist   = {};   // best cost to reach each node
  const prev   = {};   // previous node on best path
  const prevEdge = {}; // edge used to arrive
  const visited = new Set();

  NODES.forEach(n => { dist[n] = Infinity; prev[n] = null; prevEdge[n] = null; });
  dist[start] = 0;

  // Simple priority-queue via sorted array (fine for small graphs)
  const pq = [{ node: start, cost: 0 }];

  while (pq.length) {
    // Extract minimum
    pq.sort((a, b) => a.cost - b.cost);
    const { node: u } = pq.shift();

    if (visited.has(u)) continue;
    visited.add(u);

    if (u === end) break;

    for (const edge of graph[u]) {
      if (visited.has(edge.to)) continue;
      const newCost = dist[u] + edge[criteria];
      if (newCost < dist[edge.to]) {
        dist[edge.to] = newCost;
        prev[edge.to] = u;
        prevEdge[edge.to] = edge;
        pq.push({ node: edge.to, cost: newCost });
      }
    }
  }

  if (dist[end] === Infinity) return null;

  // Reconstruct path
  const path  = [];
  const steps = [];
  let cur = end;
  while (cur !== null) {
    path.unshift(cur);
    if (prevEdge[cur]) steps.unshift({ from: prev[cur], ...prevEdge[cur] });
    cur = prev[cur];
  }

  return { path, cost: dist[end], steps };
}

// ── 4. Populate Selects & Edge Table ─────────────────────────
function populateUI() {
  const startSel = document.getElementById("startNode");
  const endSel   = document.getElementById("endNode");

  NODES.forEach(n => {
    startSel.add(new Option(n, n));
    endSel.add(new Option(n, n));
  });
  // Default different nodes
  endSel.value = NODES[NODES.length - 1] !== NODES[0] ? NODES[NODES.length - 1] : NODES[1];

  // Edge table
  const tbody = document.getElementById("edgeBody");
  RAW_EDGES.forEach(e => {
    const tr = document.createElement("tr");
    tr.innerHTML = `<td>${e.from}</td><td>${e.to}</td>
      <td>${e.distance}</td><td>${e.time}</td><td>${e.fuel}</td>`;
    tbody.appendChild(tr);
  });
}

// ── 5. Canvas Graph Drawing ───────────────────────────────────
const canvas  = document.getElementById("graphCanvas");
const ctx     = canvas.getContext("2d");
const tooltip = document.getElementById("tooltip");

// Fixed layout positions (normalized 0–1, mapped to canvas)
const NODE_POS = {
  IMUS:     { x: 0.18, y: 0.50 },
  BACOOR:   { x: 0.38, y: 0.22 },
  NOVELETA: { x: 0.18, y: 0.75 },
  DASMA:    { x: 0.58, y: 0.18 },
  KAWIT:    { x: 0.72, y: 0.38 },
  INDANG:   { x: 0.88, y: 0.55 },
  SILANG:   { x: 0.68, y: 0.65 },
  GENTRI:   { x: 0.45, y: 0.82 },
};

let activePath = [];   // nodes in the current highlighted path

function getXY(name) {
  const p = NODE_POS[name];
  return { x: p.x * canvas.width, y: p.y * canvas.height };
}

function drawArrow(x1, y1, x2, y2, color, width) {
  const headLen = 10;
  const angle   = Math.atan2(y2 - y1, x2 - x1);

  // Shorten to not overlap node circles
  const R = 20;
  const sx = x1 + R * Math.cos(angle);
  const sy = y1 + R * Math.sin(angle);
  const ex = x2 - R * Math.cos(angle);
  const ey = y2 - R * Math.sin(angle);

  ctx.beginPath();
  ctx.moveTo(sx, sy);
  ctx.lineTo(ex, ey);
  ctx.strokeStyle = color;
  ctx.lineWidth   = width;
  ctx.stroke();

  // Arrowhead
  ctx.beginPath();
  ctx.moveTo(ex, ey);
  ctx.lineTo(ex - headLen * Math.cos(angle - Math.PI / 7),
             ey - headLen * Math.sin(angle - Math.PI / 7));
  ctx.lineTo(ex - headLen * Math.cos(angle + Math.PI / 7),
             ey - headLen * Math.sin(angle + Math.PI / 7));
  ctx.closePath();
  ctx.fillStyle = color;
  ctx.fill();
}

function isInActivePath(from, to) {
  for (let i = 0; i < activePath.length - 1; i++) {
    if (activePath[i] === from && activePath[i + 1] === to) return true;
  }
  return false;
}

function drawGraph() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // Draw edges
  RAW_EDGES.forEach(e => {
    const a = getXY(e.from);
    const b = getXY(e.to);
    const inPath = isInActivePath(e.from, e.to);
    const color  = inPath ? "#9b59f5" : "#444466";
    const width  = inPath ? 2.5 : 1.2;
    drawArrow(a.x, a.y, b.x, b.y, color, width);

    // Edge label (midpoint)
    const mx = (a.x + b.x) / 2;
    const my = (a.y + b.y) / 2;
    const angle = Math.atan2(b.y - a.y, b.x - a.x);
    const offset = 12;

    ctx.save();
    ctx.font = "bold 10px 'Segoe UI', sans-serif";
    ctx.fillStyle = inPath ? "#c084fc" : "#666699";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    // perpendicular offset so label doesn't sit on the line
    ctx.fillText(
      `${e.distance}km`,
      mx - offset * Math.sin(angle),
      my + offset * Math.cos(angle)
    );
    ctx.restore();
  });

  // Draw nodes
  NODES.forEach(name => {
    const { x, y } = getXY(name);
    const inPath   = activePath.includes(name);

    // Outer glow for path nodes
    if (inPath) {
      ctx.beginPath();
      ctx.arc(x, y, 28, 0, Math.PI * 2);
      ctx.fillStyle = "rgba(155,89,245,0.15)";
      ctx.fill();
    }

    // Circle
    ctx.beginPath();
    ctx.arc(x, y, 20, 0, Math.PI * 2);
    ctx.fillStyle   = inPath ? "#9b59f5" : "#1e1e2e";
    ctx.strokeStyle = inPath ? "#c084fc" : "#5a5a8a";
    ctx.lineWidth   = inPath ? 2.5 : 1.5;
    ctx.fill();
    ctx.stroke();

    // Label
    ctx.font        = "bold 11px 'Segoe UI', sans-serif";
    ctx.fillStyle   = inPath ? "#fff" : "#c0c0e0";
    ctx.textAlign   = "center";
    ctx.textBaseline = "middle";
    ctx.fillText(name, x, y);
  });
}

function resizeCanvas() {
  const wrap = canvas.parentElement;
  canvas.width  = wrap.clientWidth;
  canvas.height = 460;
  drawGraph();
}

// ── 6. Tooltip on hover ───────────────────────────────────────
canvas.addEventListener("mousemove", e => {
  const rect   = canvas.getBoundingClientRect();
  const mx     = (e.clientX - rect.left) * (canvas.width  / rect.width);
  const my     = (e.clientY - rect.top)  * (canvas.height / rect.height);
  let   found  = null;

  // Check if mouse near any edge midpoint
  RAW_EDGES.forEach(edge => {
    const a   = getXY(edge.from);
    const b   = getXY(edge.to);
    const mid = { x: (a.x + b.x) / 2, y: (a.y + b.y) / 2 };
    const d   = Math.hypot(mx - mid.x, my - mid.y);
    if (d < 18) found = edge;
  });

  if (found) {
    tooltip.innerHTML =
      `<b>${found.from} → ${found.to}</b><br>
       📏 ${found.distance} km &nbsp; ⏱ ${found.time} mins &nbsp; ⛽ ${found.fuel} L`;
    tooltip.style.left = (e.clientX - rect.left + 12) + "px";
    tooltip.style.top  = (e.clientY - rect.top  - 10) + "px";
    tooltip.classList.remove("hidden");
  } else {
    tooltip.classList.add("hidden");
  }
});
canvas.addEventListener("mouseleave", () => tooltip.classList.add("hidden"));

// ── 7. Find Path Handler ──────────────────────────────────────
document.getElementById("findBtn").addEventListener("click", () => {
  const start    = document.getElementById("startNode").value;
  const end      = document.getElementById("endNode").value;
  const criteria = document.getElementById("criteria").value;

  const resultDiv  = document.getElementById("result");
  const noPathDiv  = document.getElementById("no-path");

  resultDiv.classList.add("hidden");
  noPathDiv.classList.add("hidden");
  activePath = [];

  if (start === end) {
    noPathDiv.querySelector("span").textContent =
      "⚠ Start and End nodes must be different.";
    noPathDiv.classList.remove("hidden");
    drawGraph();
    return;
  }

  const result = dijkstra(start, end, criteria);

  if (!result) {
    noPathDiv.querySelector("span").textContent =
      `⚠ No path found from ${start} to ${end}.`;
    noPathDiv.classList.remove("hidden");
    activePath = [];
    drawGraph();
    return;
  }

  activePath = result.path;
  drawGraph();

  // Compute all totals (not just the optimized criterion)
  const totals = result.steps.reduce(
    (acc, s) => {
      acc.distance += s.distance;
      acc.time     += s.time;
      acc.fuel     += s.fuel;
      return acc;
    },
    { distance: 0, time: 0, fuel: 0 }
  );

  // Title
  document.getElementById("result-title").textContent =
    `Shortest path from ${start} to ${end} (optimized by ${criteria})`;

  // Path nodes
  const pathRow = document.getElementById("path-display");
  pathRow.innerHTML = "";
  result.path.forEach((node, i) => {
    if (i > 0) {
      const arr = document.createElement("span");
      arr.className = "path-arrow";
      arr.textContent = " → ";
      pathRow.appendChild(arr);
    }
    const span = document.createElement("span");
    span.className = "path-node";
    span.textContent = node;
    pathRow.appendChild(span);
  });

  // Stats
  const criteriaLabel = { distance: "Distance", time: "Time", fuel: "Fuel" }[criteria];
  const criteriaUnit  = { distance: "km",        time: "mins", fuel: "L"   }[criteria];
  document.getElementById("stats-display").innerHTML = `
    <div class="stat-chip ${criteria === 'distance' ? 'highlight' : ''}">
      <span class="label">Total Distance</span>
      <span class="value">${totals.distance} km</span>
    </div>
    <div class="stat-chip ${criteria === 'time' ? 'highlight' : ''}">
      <span class="label">Total Time</span>
      <span class="value">${totals.time} mins</span>
    </div>
    <div class="stat-chip ${criteria === 'fuel' ? 'highlight' : ''}">
      <span class="label">Total Fuel</span>
      <span class="value">${totals.fuel.toFixed(1)} L</span>
    </div>
    <div class="stat-chip">
      <span class="label">Hops</span>
      <span class="value">${result.steps.length}</span>
    </div>
  `;

  // Steps table
  const tbody = document.getElementById("steps-body");
  tbody.innerHTML = "";
  result.steps.forEach((s, i) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${i + 1}</td>
      <td>${s.from}</td>
      <td>${s.to}</td>
      <td>${s.distance}</td>
      <td>${s.time}</td>
      <td>${s.fuel}</td>
    `;
    tbody.appendChild(tr);
  });

  // Footer totals
  document.getElementById("steps-foot").innerHTML = `
    <tr>
      <td colspan="3">TOTAL</td>
      <td>${totals.distance} km</td>
      <td>${totals.time} mins</td>
      <td>${totals.fuel.toFixed(1)} L</td>
    </tr>
  `;

  resultDiv.classList.remove("hidden");
  resultDiv.scrollIntoView({ behavior: "smooth", block: "nearest" });
});

// ── 8. Reset Handler ──────────────────────────────────────────
document.getElementById("resetBtn").addEventListener("click", () => {
  activePath = [];
  drawGraph();
  document.getElementById("result").classList.add("hidden");
  document.getElementById("no-path").classList.add("hidden");
  document.getElementById("startNode").selectedIndex = 0;
  document.getElementById("endNode").selectedIndex   = 0;
  document.getElementById("criteria").selectedIndex  = 0;
});

// ── 9. Init ───────────────────────────────────────────────────
populateUI();
window.addEventListener("resize", resizeCanvas);
resizeCanvas();