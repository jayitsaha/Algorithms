"""
gen_sort_items_by_groups_respecting_dependencies.py
Regenerates the Notion page IN-PLACE for:
  #1203 Sort Items by Groups Respecting Dependencies (Hard, Graph, Two-Level Topo Sort)
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-813c-aaa9-dd8150723fa9"

# ── 1. Set Properties ────────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=1203,
    pattern="Graph",
    subpatterns=["Two-Level Topo Sort"],
    tc="O(n+m+E)",
    sc="O(n+m+E)",
    key_insight="Run Kahn's BFS topo sort at the item level AND group level separately, then bucket items by group and emit in group-topo order.",
    icon="🔴",
)
print("Properties set OK.")

# ── 2. Wipe old body ─────────────────────────────────────────────────────────
print("Wiping old body...")
deleted = N.wipe_page(PAGE_ID)
print(f"Wiped {deleted} blocks.")

# ── 3. Build body blocks ──────────────────────────────────────────────────────
blocks = []

# ─── Problem Statement ───────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("LeetCode #1203 — Hard\n\n", {}),
        ("Given ", {}),
        ("n", {"code": True}),
        (" items numbered 0..n-1, each belonging to one of ", {}),
        ("m", {"code": True}),
        (" groups (or ", {}),
        ("group[i] == -1", {"code": True}),
        (" if ungrouped). You are also given ", {}),
        ("beforeItems[i]", {"code": True}),
        (" — a list of items that MUST appear before item ", {}),
        ("i", {"code": True}),
        (" in the output.\n\n", {}),
        ("Return any valid ordering that satisfies:\n"
         "1. All before-dependencies (item b appears before item i whenever b is in beforeItems[i]).\n"
         "2. All items of the same group appear consecutively (no interleaving between groups).\n\n"
         "Return [] if no valid ordering exists (cycle detected).", {}),
    ])),
    N.divider(),
]

# ─── Solution 1: Two-Level Kahn's BFS (Interview Pick) ──────────────────────
SOL1_CODE = """\
from collections import defaultdict, deque

def sortItems(n, m, group, beforeItems):
    # Step 1: Assign synthetic group IDs to ungrouped items
    gid = m
    for i in range(n):
        if group[i] == -1:
            group[i] = gid
            gid += 1

    # Step 2: Build item graph and group graph simultaneously
    item_graph = defaultdict(list)   # before -> item
    item_indeg = [0] * n
    grp_graph  = defaultdict(set)    # use set to deduplicate group edges!
    grp_indeg  = [0] * gid           # size = gid (not m), covers synthetic groups

    for i in range(n):
        for b in beforeItems[i]:     # b must come before i
            item_graph[b].append(i)
            item_indeg[i] += 1
            if group[b] != group[i]:  # cross-group dependency
                if group[i] not in grp_graph[group[b]]:  # dedup!
                    grp_graph[group[b]].add(group[i])
                    grp_indeg[group[i]] += 1

    # Step 3: Kahn's BFS topological sort helper
    def topo(nodes, graph, indeg):
        q = deque(v for v in nodes if indeg[v] == 0)
        order = []
        while q:
            v = q.popleft()
            order.append(v)
            for nb in graph[v]:
                indeg[nb] -= 1
                if indeg[nb] == 0:
                    q.append(nb)
        return order

    # Step 4: Topo sort items, then groups
    item_order = topo(range(n), item_graph, item_indeg)
    if len(item_order) != n:         # item-level cycle
        return []
    grp_order = topo(range(gid), grp_graph, grp_indeg)
    if len(grp_order) != gid:        # group-level cycle
        return []

    # Step 5: Bucket items by group (preserving item topo order)
    buckets = defaultdict(list)
    for item in item_order:
        buckets[group[item]].append(item)

    # Step 6: Emit groups in group-topo order (each group's bucket contiguously)
    result = []
    for g in grp_order:
        result.extend(buckets[g])
    return result
"""

blocks += [
    N.h2("Solution 1 — Two-Level Kahn's BFS (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We must produce an ordering of items such that (a) dependencies are respected and (b) all items of a group appear consecutively. The ordering constraint on items is a classic topological sort. The contiguity constraint on groups implies that if any item in group A depends on any item in group B, all of group B must appear before all of group A — i.e., there is a hidden dependency between the groups themselves."),
        N.h4("What Doesn't Work"),
        N.para("A single topological sort of items alone doesn't guarantee groups are contiguous — items from different groups could be interleaved if their per-item dependencies allow it. Trying to enforce contiguity as a post-processing step is complex and error-prone."),
        N.h4("The Key Observation"),
        N.para("Cross-group item dependencies create implicit dependencies between groups. If item b (group X) must precede item i (group Y), then the ENTIRE group X must precede the ENTIRE group Y. So we have TWO independent DAGs: one over items, one over groups. Both must be topologically sorted."),
        N.h4("Building the Solution"),
        N.para(
            "1. Unify the group concept: assign synthetic group IDs to ungrouped items so every item has a group.\n"
            "2. Build BOTH DAGs in a single pass over beforeItems.\n"
            "3. Run Kahn's BFS on item DAG. If cycle detected (result length < n): return [].\n"
            "4. Run Kahn's BFS on group DAG. If cycle detected: return [].\n"
            "5. Bucket items by their group, in item-topo order.\n"
            "6. Emit buckets in group-topo order."
        ),
        N.callout(
            "Analogy: Think of items as employees and groups as departments. A valid org-chart schedule "
            "must place all of Department A before Department B if any A-employee needs a result from "
            "any B-employee. Sort within departments (item topo), sort between departments (group topo), "
            "then schedule all of Dept A, then all of Dept B, etc.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("🔬 Algorithm Deep-Dive: Kahn's BFS Topological Sort"),
    N.para(N.rich([
        ("Origin: ", {"bold": True}),
        ("Kahn's algorithm (1962) finds a topological ordering of a DAG in O(V+E) time using BFS. "
         "It processes nodes in 'dependency order': a node is ready to emit when all its prerequisites have been emitted (in-degree reaches 0). "
         "Cycle detection is a free side-effect: if the emitted count is less than the total node count, at least one cycle exists.\n\n", {}),
        ("Core Invariant: ", {"bold": True}),
        ("When a node v is dequeued and emitted, every node that had an edge pointing to v has already been emitted. "
         "This guarantees the output is a valid topological ordering.\n\n", {}),
        ("Why it works: ", {"bold": True}),
        ("A node enters the queue only when its in-degree reaches 0 — meaning all its prerequisites are done. "
         "The BFS ordering then naturally emits nodes in dependency order. "
         "Any node in a cycle never reaches in-degree 0 (its cycle partners always hold one pending edge), "
         "so it's never emitted — giving the length check its power.", {}),
    ])),
    N.code("""\
# Kahn's Algorithm Template
from collections import deque

def kahn_topo_sort(n, adj, indeg):
    queue = deque(v for v in range(n) if indeg[v] == 0)
    order = []
    while queue:
        v = queue.popleft()
        order.append(v)
        for nb in adj[v]:
            indeg[nb] -= 1
            if indeg[nb] == 0:
                queue.append(nb)
    return order if len(order) == n else []  # [] means cycle exists
"""),
    N.h3("Code"),
    N.code(SOL1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([
        ("gid = m", {"code": True}), (" — Next available synthetic group ID. Real groups are 0..m-1.", {})])),
    N.para(N.rich([
        ("if group[i] == -1: group[i] = gid; gid += 1", {"code": True}),
        (" — Give each ungrouped item its own private singleton group.", {})])),
    N.para(N.rich([
        ("grp_graph = defaultdict(set)", {"code": True}),
        (" — Use a SET (not list) to automatically deduplicate group edges.", {})])),
    N.para(N.rich([
        ("grp_indeg = [0] * gid", {"code": True}),
        (" — Size must be gid (real + synthetic groups), NOT just m. Using m causes index-out-of-bounds.", {})])),
    N.para(N.rich([
        ("if group[b] != group[i]:", {"code": True}),
        (" — Only add group edge for CROSS-group dependencies. Same-group deps are handled by item topo sort.", {})])),
    N.para(N.rich([
        ("if group[i] not in grp_graph[group[b]]:", {"code": True}),
        (" — Check before adding to prevent duplicate increments of grp_indeg, which would cause false cycle detection.", {})])),
    N.para(N.rich([
        ("q = deque(v for v in nodes if indeg[v] == 0)", {"code": True}),
        (" — Seed Kahn's queue with all zero-in-degree nodes (no prerequisites).", {})])),
    N.para(N.rich([
        ("for nb in graph[v]: indeg[nb] -= 1", {"code": True}),
        (" — 'Complete' node v: remove its outgoing edges from the graph by decrementing successors' in-degrees.", {})])),
    N.para(N.rich([
        ("if len(item_order) != n: return []", {"code": True}),
        (" — Cycle check: if we couldn't emit all n items, a cycle prevented some from reaching in-degree 0.", {})])),
    N.para(N.rich([
        ("for item in item_order: buckets[group[item]].append(item)", {"code": True}),
        (" — Bucket items by their group. Since we iterate item_order (already dep-sorted), "
         "the bucket for each group automatically has items in a valid dep order.", {})])),
    N.para(N.rich([
        ("for g in grp_order: result.extend(buckets[g])", {"code": True}),
        (" — Emit each group's bucket consecutively, in the group-topo order. "
         "This satisfies both the contiguity constraint and the cross-group ordering constraint.", {})])),
    N.divider(),
]

# ─── Solution 2: DFS-Based Topo Sort ────────────────────────────────────────
SOL2_CODE = """\
from collections import defaultdict

def sortItems(n, m, group, beforeItems):
    # Step 1: Assign synthetic group IDs
    gid = m
    for i in range(n):
        if group[i] == -1:
            group[i] = gid
            gid += 1

    # Step 2: Build item and group graphs
    item_graph = defaultdict(list)
    grp_graph  = defaultdict(set)

    for i in range(n):
        for b in beforeItems[i]:
            item_graph[b].append(i)
            if group[b] != group[i]:
                grp_graph[group[b]].add(group[i])

    # Step 3: DFS-based topo sort with cycle detection
    # Colors: 0=WHITE (unvisited), 1=GRAY (in stack), 2=BLACK (done)
    def dfs_topo(nodes, graph):
        color = {v: 0 for v in nodes}
        order = []
        has_cycle = [False]

        def dfs(v):
            if has_cycle[0]: return
            color[v] = 1  # GRAY: in current DFS path
            for nb in graph.get(v, []):
                if color[nb] == 1:   # back edge -> cycle!
                    has_cycle[0] = True
                    return
                if color[nb] == 0:
                    dfs(nb)
            color[v] = 2  # BLACK: fully processed
            order.append(v)

        for v in nodes:
            if color[v] == 0:
                dfs(v)

        if has_cycle[0]:
            return []
        return order[::-1]  # reverse post-order = topo order

    item_order = dfs_topo(range(n), item_graph)
    if not item_order: return []

    grp_order = dfs_topo(range(gid), grp_graph)
    if not grp_order: return []

    buckets = defaultdict(list)
    for item in item_order:
        buckets[group[item]].append(item)

    result = []
    for g in grp_order:
        result.extend(buckets[g])
    return result
"""

blocks += [
    N.h2("Solution 2 — DFS-Based Topological Sort"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same two-level structure as Solution 1, but we use DFS instead of BFS for topological sorting. "
               "DFS produces a post-order traversal; reversing it gives the topological order."),
        N.h4("What Doesn't Work"),
        N.para("Naive DFS without color-coding cannot detect cycles — we might revisit nodes infinitely. "
               "We need the GRAY/WHITE/BLACK (3-color) approach to distinguish back edges (cycles) "
               "from cross/forward edges."),
        N.h4("The Key Observation"),
        N.para("In DFS, a back edge (neighbor has color GRAY, meaning it's in the current recursion stack) "
               "indicates a cycle. The post-order of DFS (when we finish exploring all of a node's successors) "
               "reversed is a valid topological ordering."),
        N.h4("Building the Solution"),
        N.para("Use 3-color DFS on both item graph and group graph. "
               "If a back edge is found, return [] immediately. "
               "Post-order reversed = topo order. The bucketing and merge step is identical to Solution 1."),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([
        ("color[v] = 1  # GRAY", {"code": True}),
        (" — Mark v as 'in progress'. If we encounter a GRAY node during DFS, we found a cycle.", {})])),
    N.para(N.rich([
        ("if color[nb] == 1: has_cycle[0] = True", {"code": True}),
        (" — Back edge: nb is already in current DFS stack → cycle detected.", {})])),
    N.para(N.rich([
        ("color[v] = 2  # BLACK", {"code": True}),
        (" — Mark v as done. All its descendants have been processed.", {})])),
    N.para(N.rich([
        ("order.append(v)  # post-order", {"code": True}),
        (" — We add v AFTER processing all its successors. Reversing this gives topo order.", {})])),
    N.para(N.rich([
        ("return order[::-1]", {"code": True}),
        (" — Reverse post-order gives the topological ordering (earlier nodes first).", {})])),
    N.divider(),
]

# ─── Complexity Table ────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Brute Force (all permutations)", "O(n!)", "O(n)", "Infeasible for n > 10"],
        ["Two-Level Kahn's BFS (optimal)", "O(n+m+E)", "O(n+m+E)", "Interview pick — simple, cycle-detection free"],
        ["DFS-Based Topo Sort", "O(n+m+E)", "O(n+m+E)", "Same complexity, recursion stack overhead"],
    ]),
    N.divider(),
]

# ─── Pattern Classification ──────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Graph", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Two-Level Topo Sort", {})])),
    N.para(N.rich([
        ("Verified: ", {"bold": True}),
        ("DSA_Patterns_and_SubPatterns_Guide.md Section 17.3 — "
         "\"Sort Items by Groups Respecting Dependencies | Hard | Two-Level Topo Sort\"", {})
    ])),
    N.callout(
        "When to recognize this pattern:\n"
        "• 'Must come before' / 'prerequisite' / 'dependency ordering' → Topological Sort\n"
        "• 'Items must appear consecutively' / 'groups must be contiguous' → Two-Level DAG\n"
        "• 'Return any valid order or [] if impossible' → Kahn's with cycle check\n"
        "• 'group[i] == -1' (ungrouped items) → Assign synthetic singleton group IDs",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ─── Related Problems ────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Topological Sort / Two-Level technique:"),
    N.bullet(N.rich([("Course Schedule II", {"bold": True}), (" (Medium) — Single-level Kahn's BFS topo sort with cycle detection", {})])),
    N.bullet(N.rich([("Alien Dictionary", {"bold": True}), (" (Hard) — Build graph from character ordering constraints, then topo sort", {})])),
    N.bullet(N.rich([("Parallel Courses III", {"bold": True}), (" (Hard) — Topo sort + critical path DP on weighted DAG", {})])),
    N.bullet(N.rich([("Find All Possible Recipes from Given Supplies", {"bold": True}), (" (Medium) — Topo sort with supply availability check", {})])),
    N.bullet(N.rich([("Sequence Reconstruction", {"bold": True}), (" (Medium) — Verify that a unique topological order exists", {})])),
    N.bullet(N.rich([("Largest Color Value in a Directed Graph", {"bold": True}), (" (Hard) — Topo sort + DP tracking color frequencies", {})])),
    N.bullet(N.rich([("Minimum Height Trees", {"bold": True}), (" (Medium) — BFS leaf-removal (topological peeling) to find tree centroid", {})])),
    N.para("These problems share the same core technique: model ordering constraints as a DAG and use Kahn's BFS or DFS post-order to find a valid topological ordering. The Two-Level variant adds a second DAG at the group level."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 17.3 Topological Sort", "📚", "gray_background"),
]

# ─── Interactive Visual Explainer ────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("sort_items_by_groups_respecting_dependencies")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── 4. Append blocks ─────────────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks to Notion...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
