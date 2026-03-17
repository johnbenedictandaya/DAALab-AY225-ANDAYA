# MidtermLab2 — Cavite Node Network Analyzer

## Overview
A browser-based tool that visualizes a directed graph of Cavite-area locations and computes the shortest path between any two nodes using **Dijkstra's Algorithm**. Built with pure HTML, CSS, and vanilla JavaScript — no dependencies required.

---

## Features

### Part 1 — Node Map
- Interactive canvas-drawn directed graph with arrow edges
- 8 nodes: IMUS, BACOOR, DASMA, KAWIT, INDANG, SILANG, GENTRI, NOVELETA
- 14 directed edges from the provided dataset
- Hover tooltips showing edge weight details (distance / time / fuel)
- Pan (click+drag) and zoom (scroll wheel or buttons) navigation
- Path highlighting: active shortest path glows orange on the graph

### Part 2 — Shortest Path (Dijkstra's Algorithm)
- Select any **Start** and **End** node via dropdowns
- Choose optimization criterion: **Distance (km)**, **Time (mins)**, or **Fuel (Liters)**
- Displays the computed path, total distance, total time, and total fuel
- Results are also logged to the browser console for verification

---

## Algorithm Used: Dijkstra's Algorithm

Dijkstra's algorithm finds the shortest path from a source node to all other nodes in a weighted directed graph with non-negative weights.

### Why Dijkstra?
- All edge weights (distance, time, fuel) are **non-negative** — a hard requirement for Dijkstra
- It guarantees the **optimal (shortest/cheapest) path**
- Efficient for small-to-medium graphs like this one

### How It Works (step-by-step)
1. Initialize all node costs to `Infinity`, except the start node (cost = 0)
2. Use a priority queue sorted by current known cost
3. Repeatedly extract the lowest-cost unvisited node `u`
4. For each neighbor `v` of `u`, check if going through `u` is cheaper than the known cost to `v`
5. If yes, update `v`'s cost and record `u` as its predecessor
6. Continue until the destination node is reached (or queue is empty)
7. Reconstruct the path by backtracking through predecessors

### Complexity
- Time: O((V + E) log V) with a proper priority queue
- Space: O(V) for distance and predecessor tables

---

## Graph Structure

```
Adjacency List (directed edges):
IMUS     → BACOOR (10km, 15min, 1.2L)
IMUS     → NOVELETA (10km, 15min, 1.2L)
BACOOR   → DASMA (12km, 25min, 1.5L)
BACOOR   → SILANG (10km, 25min, 1.3L)
DASMA    → KAWIT (12km, 25min, 1.5L)
DASMA    → SILANG (12km, 25min, 1.5L)
KAWIT    → INDANG (12km, 25min, 1.2L)
INDANG   → SILANG (14km, 25min, 1.5L)
SILANG   → GENTRI (10km, 25min, 1.3L)
SILANG   → BACOOR (10km, 25min, 1.3L)
SILANG   → KAWIT (14km, 25min, 1.2L)
GENTRI   → NOVELETA (10km, 25min, 1.5L)
NOVELETA → IMUS (10km, 15min, 1.2L)
NOVELETA → BACOOR (10km, 15min, 1.2L)
```

---

## Sample Output

```
=== Shortest Path (distance) ===
From: IMUS → To: SILANG
Path: IMUS → BACOOR → SILANG
Total Distance: 20 km
Total Time:     40 mins
Total Fuel:     2.5 Liters
```

---

## How to Run
1. Open `MidtermLab2-[Lastname].html` in any modern browser (Chrome, Firefox, Edge)
2. No server or installation needed — fully self-contained

---

## Challenges Faced

1. **Edge directionality** — The graph is directed (one-way edges), so paths are not always reversible. Dijkstra correctly handles this by only traversing edges in their defined direction.

2. **Multiple criteria** — The same algorithm runs three times conceptually (once per criterion). Each run uses a different edge weight property while tracking all three totals along the final path.

3. **Canvas layout** — Node positions were manually tuned to approximate geographic layout of Cavite municipalities and to avoid visual overlap of edge labels.

4. **Path reconstruction** — After Dijkstra terminates, the path is reconstructed by backtracking through the `prev[]` array from destination to source, then reversing.

---

## File Structure

```
MIDTERM-LAB-2/
├── MidtermLab2-[Lastname].html   ← Main program (HTML + CSS + JS)
└── readme.md                     ← This file
```

---

*Submitted for CS course — Midterm Laboratory Activity 2*
