"""
gen_most_stones_removed_with_same_row_or_column.py
Regenerates Notion page IN-PLACE for LC #947.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81d9-a88f-f0b4ef956afd"

# ── 1. Properties ──────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=947,
    pattern="Graph",
    subpatterns=["Union by Row/Column"],
    tc="O(n · α(n))",
    sc="O(n)",
    key_insight="Stones sharing row/col form connected components; answer = n − #components. Union each stone's row-node with its col-node (offset) to group without O(n²) pairwise comparison.",
    icon="🟡"
)
print("Properties set.")

# ── 2. Wipe old content ────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3. Build body ──────────────────────────────────────────────────
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("On a 2D plane, we place ", {}),
        ("n", {"code": True}),
        (" stones at integer coordinates. A stone can be removed if it shares a row or column with another stone that has not been removed yet. Return the ", {}),
        ("maximum number of stones", {"bold": True}),
        (" that can be removed.", {}),
    ])),
    N.para(N.rich([
        ("Constraints: ", {"bold": True}),
        ("1 ≤ n ≤ 1000, 0 ≤ row, col ≤ 10000, no two stones are at the same position.", {}),
    ])),
    N.divider(),
]

# ── Solution 1: Union-Find (Interview Pick) ──
blocks += [
    N.h2("Solution 1 — Union-Find by Row/Column (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Instead of asking 'which stones CAN be removed?', ask 'which stones MUST stay?' A stone must stay if it is the sole stone in its row AND the sole stone in its column — it has no neighbor to enable removal. These are the 'survivors'. There is exactly one survivor per connected component. So: survivors = components, removals = n − components."),
        N.h4("What Doesn't Work"),
        N.para("Naive simulation: try removing stones one-by-one greedily. This requires checking all remaining stones each time — O(n²) per removal, O(n³) total. We need a structural insight, not iteration."),
        N.h4("The Key Observation"),
        N.para("Sharing a row or column is a connectivity relation. If A shares a row with B, and B shares a column with C, then A, B, C are transitively connected — within this group, all but one can be removed. This is precisely the structure of connected components in a graph."),
        N.h4("Building the Solution"),
        N.para("Step 1: Model stones as a graph where edges connect stones sharing a row or column. Step 2: Count connected components. Step 3: Return n − components. For efficiency, skip building O(n²) edges — instead use Union-Find where each stone's ROW-NODE is unioned with its COLUMN-NODE. Two stones sharing row r both union with r → automatically in the same component."),
        N.callout("Analogy: Think of rows and columns as 'hubs'. Each stone plugs into its row-hub AND column-hub. Two stones plugged into the same hub are connected. Union-Find merges hubs transitively.", "🧠", "blue_background"),
    ]),
    N.h3("🔬 Algorithm Deep-Dive: Union-Find (Disjoint Set Union)"),
    N.para("Union-Find is a data structure for maintaining a partition of elements into disjoint sets, supporting two operations: find(x) — return the root/representative of x's set; union(a,b) — merge the sets containing a and b. With path compression and union by rank, both operations run in O(α(n)) amortized time, where α is the inverse Ackermann function (practically ≤ 4 for all real inputs)."),
    N.para(N.rich([
        ("Key trick for this problem: ", {"bold": True}),
        ("Union row-node r with column-node c+10001. Rows occupy integers [0,10000]; columns+offset occupy [10001,20001]. Disjoint ranges mean no false merges between 'row 5' and 'column 5' (both raw integer 5 without the offset).", {}),
    ])),
    N.h3("Code"),
    N.code("""\
def removeStones(stones: list[list[int]]) -> int:
    parent = {}

    def find(x):
        if x not in parent:
            parent[x] = x           # lazy initialization
        if parent[x] != x:
            parent[x] = find(parent[x])  # path compression
        return parent[x]

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb         # merge: ra's root becomes rb

    # Union phase: link each stone's row-node to its col-node
    for r, c in stones:
        union(r, c + 10001)

    # Count phase: unique roots among stone row-nodes = #components
    seen = set()
    for r, c in stones:
        seen.add(find(r))

    return len(stones) - len(seen)
"""),
    N.h3("Line by Line"),
    N.para(N.rich([("parent = {}", {"code": True}), (" — lazy Union-Find dict; nodes auto-initialize on first find() call.", {})])),
    N.para(N.rich([("find(x)", {"code": True}), (" — returns root of x's component. If x is new, it becomes its own root. Path compression flattens the tree so future finds are O(1).", {})])),
    N.para(N.rich([("union(a, b)", {"code": True}), (" — finds both roots; if different, sets parent[ra] = rb, merging the two sets.", {})])),
    N.para(N.rich([("union(r, c + 10001)", {"code": True}), (" — the core step. Links row-node r to col-node c+10001. Any two stones sharing row r will both link to the same r node → same component root.", {})])),
    N.para(N.rich([("seen.add(find(r))", {"code": True}), (" — collect unique roots from row-nodes of all stones. Each unique root = one connected component.", {})])),
    N.para(N.rich([("return len(stones) - len(seen)", {"code": True}), (" — n minus components = max stones removable (one survivor per component).", {})])),
    N.divider(),
]

# ── Solution 2: DFS ──
blocks += [
    N.h2("Solution 2 — DFS on Adjacency List (Intuitive, O(n²))"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same formula: answer = n − #connected_components. Now model it explicitly as a graph: nodes are stones, edges connect any two stones sharing a row or column."),
        N.h4("What Doesn't Work"),
        N.para("We can't avoid comparing pairs of stones to build the adjacency list — that's O(n²). This approach is correct but slow for large n."),
        N.h4("The Key Observation"),
        N.para("Once the graph is built, connected components are found by standard DFS/BFS. Each unvisited node starts a new DFS, incrementing the component count."),
        N.h4("Building the Solution"),
        N.para("Step 1: For every pair (i,j), check if stones i and j share a row or column. If yes, add edges adj[i]↔adj[j]. Step 2: DFS from each unvisited stone, counting components. Step 3: return n − components."),
    ]),
    N.h3("Code"),
    N.code("""\
def removeStones(stones: list[list[int]]) -> int:
    n = len(stones)
    adj = [[] for _ in range(n)]

    for i in range(n):
        for j in range(i + 1, n):
            if stones[i][0] == stones[j][0] or stones[i][1] == stones[j][1]:
                adj[i].append(j)
                adj[j].append(i)

    visited = [False] * n
    components = 0

    def dfs(node):
        visited[node] = True
        for neighbor in adj[node]:
            if not visited[neighbor]:
                dfs(neighbor)

    for i in range(n):
        if not visited[i]:
            dfs(i)
            components += 1

    return n - components
"""),
    N.h3("Line by Line"),
    N.para(N.rich([("adj = [[] for _ in range(n)]", {"code": True}), (" — adjacency list for the stone graph.", {})])),
    N.para(N.rich([("if stones[i][0] == stones[j][0] or stones[i][1] == stones[j][1]", {"code": True}), (" — check same row (index 0) or same column (index 1).", {})])),
    N.para(N.rich([("dfs(node)", {"code": True}), (" — marks all reachable stones as visited, flooding the entire component.", {})])),
    N.para(N.rich([("components += 1", {"code": True}), (" — each DFS invocation from an unvisited node = one new component.", {})])),
    N.para(N.rich([("return n - components", {"code": True}), (" — same formula as Union-Find approach.", {})])),
    N.divider(),
]

# ── Complexity Table ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["DFS on Adjacency List", "O(n²)", "O(n²)"],
        ["Union-Find by Row/Col (optimal)", "O(n · α(n)) ≈ O(n)", "O(n)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Graph", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Union by Row/Column — a specialized Union-Find technique for 2D coordinate problems where row and column membership drives transitive connectivity.", {})])),
    N.callout(
        "When to recognize this pattern: (1) Items on a 2D grid connect via shared row OR column. (2) 'Remove if connected to another' — always leads to n − #components. (3) Large coordinate space → treat rows and columns as abstract nodes to avoid O(n²) pairwise comparison.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Union-Find / connected-components technique:"),
]
related = [
    ("Number of Islands", "Medium", "Classic 2D grid connected components via DFS or Union-Find — count 1-islands (#200)"),
    ("Redundant Connection", "Medium", "Find the extra edge that creates a cycle — detect same-root union (#684)"),
    ("Number of Connected Components in an Undirected Graph", "Medium", "Direct component count on edge list with Union-Find (#323)"),
    ("Accounts Merge", "Medium", "Union-Find on string keys (emails) to merge accounts with shared addresses (#721)"),
    ("Longest Consecutive Sequence", "Medium", "Union consecutive numbers into chains, find max-size component (#128)"),
    ("Graph Valid Tree", "Medium", "n−1 edges AND single component → valid tree (#261)"),
    ("Making a Large Island", "Hard", "Flip one 0 to 1, maximize merged component size — UF with size tracking (#827)"),
]
for name, diff, note in related:
    blocks.append(N.bullet(N.rich([
        (name, {"bold": True}),
        (f" ({diff})", {}),
        (" — " + note, {}),
    ])))
blocks.append(N.para("These problems share the core insight: model as a graph, count connected components, derive the answer from component structure."))
blocks.append(N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Graph section → Union-Find sub-pattern. Sub-Pattern verified via analysis (Union by Row/Column is a specialized technique not in the standard table but derived from the Union-Find sub-pattern).", "📚", "gray_background"))

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("most_stones_removed_with_same_row_or_column")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})
    ])),
]

# ── Append ──
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
print(f"Total blocks appended: {len(blocks)}")
