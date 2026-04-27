"""
Travelling Salesman Problem - Node Map & Shortest Path Finder
Algorithm: Dijkstra's (for distance / time / fuel)
"""

import heapq

# ── 1. Raw Edge Data ──────────────────────────────────────────
RAW_EDGES = [
    {"from": "IMUS",     "to": "BACOOR",   "distance": 10, "time": 15, "fuel": 1.2},
    {"from": "BACOOR",   "to": "DASMA",    "distance": 12, "time": 25, "fuel": 1.5},
    {"from": "DASMA",    "to": "KAWIT",    "distance": 12, "time": 25, "fuel": 1.5},
    {"from": "KAWIT",    "to": "INDANG",   "distance": 12, "time": 25, "fuel": 1.2},
    {"from": "INDANG",   "to": "SILANG",   "distance": 14, "time": 25, "fuel": 1.5},
    {"from": "SILANG",   "to": "GENTRI",   "distance": 10, "time": 25, "fuel": 1.3},
    {"from": "GENTRI",   "to": "NOVELETA", "distance": 10, "time": 25, "fuel": 1.5},
    {"from": "NOVELETA", "to": "IMUS",     "distance": 10, "time": 15, "fuel": 1.2},
    {"from": "BACOOR",   "to": "SILANG",   "distance": 10, "time": 25, "fuel": 1.3},
    {"from": "DASMA",    "to": "SILANG",   "distance": 12, "time": 25, "fuel": 1.5},
    {"from": "SILANG",   "to": "BACOOR",   "distance": 10, "time": 25, "fuel": 1.3},
    {"from": "NOVELETA", "to": "BACOOR",   "distance": 10, "time": 15, "fuel": 1.2},
    {"from": "SILANG",   "to": "KAWIT",    "distance": 14, "time": 25, "fuel": 1.2},
    {"from": "IMUS",     "to": "NOVELETA", "distance": 10, "time": 15, "fuel": 1.2},
]

# ── 2. Build Graph ────────────────────────────────────────────
def build_graph(edges):
    nodes = sorted(set(n for e in edges for n in (e["from"], e["to"])))
    graph = {n: [] for n in nodes}
    for e in edges:
        graph[e["from"]].append({
            "to": e["to"],
            "distance": e["distance"],
            "time": e["time"],
            "fuel": e["fuel"]
        })
    return nodes, graph

# ── 3. Dijkstra's Algorithm ───────────────────────────────────
def dijkstra(graph, nodes, start, end, criteria):
    dist = {n: float("inf") for n in nodes}
    prev = {n: None for n in nodes}
    prev_edge = {n: None for n in nodes}
    dist[start] = 0

    # Priority queue: (cost, node)
    pq = [(0, start)]

    while pq:
        cost, u = heapq.heappop(pq)

        if cost > dist[u]:
            continue

        if u == end:
            break

        for edge in graph[u]:
            v = edge["to"]
            new_cost = dist[u] + edge[criteria]
            if new_cost < dist[v]:
                dist[v] = new_cost
                prev[v] = u
                prev_edge[v] = edge
                heapq.heappush(pq, (new_cost, v))

    if dist[end] == float("inf"):
        return None

    # Reconstruct path
    path = []
    steps = []
    cur = end
    while cur is not None:
        path.insert(0, cur)
        if prev_edge[cur]:
            step = {"from": prev[cur], **prev_edge[cur]}
            steps.insert(0, step)
        cur = prev[cur]

    return {"path": path, "cost": dist[end], "steps": steps}

# ── 4. Display Node Map ───────────────────────────────────────
def display_node_map(edges):
    print("\n" + "=" * 55)
    print("  PART 1: NODE MAP")
    print("=" * 55)
    print(f"{'From':<12} {'To':<12} {'Distance':>10} {'Time':>8} {'Fuel':>8}")
    print("-" * 55)
    for e in edges:
        print(f"{e['from']:<12} {e['to']:<12} {str(e['distance']) + ' km':>10} "
              f"{str(e['time']) + ' min':>8} {str(e['fuel']) + ' L':>8}")
    print("=" * 55)

# ── 5. Display Shortest Path Result ──────────────────────────
def display_result(start, end, criteria, result):
    print("\n" + "=" * 55)
    print("  PART 2: SHORTEST PATH RESULT")
    print("=" * 55)
    print(f"  From     : {start}")
    print(f"  To       : {end}")
    print(f"  Optimize : {criteria.upper()}")
    print("-" * 55)

    path_str = " -> ".join(result["path"])
    print(f"  Path: {path_str}")
    print("-" * 55)

    # Compute totals
    total_dist = sum(s["distance"] for s in result["steps"])
    total_time = sum(s["time"] for s in result["steps"])
    total_fuel = sum(s["fuel"] for s in result["steps"])

    print(f"  Total Distance : {total_dist} km")
    print(f"  Total Time     : {total_time} mins")
    print(f"  Total Fuel     : {total_fuel:.1f} L")
    print("-" * 55)

    # Step-by-step breakdown
    print(f"\n  {'Step':<6} {'From':<12} {'To':<12} {'Dist':>6} {'Time':>6} {'Fuel':>6}")
    print("  " + "-" * 48)
    for i, s in enumerate(result["steps"], 1):
        print(f"  {i:<6} {s['from']:<12} {s['to']:<12} "
              f"{str(s['distance'])+'km':>6} {str(s['time'])+'min':>6} {str(s['fuel'])+'L':>6}")
    print("  " + "-" * 48)
    fuel_str = f"{total_fuel:.1f}L"
    print(f"  {'TOTAL':<6} {'':<12} {'':<12} "
          f"{str(total_dist)+'km':>6} {str(total_time)+'min':>6} {fuel_str:>6}")
    print("=" * 55)

# ── 6. Get User Input ─────────────────────────────────────────
def get_user_input(nodes):
    print("\n  Available Nodes:")
    for i, n in enumerate(nodes, 1):
        print(f"    {i}. {n}")

    print()
    while True:
        start = input("  Enter Start Node: ").strip().upper()
        if start in nodes:
            break
        print(f"  Invalid node. Choose from: {', '.join(nodes)}")

    while True:
        end = input("  Enter End Node  : ").strip().upper()
        if end in nodes and end != start:
            break
        if end == start:
            print("  Start and End nodes must be different.")
        else:
            print(f"  Invalid node. Choose from: {', '.join(nodes)}")

    print("\n  Optimize by:")
    print("    1. Distance (km)")
    print("    2. Time (mins)")
    print("    3. Fuel (L)")
    criteria_map = {"1": "distance", "2": "time", "3": "fuel",
                    "distance": "distance", "time": "time", "fuel": "fuel"}
    while True:
        choice = input("  Enter choice (1/2/3): ").strip().lower()
        if choice in criteria_map:
            criteria = criteria_map[choice]
            break
        print("  Invalid choice. Enter 1, 2, or 3.")

    return start, end, criteria

# ── 7. Main ───────────────────────────────────────────────────
def main():
    print("\n" + "=" * 55)
    print("  TRAVELLING SALESMAN PROBLEM")
    print("  Node Map Visualizer & Shortest Path Finder")
    print("=" * 55)

    nodes, graph = build_graph(RAW_EDGES)

    while True:
        display_node_map(RAW_EDGES)
        start, end, criteria = get_user_input(nodes)

        result = dijkstra(graph, nodes, start, end, criteria)

        if result is None:
            print(f"\n  ⚠ No path found from {start} to {end}.")
        else:
            display_result(start, end, criteria, result)

        again = input("\n  Find another path? (y/n): ").strip().lower()
        if again != "y":
            print("\n  Goodbye!\n")
            break

if __name__ == "__main__":
    main()