"""
gen_course_schedule_iv.py — Notion update for Course Schedule IV (LeetCode #1462)
Run from: /Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms/
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notion_lib as N

PAGE_ID = "39193418-809c-8129-bfe9-f21743b98bb2"
SLUG = "course_schedule_iv"

print("Step 1: Set page properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=1462,
    pattern="Graph",
    subpatterns=["Topo Sort + Reachability"],
    tc="O(n² + n·|E|)",
    sc="O(n²)",
    key_insight="Precompute n×n reachability matrix via topological sort + propagation; reach[i][v] |= reach[i][u] for edge u→v answers all queries in O(1).",
    icon="🟡"
)
print("  Properties set OK.")

print("Step 2: Wipe existing page body...")
n_deleted = N.wipe_page(PAGE_ID)
print(f"  Deleted {n_deleted} blocks.")

print("Step 3: Build and append content blocks...")

# ── Problem section ──
blocks = []
blocks.append(N.h2("Problem"))
blocks.append(N.para(
    "You have n courses labeled 0 to n-1. You are given an array prerequisites where "
    "prerequisites[i] = [a, b] indicates that course a must be taken before course b. "
    "You are also given an array queries where queries[j] = [u, v]. For the j-th query, "
    "you should answer whether course u is a prerequisite of course v or not (directly or indirectly). "
    "Return a boolean array answer, where answer[j] is the answer to the j-th query."
))
blocks.append(N.callout(
    N.rich([
        ("Constraints: ", {"bold": True}),
        ("2 ≤ n ≤ 100, 0 ≤ prerequisites.length ≤ n*(n-1)/2, "
         "0 ≤ queries.length ≤ 10⁴. The graph is a DAG (no cycles).")
    ]),
    "📌", "blue_background"
))
blocks.append(N.divider())

# ── Solution 1 — Optimal ──
blocks.append(N.h2("Solution 1 — Topological Sort + Reachability Matrix (Interview Pick)"))

blocks.append(N.toggle_h3("💡 Intuition: How to Arrive at This", [
    N.h4("Reframe the Problem"),
    N.para(
        "Prerequisites form a directed graph. Course u is a prerequisite of v if and only if "
        "there exists a directed path from u to v. With many queries, we need to answer each "
        "'can u reach v?' in O(1) — so precompute ALL reachability pairs."
    ),
    N.h4("What Doesn't Work"),
    N.para(
        "Naive: BFS/DFS from u for each query [u, v]. Time = O(q × (n + E)) where q can be 10⁴. "
        "With n=100 and 10⁴ queries, this is 10⁶ graph traversals — acceptable for constraints "
        "here, but we can do much better with precomputation."
    ),
    N.h4("The Key Observation"),
    N.para(
        "If we process nodes in topological order and maintain reach[i][j] = True when i can reach j, "
        "then for each edge u→v we can propagate: reach[i][v] |= reach[i][u] for all i. "
        "This means 'every ancestor of u is also an ancestor of v.' "
        "Topological order guarantees reach[i][u] is fully computed when we process edge u→v."
    ),
    N.h4("Building the Solution"),
    N.para(
        "1. Seed the matrix with direct edges (reach[a][b] = True for each prerequisite [a, b]). "
        "2. Use Kahn's BFS (topological sort): enqueue nodes with in-degree 0. "
        "3. When processing node u, for each neighbor v: propagate reach[i][v] |= reach[i][u] for all i. "
        "4. Decrement indegree[v]; enqueue v when it hits 0. "
        "5. Answer queries in O(1): return reach[u][v]."
    ),
    N.callout(
        "Analogy: Imagine 'reachability' as water flowing downstream. "
        "When we process node u, all water from upstream has already collected in u. "
        "Processing edge u→v then pours all that water into v simultaneously.",
        "🌊", "blue_background"
    ),
]))

blocks.append(N.h3("Algorithm Deep-Dive: Kahn's Algorithm (Topological Sort)"))
blocks.append(N.para(N.rich([
    ("Kahn's Algorithm (1962)", {"bold": True}),
    " is a BFS-based method to compute a topological ordering of a DAG. "
    "Core invariant: a node is dequeued only when its in-degree reaches 0, meaning all its "
    "predecessors have been processed. This guarantees that when we propagate through edge u→v, "
    "all paths leading into u are already captured in reach[·][u]. "
    "If any nodes remain unprocessed (in-degree still > 0) after BFS, the graph has a cycle. "
    "Recognition signals: 'process nodes in dependency order', 'compute something incrementally on a DAG'."
])))

blocks.append(N.h3("Code"))
blocks.append(N.code(
"""from collections import deque

def checkIfPrerequisite(n, prerequisites, queries):
    graph = [[] for _ in range(n)]
    indegree = [0] * n
    reach = [[False] * n for _ in range(n)]

    for a, b in prerequisites:
        graph[a].append(b)
        indegree[b] += 1
        reach[a][b] = True  # seed direct edges

    queue = deque(i for i in range(n) if indegree[i] == 0)

    while queue:
        u = queue.popleft()
        for v in graph[u]:
            for i in range(n):
                reach[i][v] |= reach[i][u]  # propagate all ancestors of u to v
            indegree[v] -= 1
            if indegree[v] == 0:
                queue.append(v)

    return [reach[u][v] for u, v in queries]""",
    "python"
))

blocks.append(N.h3("Line by Line"))
blocks.append(N.para(N.rich([("graph = [[] for _ in range(n)]", {"code": True}), " — Adjacency list; graph[a] stores all courses that directly follow a."])))
blocks.append(N.para(N.rich([("indegree = [0] * n", {"code": True}), " — In-degree array; indegree[b] counts how many prerequisites b has."])))
blocks.append(N.para(N.rich([("reach = [[False]*n for _ in range(n)]", {"code": True}), " — n×n boolean matrix; reach[i][j] = True means i is a prereq of j."])))
blocks.append(N.para(N.rich([("for a, b in prerequisites:", {"code": True}), " — Process each direct prerequisite pair. Build graph, update indegrees, seed matrix."])))
blocks.append(N.para(N.rich([("reach[a][b] = True", {"code": True}), " — Seed: course a directly reaches course b. This is the foundation for propagation."])))
blocks.append(N.para(N.rich([("queue = deque(i for i in range(n) if indegree[i] == 0)", {"code": True}), " — Start BFS with all courses that have no prerequisites."])))
blocks.append(N.para(N.rich([("u = queue.popleft()", {"code": True}), " — Dequeue the next node in topological order; all its predecessors are done."])))
blocks.append(N.para(N.rich([("for v in graph[u]:", {"code": True}), " — Process each course that directly depends on u."])))
blocks.append(N.para(N.rich([("reach[i][v] |= reach[i][u]", {"code": True}), " — KEY LINE: if node i can reach u, then i can also reach v (via edge u→v). Iterating over all i propagates all ancestors."])))
blocks.append(N.para(N.rich([("indegree[v] -= 1; if ... queue.append(v)", {"code": True}), " — Decrement v's in-degree. When it hits 0, all of v's prerequisites are done — enqueue v."])))
blocks.append(N.para(N.rich([("return [reach[u][v] for u, v in queries]", {"code": True}), " — O(1) per query: precomputed matrix lookup. No graph traversal needed."])))
blocks.append(N.divider())

# ── Solution 2 — Brute Force ──
blocks.append(N.h2("Solution 2 — BFS per Query (Brute Force)"))

blocks.append(N.toggle_h3("💡 Intuition: How to Arrive at This", [
    N.h4("Reframe the Problem"),
    N.para("For each query [u, v], we need to know if there's a directed path from u to v in the prerequisite graph."),
    N.h4("What Doesn't Work"),
    N.para("DFS with full recursion can be slow if queries repeat similar paths — no caching of previous results."),
    N.h4("The Key Observation"),
    N.para("BFS from the source u explores all reachable nodes level by level. If we find v, return True. Simple and correct."),
    N.h4("Building the Solution"),
    N.para("Build adjacency list. For each query [u, v], run a fresh BFS from u. Stop early if v is found."),
]))

blocks.append(N.h3("Code"))
blocks.append(N.code(
"""from collections import deque

def checkIfPrerequisite_brute(n, prerequisites, queries):
    graph = [[] for _ in range(n)]
    for a, b in prerequisites:
        graph[a].append(b)

    def bfs(src, dst):
        if src == dst:
            return False  # not a prerequisite of itself
        visited = {src}
        queue = deque([src])
        while queue:
            node = queue.popleft()
            for nb in graph[node]:
                if nb == dst:
                    return True
                if nb not in visited:
                    visited.add(nb)
                    queue.append(nb)
        return False

    return [bfs(u, v) for u, v in queries]""",
    "python"
))
blocks.append(N.divider())

# ── Complexity ──
N.append_blocks(PAGE_ID, blocks)
blocks = []

blocks.append(N.h2("Complexity"))
blocks.append(N.table([
    ["Solution", "Precompute Time", "Query Time", "Space"],
    ["BFS per Query (Brute)", "O(n + E)", "O(n + E) per query", "O(n)"],
    ["Topo Sort + Reach Matrix ✓", "O(n² + n·|E|)", "O(1)", "O(n²)"],
    ["Floyd-Warshall (alternative)", "O(n³)", "O(1)", "O(n²)"],
]))
blocks.append(N.divider())

# ── Pattern Classification ──
blocks.append(N.h2("🏷️ Pattern Classification"))
blocks.append(N.para(N.rich([("Main Pattern: ", {"bold": True}), "Graph"])))
blocks.append(N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Topo Sort + Reachability (Transitive Closure via Topological Sort)"])))
blocks.append(N.callout(
    N.rich([
        ("When to recognize this pattern: ", {"bold": True}),
        ("'Is A a prerequisite of B?' with multiple queries on a DAG. "
         "Constraint: n is small enough for O(n²) space. "
         "Keywords: prerequisite, dependency, reachability, directed graph, query pairs.")
    ]),
    "🔎", "green_background"
))
blocks.append(N.divider())

# ── Related Problems ──
blocks.append(N.h2("🔗 Related Problems"))
blocks.append(N.para("Problems using the same topological sort / DAG reachability technique:"))
blocks.append(N.bullet(N.rich([("Course Schedule", {"bold": True}), " (Medium) — Detect cycle in prerequisite graph via topological sort (#207)"])))
blocks.append(N.bullet(N.rich([("Course Schedule II", {"bold": True}), " (Medium) — Return valid topological ordering of all n courses (#210)"])))
blocks.append(N.bullet(N.rich([("All Paths From Source to Target", {"bold": True}), " (Medium) — DFS to enumerate all paths in DAG from 0 to n-1 (#797)"])))
blocks.append(N.bullet(N.rich([("Find Eventual Safe States", {"bold": True}), " (Medium) — Nodes that can't reach any cycle; reverse topological sort (#802)"])))
blocks.append(N.bullet(N.rich([("Parallel Courses", {"bold": True}), " (Medium) — Minimum semesters; longest path in DAG via topological DP (#1136)"])))
blocks.append(N.bullet(N.rich([("Minimum Height Trees", {"bold": True}), " (Medium) — Iterative leaf-pruning topological sort to find tree centroid (#310)"])))
blocks.append(N.para("These problems share the same core technique: processing a DAG in dependency order and propagating information downstream."))
blocks.append(N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 7 (Graph) · Sub-Pattern: Topo Sort + Reachability", "📚", "gray_background"))

# ── Embed section ──
blocks.append(N.divider())
blocks.append(N.h2("🎯 Interactive Visual Explainer"))
blocks.append(N.embed(N.embed_url_for(SLUG)))
blocks.append(N.para(N.rich([
    ("Step through the algorithm visually — use Next/Prev or arrow keys.",
     {"italic": True, "color": "gray"})
])))

N.append_blocks(PAGE_ID, blocks)
print(f"  Appended all blocks OK.")

# Verify
count = len(N.get_children(PAGE_ID))
print(f"  Total blocks now: {count}")
print(f"NOTION OK {PAGE_ID}")
