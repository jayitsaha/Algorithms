"""gen_find_eventual_safe_states.py — Notion update for LeetCode #802."""
import sys, os
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-81e6-b158-e520ef7fa7e0"

# ── 1) Properties ────────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=802,
    pattern="Graph",
    subpatterns=["Reverse Graph Topo Sort"],
    tc="O(V+E)",
    sc="O(V+E)",
    key_insight="Reverse the graph; BFS from terminal nodes (out_deg=0). Nodes Kahn's never reaches are in cycles — unsafe.",
    icon="🟡",
)
print("Properties set.")

# ── 2) Wipe old body ─────────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3) Build body blocks ─────────────────────────────────────────────────────
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a directed graph with ", {}),
        ("n", {"code": True}),
        (" nodes (0 to n−1), where ", {}),
        ("graph[i]", {"code": True}),
        (" lists all nodes node ", {}),
        ("i", {"code": True}),
        (" has a directed edge to. A node is a ", {}),
        ("terminal node", {"bold": True}),
        (" if it has no outgoing edges. A node is a ", {}),
        ("safe node", {"bold": True}),
        (" if every possible path starting from that node eventually leads to a terminal node. "
         "Return all safe nodes, sorted in ascending order.", {}),
    ])),
    N.divider(),
]

# Solution 1 — Reverse Graph + Kahn's BFS
blocks += [
    N.h2("Solution 1 — Reverse Graph + Kahn's BFS (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("A path from node X fails to terminate if and only if it enters a cycle. So 'safe' means: no cycle is reachable from X. 'Unsafe' means: on a cycle, or there exists some path leading into one."),
        N.h4("What Doesn't Work"),
        N.para("A naive DFS from every node to check for cycles would be O(V·(V+E)) — recomputing the same reachability repeatedly. We need a way to compute safety for all nodes in a single O(V+E) pass."),
        N.h4("The Key Observation"),
        N.para("Safety propagates backward. Terminal nodes (no exits) are trivially safe. Any node whose EVERY exit leads to a safe node is also safe. This backward propagation can be efficiently driven by reversing the graph edges and running Kahn's BFS from terminals as seeds."),
        N.h4("Building the Solution"),
        N.para("1) Build reverse adjacency list + track out_deg[u] = original out-degree of u. "
               "2) Push all nodes with out_deg==0 into queue (terminals = safe seeds). "
               "3) BFS: pop v → safe.add(v). For each u in rev[v]: decrement out_deg[u]. If out_deg[u]==0, enqueue u. "
               "4) Return sorted(safe). Nodes never enqueued are in cycles."),
        N.callout(
            "Analogy: Think of safety spreading like water flowing upstream. Terminals are the ocean. Water flows backward up each river until it hits a cycle — cycles trap the water, never letting it reach the ocean.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("🔬 Algorithm Deep-Dive: Kahn's Algorithm on a Reversed Graph"),
    N.para("Kahn's Algorithm (1962) produces topological orderings of DAGs by repeatedly removing nodes with in-degree 0. Here we repurpose it: run it on the reversed graph, seeded from terminal nodes. Nodes that Kahn's never processes have their 'in-degree' (= original out-degree) kept non-zero by cycle partners — they are implicitly detected as cycle members."),
    N.para("Core invariant: out_deg[u] = number of u's original exits NOT YET confirmed safe. When it hits 0, all of u's paths lead to safe nodes → u is safe."),
    N.h3("Code"),
    N.code("""\
from collections import deque

def eventualSafeNodes(graph):
    n = len(graph)
    rev = [[] for _ in range(n)]   # reversed adjacency list
    out_deg = [0] * n              # original out-degree per node

    for u in range(n):
        for v in graph[u]:
            rev[v].append(u)       # reverse edge: v → u
            out_deg[u] += 1        # count u's original exits

    # Terminal nodes (out_deg==0) are trivially safe — seed the queue
    queue = deque(i for i in range(n) if out_deg[i] == 0)
    safe = set()

    while queue:
        v = queue.popleft()        # v is confirmed safe
        safe.add(v)
        for u in rev[v]:           # who originally pointed to v?
            out_deg[u] -= 1        # one fewer unresolved exit for u
            if out_deg[u] == 0:    # all of u's exits are now safe
                queue.append(u)    # u is safe — enqueue it

    return sorted(safe)            # problem requires sorted output
"""),
    N.h3("Line by Line"),
    N.para(N.rich([("rev = [[] for _ in range(n)]", {"code": True}), " — Build the reverse adjacency list: for each original edge u→v, we store v→u here."])),
    N.para(N.rich([("out_deg = [0] * n", {"code": True}), " — Track how many original outgoing edges each node has. When this reaches 0, all exits lead to safe nodes."])),
    N.para(N.rich([("rev[v].append(u); out_deg[u] += 1", {"code": True}), " — Two operations per original edge: record the reverse direction, and count u's exits."])),
    N.para(N.rich([("queue = deque(i for i in range(n) if out_deg[i] == 0)", {"code": True}), " — Terminal nodes have no outgoing edges. They are safe seeds. All others start unresolved."])),
    N.para(N.rich([("v = queue.popleft()", {"code": True}), " — Pop a confirmed safe node. O(1) with deque."])),
    N.para(N.rich([("for u in rev[v]", {"code": True}), " — These are nodes that originally had edge u→v. Since v is now safe, one of each u's exits is resolved."])),
    N.para(N.rich([("out_deg[u] -= 1", {"code": True}), " — Decrement. Tracks 'how many of u's exits are still unresolved.' Cycle partners keep each other's counts elevated."])),
    N.para(N.rich([("if out_deg[u] == 0: queue.append(u)", {"code": True}), " — All of u's exits lead to safe nodes. u earns safe status. Enqueue for propagation."])),
    N.para(N.rich([("return sorted(safe)", {"code": True}), " — Collect all enqueued (safe) nodes and sort. Nodes never enqueued are in or lead to cycles."])),
    N.divider(),
]

# Solution 2 — DFS 3-Color
blocks += [
    N.h2("Solution 2 — DFS with 3-Color Marking"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Run DFS from each node. During DFS, if we ever revisit a node currently on the recursion stack (a 'gray' node), we found a back edge — that means a cycle exists, so the starting node is unsafe."),
        N.h4("What Doesn't Work"),
        N.para("Plain cycle detection (visited/not) doesn't distinguish between 'visited in this DFS path' and 'visited but confirmed safe in a previous DFS.' We need 3 states."),
        N.h4("The Key Observation"),
        N.para("3 colors: white (unvisited), gray (in current DFS stack), black (confirmed safe). A gray node reached again = back edge = cycle. A black node = guaranteed safe path. Memoize the black result to avoid recomputation."),
        N.h4("Building the Solution"),
        N.para("DFS with color array. On entry: mark gray. Recurse on neighbors. If any neighbor returns False (unsafe), mark current as... unsafe (leave gray, or use a 4th state). If all succeed, mark black (safe). Return True/False."),
        N.callout("Key: Gray means 'ancestor in current path.' Reaching gray = cycle = False. Black means 'already confirmed safe — trust the cache.' White means 'not yet explored.'", "💡", "gray_background"),
    ]),
    N.h3("Code"),
    N.code("""\
def eventualSafeNodes(graph):
    n = len(graph)
    color = [0] * n  # 0=white (unvisited), 1=gray (in stack), 2=black (safe)

    def dfs(node):
        if color[node] == 1: return False   # back edge → cycle → unsafe
        if color[node] == 2: return True    # already confirmed safe
        color[node] = 1                     # mark "currently on DFS path"
        for nei in graph[node]:
            if not dfs(nei):
                return False                # any unsafe successor → unsafe
        color[node] = 2                     # all paths lead to safety
        return True

    return [i for i in range(n) if dfs(i)]  # sorted because i=0..n-1
"""),
    N.h3("Line by Line"),
    N.para(N.rich([("color = [0] * n", {"code": True}), " — 3-state array. 0=unseen, 1=on current path, 2=confirmed safe."])),
    N.para(N.rich([("if color[node] == 1: return False", {"code": True}), " — We reached a node already in the current DFS stack. This is a back edge, proving a cycle. Return False (unsafe)."])),
    N.para(N.rich([("if color[node] == 2: return True", {"code": True}), " — This node was previously confirmed safe. Trust the cache. Return True immediately."])),
    N.para(N.rich([("color[node] = 1", {"code": True}), " — Mark node as 'in current DFS path.' Any DFS reaching this node again from a descendant will detect the cycle."])),
    N.para(N.rich([("if not dfs(nei): return False", {"code": True}), " — If any successor is unsafe, this node is also unsafe (has a path leading to a cycle)."])),
    N.para(N.rich([("color[node] = 2; return True", {"code": True}), " — All successors are safe. This node is safe. Mark black so future DFS calls trust this result."])),
    N.callout("⚠️ When a node is found unsafe (returns False), we leave it as gray (1), NOT setting it to black. This is intentional — if we reach it again from another DFS path, we again detect it as unsafe. Some implementations use a 4th color (unsafe=3) for clarity.", "⚠️", "yellow_background"),
    N.divider(),
]

# Complexity
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute-force DFS (no memo)", "O(V·(V+E))", "O(V)"],
        ["DFS 3-Color", "O(V+E)", "O(V) + recursion stack"],
        ["Reverse Graph + Kahn's BFS ✓", "O(V+E)", "O(V+E)"],
    ]),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Graph (Directed Graph Problems)"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Reverse Graph Topo Sort — run Kahn's BFS on the reversed graph seeded from sink/terminal nodes; also Cycle Detection via 3-color DFS"])),
    N.callout(
        "When to recognize this pattern: 'Every path from X eventually reaches [type of node]' → reverse edges, BFS from that node type. "
        "'Find nodes that only lead to sinks/terminals' → same. "
        "'Propagate a property backward through a directed graph' → reverse + BFS. "
        "Nodes Kahn's never processes = cycle members.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Topological Sort / Cycle Detection on Directed Graphs):"),
    N.bullet(N.rich([("Course Schedule", {"bold": True}), " (Medium) — Can all courses be finished? Kahn's or 3-color DFS cycle detection. #207"])),
    N.bullet(N.rich([("Course Schedule II", {"bold": True}), " (Medium) — Output a valid course order if possible — full Kahn's topo sort. #210"])),
    N.bullet(N.rich([("All Paths From Source to Target", {"bold": True}), " (Medium) — Find all paths from 0 to n-1 in a DAG; DFS backtracking. #797"])),
    N.bullet(N.rich([("Minimum Height Trees", {"bold": True}), " (Medium) — Peel leaf nodes iteratively — structurally identical Kahn's-style BFS from leaves. #310"])),
    N.bullet(N.rich([("Parallel Courses", {"bold": True}), " (Medium) — Minimum semesters via topo BFS with level tracking. #1136"])),
    N.bullet(N.rich([("Longest Path in a DAG with Constraints", {"bold": True}), " (Hard) — Topo sort + DP on resulting order. #2392"])),
    N.para("These problems share the core technique: directed graph traversal with cycle awareness, or backward propagation via reversed edges."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Graph section, Topological Sort sub-pattern. Sub-Pattern: Reverse Graph Topo Sort (Kahn's BFS on reversed adjacency list).", "📚", "gray_background"),
]

# Embed
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("find_eventual_safe_states")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── 4) Append all blocks ─────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID} — {len(blocks)} blocks appended.")
