'use strict';

/* ── CONSTANTS ──────────────────────────────────────────────── */

const DATASETS = {
  train: { file: 'archive/fashion-mnist_train.csv', label: 'Training Set (60k)', estimatedRows: 60000 },
  test:  { file: 'archive/fashion-mnist_test.csv',  label: 'Test Set (10k)',      estimatedRows: 10000 }
};

const CLASS_NAMES = [
  'T-shirt/Top', 'Trouser', 'Pullover', 'Dress', 'Coat',
  'Sandal',      'Shirt',   'Sneaker',  'Bag',   'Ankle Boot'
];

const CLASS_COLORS = [
  '#00ffa3', '#38bdf8', '#a78bfa', '#ffb300', '#ff4c8b',
  '#34d399', '#f97316', '#818cf8', '#fb923c', '#22d3ee'
];

/** Maximum scatter-plot points regardless of dataset size. */
const SCATTER_MAX = 500;

/* ── APPLICATION STATE ──────────────────────────────────────── */

let ACTIVE_DATASET = 'test';

/**
 * allRows: Array<{ label:number, pixels:Uint8Array }>
 * Kept flat for compatibility with filter/sort/table code.
 */
let allRows  = [];
let rowCount = 0;

/** Chart.js instances */
let chartBar     = null;
let chartScatter = null;

/**
 * cachedStats — populated by calculateStatsSinglePass after load.
 * All downstream rendering reads from here; no re-scan of allRows.
 * Shape: Array<{ label, name, count, mean, stdDev, variance, pearson }>
 */
let cachedStats = null;

/* ════════════════════════════════════════════════════════════════
   PERFORMANCE UTILITIES
   ════════════════════════════════════════════════════════════════ */

/**
 * reservoirSample(arr, k)
 * Returns a new array of min(k, arr.length) items chosen uniformly
 * at random via reservoir sampling.  O(n) time, O(k) space.
 */
function reservoirSample(arr, k) {
  const n = arr.length;
  if (k >= n) return arr.slice();
  const result = arr.slice(0, k);
  for (let i = k; i < n; i++) {
    const j = (Math.random() * (i + 1)) | 0;
    if (j < k) result[j] = arr[i];
  }
  return result;
}

/**
 * makeImageCanvas — optimised.
 * Draws at native 28×28 (784-pixel loop) then relies on CSS
 * width/height for the visual 2× upscale.  GPU compositing handles
 * the scaling for free; `translateZ(0)` promotes to its own layer.
 */
function makeImageCanvas(pixels) {
  const SIZE   = 28;
  const canvas = document.createElement('canvas');
  canvas.width  = SIZE;
  canvas.height = SIZE;
  canvas.style.width          = `${SIZE * 2}px`;
  canvas.style.height         = `${SIZE * 2}px`;
  canvas.style.imageRendering = 'pixelated';
  canvas.style.transform      = 'translateZ(0)';

  const ctx  = canvas.getContext('2d');
  const imgd = ctx.createImageData(SIZE, SIZE);
  const buf  = imgd.data;  // Uint8ClampedArray, 784 × 4 bytes

  // Single flat loop — no nested loops, no branching
  for (let i = 0; i < 784; i++) {
    const v   = pixels[i];
    const off = i << 2;   // i * 4
    buf[off]     = v;
    buf[off + 1] = v;
    buf[off + 2] = v;
    buf[off + 3] = 255;
  }

  ctx.putImageData(imgd, 0, 0);
  return canvas;
}

/** arrayMean — used only on small arrays (10-element stat vectors). */
function arrayMean(arr) {
  let s = 0;
  for (let i = 0; i < arr.length; i++) s += arr[i];
  return arr.length ? s / arr.length : 0;
}

/* ── UI helpers ─────────────────────────────────────────────── */

function setOverlay(visible, pct = 0, message = '') {
  document.getElementById('loadingOverlay').classList.toggle('visible', visible);
  document.getElementById('progressFill').style.width = `${pct}%`;
  document.getElementById('loadingMsg').textContent   = message;
}

function setStatus(state, text) {
  document.getElementById('statusDot').className     = `status-indicator ${state}`;
  document.getElementById('statusLabel').textContent = text;
}

function initPixelGrid() {
  const grid = document.getElementById('pixelGrid');
  grid.innerHTML = '';
  for (let i = 0; i < 49; i++) {
    const cell = document.createElement('div');
    cell.className = 'pixel-cell';
    cell.style.setProperty('--dur',   `${(0.6 + Math.random() * 1.2).toFixed(2)}s`);
    cell.style.setProperty('--delay', `${(Math.random() * 1.0).toFixed(2)}s`);
    grid.appendChild(cell);
  }
}

function setActiveNav(sectionId) {
  document.querySelectorAll('.nav-link').forEach(link => {
    link.classList.toggle('active', link.dataset.section === sectionId);
  });
  const titleMap = {
    'sec-overview':   'Overview',   'sec-charts':     'Charts',
    'sec-statistics': 'Statistics', 'sec-dataset':    'Dataset',
    'sec-insights':   'Insights'
  };
  const el = document.getElementById('bcCurrent');
  if (el && titleMap[sectionId]) el.textContent = titleMap[sectionId];
}

function toggleSidebar() {
  document.getElementById('sidebar').classList.toggle('open');
}

/* ════════════════════════════════════════════════════════════════
   MODULE 1 — STUDENT 1
   ════════════════════════════════════════════════════════════════ */

/* ─────────────────────────────────────────────────────────────
   selectDataset(key)
   Updates ACTIVE_DATASET, syncs UI, wipes stale data + charts.
───────────────────────────────────────────────────────────── */
function selectDataset(key) {
  if (!DATASETS[key]) return;
  ACTIVE_DATASET = key;
  const ds = DATASETS[key];

  document.getElementById('dsTrainBtn').classList.toggle('active', key === 'train');
  document.getElementById('dsTestBtn').classList.toggle('active',  key === 'test');
  document.getElementById('activePathLabel').textContent = ds.file;
  document.getElementById('loadingPath').textContent     = ds.file;

  allRows     = [];
  rowCount    = 0;
  cachedStats = null;
  setStatus('idle', `${ds.label} selected — load to begin`);

  ['stat-total', 'stat-avgpixel'].forEach(id => {
    const el = document.getElementById(id);
    if (el) { el.textContent = '—'; el.classList.remove('loaded'); }
  });
  const bt = document.getElementById('bar-total');
  const ba = document.getElementById('bar-avgpixel');
  if (bt) bt.style.width = '0%';
  if (ba) ba.style.width = '0%';

  document.getElementById('tableBody').innerHTML =
    `<tr><td colspan="7" class="placeholder-row">Click <strong>Load Dataset</strong> to begin…</td></tr>`;
  document.getElementById('analysisTableBody').innerHTML =
    `<tr><td colspan="7" class="placeholder-row">Load the dataset to compute statistics…</td></tr>`;
  document.getElementById('tableInfo').textContent = '—';
  document.getElementById('insightsContainer').innerHTML = `
    <div class="insight-placeholder">
      <svg width="48" height="48" viewBox="0 0 24 24" fill="none" opacity=".3">
        <path d="M12 2a7 7 0 0 1 7 7c0 3-1.8 5.5-4.3 6.7V18H9.3v-2.3C6.8 14.5 5 12 5 9a7 7 0 0 1 7-7z"
              stroke="currentColor" stroke-width="1.5"/>
        <rect x="9" y="19" width="6" height="1.5" rx=".75" fill="currentColor"/>
        <rect x="10" y="21" width="4" height="1" rx=".5" fill="currentColor"/>
      </svg>
      <p>Insights will appear here after loading the dataset.</p>
    </div>`;

  if (chartBar)     { chartBar.destroy();     chartBar     = null; }
  if (chartScatter) { chartScatter.destroy(); chartScatter = null; }
}

/* ─────────────────────────────────────────────────────────────
   loadDataset()
   ──────────────────────────────────────────────────────────
   Streams CSV off the main thread (worker:true).
   On complete, uses a two-frame rAF pipeline so the browser
   paints the "done" state before starting heavy work.
───────────────────────────────────────────────────────────── */
function loadDataset() {
  const ds = DATASETS[ACTIVE_DATASET];

  document.getElementById('loadBtn').disabled = true;
  allRows     = [];
  rowCount    = 0;
  cachedStats = null;
  initPixelGrid();
  setOverlay(true, 0, 'Opening stream…');
  setStatus('loading', `Streaming ${ds.label}…`);
  document.getElementById('loadingPath').textContent = ds.file;

  let rowsParsed = 0;

  Papa.parse(ds.file, {
    download      : true,
    worker        : false,   // worker:true silently hangs on local servers (relative path can't be fetched by Web Worker)
    header        : true,
    skipEmptyLines: true,
    dynamicTyping : true,

    // ── chunk ────────────────────────────────────────────────
    chunk(results) {
      const rows = results.data;
      for (let r = 0; r < rows.length; r++) {
        const row   = rows[r];
        const label = parseInt(row['label'], 10);
        if (isNaN(label) || label < 0 || label > 9) continue;

        const pixels = new Uint8Array(784);
        for (let i = 1; i <= 784; i++) pixels[i - 1] = Number(row[`pixel${i}`]) || 0;

        allRows.push({ label, pixels });
        rowsParsed++;
      }

      const pct = Math.min(95, Math.round((rowsParsed / ds.estimatedRows) * 100));
      setOverlay(true, pct, `Parsed ${rowsParsed.toLocaleString()} rows…`);
    },

    // ── complete ─────────────────────────────────────────────
    complete() {
      rowCount = allRows.length;
      setOverlay(true, 100, 'Rendering dashboard…');

      /*
       * Two-frame rAF pipeline
       * ───────────────────────
       * Frame 1  Paint the "done" chrome first (overlay hide, status,
       *          summary cards).  calculateStats is pure math — fast.
       * Frame 2  Heavy DOM + WebGL work (table, Chart.js).  Browser
       *          has already shown a responsive frame so nothing
       *          feels frozen even with 60k rows.
       */
      requestAnimationFrame(() => {
        // Frame 1 — lightweight, lets browser show "done" state
        setOverlay(false);
        setStatus('done', `${rowCount.toLocaleString()} rows loaded`);
        document.getElementById('loadBtn').disabled = false;

        // Single-pass stats run here — pure numeric, no DOM touches
        cachedStats = calculateStatsSinglePass(allRows);
        renderSummaryCards();

        // Frame 2 — DOM heavy-lifting deferred one more frame
        requestAnimationFrame(() => {
          applyFilterSort();      // table rows
          initCharts(allRows);    // Chart.js (downsampled scatter)
          renderAnalysisTable();  // stats table from cache
          renderInsights();       // insight cards from cache
        });
      });
    },

    // ── error ────────────────────────────────────────────────
    error(err) {
      setOverlay(false);
      setStatus('error', 'Load failed');
      document.getElementById('loadBtn').disabled = false;
      document.getElementById('tableBody').innerHTML = `
        <tr><td colspan="7" class="placeholder-row" style="color:#ff4c8b">
          ✕ Could not load <code>${ds.file}</code>.<br>
          Serve over HTTP (not <code>file://</code>) and confirm the
          <code>archive/</code> folder is next to this HTML file.<br><br>
          Error: ${err.message || String(err)}
        </td></tr>`;
      console.error('[Fashion-MNIST] PapaParse error:', err);
    }
  });
}

/* ─────────────────────────────────────────────────────────────
   renderSummaryCards()
   Reads from cachedStats — no extra pass over allRows.
───────────────────────────────────────────────────────────── */
function renderSummaryCards() {
  if (!rowCount || !cachedStats) return;

  const elTotal = document.getElementById('stat-total');
  elTotal.textContent = rowCount.toLocaleString();
  elTotal.classList.add('loaded');
  document.getElementById('bar-total').style.width = '100%';

  const uniqueClasses = cachedStats.filter(s => s.count > 0).length;
  const elClasses = document.getElementById('stat-classes');
  elClasses.textContent = uniqueClasses;
  elClasses.classList.add('loaded');
  document.getElementById('bar-classes').style.width = `${(uniqueClasses / 10) * 100}%`;

  document.getElementById('stat-features').classList.add('loaded');

  // Weighted mean of class means — derived from cache, no rescan
  let wSum = 0, wCount = 0;
  for (let i = 0; i < cachedStats.length; i++) {
    wSum   += cachedStats[i].mean * cachedStats[i].count;
    wCount += cachedStats[i].count;
  }
  const avgIntensity = wCount > 0 ? wSum / wCount : 0;
  const elAvg = document.getElementById('stat-avgpixel');
  elAvg.textContent = avgIntensity.toFixed(2);
  elAvg.classList.add('loaded');
  document.getElementById('bar-avgpixel').style.width = `${(avgIntensity / 255) * 100}%`;
}

/* ════════════════════════════════════════════════════════════════
   MODULE 2 — STUDENT 2
   ════════════════════════════════════════════════════════════════ */

/* ─────────────────────────────────────────────────────────────
   calculateStatsSinglePass(data)
   ──────────────────────────────────────────────────────────
   ONE for-loop over data.  Per-class accumulators:
     count[l]   — row count
     sum[l]     — Σ(per-row pixel mean)
     sumSq[l]   — Σ(per-row pixel mean²)   → variance via E[X²]−(EX)²
     means[l]   — Array of per-row means    → Pearson r vs label-0

   A second micro-loop over 10 classes (not allData) finalises
   stdDev, variance, and Pearson r.

   No .filter(), .map(), or .reduce() on the large array.
───────────────────────────────────────────────────────────── */
function calculateStatsSinglePass(data) {
  const N = data.length;
  if (!N) return CLASS_NAMES.map((name, label) =>
    ({ label, name, count: 0, mean: 0, stdDev: 0, variance: 0, pearson: NaN }));

  // Float64Array avoids JS-object boxing for hot numeric accumulation
  const count = new Float64Array(10);
  const sum   = new Float64Array(10);
  const sumSq = new Float64Array(10);

  // Per-class arrays of per-row means (one number per row, not 784 pixels)
  const means = [[], [], [], [], [], [], [], [], [], []];

  // ── THE single pass ───────────────────────────────────────
  for (let i = 0; i < N; i++) {
    const row = data[i];
    const lbl = row.label;
    const px  = row.pixels;

    // Inline pixel mean — no Array.from, no helper function call
    let s = 0;
    for (let p = 0; p < 784; p++) s += px[p];
    const m = s / 784;

    count[lbl]++;
    sum[lbl]   += m;
    sumSq[lbl] += m * m;
    means[lbl].push(m);
  }

  // ── Micro-loop over 10 classes — not over allData ─────────
  const ref     = means[0];                             // label-0 mean vector
  const refMean = count[0] > 0 ? sum[0] / count[0] : 0;

  return CLASS_NAMES.map((name, label) => {
    const c = count[label];
    if (c === 0) return { label, name, count: 0, mean: 0, stdDev: 0, variance: 0, pearson: NaN };

    const mean = sum[label] / c;
    // Variance via computational formula: E[X²] − (E[X])²
    // More numerically stable than two-pass when means are large
    const variance = Math.max(0, sumSq[label] / c - mean * mean);
    const stdDev   = Math.sqrt(variance);

    // Pearson r vs label-0
    let pearson = NaN;
    if (label === 0) {
      pearson = 1;  // perfect autocorrelation
    } else if (ref.length > 0) {
      const cls    = means[label];
      const minLen = Math.min(cls.length, ref.length);
      const clsMean = mean;
      let   num = 0, sA = 0, sB = 0;
      for (let i = 0; i < minLen; i++) {
        const da = cls[i] - clsMean;
        const db = ref[i] - refMean;
        num += da * db;
        sA  += da * da;
        sB  += db * db;
      }
      const denom = Math.sqrt(sA * sB);
      pearson = denom === 0 ? NaN : num / denom;
    }

    return { label, name, count: c, mean, stdDev, variance, pearson };
  });
}

/* ─────────────────────────────────────────────────────────────
   initCharts(data)
   ──────────────────────────────────────────────────────────
   Bar chart  — pulls counts directly from cachedStats (no rescan).
   Scatter    — reservoir-sampled to SCATTER_MAX points.
               Dataset size never affects Chart.js frame time.
───────────────────────────────────────────────────────────── */
function initCharts(data) {
  if (!data || data.length === 0) return;

  // ── Bar chart (counts from cache — zero allRows scan) ──────
  const labelCounts = cachedStats.map(s => s.count);

  const barCtx = document.getElementById('barChart').getContext('2d');
  if (chartBar) chartBar.destroy();

  chartBar = new Chart(barCtx, {
    type: 'bar',
    data: {
      labels: CLASS_NAMES,
      datasets: [{
        label: 'Samples',
        data: labelCounts,
        backgroundColor: CLASS_COLORS.map(c => c + 'bb'),
        borderColor: CLASS_COLORS,
        borderWidth: 1.5,
        borderRadius: 5,
        borderSkipped: false,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: { duration: 500 },
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: '#0d1217', titleColor: '#00ffa3',
          bodyColor: '#6b8fa8', borderColor: '#1e2d3d', borderWidth: 1,
          callbacks: { label: ctx => `  ${ctx.parsed.y.toLocaleString()} samples` }
        }
      },
      scales: {
        x: {
          ticks: { color: '#6b8fa8', font: { family: 'JetBrains Mono', size: 9 }, maxRotation: 40, minRotation: 40 },
          grid:  { color: '#1e2d3d' }
        },
        y: {
          ticks: { color: '#6b8fa8', font: { family: 'JetBrains Mono', size: 9 } },
          grid:  { color: '#1e2d3d' }
        }
      }
    }
  });

  // ── Scatter chart — reservoir-sampled ──────────────────────
  //
  // Downsampling strategy: reservoir sampling gives a statistically
  // uniform random sample across the entire dataset rather than
  // just the first N rows.  SCATTER_MAX = 500 points total.
  const sample     = reservoirSample(data, SCATTER_MAX);
  const sampleSize = sample.length;

  // Per-class point arrays (loop once over the sample)
  const classBuckets = Array.from({ length: 10 }, () => []);
  for (let i = 0; i < sampleSize; i++) {
    const row = sample[i];
    let s = 0;
    for (let p = 0; p < 784; p++) s += row.pixels[p];
    classBuckets[row.label].push({ x: i, y: s / 784 });
  }

  const scatterDatasets = CLASS_NAMES.map((name, label) => ({
    label,
    data:            classBuckets[label],
    backgroundColor: CLASS_COLORS[label] + '99',
    borderColor:     CLASS_COLORS[label],
    borderWidth:     0,
    pointRadius:     3,
    pointHoverRadius:5,
    label:           name,
  }));

  const scatterCtx = document.getElementById('scatterChart').getContext('2d');
  if (chartScatter) chartScatter.destroy();

  chartScatter = new Chart(scatterCtx, {
    type: 'scatter',
    data: { datasets: scatterDatasets },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: { duration: 500 },
      plugins: {
        legend: {
          position: 'bottom',
          labels: { color: '#6b8fa8', font: { family: 'JetBrains Mono', size: 9 }, boxWidth: 9, padding: 8 }
        },
        tooltip: {
          backgroundColor: '#0d1217', titleColor: '#00ffa3',
          bodyColor: '#6b8fa8', borderColor: '#1e2d3d', borderWidth: 1,
          callbacks: { label: ctx => `  ${ctx.dataset.label}: μ = ${ctx.parsed.y.toFixed(1)}` }
        }
      },
      scales: {
        x: {
          title: {
            display: true,
            text: `Sample Index (${sampleSize.toLocaleString()} sampled of ${rowCount.toLocaleString()})`,
            color: '#3a5468', font: { family: 'JetBrains Mono', size: 9 }
          },
          ticks: { color: '#3a5468', font: { size: 9 } }, grid: { color: '#1e2d3d' }
        },
        y: {
          title: { display: true, text: 'Mean Pixel', color: '#3a5468', font: { family: 'JetBrains Mono', size: 9 } },
          ticks: { color: '#3a5468', font: { size: 9 } }, grid: { color: '#1e2d3d' }
        }
      }
    }
  });
}

/* ─────────────────────────────────────────────────────────────
   renderAnalysisTable()
   Reads from cachedStats — zero re-scan of allRows.
───────────────────────────────────────────────────────────── */
function renderAnalysisTable() {
  if (!cachedStats) return;
  const tbody = document.getElementById('analysisTableBody');
  const frag  = document.createDocumentFragment();
  tbody.innerHTML = '';

  cachedStats.forEach(s => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${s.label}</td>
      <td>${s.name}</td>
      <td>${s.count.toLocaleString()}</td>
      <td>${s.mean.toFixed(3)}</td>
      <td>${s.stdDev.toFixed(3)}</td>
      <td>${s.variance.toFixed(3)}</td>
      <td>${isNaN(s.pearson) ? '—' : s.pearson.toFixed(4)}</td>`;
    frag.appendChild(tr);
  });
  tbody.appendChild(frag);
}