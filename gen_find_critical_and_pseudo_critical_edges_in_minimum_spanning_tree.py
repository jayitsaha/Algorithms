"""
gen_find_critical_and_pseudo_critical_edges_in_minimum_spanning_tree.py
Creates/updates the Notion page for LeetCode #1489.
notion_page_id = None → create fresh page.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

# ── Step 0: Create fresh page (notion_page_id is null) ──
PAGE_ID = N.create_page(
    "Find Critical and Pseudo-Critical Edges in Minimum Spanning Tree",
    1489, "Hard", "🔴"
)
print(f"Created page: {PAGE_ID}")

# ── Step 1: Set properties ──
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=1489,
    pattern="Graph",
    subpatterns=["Include or Exclude Each Edge"],
    tc="O(E² · α(V))",
    sc="O(V)",
    key_insight="For each edge: skip it (cost rises → critical) or force it (cost same → pseudo-critical) using repeated Kruskal's runs.",
    icon="🔴"
)
print("Properties set.")

# ── Step 2: Wipe existing body (fresh page has none, but wipe is safe) ──
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} existing blocks.")

# ── Step 3: Build body blocks ──
PROBLEM_STATEMENT = (
    "Given a weighted undirected connected graph with n nodes and an array of edges where "
    "edges[i] = [u, v, w] represents a bidirectional edge between nodes u and v with weight w, "
    "find all the critical and pseudo-critical edges in the minimum spanning tree (MST) of the graph.\n\n"
    "An MST edge whose deletion from the graph would cause the MST weight to increase is called a "
    "critical edge. On the other hand, a pseudo-critical edge is an edge that can appear in some MSTs "
    "but not all.\n\n"
    "Return them as lists: [critical_edges, pseudo_critical_edges] using original edge indices."
)

SOL1_CODE = '''\
def findCriticalAndPseudoCriticalEdges(n, edges):
    # Attach original index before sorting by weight
    indexed = [(w, u, v, i) for i, (u, v, w) in enumerate(edges)]
    indexed.sort()
    E = len(indexed)

    def make_uf(n):
        parent = list(range(n))
        rank = [0] * n
        return parent, rank

    def find(p, x):
        while p[x] != x:
            p[x] = p[p[x]]   # path compression (halving)
            x = p[x]
        return x

    def union(p, r, a, b):
        ra, rb = find(p, a), find(p, b)
        if ra == rb:
            return False   # already same component -> cycle
        if r[ra] < r[rb]:
            ra, rb = rb, ra
        p[rb] = ra
        if r[ra] == r[rb]:
            r[ra] += 1
        return True

    def kruskal(skip=-1, force=-1):
        p, r = make_uf(n)
        cost = 0
        used = 0
        if force != -1:
            w, u, v, _ = indexed[force]
            union(p, r, u, v)
            cost += w
            used += 1
        for i, (w, u, v, _) in enumerate(indexed):
            if i == skip or i == force:
                continue
            if union(p, r, u, v):
                cost += w
                used += 1
        return cost if used == n - 1 else float('inf')

    base = kruskal()                          # reference MST weight
    critical, pseudo = [], []

    for i, (_, _, _, orig) in enumerate(indexed):
        if kruskal(skip=i) > base:           # excluding raises cost → critical
            critical.append(orig)
        elif kruskal(force=i) == base:       # forcing doesn't raise cost → pseudo
            pseudo.append(orig)

    return [critical, pseudo]
'''

SOL2_CODE = '''\
# Brute force: try all spanning trees (exponential -- only for understanding)
from itertools import combinations

def findCriticalAndPseudoCriticalEdges_brute(n, edges):
    E = len(edges)

    def spanning_tree_weight(included_edges):
        # build adjacency, check connectivity, return total weight
        adj = {i: [] for i in range(n)}
        for u, v, w in included_edges:
            adj[u].append((v, w)); adj[v].append((u, w))
        visited = set(); stack = [0]
        total = 0
        while stack:
            node = stack.pop()
            if node in visited: continue
            visited.add(node)
            for nb, w in adj[node]:
                if nb not in visited:
                    stack.append(nb)
                    total += w
        return total if len(visited) == n else float('inf')

    # Generate all spanning trees (not practical for large inputs)
    # This is O(2^E * V) -- illustrative only
    best = float('inf')
    all_msts = []
    for size in range(n-1, E+1):
        for combo in combinations(range(E), size):
            subset = [edges[i] for i in combo]
            w = spanning_tree_weight(subset)
            if w < best:
                best = w; all_msts = [set(combo)]
            elif w == best:
                all_msts.append(set(combo))

    critical = [i for i in range(E) if all(i in mst for mst in all_msts)]
    pseudo   = [i for i in range(E) if not all(i in mst for mst in all_msts)
                                    and any(i in mst for mst in all_msts)]
    return [critical, pseudo]
'''

blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(PROBLEM_STATEMENT),
    N.divider(),
]

# ── Solution 1: Optimal ──
blocks += [
    N.h2("Solution 1 — Include/Exclude Edge Testing + Kruskal's (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We're not just finding one MST — we need to classify every edge as critical "
            "(in every possible MST), pseudo-critical (in some but not all MSTs), or neither. "
            "The key challenge is that there can be multiple valid MSTs when some edges share the same weight."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Finding a single MST and checking which of its edges are 'bridges' doesn't work — "
            "it only gives you one MST. An edge might be in one MST but not another (pseudo-critical). "
            "You cannot determine this by examining a single MST structure."
        ),
        N.h4("The Key Observation"),
        N.para(
            "To check if an edge e is CRITICAL: try building an MST without e. If the cost "
            "increases, e was irreplaceable in every MST. To check if e is PSEUDO-CRITICAL: "
            "force e into the MST first, then greedily complete. If the total equals the base "
            "MST cost, then e participates in at least one valid MST."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. Sort edges by weight (Kruskal's requires this). Preserve original indices.\n"
            "2. Compute base MST weight using standard Kruskal's.\n"
            "3. For each edge i: run kruskal(skip=i). If cost > base → critical.\n"
            "4. Else: run kruskal(force=i). If cost == base → pseudo-critical.\n"
            "5. Each kruskal() call is O(E·α(V)), and we run O(E) of them → O(E²·α(V)) total."
        ),
        N.callout(
            "Analogy: Think of each edge as a road. Critical roads are ones where closing them "
            "forces a detour with more total mileage. Pseudo-critical roads are routes you COULD "
            "take to reach the same optimal total — but parallel routes of equal length also exist.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOL1_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("indexed = [(w,u,v,i) ...]", {"code": True}), " — Attach original index i to each edge before sorting. After sorting by weight w, we need i to report back in original numbering."])),
    N.para(N.rich([("indexed.sort()", {"code": True}), " — Sort by (w, u, v, i). Kruskal's must process cheapest edges first for the greedy property to hold."])),
    N.para(N.rich([("make_uf(n)", {"code": True}), " — Create a fresh Union-Find for each Kruskal's run. Each test (skip/force) needs independent state."])),
    N.para(N.rich([("find(p, x)", {"code": True}), " — Path compression with halving: p[x] = p[p[x]] skips one level up each call, amortizing to near-O(1) per find."])),
    N.para(N.rich([("union(p, r, a, b)", {"code": True}), " — Returns True if a and b were in different components (merge occurred). Returns False if they're already connected (adding this edge would create a cycle)."])),
    N.para(N.rich([("kruskal(skip=-1, force=-1)", {"code": True}), " — Runs Kruskal's with an optional edge to skip (exclusion test) or force first (inclusion test). Returns inf if fewer than n-1 edges were used (graph disconnected)."])),
    N.para(N.rich([("if force != -1:", {"code": True}), " — If forcing an edge, pre-add it: union its endpoints and add weight to cost before the main loop."])),
    N.para(N.rich([("if union(...): cost += w; used += 1", {"code": True}), " — Greedy selection: only add this edge if it merges two different components (no cycle)."])),
    N.para(N.rich([("return cost if used == n-1 else float('inf')", {"code": True}), " — A valid spanning tree uses exactly n-1 edges. If we used fewer, the graph was disconnected — return infinity to signal failure."])),
    N.para(N.rich([("if kruskal(skip=i) > base:", {"code": True}), " — CRITICAL TEST: skip edge i and recompute. If cost rises → i is irreplaceable → critical."])),
    N.para(N.rich([("elif kruskal(force=i) == base:", {"code": True}), " — PSEUDO-CRITICAL TEST: force edge i. If cost same → i fits in at least one valid MST → pseudo-critical. The elif prevents testing critical edges twice."])),
    N.divider(),
]

# ── Solution 2: Brute Force ──
blocks += [
    N.h2("Solution 2 — Brute Force: Enumerate All Spanning Trees"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "The most direct interpretation: find all possible spanning trees, check which edges "
            "appear in all of them (critical) vs. some of them (pseudo-critical)."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "O(2^E) enumeration is infeasible for large E. With E up to 200, this is 2^200 combinations — "
            "astronomically expensive. This approach only works for tiny test cases to verify correctness."
        ),
        N.h4("The Key Observation"),
        N.para(
            "The brute force is conceptually clearest: enumerate all spanning subsets, filter to those "
            "with minimum total weight, then classify edges by their presence across all optimal spanning trees."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Try all subsets of size n-1 to n+... edges. Compute spanning tree weight for each. "
            "Track the minimum weight and all spanning trees that achieve it. Classify each edge."
        ),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE, "python"),
    N.h3("When to Use"),
    N.para("Only for verification / tiny inputs (n ≤ 5, E ≤ 10). In interviews, state this approach to show you understand the problem definition, then immediately propose the O(E²·α(V)) Kruskal's solution."),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (all spanning trees)", "O(2^E · V)", "O(V + E)"],
        ["Include/Exclude + Kruskal's (optimal)", "O(E² · α(V))", "O(V)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Graph (MST — Minimum Spanning Tree / Union-Find)"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Include or Exclude Each Edge (edge role analysis in spanning trees using Kruskal's subroutine)"])),
    N.para(N.rich([("Named Algorithms: ", {"bold": True}), "Kruskal's MST Algorithm + Union-Find with Path Compression & Union by Rank"])),
    N.callout(
        "When to recognize this pattern:\n"
        "• 'Classify edges in MST' (critical / bridge / pseudo-critical)\n"
        "• 'Find minimum spanning tree' with additional constraints\n"
        "• 'Which edges can be swapped without raising cost?'\n"
        "• Weight ties between edges (multiple valid MSTs)\n"
        "• O(E) graph algorithms with edge-level analysis",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (MST / Union-Find / Edge Analysis):"),
    N.bullet(N.rich([("Min Cost to Connect All Points", {"bold": True}), " (Medium) — Kruskal's on implicit complete graph; build MST from scratch (#1584)"])),
    N.bullet(N.rich([("Redundant Connection", {"bold": True}), " (Medium) — Use Union-Find to detect the cycle-forming edge in a spanning tree (#684)"])),
    N.bullet(N.rich([("Critical Connections in a Network", {"bold": True}), " (Hard) — Find bridges (critical edges) using Tarjan's DFS; similar 'remove edge, check graph' logic (#1192)"])),
    N.bullet(N.rich([("Number of Operations to Make Network Connected", {"bold": True}), " (Medium) — Count connected components and redundant edges with Union-Find (#1319)"])),
    N.bullet(N.rich([("Optimize Water Distribution in a Village", {"bold": True}), " (Hard) — MST with virtual node; Kruskal's on extended edge set (#1168)"])),
    N.bullet(N.rich([("Connecting Cities With Minimum Cost", {"bold": True}), " (Medium) — Classic MST using Kruskal's + Union-Find (#1135)"])),
    N.bullet(N.rich([("Smallest String With Swaps", {"bold": True}), " (Medium) — Union-Find to group nodes, then sort within each component (#1202)"])),
    N.para("These problems share the same core technique: Union-Find for component tracking + Kruskal's greedy edge selection."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 7: Graph Algorithms → Union-Find (Disjoint Set Union)", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("find_critical_and_pseudo_critical_edges_in_minimum_spanning_tree")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Page URL: https://www.notion.so/{PAGE_ID.replace('-','')}")
