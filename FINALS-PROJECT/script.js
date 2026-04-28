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