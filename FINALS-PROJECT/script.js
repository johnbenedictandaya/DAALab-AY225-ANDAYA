/**
 * ════════════════════════════════════════════════════════════════
 * Fashion-MNIST Dashboard · script.js  (Performance Rewrite)
 * ────────────────────────────────────────────────────────────────
 * Optimisations applied vs. previous version
 * ──────────────────────────────────────────
 *  1. worker:true  — CSV parsing is entirely off the main thread.
 *  2. Single-pass stats engine — one for-loop computes Sum, SumSq,
 *     Count, and the per-row means needed for Pearson r.
 *     No .filter()/.map()/.reduce() on the large array.
 *  3. Scatter downsampling — reservoir-sampled to SCATTER_MAX (500)
 *     points so Chart.js never pushes > 500 GPU quads.
 *  4. requestAnimationFrame pipeline — two-frame hand-off lets the
 *     browser paint the "done" overlay before heavy DOM/WebGL work.
 *  5. Canvas efficiency — draws at native 28×28 (784-pixel loop)
 *     then uses CSS width/height for visual 2× upscale, cutting the
 *     inner loop from 3 136 to 784 iterations per image.
 *  6. Stat cache — calculateStatsSinglePass runs once; renderCards,
 *     renderAnalysisTable, renderInsights all read from the cache.
 * ════════════════════════════════════════════════════════════════
 */

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