"""gen_number_of_provinces.py — Notion page rebuild for Number of Provinces (LC #547)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8195-81b3-d5aed650f8f6"

# ─── 1) Set properties ───────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=547,
    pattern="Graph",
    subpatterns=["Union Find or DFS"],
    tc="O(n²·α(n))",
    sc="O(n)",
    key_insight="Count connected components by unioning city pairs where isConnected[i][j]=1; each merge reduces province count by 1.",
    icon="🟡"
)
print("Properties set ✓")

# ─── 2) Wipe existing body ───────────────────────────────────────────────────
n_wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {n_wiped} old blocks ✓")

# ─── 3) Build blocks ─────────────────────────────────────────────────────────
blocks = []

# ── Problem statement ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("There are ", {}),
        ("n", {"code": True}),
        (" cities. You are given an ", {}),
        ("n×n", {"code": True}),
        (" matrix ", {}),
        ("isConnected", {"code": True}),
        (" where ", {}),
        ("isConnected[i][j] = 1", {"code": True}),
        (" means city ", {}),
        ("i", {"code": True}),
        (" and city ", {}),
        ("j", {"code": True}),
        (" are directly connected. A province is a group of cities that are directly or indirectly connected. Return the total number of provinces.", {})
    ])),
    N.divider(),
]

# ── Solution 1 — Union-Find ──
UNION_FIND_CODE = """\
def findCircleNum(isConnected):
    n = len(isConnected)
    parent = list(range(n))      # parent[i] = i: each city is its own root
    count = n                    # assume n provinces initially

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])   # path compression
        return parent[x]

    for i in range(n):
        for j in range(i + 1, n):        # upper triangle only
            if isConnected[i][j]:
                ri, rj = find(i), find(j)
                if ri != rj:             # different provinces — merge
                    parent[rj] = ri
                    count -= 1

    return count"""

blocks += [
    N.h2("Solution 1 — Union-Find with Path Compression (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("A 'province' is a connected component in an undirected graph. The question is simply: how many connected components exist? The n×n matrix encodes edges — cell (i,j)=1 means edge i-j."),
        N.h4("What Doesn't Work"),
        N.para("Brute force: count cells with value 1 — wrong, this counts direct edges, not groups. DFS works but requires maintaining a visited array and is harder to extend to dynamic edge insertion."),
        N.h4("The Key Observation"),
        N.para("If we start with n independent groups and merge groups whenever we find a road, the final number of groups is our answer. Union-Find is the perfect data structure for this — it merges in near-O(1) and never double-counts."),
        N.h4("Building the Solution"),
        N.para("Initialize parent[i]=i (each city its own root), count=n. Scan upper triangle. For each isConnected[i][j]=1, find roots of i and j. If different, merge (parent[rj]=ri) and count-=1. Return count."),
        N.callout("Analogy: Think of each city as an island. Each road is a bridge. Union-Find tracks which islands merge as we add bridges. At the end, count the distinct landmasses.", "🌊", "blue_background"),
    ]),
    N.h3("🔬 Algorithm Deep-Dive: Union-Find (DSU)"),
    N.para("Union-Find (Disjoint Set Union) was introduced by Galler & Fischer (1964), with near-linear analysis by Tarjan (1975). It answers 'same group?' and 'merge groups' in near-O(1) amortized time."),
    N.para(N.rich([
        ("Core invariant: ", {"bold": True}),
        ("Every node has a parent pointer leading to its component root. Two nodes share a component iff ", {}),
        ("find(a) == find(b)", {"code": True}),
        (". Path compression flattens trees so future lookups skip directly to the root. Union by rank attaches smaller trees under taller ones to prevent long chains.", {})
    ])),
    N.h3("Code"),
    N.code(UNION_FIND_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("parent = list(range(n))", {"code": True}), (" — each city i starts as its own root (parent[i] = i); n independent components.", {})])),
    N.para(N.rich([("count = n", {"code": True}), (" — begin with n provinces; we reduce this on every successful merge.", {})])),
    N.para(N.rich([("def find(x)", {"code": True}), (" — recursively chase parent pointers to the root. Path compression: set parent[x] = find(parent[x]) so x points directly to root after this call.", {})])),
    N.para(N.rich([("for j in range(i + 1, n)", {"code": True}), (" — scan upper triangle only; matrix is symmetric, scanning both halves would process each edge twice.", {})])),
    N.para(N.rich([("if isConnected[i][j]", {"code": True}), (" — only act on direct roads (=1); skip 0s.", {})])),
    N.para(N.rich([("ri, rj = find(i), find(j)", {"code": True}), (" — get root of each city's component; path compression fires here.", {})])),
    N.para(N.rich([("if ri != rj", {"code": True}), (" — critical guard: only merge if they are in DIFFERENT components. If same root, they're already united — skip to avoid double-decrement.", {})])),
    N.para(N.rich([("parent[rj] = ri", {"code": True}), (" — attach rj's tree under ri. Now all of rj's cities have ri as their root (lazily, via path compression on future finds).", {})])),
    N.para(N.rich([("count -= 1", {"code": True}), (" — two provinces just became one. Decrement the province count.", {})])),
    N.divider(),
]

# ── Solution 2 — DFS ──
DFS_CODE = """\
def findCircleNum(isConnected):
    n = len(isConnected)
    visited = [False] * n
    count = 0

    def dfs(city):
        for neighbor in range(n):
            if isConnected[city][neighbor] and not visited[neighbor]:
                visited[neighbor] = True
                dfs(neighbor)

    for i in range(n):
        if not visited[i]:
            visited[i] = True
            dfs(i)      # flood-fill all cities in this province
            count += 1  # one full province explored

    return count"""

blocks += [
    N.h2("Solution 2 — DFS Flood-Fill"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Imagine painting: start from any unvisited city, paint all cities reachable from it one color. Each time you pick up a new paint color (unvisited city), that's a new province."),
        N.h4("What Doesn't Work"),
        N.para("Naive BFS without a visited array would revisit cities infinitely in cycles. We must mark each city before recursing."),
        N.h4("The Key Observation"),
        N.para("Every unvisited city we find as a starting point represents a brand-new province we haven't seen yet. DFS from it marks the entire province."),
        N.h4("Building the Solution"),
        N.para("Keep a visited array. For each unvisited city i, increment count and DFS from i — marking all reachable cities. Return count."),
        N.callout("DFS is often easier to explain verbally in an interview. Union-Find is more elegant for dynamic scenarios. Both are O(n²) for this problem.", "💡", "green_background"),
    ]),
    N.h3("Code"),
    N.code(DFS_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("visited = [False] * n", {"code": True}), (" — track which cities have been explored.", {})])),
    N.para(N.rich([("def dfs(city)", {"code": True}), (" — recursively visit all neighbors of city that haven't been visited yet.", {})])),
    N.para(N.rich([("if not visited[i]", {"code": True}), (" — unvisited city = start of a new province we haven't counted yet.", {})])),
    N.para(N.rich([("visited[i] = True; dfs(i)", {"code": True}), (" — mark and flood-fill the entire province starting from city i.", {})])),
    N.para(N.rich([("count += 1", {"code": True}), (" — after DFS finishes, one complete province has been explored.", {})])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Union-Find", "O(n²·α(n)) ≈ O(n²)", "O(n) — parent array"],
        ["DFS", "O(n²)", "O(n) — visited + call stack"],
    ]),
    N.para("α(n) = inverse Ackermann function; effectively constant for all practical n. The n² matrix scan dominates both approaches."),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Graph — finding connected components in an undirected graph represented as an adjacency matrix.", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Union Find or DFS — from DSA Guide Section 17.4 (Union Find). Both approaches solve connected-components counting; Union-Find is preferred for dynamic connectivity.", {})])),
    N.callout(
        "When to recognize this pattern:\n"
        "• 'Number of groups / provinces / islands / clusters'\n"
        "• Input is adjacency matrix OR edge list (graph encoded)\n"
        "• 'Are these two nodes connected?' queries\n"
        "• Dynamic edge insertion (Union-Find preferred)\n"
        "• Cycle detection in undirected graphs",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Union Find / DFS connected-components technique:"),
    N.bullet(N.rich([("Number of Islands", {"bold": True}), (" (Medium) — 2D grid version; DFS flood-fill each island of 1s", {})])),
    N.bullet(N.rich([("Number of Connected Components in Undirected Graph", {"bold": True}), (" (Medium) — edge list input instead of adjacency matrix; same Union-Find approach", {})])),
    N.bullet(N.rich([("Redundant Connection", {"bold": True}), (" (Medium) — Union-Find cycle detection: find the edge where find(i)==find(j) before union", {})])),
    N.bullet(N.rich([("Graph Valid Tree", {"bold": True}), (" (Medium) — n-1 edges + no cycle via Union-Find = valid tree", {})])),
    N.bullet(N.rich([("Accounts Merge", {"bold": True}), (" (Medium) — union accounts sharing an email; same component = same person", {})])),
    N.bullet(N.rich([("Most Stones Removed with Same Row or Column", {"bold": True}), (" (Medium) — union stones sharing a row or column index", {})])),
    N.bullet(N.rich([("Making a Large Island", {"bold": True}), (" (Hard) — Union-Find to label and size existing islands, then simulate flipping one 0 to 1", {})])),
    N.para("These problems all reduce to: 'count or query connected components.' Union-Find handles them all in near-linear time."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 17.4 — Union Find (Disjoint Set)", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("number_of_provinces")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

# ─── 4) Append blocks ────────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"Appended {len(blocks)} blocks ✓")
print("NOTION OK", PAGE_ID)
