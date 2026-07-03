"""
gen_largest_bst_subtree.py — Notion update for LeetCode #333 Largest BST Subtree
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8103-a2f6-f541fad953cd"
SLUG = "largest_bst_subtree"

# ── 1) Set properties ──────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=333,
    pattern="Trees",
    subpatterns=["Post-order with Range"],
    tc="O(n)",
    sc="O(h)",
    key_insight="Post-order DFS returns (is_bst, size, min, max); parent validates in O(1) using l_max and r_min.",
    icon="🟡"
)
print("Properties set.")

# ── 2) Wipe old body ───────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3) Build body ──────────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given the ", {}),
        ("root", {"code": True}),
        (" of a binary tree, find the largest subtree which is a Binary Search Tree (BST), "
         "and return the number of nodes in that subtree. A subtree must include a node and ALL its "
         "descendants. A BST requires every value in the left subtree to be strictly less than the "
         "node value, and every value in the right subtree to be strictly greater — recursively.", {})
    ])),
    N.para(N.rich([
        ("Example: Input tree [10, 5, 15, null, null, 6, 20]. The subtree rooted at 15 "
         "({6, 15, 20}) is the largest BST with size=3. The whole tree is NOT a BST because "
         "node 6 (in right subtree of 10) is less than 10.", {})
    ])),
    N.callout("Edge cases: single node → always BST of size 1. Empty tree → return 0. "
              "If entire tree is a BST → return n.", "⚠️", "yellow_background"),
    N.divider(),
]

# ── Solution 1: Post-order DFS (Optimal) ──
blocks += [
    N.h2("Solution 1 — Post-order DFS with Range Tuple (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to find the largest connected subtree (rooted at some node) that satisfies BST "
               "rules. The key question: how do we know if a subtree is a valid BST without re-scanning "
               "every descendant from scratch each time?"),
        N.h4("What Doesn't Work"),
        N.para("Brute force: for each of the n nodes, run an O(n) BST validation — gives O(n²) total. "
               "Also, checking only direct children is WRONG: a subtree can fail BST not just because "
               "a direct child has the wrong value, but because a grandchild or deeper descendant violates "
               "the global ordering constraint."),
        N.h4("The Key Observation"),
        N.para("If we are at node X, we need: (1) is the left subtree a BST? (2) is the right subtree a BST? "
               "(3) is the MAXIMUM value in the entire left subtree less than X.val? "
               "(4) is the MINIMUM value in the entire right subtree greater than X.val? "
               "If we make each DFS call RETURN its min and max values, we can answer (3) and (4) in O(1)."),
        N.h4("Building the Solution"),
        N.para("Design the return type: (is_bst, size, min_val, max_val). "
               "Use post-order traversal so children return their tuples before the parent needs them. "
               "For null nodes, return sentinel values: min=+inf, max=-inf. "
               "These sentinels make leaf nodes automatically valid: l_max(-inf) < X.val < r_min(+inf) always holds."),
        N.callout("Analogy: Think of each DFS call as a 'quality inspector' that examines a factory "
                  "section and returns a report: (passes_inspection, worker_count, lowest_id, highest_id). "
                  "The parent inspector uses these reports from both sub-factories to decide if the whole "
                  "combined factory passes — without re-inspecting every worker.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code("""\
def largestBSTSubtree(root) -> int:
    ans = [0]  # list so nested function can mutate it

    def dfs(node):
        # Returns (is_bst, size, min_val, max_val)
        if not node:
            # Null: valid BST, size 0, sentinels for min/max
            return True, 0, float('inf'), float('-inf')

        l_bst, l_sz, l_min, l_max = dfs(node.left)   # post-order: left first
        r_bst, r_sz, r_min, r_max = dfs(node.right)  # then right

        # Three conditions for current node to form a BST:
        # (a) left subtree is BST, (b) right subtree is BST,
        # (c) l_max (global max of left) < node.val < r_min (global min of right)
        if l_bst and r_bst and l_max < node.val < r_min:
            sz = l_sz + r_sz + 1
            ans[0] = max(ans[0], sz)
            # Return global min and max of THIS entire subtree
            return True, sz, min(node.val, l_min), max(node.val, r_max)

        return False, 0, 0, 0  # not a BST; signal failure upward

    dfs(root)
    return ans[0]
"""),
    N.h3("Line by Line"),
    N.para(N.rich([("ans = [0]", {"code": True}),
                   (" — Mutable list (not int) so the nested dfs() function can update it via closure.", {})])),
    N.para(N.rich([("if not node:", {"code": True}),
                   (" — Base case: null node. Returns (True, 0, +inf, -inf). "
                    "The sentinel values (+inf for min, -inf for max) mean 'no constraint from this empty side.'", {})])),
    N.para(N.rich([("l_bst, l_sz, l_min, l_max = dfs(node.left)", {"code": True}),
                   (" — Post-order: recurse into left child first. Unpack all four return values. "
                    "Using named variables instead of indices prevents a very common off-by-one bug.", {})])),
    N.para(N.rich([("r_bst, r_sz, r_min, r_max = dfs(node.right)", {"code": True}),
                   (" — Recurse into right child. Now we have both children's full range information.", {})])),
    N.para(N.rich([("l_max < node.val < r_min", {"code": True}),
                   (" — This is the crucial global check. l_max is the LARGEST value anywhere in the "
                    "left subtree; r_min is the SMALLEST value anywhere in the right subtree. "
                    "If both bounds respect node.val, the entire BST ordering is satisfied.", {})])),
    N.para(N.rich([("sz = l_sz + r_sz + 1", {"code": True}),
                   (" — Current BST size = left size + right size + 1 (for the current node itself).", {})])),
    N.para(N.rich([("return True, sz, min(node.val, l_min), max(node.val, r_max)", {"code": True}),
                   (" — min(node.val, l_min) is the global minimum across the current subtree "
                    "(node.val might be the min if left is empty; otherwise l_min is smaller). "
                    "Similarly for max.", {})])),
    N.para(N.rich([("return False, 0, 0, 0", {"code": True}),
                   (" — Not a BST. Return False so any ancestor also returns False — "
                    "a BST cannot be built through an invalid subtree.", {})])),
    N.divider(),
]

# ── Solution 2: Brute Force O(n^2) ──
blocks += [
    N.h2("Solution 2 — Brute Force: Validate Each Node Separately"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Start with the simplest idea: try every node as the root of a potential BST subtree. "
               "For each node, run a standard BST validation on its subtree. If it passes, count its nodes."),
        N.h4("What Doesn't Work (Why We Optimize)"),
        N.para("For each of the n nodes, BST validation takes O(n) time (visiting every descendant). "
               "Total: O(n²). For n=10,000 nodes this is 100 million operations — too slow."),
        N.h4("The Key Observation"),
        N.para("When the root's left subtree is invalid, we recurse into its left and right children "
               "separately. This re-validates many of the same nodes repeatedly. The optimal solution "
               "eliminates this redundancy by passing information upward in a single pass."),
        N.h4("Building the Solution"),
        N.para("Write is_bst(node, lo, hi) with range constraints, and count(node) to count nodes. "
               "Then solve(node): if the full subtree is a BST return its count; else take the max "
               "of solve(left) and solve(right). This O(n²) solution is worth mentioning first in "
               "an interview as a baseline."),
    ]),
    N.h3("Code"),
    N.code("""\
def largestBSTSubtree_brute(root) -> int:
    def is_bst(node, lo, hi):
        if not node: return True
        if not (lo < node.val < hi): return False
        return (is_bst(node.left, lo, node.val) and
                is_bst(node.right, node.val, hi))

    def count(node):
        if not node: return 0
        return 1 + count(node.left) + count(node.right)

    def solve(node):
        if not node: return 0
        if is_bst(node, float('-inf'), float('inf')):
            return count(node)
        return max(solve(node.left), solve(node.right))

    return solve(root)
"""),
    N.h3("Line by Line"),
    N.para(N.rich([("is_bst(node, lo, hi)", {"code": True}),
                   (" — Standard BST validation passing valid value range (lo, hi) downward. "
                    "Every node must be strictly between lo and hi.", {})])),
    N.para(N.rich([("count(node)", {"code": True}),
                   (" — Simple O(n) subtree node count.", {})])),
    N.para(N.rich([("if is_bst(node, float('-inf'), float('inf')):", {"code": True}),
                   (" — If current node's subtree is valid, return its count (no need to check children "
                    "separately — this is the largest BST rooted here).", {})])),
    N.para(N.rich([("return max(solve(node.left), solve(node.right))", {"code": True}),
                   (" — Current node's subtree is not a BST; recurse into both halves independently.", {})])),
    N.divider(),
]

# ── Complexity table ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Post-order DFS with range tuple (optimal)", "O(n)", "O(h)"],
        ["Brute force — validate each node", "O(n²)", "O(h)"],
    ]),
    N.para("h = tree height. O(log n) for balanced trees, O(n) for skewed trees (single chain)."),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Trees", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Post-order with Range (DFS: Postorder)", {})])),
    N.callout(
        "When to recognize this pattern: (1) problem asks about a subtree property "
        "(BST, balanced, max path, etc.), (2) the property at a node depends on both children's "
        "results PLUS aggregated information (min, max, height, count) from all descendants, "
        "(3) you need to answer the query bottom-up in a single pass.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same post-order with returned state technique:"),
    N.bullet(N.rich([("Validate Binary Search Tree", {"bold": True}),
                     (" (Medium) — Same range-passing idea; simpler as it only asks yes/no for the whole tree.", {})])),
    N.bullet(N.rich([("Diameter of Binary Tree", {"bold": True}),
                     (" (Easy) — Post-order returns height; parent combines left+right arms for diameter.", {})])),
    N.bullet(N.rich([("Balanced Binary Tree", {"bold": True}),
                     (" (Easy) — Post-order returns (is_balanced, height); exact same 2-tuple pattern.", {})])),
    N.bullet(N.rich([("Binary Tree Maximum Path Sum", {"bold": True}),
                     (" (Hard) — Post-order with global max; child returns best single-arm gain for parent.", {})])),
    N.bullet(N.rich([("Count Good Nodes in Binary Tree", {"bold": True}),
                     (" (Medium) — Pre-order DFS passing max-so-far; complementary top-down approach.", {})])),
    N.bullet(N.rich([("Kth Smallest Element in a BST", {"bold": True}),
                     (" (Medium) — In-order traversal of a BST; exploits BST sorted order property.", {})])),
    N.bullet(N.rich([("Binary Tree Cameras", {"bold": True}),
                     (" (Hard) — Post-order returning (covered, camera, not_covered) state per node.", {})])),
    N.para("These problems share the same core technique: design the DFS return type to bubble up "
           "exactly what the parent needs, process children first (post-order), and combine results at each node."),
    N.callout("📚 Pattern Classification: Trees / DFS: Postorder — This sub-pattern is listed in the "
              "DSA Patterns Guide under Tree Patterns as 'DFS: Postorder (Left → Right → Root)'.",
              "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.",
                    {"italic": True, "color": "gray"})])),
]

# ── Append all blocks ──────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"Notion body rebuilt. Total blocks: {len(blocks)}")
print(f"NOTION OK {PAGE_ID}")
