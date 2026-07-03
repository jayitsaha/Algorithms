#!/usr/bin/env python3
"""
Notion page generator for: Maximize Spanning Tree Stability with Upgrades
Custom/proprietary problem. leetcode_number=0. notion_page_id=None → create new.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

SLUG = "maximize_spanning_tree_stability_with_upgrades"
PAGE_ID = None  # Fresh page — will be created

# ── Step 1: Create the page ──────────────────────────────────────────────────
print("Creating Notion page...")
PAGE_ID = N.create_page(
    "Maximize Spanning Tree Stability with Upgrades",
    0,
    "Hard",
    "🔴"
)
print(f"Created page: {PAGE_ID}")

# ── Step 2: Set properties ──────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=0,
    pattern="Graph",
    subpatterns=["Binary Search on Answer", "Kruskal MST", "Union-Find"],
    tc="O(E log E · log W)",
    sc="O(N + E)",
    key_insight="Binary search on target min weight T; feasibility = Kruskal's MST using free edges first, then upgrade edges (at most k).",
    icon="🔴",
    status="Solved",
    source="LeetCode"
)
print("Properties set.")

# ── Step 3: Build body blocks ──────────────────────────────────────────────
print("Building body blocks...")
blocks = []

# ── Problem statement ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a weighted undirected graph with "),
        ("n", {"code": True}),
        (" nodes and "),
        ("m", {"code": True}),
        (" edges (each edge has a stability weight), and "),
        ("k", {"code": True}),
        (" upgrade tokens each boosting an edge weight by "),
        ("delta", {"code": True}),
        (", find the maximum possible minimum edge weight across any spanning tree achievable using at most "),
        ("k", {"code": True}),
        (" upgrades. This is the 'stability' of the most stable spanning tree you can build.")
    ])),
    N.callout(
        N.rich([
            ("Example: n=5, edges=[(0,1,5),(0,2,8),(1,2,6),(1,3,4),(2,4,7),(3,4,2)], k=1, delta=4.\n"),
            ("Answer: 6 — upgrade edge (1,3) from 4→8, build spanning tree with edges (0,2,8),(2,4,7),(1,2,6),(1,3,8). Min edge = 6.")
        ]),
        "📋", "gray_background"
    ),
    N.divider()
]

# ── Solution 1 — Binary Search + Kruskal (Interview Pick) ──────────────────
blocks += [
    N.h2("Solution 1 — Binary Search on Answer + Kruskal's MST (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We want the best possible minimum edge weight across any spanning tree, given we can strengthen up to k edges. Instead of directly constructing the optimal tree (hard), ask: for a fixed target T, is it even possible to build a spanning tree where all edges weigh ≥ T using ≤ k upgrades?"),
        N.h4("What Doesn't Work"),
        N.para("Brute force: try all C(m, k) subsets of edges to upgrade, then run max-MST on each. This is exponential in both m and k. Even for moderate graphs this is infeasible."),
        N.h4("The Key Observation"),
        N.para("'Maximize the minimum' → Binary Search on the Answer. The feasibility function f(T) = (can we span the graph with min weight ≥ T using ≤ k upgrades) is MONOTONE: if T is achievable, all T' < T are also achievable. Binary search exploits this monotonicity to find the exact boundary."),
        N.h4("Building the Solution"),
        N.para("1. Set lo = min edge weight, hi = max edge weight + k*delta.\n2. Binary search on T: compute mid, call feasible(mid).\n3. feasible(T): classify edges as free (w≥T), upgradeable (w+delta≥T>w), or unusable. Run Kruskal's on free first (no cost), then upgradeable (counting each union as an upgrade). Check: all nodes connected AND upgrades_used ≤ k.\n4. If feasible: lo = mid+1 (go higher). Else: hi = mid-1. Answer = hi after loop."),
        N.callout("Analogy: like searching for the highest bridge clearance you can guarantee on a cross-country road trip when you can raise k bridges by a fixed amount.", "🧠", "blue_background"),
    ]),
    N.h3("🔬 Algorithm Deep-Dive: Kruskal's MST + Binary Search on Answer"),
    N.para(N.rich([
        ("Kruskal's Algorithm", {"bold": True}),
        (" (Kruskal, 1956): Builds an MST by sorting edges by weight and greedily adding each that doesn't form a cycle (using Union-Find to detect cycles). When combined with "),
        ("Binary Search on Answer", {"bold": True}),
        (", it becomes the canonical approach for 'max-min' spanning tree problems with resource constraints.")
    ])),
    N.code(
        "# Core template: Binary Search + Kruskal\n"
        "def solve(n, edges, k, delta):\n"
        "    def find(p, x):  # path-compressed\n"
        "        while p[x] != x: p[x] = p[p[x]]; x = p[x]\n"
        "        return x\n"
        "    def union(p, rank, a, b):\n"
        "        a, b = find(p,a), find(p,b)\n"
        "        if a==b: return False\n"
        "        if rank[a] < rank[b]: a,b = b,a\n"
        "        p[b]=a; rank[a]+=(rank[a]==rank[b]); return True\n"
        "    def feasible(T):\n"
        "        p, rank = list(range(n)), [0]*n\n"
        "        free = [(u,v,w) for u,v,w in edges if w>=T]\n"
        "        upg  = [(u,v,w) for u,v,w in edges if w+delta>=T>w]\n"
        "        used = 0\n"
        "        for u,v,_ in sorted(free, key=lambda e:-e[2]):\n"
        "            union(p, rank, u, v)\n"
        "        for u,v,_ in sorted(upg, key=lambda e:-e[2]):\n"
        "            if union(p, rank, u, v): used+=1\n"
        "        return len(set(find(p,i) for i in range(n)))==1 and used<=k\n"
        "    lo = min(w for _,_,w in edges)\n"
        "    hi = max(w for _,_,w in edges) + k*delta\n"
        "    while lo<=hi:\n"
        "        mid=(lo+hi)//2\n"
        "        if feasible(mid): lo=mid+1\n"
        "        else: hi=mid-1\n"
        "    return hi"
    ),
    N.para(N.rich([
        ("Invariant", {"bold": True}),
        (": After each binary search iteration, every T ≤ lo-1 is proven feasible; every T ≥ hi+1 is infeasible. When lo > hi, the answer is hi (= lo-1).\n\n"),
        ("Why greedy works", {"bold": True}),
        (": For fixed T, using free edges before upgrades is optimal — it minimizes the number of upgrades consumed for any given spanning tree.")
    ])),
    N.h3("Code"),
    N.code(
        "def maxStability(n, edges, k, delta):\n"
        "    def find(p, x):\n"
        "        while p[x] != x: p[x] = p[p[x]]; x = p[x]\n"
        "        return x\n"
        "    def union(p, rank, a, b):\n"
        "        a, b = find(p, a), find(p, b)\n"
        "        if a == b: return False\n"
        "        if rank[a] < rank[b]: a, b = b, a\n"
        "        p[b] = a; rank[a] += (rank[a] == rank[b])\n"
        "        return True\n"
        "    def feasible(target):\n"
        "        p = list(range(n)); rank = [0] * n\n"
        "        free = [(u,v,w) for u,v,w in edges if w >= target]\n"
        "        upg  = [(u,v,w) for u,v,w in edges if w+delta >= target > w]\n"
        "        upgrades_used = 0\n"
        "        for u,v,w in sorted(free, key=lambda e:-e[2]):\n"
        "            union(p, rank, u, v)\n"
        "        for u,v,w in sorted(upg,  key=lambda e:-e[2]):\n"
        "            if union(p, rank, u, v):\n"
        "                upgrades_used += 1\n"
        "        roots = len(set(find(p, i) for i in range(n)))\n"
        "        return roots == 1 and upgrades_used <= k\n"
        "    lo = min(w for _,_,w in edges)\n"
        "    hi = max(w for _,_,w in edges) + k * delta\n"
        "    while lo <= hi:\n"
        "        mid = (lo + hi) // 2\n"
        "        if feasible(mid): lo = mid + 1\n"
        "        else:             hi = mid - 1\n"
        "    return hi"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("find(p, x)", {"code": True}), " — Path-compressed Union-Find root lookup. The path halving (p[x]=p[p[x]]) flattens the tree for O(α(n)) amortized."])),
    N.para(N.rich([("union(p, rank, a, b)", {"code": True}), " — Union by rank: attach the smaller tree under the larger. Returns True if a merge happened (different components), False if already same."])),
    N.para(N.rich([("free = [...] / upg = [...]", {"code": True}), " — Classify every edge: free (no upgrade needed), upgradeable (one token makes it viable), or discard (can't reach target even with upgrade)."])),
    N.para(N.rich([("sorted(free, key=lambda e:-e[2])", {"code": True}), " — Kruskal's requires sorted edges. We sort descending by weight but for feasibility this doesn't change correctness — it optimizes which edges we use, minimizing wasted capacity."])),
    N.para(N.rich([("if union(p,rank,u,v): upgrades_used+=1", {"code": True}), " — Only count upgrade tokens for edges that actually connected two components. Edges causing cycles are skipped (union returns False)."])),
    N.para(N.rich([("roots == 1 and upgrades_used <= k", {"code": True}), " — Spanning tree exists (one component) AND budget not exceeded → feasible."])),
    N.para(N.rich([("lo, hi = min_w, max_w + k*delta", {"code": True}), " — Tightest possible bounds. We never need T outside this range."])),
    N.para(N.rich([("if feasible(mid): lo=mid+1  else: hi=mid-1", {"code": True}), " — Standard binary search on the monotone boundary. After loop: hi = largest feasible T."])),
    N.divider()
]

# ── Solution 2 — Brute Force ──────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Brute Force: Try All Upgrade Subsets"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The most direct reading: enumerate all ways to choose which k edges to upgrade, apply the upgrades, run max-min spanning tree, take the best result."),
        N.h4("What Doesn't Work"),
        N.para("With m edges and k tokens, there are C(m, k) upgrade subsets. For m=20, k=5 that's 15504 subsets. For m=1000, k=10, it's astronomical. Totally infeasible."),
        N.h4("The Key Observation"),
        N.para("This brute force is correct (good for testing), but exponential. It motivates the need for binary search to avoid enumerating subsets explicitly."),
        N.h4("Building the Solution"),
        N.para("For each subset of edges to upgrade: apply upgrades, run Kruskal's to find the max-min spanning tree (Kruskal descending, take minimum edge in resulting tree), track global maximum."),
    ]),
    N.h3("Code"),
    N.code(
        "from itertools import combinations\n\n"
        "def maxStabilityBrute(n, edges, k, delta):\n"
        "    def max_min_mst(n, weighted_edges):\n"
        "        # Kruskal's for maximum spanning tree (sort descending)\n"
        "        p = list(range(n))\n"
        "        def find(x):\n"
        "            while p[x] != x: p[x] = p[p[x]]; x = p[x]\n"
        "            return x\n"
        "        mst_min = float('inf')\n"
        "        for u,v,w in sorted(weighted_edges, key=lambda e:-e[2]):\n"
        "            ru, rv = find(u), find(v)\n"
        "            if ru != rv:\n"
        "                p[ru] = rv\n"
        "                mst_min = min(mst_min, w)\n"
        "        # Check if connected\n"
        "        if len(set(find(i) for i in range(n))) > 1:\n"
        "            return -1  # disconnected\n"
        "        return mst_min\n\n"
        "    best = -1\n"
        "    for num_upg in range(k + 1):\n"
        "        for chosen in combinations(range(len(edges)), num_upg):\n"
        "            new_edges = [list(e) for e in edges]\n"
        "            for idx in chosen:\n"
        "                new_edges[idx][2] += delta\n"
        "            result = max_min_mst(n, new_edges)\n"
        "            best = max(best, result)\n"
        "    return best"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("for num_upg in range(k+1)", {"code": True}), " — Try using 0, 1, ..., k upgrades (we may not need all k)."])),
    N.para(N.rich([("for chosen in combinations(...)", {"code": True}), " — Every possible subset of that many edges to upgrade — C(m, num_upg) subsets."])),
    N.para(N.rich([("new_edges[idx][2] += delta", {"code": True}), " — Apply upgrade: add delta to the chosen edge's weight."])),
    N.para(N.rich([("max_min_mst(n, new_edges)", {"code": True}), " — Find the maximum spanning tree and return its minimum edge weight (the 'stability')."])),
    N.divider()
]

# ── Complexity table ────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (all subsets)", "O(2^E · E log E)", "O(N+E)"],
        ["Binary Search + Kruskal (Optimal)", "O(E log E · log W)", "O(N+E)"],
    ]),
    N.divider()
]

# ── Pattern Classification ──────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Graph"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Binary Search on Answer + Kruskal MST + Union-Find"])),
    N.callout(
        "When to recognize this pattern:\n"
        "• Problem asks to 'maximize the minimum' or 'minimize the maximum' over a graph structure\n"
        "• Resource constraints (budget, upgrades, k operations) modify edge weights or connectivity\n"
        "• A feasibility check (spanning tree existence) is easier to implement than direct optimization\n"
        "• The feasibility function is monotone in the optimization parameter",
        "🔎", "green_background"
    ),
    N.para(N.rich([
        ("Note: ", {"italic": True}),
        ("The sub-pattern 'Binary Search on Answer + Kruskal MST' is based on analysis of this custom problem. "
         "The component techniques (Binary Search on Answer, Kruskal's MST, Union-Find) each appear in the "
         "DSA guide, but their combination for this specific variant is a new classification.", {"italic": True})
    ])),
    N.divider()
]

# ── Related Problems ────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Binary Search on Answer + Graph):"),
    N.bullet(N.rich([("Path With Minimum Effort", {"bold": True}), " (Medium, LeetCode #1631) — Binary search on max edge weight in a grid path; Dijkstra/BFS feasibility check."])),
    N.bullet(N.rich([("Swim in Rising Water", {"bold": True}), " (Hard, LeetCode #778) — Binary search on water level; BFS/DSU to check reachability."])),
    N.bullet(N.rich([("Min Cost to Connect All Points", {"bold": True}), " (Medium, LeetCode #1584) — Standard Kruskal's/Prim's MST, same Union-Find toolkit."])),
    N.bullet(N.rich([("Find Critical and Pseudo-Critical Edges in MST", {"bold": True}), " (Hard, LeetCode #1489) — Deep MST analysis; which edges always/sometimes appear."])),
    N.bullet(N.rich([("Cheapest Flights Within K Stops", {"bold": True}), " (Medium, LeetCode #787) — Resource-constrained graph traversal; Bellman-Ford/modified Dijkstra."])),
    N.bullet(N.rich([("Koko Eating Bananas", {"bold": True}), " (Medium, LeetCode #875) — Binary Search on Answer template (non-graph); monotone feasibility check."])),
    N.bullet(N.rich([("Magnetic Force Between Two Balls", {"bold": True}), " (Medium, LeetCode #1552) — Binary search on minimum gap; feasibility via greedy placement."])),
    N.para("These problems share the core technique: binary search on the answer value, with a monotone feasibility check that tests whether a target threshold is achievable."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 6 (Graph Algorithms) · Sub-Pattern: Binary Search on Answer + MST · Source: Analysis", "📚", "gray_background"),
]

# ── Embed ────────────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ]))
]

# ── Append all blocks ────────────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks to page {PAGE_ID}...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")

# ── Print result for harness ──────────────────────────────────────────────
print(f"PAGE_ID={PAGE_ID}")
