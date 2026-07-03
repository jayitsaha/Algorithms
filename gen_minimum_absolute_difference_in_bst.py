"""
Notion update script for: Minimum Absolute Difference in BST (#530)
Pattern: Trees · Subpattern: Same as Min Distance (In-order, Track Prev)
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-81d0-8424-cee2bfe88346"
SLUG    = "minimum_absolute_difference_in_bst"

# ── 1. Set properties ──────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=530,
    pattern="Trees",
    subpatterns=["Same as Min Distance"],
    tc="O(n)",
    sc="O(h)",
    key_insight="In-order traversal of a BST yields sorted values; the minimum absolute difference must be between adjacent values in that sorted sequence.",
    icon="🟢"
)
print("Properties set.")

# ── 2. Wipe old content ────────────────────────────────────────────
print("Wiping old blocks...")
deleted = N.wipe_page(PAGE_ID)
print(f"Deleted {deleted} old blocks.")

# ── 3. Build body ──────────────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given the ", {}),
        ("root", {"code": True}),
        (" of a Binary Search Tree (BST), return the minimum absolute difference between the values of any two different nodes in the tree."),
    ])),
    N.para("Constraints: The number of nodes is in the range [2, 10⁴]. Node values are in [0, 10⁵]. This is identical to LeetCode #783 (Minimum Distance Between BST Nodes)."),
    N.divider(),
]

# ── Solution 1: In-Order with Prev (Optimal) ───────────────────────
blocks += [
    N.h2("Solution 1 — In-Order Traversal with Prev Pointer (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We want the smallest gap between any two node values in a BST. There are up to n*(n-1)/2 pairs — checking all of them is O(n²). We need a smarter approach that uses the BST structure."),
        N.h4("What Doesn't Work"),
        N.para("Brute force: visit every pair of nodes and compute their absolute difference. O(n²) time. Does not leverage the BST property at all. Even the 'collect all values then sort' approach requires an explicit O(n log n) sort, which is also unnecessary for a BST."),
        N.h4("The Key Observation"),
        N.para("In a BST, in-order traversal (Left → Root → Right) visits nodes in STRICTLY ASCENDING sorted order. This is the BST's fundamental property. Once values are in sorted order, the minimum difference can ONLY come from two adjacent values — never from values far apart (by the triangle inequality: |a-c| = |a-b| + |b-c| ≥ min(|a-b|, |b-c|))."),
        N.h4("Building the Solution"),
        N.para("So we do an in-order DFS and track just the PREVIOUS node's value in 'prev'. At each node: compute diff = curr.val - prev (always non-negative), update min_diff, then set prev = curr.val. This is a single O(n) pass with O(h) space — no array needed."),
        N.callout("Analogy: Imagine walking through a sorted list and only comparing each number to the one right before it. You'd find the minimum gap without ever comparing non-adjacent pairs.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code("""def getMinimumDifference(root) -> int:
    self.min_diff = float('inf')
    self.prev = None

    def inorder(node):
        if not node:
            return
        inorder(node.left)           # 1. go left (smaller values first)
        if self.prev is not None:
            diff = node.val - self.prev
            self.min_diff = min(self.min_diff, diff)
        self.prev = node.val         # 2. update prev to current
        inorder(node.right)          # 3. go right (larger values next)

    inorder(root)
    return self.min_diff"""),
    N.h3("Line by Line"),
    N.para(N.rich([("self.min_diff = float('inf')", {"code": True}), " — Start with infinity: no minimum found yet."])),
    N.para(N.rich([("self.prev = None", {"code": True}), " — No previous node visited. Will be set on first node."])),
    N.para(N.rich([("if not node: return", {"code": True}), " — Base case: null node means we hit a leaf's child — backtrack."])),
    N.para(N.rich([("inorder(node.left)", {"code": True}), " — Recurse left BEFORE processing current node — ensures ascending order."])),
    N.para(N.rich([("if self.prev is not None:", {"code": True}), " — Skip the very first node (no previous value to subtract)."])),
    N.para(N.rich([("diff = node.val - self.prev", {"code": True}), " — Compute gap. Always ≥ 0 since we visit in ascending order. No abs() needed."])),
    N.para(N.rich([("self.min_diff = min(self.min_diff, diff)", {"code": True}), " — Update the running minimum."])),
    N.para(N.rich([("self.prev = node.val", {"code": True}), " — Record this node's value as the new 'previous' for the next node."])),
    N.para(N.rich([("inorder(node.right)", {"code": True}), " — Recurse right AFTER processing current — larger values come next."])),
    N.para(N.rich([("return self.min_diff", {"code": True}), " — After full traversal, this is the global minimum gap."])),
    N.divider(),
]

# ── Solution 2: Collect In-Order Array ────────────────────────────
blocks += [
    N.h2("Solution 2 — Collect In-Order Array, then Scan"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Instead of optimizing space, collect all BST values into an array via in-order traversal (giving sorted order for free), then simply scan adjacent pairs for the minimum gap."),
        N.h4("What Doesn't Work"),
        N.para("This approach works correctly and is O(n) time — the issue is it uses O(n) extra space for the array, when we could track just one 'prev' value instead."),
        N.h4("The Key Observation"),
        N.para("The BST in-order property means we get sorted order without sorting. Appending to an array during in-order traversal is straightforward and easy to verify for correctness."),
        N.h4("Building the Solution"),
        N.para("Run in-order DFS, appending each node's value. Then iterate the resulting array, computing adjacent differences and returning the minimum."),
        N.callout("Use this approach in an interview if you want a simpler-to-explain version before optimizing space to O(h).", "💡", "green_background"),
    ]),
    N.h3("Code"),
    N.code("""def getMinimumDifference(root) -> int:
    vals = []

    def inorder(node):
        if not node:
            return
        inorder(node.left)
        vals.append(node.val)    # collect in sorted order
        inorder(node.right)

    inorder(root)
    return min(vals[i] - vals[i-1] for i in range(1, len(vals)))"""),
    N.h3("Line by Line"),
    N.para(N.rich([("vals = []", {"code": True}), " — Array to collect all node values in sorted order."])),
    N.para(N.rich([("vals.append(node.val)", {"code": True}), " — Append during in-order visit — result is sorted ascending."])),
    N.para(N.rich([("min(vals[i] - vals[i-1] for i in range(1, len(vals)))", {"code": True}), " — Scan adjacent pairs and find the minimum gap."])),
    N.divider(),
]

# ── Solution 3: Brute Force ───────────────────────────────────────
blocks += [
    N.h2("Solution 3 — Brute Force: Collect all Values + Sort (O(n log n))"),
    N.h3("Code"),
    N.code("""def getMinimumDifference(root) -> int:
    vals = []

    def dfs(node):           # any traversal order works here
        if not node:
            return
        vals.append(node.val)
        dfs(node.left)
        dfs(node.right)

    dfs(root)
    vals.sort()              # sort separately (in-order gives this FREE!)
    return min(vals[i] - vals[i-1] for i in range(1, len(vals)))"""),
    N.para("This approach ignores the BST property entirely: it collects all values in any order (preorder here), then sorts them explicitly. The sort dominates at O(n log n). Mention this as a starting point, then immediately propose the O(n) in-order approach."),
    N.divider(),
]

# ── Complexity ────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (collect + sort)", "O(n log n)", "O(n)"],
        ["Collect In-Order Array", "O(n)", "O(n)"],
        ["In-Order with Prev (optimal)", "O(n)", "O(h) — O(log n) balanced, O(n) skewed"],
    ]),
    N.divider(),
]

# ── Pattern Classification ────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Trees (Section 11 — Tree Traversals)"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Same as Min Distance (In-Order Traversal, Track Prev) — Guide Section 11.3"])),
    N.callout(
        "When to recognize this pattern: (1) Problem involves a BST — not just a binary tree. (2) You need values in sorted order (min, max, kth, gap). (3) Comparing adjacent nodes in sorted sequence solves the problem. Signal words: 'minimum difference', 'kth smallest', 'validate BST', 'sorted order'.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same BST In-Order Traversal technique:"),
    N.bullet(N.rich([("Minimum Distance Between BST Nodes", {"bold": True}), " (Easy) — Identical problem, alternate number (#783). Use this problem interchangeably in study."])),
    N.bullet(N.rich([("Kth Smallest Element in a BST", {"bold": True}), " (Medium) — In-order traversal; decrement counter at each visit, return on hit (#230)."])),
    N.bullet(N.rich([("Validate Binary Search Tree", {"bold": True}), " (Medium) — In-order must produce strictly ascending values; track prev, check curr > prev (#98)."])),
    N.bullet(N.rich([("Recover Binary Search Tree", {"bold": True}), " (Medium) — In-order to identify the two nodes whose values are swapped; swap them back (#99)."])),
    N.bullet(N.rich([("Binary Search Tree Iterator", {"bold": True}), " (Medium) — Controlled in-order using an explicit stack; next() in O(1) avg, hasNext() in O(1) (#173)."])),
    N.bullet(N.rich([("Convert Sorted Array to Binary Search Tree", {"bold": True}), " (Easy) — Inverse: given a sorted array, reconstruct a height-balanced BST using divide-and-conquer (#108)."])),
    N.para("These problems share the same core technique: BST in-order traversal yields a sorted sequence, enabling efficient comparisons between consecutive values."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 11.3 (Trees → In-Order Traversal). Sub-Pattern: 'Same as Min Distance'.", "📚", "gray_background"),
]

# ── Embed ─────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ─────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
