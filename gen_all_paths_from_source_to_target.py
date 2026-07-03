"""
Notion page rebuild for: All Paths From Source to Target (LeetCode #797)
Page ID: 39193418-809c-81cb-8e13-fca62e3426cd
Run from: /Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms/
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81cb-8e13-fca62e3426cd"
SLUG = "all_paths_from_source_to_target"

# ── Step 1: Set properties ──────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=797,
    pattern="Graph",
    subpatterns=["DFS + Path Building"],
    tc="O(2^n * n)",
    sc="O(n)",
    key_insight="DFS with backtracking on a DAG; path.pop() undoes each choice; copy path[:] at target.",
    icon="🟡"
)
print("Properties set OK.")

# ── Step 2: Wipe old body ───────────────────────────────────────────────
print("Wiping old body...")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── Step 3: Build new body ──────────────────────────────────────────────
PROBLEM_STATEMENT = (
    "Given a directed acyclic graph (DAG) of n nodes labeled from 0 to n-1, "
    "represented as graph where graph[i] is the list of all nodes you can visit from node i, "
    "find all possible paths from node 0 to node n-1 and return them in any order. "
    "Example: graph = [[1,2],[3],[3],[]] → Output: [[0,1,3],[0,2,3]]. "
    "Node 0 connects to nodes 1 and 2. Both 1 and 2 connect to node 3 (the target)."
)

SOL1_CODE = '''\
def allPathsSourceTarget(graph):
    result = []
    path = [0]          # pre-seeded with source
    target = len(graph) - 1

    def dfs(node):
        if node == target:
            result.append(path[:])  # COPY — critical!
            return
        for neighbor in graph[node]:
            path.append(neighbor)   # Choose
            dfs(neighbor)           # Explore
            path.pop()              # Unchoose (backtrack)

    dfs(0)
    return result\
'''

SOL2_CODE = '''\
def allPathsSourceTarget(graph):
    target = len(graph) - 1
    stack = [[0]]        # stack of ENTIRE partial paths
    result = []
    while stack:
        path = stack.pop()
        node = path[-1]
        if node == target:
            result.append(path)    # no copy needed — fresh list
        for neighbor in graph[node]:
            stack.append(path + [neighbor])  # creates new list each time
    return result\
'''

blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(PROBLEM_STATEMENT),
    N.divider(),
]

# Solution 1 — DFS + Backtracking
blocks += [
    N.h2("Solution 1 — DFS + Backtracking (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We need every possible route from source (node 0) to target (node n-1) in a DAG. "
            "Since we need ALL routes (not just one), we cannot stop early — we must explore every branch fully."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "BFS finds paths level by level, but to collect ALL paths you'd need to store entire partial paths "
            "in the queue — O(2^n * n) space at peak. A visited set would incorrectly prune valid alternate routes "
            "(e.g., node 3 is reachable via two paths; marking it visited after the first visit would miss the second). "
            "Neither approach cleanly enumerates all possibilities."
        ),
        N.h4("The Key Observation"),
        N.para(
            "The graph is a DAG — no cycles. This means DFS always terminates without cycle detection. "
            "We can freely go deeper and deeper, and we know we'll always eventually hit the target or a dead end. "
            "When we hit the target, record the path. When we return from recursion, undo the last choice (backtrack). "
            "This 'try-record-undo' loop naturally enumerates every path."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Step 1: Initialize path = [0] (source pre-seeded). "
            "Step 2: Define dfs(node) — base case: if node == target, append path[:] to results and return. "
            "Step 3: Recursive case: for each neighbor, append to path, call dfs, then pop from path. "
            "The pop is the 'unchoose' — it restores path to its pre-call state so the next iteration sees a clean path. "
            "Step 4: Call dfs(0) to kick off the search."
        ),
        N.callout(
            "Analogy: Exploring a maze — you carry a list of rooms visited. When you reach the exit, write down your route. "
            "When you hit a dead end, erase your last step and try a different door. "
            "The backtrack (pop) is 'erasing the last step'.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOL1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("result = []", {"code": True}), " — accumulator for all complete paths found."])),
    N.para(N.rich([("path = [0]", {"code": True}), " — current partial path; pre-seeded with source node 0."])),
    N.para(N.rich([("target = len(graph) - 1", {"code": True}), " — target is always the last node (n-1) in a DAG of n nodes."])),
    N.para(N.rich([("def dfs(node):", {"code": True}), " — closure; path and result are shared by reference, so no argument passing needed."])),
    N.para(N.rich([("if node == target:", {"code": True}), " — base case: we've reached the destination — this path is complete."])),
    N.para(N.rich([("result.append(path[:])", {"code": True}), " — COPY the path snapshot. path[:] creates a new list frozen at this moment. Without this, result entries would all point to the same mutating list."])),
    N.para(N.rich([("return", {"code": True}), " — stop recursing; caller will execute the path.pop() to backtrack."])),
    N.para(N.rich([("for neighbor in graph[node]:", {"code": True}), " — iterate over every outgoing edge from the current node."])),
    N.para(N.rich([("path.append(neighbor)", {"code": True}), " — CHOOSE: extend the current path with this neighbor."])),
    N.para(N.rich([("dfs(neighbor)", {"code": True}), " — EXPLORE: fully explore the subtree reachable via this neighbor."])),
    N.para(N.rich([("path.pop()", {"code": True}), " — UNCHOOSE: remove the neighbor from path. This is backtracking — path returns to its pre-call state."])),
    N.para(N.rich([("dfs(0)", {"code": True}), " — launch DFS from node 0 (source)."])),
    N.para(N.rich([("return result", {"code": True}), " — all collected paths after full exploration."])),
    N.divider(),
]

# Solution 2 — Iterative DFS
blocks += [
    N.h2("Solution 2 — Iterative DFS with Stack of Paths"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same goal — find all paths — but using an explicit stack instead of the call stack."),
        N.h4("What Doesn't Work"),
        N.para(
            "If we pushed only node indices onto a stack (standard iterative DFS), "
            "we'd lose track of the path taken to reach each node. "
            "We need to store entire partial paths on the stack."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Instead of storing node indices on the stack, store entire partial paths as lists. "
            "When we pop a path, the current node is path[-1]. "
            "For each neighbor, push path + [neighbor] (a brand new list). "
            "When path[-1] == target, the path is complete — append it directly (no copy needed since it's already a fresh list)."
        ),
        N.h4("Building the Solution"),
        N.para(
            "This mirrors the recursive approach exactly. The trade-off: "
            "the stack may hold O(2^n) partial paths simultaneously (O(2^n * n) space total), "
            "vs the recursive approach's O(n) space. For large sparse DAGs, use the recursive approach."
        ),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("stack = [[0]]", {"code": True}), " — stack of ENTIRE partial paths (not just node indices!). Initial path is [0] (just the source)."])),
    N.para(N.rich([("path = stack.pop()", {"code": True}), " — get the most recently added partial path."])),
    N.para(N.rich([("node = path[-1]", {"code": True}), " — current node is the last element of the partial path."])),
    N.para(N.rich([("result.append(path)", {"code": True}), " — no copy needed here — path is already a fresh list (created by path + [neighbor] below)."])),
    N.para(N.rich([("stack.append(path + [neighbor])", {"code": True}), " — extend: creates a brand new list for each neighbor. This is what makes copies unnecessary at the target."])),
    N.divider(),
]

# Complexity
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space (excl. output)"],
        ["DFS + Backtracking (Recursive) ✓", "O(2^n * n)", "O(n)"],
        ["Iterative DFS (Stack of Paths)", "O(2^n * n)", "O(2^n * n)"],
    ]),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Graph Traversal"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "DFS + Path Building (Backtracking on DAG)"])),
    N.callout(
        "When to recognize this pattern: "
        "(1) Problem asks for ALL paths/combinations/solutions — not just one. "
        "(2) Graph or tree where you traverse and record complete routes. "
        "(3) DAG structure mentioned → safe to skip visited set. "
        "(4) Keywords: 'find all', 'enumerate', 'list all possible'.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (DFS + Backtracking / Path Building):"),
    N.bullet(N.rich([("Path Sum II", {"bold": True}), " (Medium) — DFS on binary tree, collect all root-to-leaf paths summing to target; identical choose/explore/unchoose pattern (#113)"])),
    N.bullet(N.rich([("Binary Tree Paths", {"bold": True}), " (Easy) — Find all root-to-leaf paths in a binary tree; simpler version of this problem (#257)"])),
    N.bullet(N.rich([("Combination Sum", {"bold": True}), " (Medium) — All combinations from an array summing to target; same backtracking skeleton (#39)"])),
    N.bullet(N.rich([("Permutations", {"bold": True}), " (Medium) — Generate all permutations; backtracking with a used[] array to track choices (#46)"])),
    N.bullet(N.rich([("Word Search", {"bold": True}), " (Medium) — DFS on 2D grid with backtracking; mark/unmark cells as visited (#79)"])),
    N.bullet(N.rich([("All Paths That Lead to Destination", {"bold": True}), " (Medium) — DFS with additional constraints on allowed destinations; extension of this problem (#1059)"])),
    N.para("These problems all share the core technique: DFS with an explicit path list, append/pop to choose/unchoose, and copy at the base case."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 8 (Graph → DFS: Backtracking). Sub-Pattern verified: DFS + Path Building.", "📚", "gray_background"),
]

# Embed
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys to watch DFS, backtracking, and path-building in action.",
         {"italic": True, "color": "gray"})
    ])),
]

print(f"Appending {len(blocks)} blocks to Notion...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
