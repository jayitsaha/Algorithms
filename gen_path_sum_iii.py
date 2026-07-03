"""
gen_path_sum_iii.py — Notion updater for Path Sum III (#437)
Run from: /Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms/
"""
import notion_lib as N

PAGE_ID = "39193418-809c-81e4-a918-d9c645c53f40"
SLUG = "path_sum_iii"

# ── 1) Set properties ──────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=437,
    pattern="Trees",
    subpatterns=["Prefix Sum + Hash Map"],
    tc="O(n)",
    sc="O(n)",
    key_insight="A downward path sum = prefix_sum(end) - prefix_sum(start ancestor); track prefix sums in a hash map during DFS and backtrack on return to keep the map path-scoped.",
    icon="🟡"
)
print("Properties set.")

# ── 2) Wipe old body ───────────────────────────────────────────────────────
deleted = N.wipe_page(PAGE_ID)
print(f"Wiped {deleted} old blocks.")

# ── 3) Build body ──────────────────────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given the root of a binary tree and an integer ", {}),
        ("targetSum", {"code": True}),
        (", return the number of paths where the sum of the node values along the path equals ", {}),
        ("targetSum", {"code": True}),
        (". A path must go downward (travelling only from parent nodes to child nodes) but does not need to start or end at the root or a leaf.", {}),
    ])),
    N.divider(),
]

# ── Solution 1: Prefix Sum + Hash Map (Optimal) ──
blocks += [
    N.h2("Solution 1 — DFS + Prefix Sum Hash Map (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to count downward paths with a given sum. A path can start at any node — that's the hard part. Think of the DFS root-to-node traversal as a 1D array of values. The prefix sum at any node is the total from root down to that node."),
        N.h4("What Doesn't Work"),
        N.para("Starting a fresh DFS from every node (brute force) works but costs O(n²). For each of n nodes, we launch an O(n) sub-DFS. On large trees this is too slow."),
        N.h4("The Key Observation"),
        N.para("A downward path from ancestor A to node B has sum = prefix_sum(B) − prefix_sum(parent of A). If we want that sum to equal target, we need: prefix_sum(parent of A) = prefix_sum(B) − target. This means: at node B, look up (curr_sum − target) in a hash map of ancestor prefix sums. Each hit is a valid path."),
        N.h4("Building the Solution"),
        N.para("1) Seed prefix_map[0] = 1 (the 'empty prefix' before root, handles root-starting paths). 2) DFS: at each node, compute curr_sum, look up the complement, insert curr_sum, recurse, then BACKTRACK by decrementing curr_sum in the map. The backtrack keeps the map scoped to only the current root-to-node path."),
        N.callout("Analogy: Think of it like the 'Subarray Sum Equals K' trick (#560) applied to a tree. The DFS path from root to the current node IS the array — and we apply the exact same prefix sum complement lookup.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code("""\
from collections import defaultdict

def pathSum(root, targetSum):
    prefix_map = defaultdict(int)
    prefix_map[0] = 1  # seed: empty prefix before root

    def dfs(node, curr_sum):
        if not node:
            return 0
        curr_sum += node.val
        # Count paths ending at this node: ancestors with prefix = curr_sum - target
        count = prefix_map[curr_sum - targetSum]
        prefix_map[curr_sum] += 1   # record this node's prefix sum
        count += dfs(node.left, curr_sum)
        count += dfs(node.right, curr_sum)
        prefix_map[curr_sum] -= 1   # BACKTRACK: unmark this node
        return count

    return dfs(root, 0)
"""),
    N.h3("Line by Line"),
    N.para(N.rich([("prefix_map = defaultdict(int)", {"code": True}), (" — creates a hash map that defaults missing keys to 0; avoids KeyError on lookups.", {})])),
    N.para(N.rich([("prefix_map[0] = 1", {"code": True}), (" — seeds the 'empty prefix' entry so paths starting from root are correctly counted when curr_sum − target == 0.", {})])),
    N.para(N.rich([("curr_sum += node.val", {"code": True}), (" — extend the running prefix sum from root to include the current node.", {})])),
    N.para(N.rich([("count = prefix_map[curr_sum - targetSum]", {"code": True}), (" — look up how many ancestors have prefix sum = curr_sum − target; each is a valid path start.", {})])),
    N.para(N.rich([("prefix_map[curr_sum] += 1", {"code": True}), (" — record this node's prefix sum before recursing so children can count paths starting here.", {})])),
    N.para(N.rich([("count += dfs(node.left, curr_sum)", {"code": True}), (" — accumulate paths from the left subtree.", {})])),
    N.para(N.rich([("count += dfs(node.right, curr_sum)", {"code": True}), (" — accumulate paths from the right subtree.", {})])),
    N.para(N.rich([("prefix_map[curr_sum] -= 1", {"code": True}), (" — CRITICAL backtrack: undo this node's entry so sibling subtrees see a clean map.", {})])),
    N.para(N.rich([("return count", {"code": True}), (" — total valid paths found in this entire subtree.", {})])),
    N.divider(),
]

# ── Solution 2: Brute Force ──
blocks += [
    N.h2("Solution 2 — Brute Force: Double DFS (O(n²))"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The simplest reading: for each node in the tree, count how many paths start at that node and sum to target. Sum all those counts."),
        N.h4("What Doesn't Work (Why We Improve It)"),
        N.para("This works correctly but runs a fresh O(n) DFS for each of n nodes, giving O(n²) total — too slow for large trees with ~50k nodes."),
        N.h4("The Key Observation"),
        N.para("At each node, maintain a 'remaining' counter (start = targetSum, subtract node.val at each step). If remaining hits 0, we found a path. Recurse left and right with updated remaining."),
        N.h4("Building the Solution"),
        N.para("Outer function tries every node as a start. Inner function (paths_from) counts paths starting at a specific node by tracking remaining budget. Combine: outer recurses the tree structure, inner recurses down paths."),
    ]),
    N.h3("Code"),
    N.code("""\
def pathSum_brute(root, targetSum):
    if not root:
        return 0

    def paths_from(node, remaining):
        \"\"\"Count paths starting exactly at this node.\"\"\\"
        if not node:
            return 0
        found = 1 if node.val == remaining else 0
        found += paths_from(node.left, remaining - node.val)
        found += paths_from(node.right, remaining - node.val)
        return found

    # Try root as start, then all starts in left and right subtrees
    return (paths_from(root, targetSum)
            + pathSum_brute(root.left, targetSum)
            + pathSum_brute(root.right, targetSum))
"""),
    N.h3("Line by Line"),
    N.para(N.rich([("paths_from(node, remaining)", {"code": True}), (" — inner DFS; counts paths starting at 'node' with budget 'remaining'.", {})])),
    N.para(N.rich([("found = 1 if node.val == remaining else 0", {"code": True}), (" — path ends here if using exactly all remaining budget.", {})])),
    N.para(N.rich([("paths_from(node.left, remaining - node.val)", {"code": True}), (" — continue path downward; subtract current node's value from budget.", {})])),
    N.para(N.rich([("pathSum_brute(root.left, targetSum)", {"code": True}), (" — outer recursion: try root.left as a new path start with full budget.", {})])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (Double DFS)", "O(n²)", "O(n) stack"],
        ["Prefix Sum + Hash Map (Optimal)", "O(n)", "O(n) map + stack"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Trees", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Prefix Sum + Hash Map (applied to DFS path, not flat array)", {})])),
    N.callout(
        "When to recognize this pattern: 'count downward paths in a tree with a given sum', path can start at any node (not just root), negative values present (ruling out binary search), or the problem is analogous to a prefix-sum array problem but on a tree traversal.",
        "🔎", "green_background"
    ),
    N.callout(
        "Core Analogy: Subarray Sum Equals K (#560) on a flat array uses prefix_sum + hash map with complement lookup. Path Sum III applies this identically — the DFS path from root to current node IS the array. The only addition is backtracking to keep the map scoped to the current branch.",
        "💡", "blue_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Prefix Sum + Hash Map complement lookup):"),
    N.bullet(N.rich([("Subarray Sum Equals K", {"bold": True}), (" (Medium) — The exact 1D array version of this pattern; prefix sum + hash map complement lookup. (#560)", {})])),
    N.bullet(N.rich([("Path Sum", {"bold": True}), (" (Easy) — Simpler root-to-leaf variant; no hash map needed; foundation for understanding Path Sum III. (#112)", {})])),
    N.bullet(N.rich([("Path Sum II", {"bold": True}), (" (Medium) — Find all root-to-leaf paths with given sum; records actual paths not just count. (#113)", {})])),
    N.bullet(N.rich([("Binary Tree Maximum Path Sum", {"bold": True}), (" (Hard) — Path can reverse direction through any node; DFS returning per-branch max. (#124)", {})])),
    N.bullet(N.rich([("Subarray Sums Divisible by K", {"bold": True}), (" (Medium) — Modular prefix sums in a hash map; complement lookup with mod. (#974)", {})])),
    N.bullet(N.rich([("Count Paths That Can Form a Palindrome in a Tree", {"bold": True}), (" (Hard) — XOR bitmask prefix sums on tree paths; same DFS+map+backtrack skeleton. (#2791)", {})])),
    N.para("These problems share the core technique: prefix sum complement lookup in a hash map, with backtracking on a tree DFS to keep the map path-scoped."),
    N.callout("Reference: DSA_Patterns_and_SubPatterns_Guide.md — Trees section, Path Sum sub-pattern. Sub-pattern 'Prefix Sum + Hash Map' verified by analysis (tree-specific application not explicitly listed in guide).", "📚", "gray_background"),
    N.divider(),
]

# ── Embed ──
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
