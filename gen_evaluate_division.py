"""
gen_evaluate_division.py — Notion update for LeetCode #399 Evaluate Division
Weighted Union-Find / BFS on Weighted Graph
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-8113-95e5-c663688add48"
SLUG = "evaluate_division"

# 1) Set properties
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=399,
    pattern="Graph",
    subpatterns=["Union-Find with Weights", "BFS: Weighted Graph Path"],
    tc="O((E+Q)*alpha(V))",
    sc="O(V+E)",
    key_insight="Model equations as weighted edges (A->B weight k, B->A weight 1/k); multiply weights along BFS path — division telescopes.",
    icon="🟡"
)
print("Properties set.")

# 2) Wipe existing content
print("Wiping old content...")
deleted = N.wipe_page(PAGE_ID)
print(f"Deleted {deleted} blocks.")

# 3) Build body — helpers
def lbl(code_str, explanation):
    """Code label + explanation paragraph."""
    return N.para(N.rich([
        (code_str, {"code": True}),
        (" — " + explanation, {})
    ]))

blocks = []

# ── Problem ──────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(
        "You are given a list of equations like A / B = k, where A and B are strings and k "
        "is a real number, plus a list of queries. For each query (Cj, Dj), return the answer "
        "to Cj / Dj. Return -1.0 if the answer does not exist (unknown variable or disconnected components)."
    ),
    N.para(
        "Example: equations = [[\"a\",\"b\"],[\"b\",\"c\"]], values = [2.0, 3.0], "
        "queries = [[\"a\",\"c\"],[\"b\",\"a\"],[\"a\",\"e\"],[\"a\",\"a\"],[\"x\",\"x\"]]. "
        "Output: [6.0, 0.5, -1.0, 1.0, -1.0]."
    ),
    N.divider(),
]

# ── Solution 1: BFS ───────────────────────────────────────────────
BFS_CODE = """\
from collections import defaultdict, deque

def calcEquation(equations, values, queries):
    # Build weighted bidirectional graph
    graph = defaultdict(dict)
    for (a, b), k in zip(equations, values):
        graph[a][b] = k          # a/b = k
        graph[b][a] = 1.0 / k   # b/a = 1/k (reverse)

    def bfs(src, dst):
        # Guard: unknown variables
        if src not in graph or dst not in graph:
            return -1.0
        # Guard: same variable
        if src == dst:
            return 1.0
        visited = {src}
        # Queue carries (node, cumulative_ratio = src/node)
        queue = deque([(src, 1.0)])
        while queue:
            node, ratio = queue.popleft()
            for nbr, w in graph[node].items():
                if nbr == dst:
                    return ratio * w   # (src/node)*(node/dst) = src/dst
                if nbr not in visited:
                    visited.add(nbr)
                    queue.append((nbr, ratio * w))
        return -1.0  # dst unreachable from src

    return [bfs(s, d) for s, d in queries]
"""

blocks += [
    N.h2("Solution 1 — BFS on Weighted Graph"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We're given pairwise ratios and asked for derived ratios. This is a graph "
            "reachability problem: can we trace a chain of known ratios from the numerator "
            "variable to the denominator variable?"
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Storing all derived ratios upfront requires O(V^2) space and preprocessing. "
            "A naive formula substitution is complicated. We need a graph traversal that "
            "naturally composes ratios along a path."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Division telescopes: (A/B) x (B/C) = A/C — the intermediate variable B "
            "cancels out. Model variables as nodes, equations as weighted edges "
            "(A->B weight k, B->A weight 1/k). The product of weights along any path "
            "from src to dst equals src/dst."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. Build adjacency list with bidirectional weighted edges.\n"
            "2. For each query (src, dst): guard for unknowns; guard for self-division.\n"
            "3. BFS from src, carrying cumulative product (invariant: product = src/currentNode).\n"
            "4. When we reach dst, return the accumulated product = src/dst."
        ),
        N.callout(
            "Analogy: Think of exchange rates. If 1 USD = 2 EUR and 1 EUR = 3 GBP, "
            "then 1 USD = 6 GBP. The EUR cancels out — same as our intermediate variable B.",
            "🧠", "blue_background"
        )
    ]),
    N.h3("Code"),
    N.code(BFS_CODE),
    N.h3("Line by Line"),
    lbl("graph = defaultdict(dict)",
        "Adjacency list: graph[u][v] = weight u/v. defaultdict handles new nodes gracefully."),
    lbl("graph[a][b] = k; graph[b][a] = 1/k",
        "Bidirectional edges: A/B=k implies B/A=1/k. Storing both lets BFS traverse in either direction without special logic."),
    lbl("if src not in graph or dst not in graph: return -1.0",
        "Guard: if either variable never appeared in any equation, we have no information. Return -1.0 immediately without BFS."),
    lbl("if src == dst: return 1.0",
        "Self-division guard: any known variable divided by itself is 1. (Unknown variables are caught by the prior guard.)"),
    lbl("queue = deque([(src, 1.0)])",
        "BFS queue carries (node, cumulative_ratio). ratio = src/node accumulated along the path. Starts at 1.0 since src/src = 1."),
    lbl("if nbr == dst: return ratio * w",
        "Early return: ratio = src/node, w = node/dst, so ratio*w = src/dst. The intermediate 'node' cancels algebraically."),
    lbl("queue.append((nbr, ratio * w))",
        "Extend path: new_ratio = src/nbr = (src/node)*(node/nbr) = ratio * w. The BFS invariant is maintained at every step."),
    N.divider(),
]

# ── Solution 2: Weighted Union-Find ──────────────────────────────
UF_CODE = """\
def calcEquation(equations, values, queries):
    parent, weight = {}, {}   # weight[x] = x / root(x)

    def find(x):
        if parent[x] != x:
            orig = parent[x]              # save old parent BEFORE recursion
            parent[x] = find(parent[x])   # path compression
            weight[x] *= weight[orig]     # x/root = (x/orig) * (orig/root)
        return parent[x]

    def union(a, b, k):   # encode a/b = k
        for v in (a, b):
            if v not in parent:
                parent[v] = v; weight[v] = 1.0   # new node is its own root
        ra, rb = find(a), find(b)
        if ra == rb: return                        # already same component
        parent[ra] = rb
        # rootA/rootB = k * (B/rootB) / (A/rootA) = k * weight[b] / weight[a]
        weight[ra] = k * weight[b] / weight[a]

    for (a, b), k in zip(equations, values):
        union(a, b, k)

    results = []
    for src, dst in queries:
        if src not in parent or dst not in parent:
            results.append(-1.0)
        elif find(src) != find(dst):
            results.append(-1.0)
        else:
            results.append(weight[src] / weight[dst])  # (src/root)/(dst/root) = src/dst
    return results
"""

UF_TEMPLATE = """\
# Core Invariant: weight[x] = x / root(x)   (maintained by find and union)

def find(x):
    if parent[x] != x:
        orig = parent[x]        # save BEFORE parent changes
        parent[x] = find(parent[x])  # path compression
        weight[x] *= weight[orig]    # multiply through: x/root = (x/orig)*(orig/root)
    return parent[x]

def union(a, b, k):   # a/b = k
    ra, rb = find(a), find(b)
    if ra == rb: return
    parent[ra] = rb
    # weight[ra] = ra/rb = k * (b/rb) / (a/ra) = k * weight[b] / weight[a]
    weight[ra] = k * weight[b] / weight[a]

# Query: src/dst
if find(src) == find(dst):
    return weight[src] / weight[dst]  # (src/root) / (dst/root) = src/dst
"""

blocks += [
    N.h2("Solution 2 — Weighted Union-Find (Interview Pick, Optimal)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "BFS repeats work for every query. Can we precompute relationships so each "
            "query is O(1)? Union-Find tracks connected components — extend it to track "
            "the numeric ratio from each node to its component root."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Standard Union-Find only gives yes/no connectivity. We need the actual ratio "
            "between two nodes. Simply knowing they are in the same group is insufficient — "
            "we need to know HOW they relate numerically to the group representative."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Maintain the invariant: weight[x] = x / root(x) at all times. "
            "If two nodes share a root, then src/dst = (src/root) / (dst/root) = "
            "weight[src] / weight[dst]. Queries become a single division after find()."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. Initialize: each node is its own root with weight 1.0 (x/x = 1).\n"
            "2. Union(A, B, k): find roots, link rootA -> rootB with computed weight.\n"
            "3. Find(x): recursively compress path, multiplying weights through the chain.\n"
            "4. Query(src, dst): same root -> weight[src]/weight[dst]; else -1.0."
        ),
        N.callout(
            "Formula derivation for union weight: we need rootA/rootB. "
            "Given A/B=k and weight[A]=A/rootA, weight[B]=B/rootB: "
            "rootA/rootB = k * weight[B] / weight[A]. "
            "This follows from: A = k*B, so rootA*(A/rootA) = k * rootB*(B/rootB), "
            "therefore rootA/rootB = k * (B/rootB) / (A/rootA).",
            "🧮", "purple_background"
        )
    ]),
    N.h3("Algorithm Deep-Dive: Weighted Union-Find"),
    N.para(
        "Standard Union-Find (Tarjan 1975) tracks connected components using a parent forest "
        "with path compression and union by rank, giving O(alpha(n)) per operation. "
        "Weighted Union-Find attaches a weight to each parent pointer representing "
        "the ratio x/parent[x], so that find() accumulates the ratio to the root."
    ),
    N.code(UF_TEMPLATE),
    N.h3("Code"),
    N.code(UF_CODE),
    N.h3("Line by Line"),
    lbl("orig = parent[x]",
        "CRITICAL: save the old parent BEFORE the recursive call. After find(parent[x]) "
        "returns, parent[x] has been compressed to point to the root. We need the "
        "intermediate parent to correctly chain the weight multiplication."),
    lbl("parent[x] = find(parent[x])",
        "Path compression: after this, parent[x] points directly to the root. "
        "Subsequent find() calls on x are O(1)."),
    lbl("weight[x] *= weight[orig]",
        "Weight update: weight[x] = x/root = (x/orig) * (orig/root) = weight_old[x] * weight[orig]. "
        "After orig's path is compressed, weight[orig] = orig/root."),
    lbl("weight[ra] = k * weight[b] / weight[a]",
        "Union link weight: rootA/rootB = k*(B/rootB)/(A/rootA) = k*weight[b]/weight[a]. "
        "Note we use weight[a] and weight[b] AFTER find(a) and find(b) have been called."),
    lbl("weight[src] / weight[dst]",
        "Query answer: weight[src] = src/root, weight[dst] = dst/root. "
        "Their quotient = (src/root)/(dst/root) = src/dst. Both must share the same root."),
    N.callout(
        "WARNING: A common bug is writing weight[x] *= weight[parent[x]] AFTER "
        "the recursive call. At that point, parent[x] has been compressed to the root, "
        "so weight[parent[x]] = weight[root] = 1.0 — giving wrong answers silently. "
        "Always save orig = parent[x] BEFORE the recursive call.",
        "⚠️", "yellow_background"
    ),
    N.divider(),
]

# ── Complexity ───────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Build Time", "Per Query", "Total"],
        ["BFS per query", "O(E)", "O(V+E)", "O(E + Q*(V+E))"],
        ["Weighted Union-Find (optimal)", "O(E*alpha(V))", "O(alpha(V)) ~ O(1)", "O((E+Q)*alpha(V))"],
        ["Floyd-Warshall (all-pairs)", "O(V^3)", "O(1)", "O(V^3 + Q)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ────────────────────────────────────────
blocks += [
    N.h2("Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Graph Algorithms", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Union-Find with Weights; BFS: Weighted Graph Path", {})])),
    N.callout(
        "When to recognize this pattern:\n"
        "(1) 'Given pairwise ratios/distances, compute transitive results' -> weighted graph or UF.\n"
        "(2) Variables linked by multiplicative relationships -> model as edges, traverse to find chain.\n"
        "(3) Many connectivity + numeric queries -> Weighted Union-Find is optimal (O(1)/query).\n"
        "(4) 'A/B = k' or 'A - B = d' constraints -> graph with weighted edges.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────────
blocks += [
    N.h2("Related Problems"),
    N.para("Problems using the same technique (Weighted Graph / Union-Find):"),
]
related = [
    ("Number of Connected Components (#323)", "Medium",
     "Standard UF without weights — same component-detection skeleton"),
    ("Redundant Connection (#684)", "Medium",
     "UF detects the one edge that creates a cycle in an undirected graph"),
    ("Network Delay Time (#743)", "Medium",
     "Dijkstra on weighted graph; additive path costs instead of multiplicative"),
    ("Path with Maximum Probability (#1514)", "Medium",
     "Dijkstra with multiplicative weights; maximize product along a path"),
    ("Accounts Merge (#721)", "Medium",
     "Union-Find with string keys; merges identity groups sharing common elements"),
    ("Find if Path Exists in Graph (#1971)", "Easy",
     "Basic BFS/UF connectivity check, unweighted variant"),
    ("Cheapest Flights Within K Stops (#787)", "Medium",
     "Constrained shortest path on weighted graph; Bellman-Ford variant"),
]
for name, diff, note in related:
    blocks.append(N.bullet(N.rich([
        (name, {"bold": True}),
        (f" ({diff}) — {note}", {})
    ])))
blocks.append(N.para(
    "These problems share the core technique: model relationships as weighted edges, "
    "traverse or union to answer queries about transitive relationships."
))
blocks.append(N.callout(
    "Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 7: Graph Algorithms\n"
    "Sub-Pattern: Union-Find with Weights / BFS: Weighted Graph Path",
    "📚", "gray_background"
))

# ── Embed ─────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the BFS algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ]))
]

# 4) Append all blocks
print(f"Appending {len(blocks)} blocks...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
