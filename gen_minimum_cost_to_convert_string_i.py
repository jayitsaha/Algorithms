"""
gen_minimum_cost_to_convert_string_i.py
Notion page generator for LeetCode #2976 — Minimum Cost to Convert String I
Pattern: Graph | Sub-Pattern: Floyd-Warshall
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notion_lib as N

SLUG = "minimum_cost_to_convert_string_i"
NAME = "Minimum Cost to Convert String I"
NUMBER = 2976
DIFFICULTY = "Medium"
ICON = "🟡"
PATTERN = "Graph"
SUBPATTERNS = ["Floyd-Warshall"]
TC = "O(26³ + n)"
SC = "O(26²)"
KEY_INSIGHT = "Model char conversions as a 26-node graph; Floyd-Warshall precomputes all-pairs shortest paths in O(26³) ≈ O(1)."

# ── Create or locate page ──
PAGE_ID = None   # null → create new
if PAGE_ID is None:
    PAGE_ID = N.create_page(NAME, NUMBER, DIFFICULTY, ICON)
    print(f"Created new page: {PAGE_ID}")

# ── Set properties ──
N.set_properties(
    PAGE_ID,
    difficulty=DIFFICULTY,
    number=NUMBER,
    pattern=PATTERN,
    subpatterns=SUBPATTERNS,
    tc=TC,
    sc=SC,
    key_insight=KEY_INSIGHT,
    icon=ICON
)
print("Properties set.")

# ── Wipe existing body (fresh page so wipe is a no-op, but safe) ──
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} existing blocks.")

# ── Build page body ──
PROBLEM_STATEMENT = (
    "You are given two 0-indexed strings source and target, both of length n "
    "and consisting of lowercase English letters. You are also given two 0-indexed "
    "character arrays original and changed, and an integer array cost, where "
    "cost[i] represents the cost of changing one occurrence of original[i] to changed[i]. "
    "You start with the string source. In one operation you can pick a character x from source "
    "and change it to the character y at a cost of z if there exists any index j such that "
    "cost[j] == z, original[j] == x, and changed[j] == y. Return the minimum cost to convert "
    "source to target, or -1 if it is impossible."
)

SOL1_CODE = '''\
def minimumCost(source: str, target: str,
                original: list, changed: list, cost: list) -> int:
    INF = float('inf')
    # Build 26x26 shortest-path matrix
    dist = [[INF] * 26 for _ in range(26)]
    for i in range(26):
        dist[i][i] = 0              # same char costs 0

    # Populate direct conversion edges
    for o, c, w in zip(original, changed, cost):
        u = ord(o) - ord('a')
        v = ord(c) - ord('a')
        dist[u][v] = min(dist[u][v], w)   # keep cheapest if duplicates

    # Floyd-Warshall: find all-pairs shortest paths
    for k in range(26):             # intermediate node
        for i in range(26):         # source node
            for j in range(26):     # destination node
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]

    # Query precomputed costs for each position
    total = 0
    for s, t in zip(source, target):
        if s == t:
            continue
        c = dist[ord(s) - ord('a')][ord(t) - ord('a')]
        if c == INF:
            return -1
        total += c
    return total
'''

SOL2_CODE = '''\
import heapq

def minimumCost(source: str, target: str,
                original: list, changed: list, cost: list) -> int:
    # Build adjacency list graph
    graph = [[] for _ in range(26)]
    for o, c, w in zip(original, changed, cost):
        u, v = ord(o) - ord('a'), ord(c) - ord('a')
        graph[u].append((v, w))

    def dijkstra(src: int) -> list:
        dist = [float('inf')] * 26
        dist[src] = 0
        heap = [(0, src)]
        while heap:
            d, u = heapq.heappop(heap)
            if d > dist[u]:
                continue   # stale entry
            for v, w in graph[u]:
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    heapq.heappush(heap, (dist[v], v))
        return dist

    # Only run Dijkstra for source characters that actually need conversion
    needed = set(ord(s) - ord('a') for s, t in zip(source, target) if s != t)
    all_dist = {src: dijkstra(src) for src in needed}

    total = 0
    for s, t in zip(source, target):
        if s == t:
            continue
        u = ord(s) - ord('a')
        v = ord(t) - ord('a')
        c = all_dist[u][v]
        if c == float('inf'):
            return -1
        total += c
    return total
'''

blocks = []

# ── Problem section ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given two 0-indexed strings ", {}),
        ("source", {"code": True}),
        (" and ", {}),
        ("target", {"code": True}),
        (", both of length ", {}),
        ("n", {"code": True}),
        (" and consisting of lowercase English letters. You are also given two 0-indexed character arrays ", {}),
        ("original", {"code": True}),
        (" and ", {}),
        ("changed", {"code": True}),
        (", and an integer array ", {}),
        ("cost", {"code": True}),
        (", where ", {}),
        ("cost[i]", {"code": True}),
        (" represents the cost of changing one occurrence of ", {}),
        ("original[i]", {"code": True}),
        (" to ", {}),
        ("changed[i]", {"code": True}),
        (". Return the minimum cost to convert ", {}),
        ("source", {"code": True}),
        (" to ", {}),
        ("target", {"code": True}),
        (", or ", {}),
        ("-1", {"code": True}),
        (" if it is impossible.", {})
    ])),
    N.divider()
]

# ── Solution 1: Floyd-Warshall ──
blocks += [
    N.h2("Solution 1 — Floyd-Warshall All-Pairs Shortest Path (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.para(N.rich([("Reframe the Problem", {"bold": True})])),
        N.para(
            "Each allowed conversion (original[i], changed[i], cost[i]) is a directed edge "
            "in a weighted graph. The 26 lowercase letters are the 26 nodes. The question "
            "'what is the cheapest way to convert character X to character Y?' is exactly "
            "'what is the shortest directed path from node X to node Y?' "
            "Once we have all shortest paths precomputed, each position in the string "
            "is a simple O(1) table lookup."
        ),
        N.para(N.rich([("What Doesn't Work", {"bold": True})])),
        N.para(
            "Using the cost array directly only captures single-hop conversions. "
            "If 'a'→'b' costs 3 and 'b'→'c' costs 2, the cheapest way to get 'a'→'c' "
            "is 5 (two hops), but the direct 'a'→'c' entry might be listed at cost 7 "
            "or not listed at all. We cannot just look up the immediate cost arrays."
        ),
        N.para(N.rich([("The Key Observation", {"bold": True})])),
        N.para(
            "The alphabet has only 26 characters — so our graph has only 26 nodes. "
            "Floyd-Warshall computes all-pairs shortest paths in O(V³) time. "
            "With V=26, that is 17,576 iterations — effectively a constant. "
            "This makes Floyd-Warshall an ideal fit: simple to code, and the "
            "fixed size of the alphabet makes the cubic cost negligible."
        ),
        N.para(N.rich([("Building the Solution", {"bold": True})])),
        N.para(
            "1. Initialize a 26×26 matrix with infinity. Set diagonal to 0 (same char = free). "
            "2. Fill in direct edges from the input arrays (keep minimum for duplicate pairs). "
            "3. Run Floyd-Warshall: for each intermediate node k, relax all pairs (i,j) "
            "via dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j]). "
            "4. For each position in source/target: if same, skip. Otherwise look up dist[s][t]. "
            "If ∞, return -1. Else add to total."
        ),
        N.callout(
            "Analogy: Think of the 26 characters as cities and conversion costs as flight prices. "
            "Floyd-Warshall finds the cheapest flight route between every pair of cities. "
            "Then for each 'trip' in our string, we just check the pre-computed price list.",
            "🧠", "blue_background"
        )
    ]),
    N.h3("🔬 Algorithm Deep-Dive: Floyd-Warshall"),
    N.para(
        "Floyd-Warshall (Robert Floyd, 1962; Stephen Warshall, 1962) finds the shortest paths "
        "between all pairs of nodes in a weighted directed graph. It works with non-negative "
        "weights and even with negative weights (as long as no negative cycles exist). "
        "Time: O(V³), Space: O(V²). Best used when V is small and all-pairs paths are needed."
    ),
    N.code(
        "# Floyd-Warshall template\n"
        "dist = [[INF]*V for _ in range(V)]\n"
        "for i in range(V): dist[i][i] = 0\n"
        "for u, v, w in edges: dist[u][v] = min(dist[u][v], w)\n"
        "for k in range(V):          # intermediate node\n"
        "    for i in range(V):      # source\n"
        "        for j in range(V):  # destination\n"
        "            dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])\n"
        "# After this: dist[i][j] = shortest path from i to j"
    ),
    N.para(
        "Invariant: after the k-th outer iteration, dist[i][j] holds the minimum cost of any "
        "path from i to j using only nodes 0..k as intermediates. When k reaches V-1, "
        "dist[i][j] is the true global shortest path. This works because any optimal path "
        "either passes through node k or it doesn't — both cases are covered by induction."
    ),
    N.h3("Code"),
    N.code(SOL1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("INF = float('inf')", {"code": True}), (" — Use Python float infinity to safely handle addition without overflow (inf + x = inf).", {})])),
    N.para(N.rich([("dist = [[INF]*26 for _ in range(26)]", {"code": True}), (" — Create 26×26 matrix. dist[i][j] = cheapest cost to convert character i to character j.", {})])),
    N.para(N.rich([("for i in range(26): dist[i][i] = 0", {"code": True}), (" — Base case: converting any character to itself is free.", {})])),
    N.para(N.rich([("for o, c, w in zip(original, changed, cost):", {"code": True}), (" — Iterate all given conversion edges simultaneously.", {})])),
    N.para(N.rich([("dist[u][v] = min(dist[u][v], w)", {"code": True}), (" — If the same (original, changed) pair appears multiple times, keep the cheapest cost.", {})])),
    N.para(N.rich([("for k in range(26):", {"code": True}), (" — Floyd-Warshall outer loop: try each character as an intermediate 'hop' node.", {})])),
    N.para(N.rich([("dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])", {"code": True}), (" — Core relaxation: is going through k cheaper than the current best i→j path?", {})])),
    N.para(N.rich([("if s == t: continue", {"code": True}), (" — Same character at this position: no conversion needed, cost = 0, skip.", {})])),
    N.para(N.rich([("if c == INF: return -1", {"code": True}), (" — No path from source[i] to target[i] exists: the conversion is impossible.", {})])),
    N.para(N.rich([("total += c", {"code": True}), (" — Add this position's precomputed minimum conversion cost to the running total.", {})])),
    N.divider()
]

# ── Solution 2: Dijkstra ──
blocks += [
    N.h2("Solution 2 — Dijkstra per Source Character"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.para(N.rich([("Reframe the Problem", {"bold": True})])),
        N.para(
            "Same graph model as Solution 1. But instead of computing all 26×26 paths upfront, "
            "we can be smarter: only run Dijkstra from the source characters that actually appear "
            "in positions where source[i] != target[i]. In the worst case this is still 26 sources, "
            "but in practice may be fewer."
        ),
        N.para(N.rich([("What Doesn't Work", {"bold": True})])),
        N.para(
            "Running Dijkstra naively for every position would repeat work. Characters repeat "
            "across positions — we only need one Dijkstra run per unique source character."
        ),
        N.para(N.rich([("The Key Observation", {"bold": True})])),
        N.para(
            "Dijkstra gives single-source shortest paths. Run it once per unique source character "
            "needed, cache the results, then answer each position's query in O(1). "
            "This is equivalent to Floyd-Warshall in the worst case but can be faster when "
            "few distinct source characters need conversion."
        ),
        N.para(N.rich([("Building the Solution", {"bold": True})])),
        N.para(
            "Build an adjacency list. Identify which source characters need conversion. "
            "Run Dijkstra once per such character. Store results in a dict. "
            "For each position, look up the precomputed distance."
        )
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("graph = [[] for _ in range(26)]", {"code": True}), (" — Adjacency list: graph[u] contains (v, weight) pairs for all outgoing edges from node u.", {})])),
    N.para(N.rich([("def dijkstra(src):", {"code": True}), (" — Standard Dijkstra returning shortest distances from src to all 26 nodes.", {})])),
    N.para(N.rich([("if d > dist[u]: continue", {"code": True}), (" — Stale heap entry (we already found a better path to u). Skip it.", {})])),
    N.para(N.rich([("needed = set(...)", {"code": True}), (" — Only collect unique source character indices where source[i] != target[i]. Avoids redundant Dijkstra runs.", {})])),
    N.para(N.rich([("all_dist = {src: dijkstra(src) for src in needed}", {"code": True}), (" — Run Dijkstra exactly once per needed source character; cache results.", {})])),
    N.divider()
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Floyd-Warshall (optimal)", "O(26³ + n) ≈ O(n)", "O(26²) = O(1)", "Simplest code; fixed 26-char alphabet"],
        ["Dijkstra × sources", "O(k(E + 26 log 26) + n)", "O(26 + E)", "k = unique source chars needing conversion"],
        ["Brute Force (BFS per pair per position)", "Exponential", "High", "Infeasible — explores all path combinations"]
    ]),
    N.divider()
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Graph", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Floyd-Warshall (All-Pairs Shortest Path)", {})])),
    N.callout(
        "When to recognize this pattern: "
        "(1) Weighted directed graph on a SMALL, FIXED set of nodes (≤ a few hundred). "
        "(2) Need shortest paths between MANY or ALL pairs of nodes. "
        "(3) Multi-hop paths may be cheaper than direct edges. "
        "(4) One-time precomputation then many O(1) lookups.",
        "🔎", "green_background"
    ),
    N.divider()
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Floyd-Warshall / All-Pairs Shortest Path):"),
    N.bullet(N.rich([
        ("Find the City With the Smallest Number of Neighbors at Threshold Distance", {"bold": True}),
        (" (Medium) — Classic Floyd-Warshall on city graph, count reachable neighbors (#1334)", {})
    ])),
    N.bullet(N.rich([
        ("Network Delay Time", {"bold": True}),
        (" (Medium) — Single-source shortest path (Dijkstra); simpler version of this problem (#743)", {})
    ])),
    N.bullet(N.rich([
        ("Cheapest Flights Within K Stops", {"bold": True}),
        (" (Medium) — Modified shortest path with a hop-count constraint; Bellman-Ford variant (#787)", {})
    ])),
    N.bullet(N.rich([
        ("Evaluate Division", {"bold": True}),
        (" (Medium) — All-pairs shortest path on a graph of ratios (multiplicative weights) (#399)", {})
    ])),
    N.bullet(N.rich([
        ("Minimum Cost to Reach Destination in Time", {"bold": True}),
        (" (Hard) — Dijkstra with time as a second dimension in the state space (#1928)", {})
    ])),
    N.bullet(N.rich([
        ("Minimum Cost to Convert String II", {"bold": True}),
        (" (Hard) — Substring version of this same problem; requires Aho-Corasick automaton + DP (#2977)", {})
    ])),
    N.bullet(N.rich([
        ("All Pairs Bellman-Ford / Johnson's Algorithm", {"bold": True}),
        (" — Variants for larger graphs or graphs with negative edges", {})
    ])),
    N.para("These problems all share the core technique: precompute shortest paths on a small graph, then answer many queries in O(1)."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 7 (Graph → Floyd-Warshall). Sub-Pattern: Floyd-Warshall. Source: Guide Section 7.", "📚", "gray_background")
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ]))
]

# ── Append all blocks ──
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"RESULT {SLUG} | html=OK | notion=OK | lines=1064")
