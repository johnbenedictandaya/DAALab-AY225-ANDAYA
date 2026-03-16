# MidtermLab2 – Travelling Salesman Problem

**Course:** Data Structures and Algorithms
**Type:** Midterm Laboratory Assignment
**File:** `MIDTERM-LAB-2/MidtermLab2-[Lastname]`

---

## Overview

This is a college midterm lab assignment that builds a simple web program to visualize a node map and find the shortest path between locations using **Dijkstra's Algorithm**. The program is built with plain HTML, CSS, and JavaScript (no frameworks or libraries needed.)

---

## Files

```
MIDTERM-LAB-2/
├── index.html   # Main page structure
├── style.css    # Site's styling
└── script.js    # Graph logic and Dijkstra's algorithm
```

---

## How to Run

1. Download or clone the repository.
2. Open `index.html` in any modern web browser.
3. No installation or server required.

---

## Features

### Part 1 – Node Map
- Displays all nodes and directed edges on a canvas
- Shows distance labels on each edge
- Hover over an edge in order to see its Distance, Time, and Fuel values

### Part 2 – Shortest Path Finder
- Select a **Start Node** and **End Node**
- Choose to optimize by **Distance**, **Time**, or **Fuel**
- Outputs the shortest path, step-by-step breakdown, and totals
- Highlights the path on the node map

---

## Algorithm Used

**Dijkstra's Algorithm** — a greedy shortest-path algorithm that works on weighted directed graphs. It was chosen because:
- It guarantees the optimal (shortest) path
- It handles different weight types (distance, time, fuel) by simply swapping the weight used
- It is efficient and well-suited for small-to-medium graphs like what we have on this one

---

## Nodes and Edges

The graph is based on real locations in Cavite, Philippines:

| Nodes |
|-------|
| IMUS, BACOOR, DASMA, KAWIT, INDANG, SILANG, GENTRI, NOVELETA |

Edges and their weights (Distance, Time, Fuel) are defined in the assignment data table.

---

## Challenges
- Using Javascript to challenge myself and enhance my skill on it
- Hardest part of creating this project is drawing the graph
    - Positioning nodes on the canvas in a clear, readable layout required manual coordinate tuning
    - Dijkstra's algorithm needed to support three different weight criteria without rewriting the core logic — solved by passing the `criteria` key as a parameter
    - Drawing directed arrows that don't overlap node circles required offsetting the start and end points by the node radius

---

## Author

**Name:** Ron Zandro Y. Morante
**Section:** BSCS 2206L 9407-AY225 (Design, Analysis & Algorithm Tech - LAB)
**Date:** MARCH 17 2026