"""
gen_path_sum_ii.py — Notion page rebuild for Path Sum II (#113)
"""
import sys, os
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-812e-bcd2-db9c5cf22dfe"

# ── 1) Set properties ─────────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=113,
    pattern="Trees",
    subpatterns=["Backtrack Path"],
    tc="O(n²)",
    sc="O(n)",
    key_insight="DFS + path.append/pop backtracking collects all root-to-leaf paths; always copy path with list(path) when recording.",
    icon="🟡"
)
print("Properties set.")

# ── 2) Wipe old body ─────────────────────────────────────────────────────────
print("Wiping old content...")
removed = N.wipe_page(PAGE_ID)
print(f"Removed {removed} blocks.")

# ── 3) Rebuild body ──────────────────────────────────────────────────────────
print("Building new content...")

blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given the ", {}),
        ("root", {"code": True}),
        (" of a binary tree and an integer ", {}),
        ("targetSum", {"code": True}),
        (", return all root-to-leaf paths where the sum of the node values equals ", {}),
        ("targetSum", {"code": True}),
        (". A leaf is a node with no children. Return each path as a list of node values in root-to-leaf order.", {})
    ])),
    N.para("Example: root = [5,4,8,11,null,13,4,7,2,null,null,5,1], targetSum = 22 → [[5,4,11,2],[5,8,4,5]]"),
    N.divider(),
]

# Solution 1 — DFS Backtracking
blocks += [
    N.h2("Solution 1 — DFS Backtracking (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to collect every root-to-leaf trail whose node values add up to the target. 'All paths' + 'collect as sequences' → DFS with a shared path list that we build on entry and undo on exit."),
        N.h4("What Doesn't Work"),
        N.para("A purely recursive approach that creates new path lists at each node works but is memory-intensive — each recursive call allocates a new list. A BFS approach queues entire path copies, leading to O(n·h) memory. Backtracking with a shared list is the most memory-efficient solution."),
        N.h4("The Key Observation"),
        N.para("The DFS call stack naturally mirrors the tree structure. When we're inside dfs(node), path contains exactly the nodes from root to node. When we return (pop), path is restored to parent's state. This structural correspondence is maintained by the append/pop discipline."),
        N.h4("Building the Solution"),
        N.para("1. Initialize results=[], path=[]. 2. In dfs(node, remain): append node.val, subtract from remain. 3. At a leaf: if remain==0, store list(path) copy. 4. Recurse left, recurse right. 5. Pop (backtrack). 6. Call dfs(root, targetSum). Return results."),
        N.callout("Analogy: Trail hiking — walk every trail, note your route, check the tally at each dead end. When you turn back, erase your last step. The same notepad is used for all trails — just add/erase as you go.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code("""def pathSum(root, targetSum):
    results, path = [], []

    def dfs(node, remain):
        if not node:
            return
        path.append(node.val)      # ① ENTER: add to path
        remain -= node.val         # ② count down remaining
        if not node.left and not node.right:   # ③ leaf?
            if remain == 0:        # ④ sum matches?
                results.append(list(path))  # ⑤ COPY the path!
        dfs(node.left, remain)     # ⑥ explore left
        dfs(node.right, remain)    # ⑦ explore right
        path.pop()                 # ⑧ BACKTRACK: undo this node

    dfs(root, targetSum)
    return results"""),
    N.h3("Line by Line"),
    N.para(N.rich([("results, path = [], []", {"code": True}), " — results accumulates all valid paths; path is the shared scratch list, reused across all recursive calls."]),),
    N.para(N.rich([("def dfs(node, remain)", {"code": True}), " — inner helper. remain is the countdown: targetSum minus the sum of nodes seen so far."]),),
    N.para(N.rich([("if not node: return", {"code": True}), " — base case for null children. A null child is not a leaf; we simply return without doing anything."]),),
    N.para(N.rich([("path.append(node.val)", {"code": True}), " — ENTER step. We commit this node to the current path."]),),
    N.para(N.rich([("remain -= node.val", {"code": True}), " — subtract this node's contribution. remain now equals targetSum minus sum of all nodes from root to current node."]),),
    N.para(N.rich([("if not node.left and not node.right", {"code": True}), " — leaf detection. A node with no children is a leaf — this is where root-to-leaf paths terminate."]),),
    N.para(N.rich([("if remain == 0", {"code": True}), " — sum check. If countdown reached zero at a leaf, this path sums to exactly targetSum."]),),
    N.para(N.rich([("results.append(list(path))", {"code": True}), " — CRITICAL: list(path) creates an independent copy. Without this, all stored paths would be references to the same (ultimately empty) list object."]),),
    N.para(N.rich([("dfs(node.left, remain)", {"code": True}), " / ", ("dfs(node.right, remain)", {"code": True}), " — explore both subtrees with the same remain value (it's a local variable in each call)."]),),
    N.para(N.rich([("path.pop()", {"code": True}), " — BACKTRACK. Removes this node from the path after both subtrees are fully explored, restoring path to parent's state."]),),
    N.divider(),
]

# Solution 2 — BFS
blocks += [
    N.h2("Solution 2 — BFS with Queued Paths (Iterative)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same goal, but avoid recursion. BFS processes nodes level by level using a queue. Each queue entry carries the node, the path accumulated to reach it, and the remaining sum."),
        N.h4("What Doesn't Work"),
        N.para("BFS cannot share a single path list (unlike DFS + backtracking) because multiple queue entries exist simultaneously at different tree positions. Each entry needs its own path snapshot."),
        N.h4("The Key Observation"),
        N.para("When we enqueue a child, we create a new path list with path + [child.val]. This is a fresh list per entry, so no copy is needed when recording at a leaf. The path is already isolated."),
        N.h4("Building the Solution"),
        N.para("Seed the queue with (root, [root.val], targetSum - root.val). While queue: pop entry, check leaf + sum, enqueue children with extended path and decremented remain."),
        N.callout("Trade-off: BFS avoids recursion stack overflow risk but uses O(n·h) memory — each of up to O(n) queue entries stores an O(h) path list. DFS backtracking uses only O(h) auxiliary memory.", "⚠️", "orange_background"),
    ]),
    N.h3("Code"),
    N.code("""from collections import deque

def pathSum(root, targetSum):
    if not root:
        return []
    results = []
    # Queue: (node, path_so_far, remaining_sum)
    q = deque([(root, [root.val], targetSum - root.val)])
    while q:
        node, path, remain = q.popleft()
        if not node.left and not node.right:
            if remain == 0:
                results.append(path)  # already a fresh list — no copy needed
        if node.left:
            q.append((node.left, path + [node.left.val], remain - node.left.val))
        if node.right:
            q.append((node.right, path + [node.right.val], remain - node.right.val))
    return results"""),
    N.h3("Line by Line"),
    N.para(N.rich([("q = deque([(root, [root.val], targetSum - root.val)])", {"code": True}), " — seed with root node, path containing root's value, and the remaining sum after subtracting root."]),),
    N.para(N.rich([("node, path, remain = q.popleft()", {"code": True}), " — unpack the front entry. path here is already a dedicated list for this traversal path."]),),
    N.para(N.rich([("results.append(path)", {"code": True}), " — safe! Each queue entry has its own path list (created by path + [...]). No reference aliasing."]),),
    N.para(N.rich([("path + [node.left.val]", {"code": True}), " — Python list concatenation creates a NEW list. The current entry's path is not mutated."]),),
    N.divider(),
]

# Complexity table
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space (auxiliary)", "Notes"],
        ["DFS Backtracking (Interview Pick)", "O(n²)", "O(n)", "Shared path list; optimal aux memory"],
        ["BFS with Queued Paths", "O(n²)", "O(n·h)", "Iterative; avoids deep recursion"],
    ]),
    N.para("Both approaches are O(n²) time: O(n) nodes visited × O(n) path copy per leaf worst case. The DFS approach wins on auxiliary memory: O(h) path + O(h) call stack vs. BFS's O(n·h) queue."),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Trees — specifically DFS with backtracking to collect all root-to-leaf paths")])  ),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Backtrack Path — maintain a shared mutable path list, append on enter, pop on exit")])),
    N.callout(
        "When to recognize this pattern: problem says 'all paths' or 'return every path' (not just existence/count). Paths are root-to-leaf. Path content (sequence of values) must be collected, not just a scalar result. You mentally model 'undo the last step when backtracking' — that's the signal.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Backtrack Path technique or related tree DFS patterns:"),
    N.bullet(N.rich([("Path Sum I", {"bold": True}), " (Easy) — Does any root-to-leaf path sum equal target? Boolean only, no collection needed. (#112)"])),
    N.bullet(N.rich([("Binary Tree Paths", {"bold": True}), " (Easy) — Return all root-to-leaf paths as strings — identical DFS/backtrack skeleton, different recording step. (#257)"])),
    N.bullet(N.rich([("Path Sum III", {"bold": True}), " (Medium) — Count paths anywhere in tree (not just root-to-leaf) summing to target. Uses prefix sum hash map at each node. (#437)"])),
    N.bullet(N.rich([("Sum Root to Leaf Numbers", {"bold": True}), " (Medium) — Treat each root-to-leaf path as a decimal number; return their total. Same traversal pattern. (#129)"])),
    N.bullet(N.rich([("All Paths From Source to Target", {"bold": True}), " (Medium) — Same backtrack template on a DAG instead of a tree. The shared path + pop discipline is identical. (#797)"])),
    N.bullet(N.rich([("Binary Tree Maximum Path Sum", {"bold": True}), " (Hard) — Max sum of any path (not just root-to-leaf). Postorder DFS returning max gain from each subtree. (#124)"])),
    N.para("These problems share the core technique: DFS + shared state that is built on descent and restored on ascent (backtracking)."),
    N.callout("Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section: Trees / Backtrack Path sub-pattern. Sub-pattern source: Guide + Analysis.", "📚", "gray_background"),
]

# Embed section
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("path_sum_ii")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

# Append all blocks in chunks
print(f"Appending {len(blocks)} blocks...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
