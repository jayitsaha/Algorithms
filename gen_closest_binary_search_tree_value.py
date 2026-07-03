"""
gen_closest_binary_search_tree_value.py
Notion in-place update for: Closest Binary Search Tree Value (LeetCode #270)
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-8189-a363-cc7fdc1a4710"

# ── 1. Set properties ──────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=270,
    pattern="Trees",
    subpatterns=["Track Closest While Searching"],
    tc="O(h)",
    sc="O(1)",
    key_insight="Walk a single root-to-null BST path; at each node go left if target < node.val, else go right, updating the closest candidate throughout.",
    icon="🟢",
)
print("Properties set.")

# ── 2. Wipe old body ───────────────────────────────────────────────────────
print("Wiping old content...")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3. Rebuild body ────────────────────────────────────────────────────────
SLUG = "closest_binary_search_tree_value"
EMBED_URL = N.embed_url_for(SLUG)

SOL1_CODE = '''\
def closestValue(root, target: float) -> int:
    closest = root.val   # first candidate: root
    node = root
    while node:
        if abs(node.val - target) < abs(closest - target):
            closest = node.val   # found a closer node
        if target < node.val:
            node = node.left     # right subtree only farther away
        else:
            node = node.right    # left subtree only farther away
    return closest
'''

SOL2_CODE = '''\
def closestValue(root, target: float) -> int:
    """Recursive: one-child recursion, O(h) time, O(h) stack space."""
    if not root:
        return float('inf')
    if target == root.val:
        return root.val          # exact match — 0 diff, can't improve
    if target < root.val:
        child = closestValue(root.left, target)
    else:
        child = closestValue(root.right, target)
    if child == float('inf'):
        return root.val          # no child in that direction
    if abs(child - target) < abs(root.val - target):
        return child             # child is closer
    return root.val              # root is closer (or tied)
'''

blocks = []

# ── Problem ────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        "Given the ", ("root", {"code": True}),
        " of a Binary Search Tree and a floating-point ",
        ("target", {"code": True}),
        ", return the integer value in the BST closest to target. "
        "The closest value is defined as the node whose value has the "
        "minimum absolute difference |node.val − target|. "
        "The tree is non-empty and guaranteed to have a unique answer.",
    ])),
    N.divider(),
]

# ── Solution 1 ─────────────────────────────────────────────────────────────
blocks += [
    N.h2("Solution 1 — Iterative BST Search (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We want the tree value with the smallest distance to a target on the number line. "
            "Instead of checking all n values, can the BST ordering help us navigate directly "
            "toward the answer?"
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Visiting every node via inorder traversal is O(n) and ignores the BST property entirely. "
            "It works, but we're throwing away the core structural advantage of the BST."
        ),
        N.h4("The Key Observation"),
        N.para(
            "At any node with value v, if target < v, then every right-subtree value r satisfies "
            "r >= v > target, so |r − target| >= |v − target|. The right subtree cannot contain "
            "a closer value. We prune it entirely. Symmetrically for the left when target >= v."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1) Start: closest = root.val (first candidate). "
            "2) At every node, update closest if current node is closer to target. "
            "3) Choose direction: if target < node.val go left, else go right. "
            "4) Stop when node = None. "
            "We walk exactly one root-to-null path — O(h) time, O(1) space."
        ),
        N.callout(
            "Analogy: Searching for a name in a sorted phone book. At each page, "
            "you know which half to eliminate — you never need to read both halves.",
            "📖", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOL1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("closest = root.val", {"code": True}), " — Initialize closest to root value; this is our first candidate since the tree is guaranteed non-empty."])),
    N.para(N.rich([("node = root", {"code": True}), " — Start the traversal pointer at root."])),
    N.para(N.rich([("while node:", {"code": True}), " — Keep iterating until we fall off the tree (node becomes None)."])),
    N.para(N.rich([("if abs(node.val - target) < abs(closest - target):", {"code": True}), " — Compare: is this node closer to target than our current best?"])),
    N.para(N.rich([("closest = node.val", {"code": True}), " — Yes — update our running best candidate."])),
    N.para(N.rich([("if target < node.val:", {"code": True}), " — BST navigation: target lies to the left of current node."])),
    N.para(N.rich([("node = node.left", {"code": True}), " — Go left; all right-subtree values are >= node.val and thus farther from target than node.val itself."])),
    N.para(N.rich([("else: node = node.right", {"code": True}), " — target >= node.val: go right; left-subtree values are <= node.val and farther from target."])),
    N.para(N.rich([("return closest", {"code": True}), " — Return the best candidate found along the single search path."])),
    N.divider(),
]

# ── Solution 2 ─────────────────────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Recursive (One-Child Recursion)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Same navigation as Solution 1, but expressed recursively. "
            "At each call, choose left or right subtree, recurse once, "
            "then compare the returned best-from-subtree with current node."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Recursing into BOTH children is a common mistake. That produces O(n) time "
            "and loses the pruning benefit — equivalent to a full tree traversal."
        ),
        N.h4("The Key Observation"),
        N.para(
            "We only ever recurse into ONE child (the one in the direction of target). "
            "The return value is the best candidate in that subtree. "
            "We compare it with root.val and return the closer one."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Base case: node is None → return infinity (no candidate here). "
            "Exact match: return immediately. "
            "Recurse into left (if target < root.val) or right (otherwise). "
            "Return the closer of root.val and the subtree's best."
        ),
        N.callout(
            "Trade-off: Recursive is elegant and easy to reason about, "
            "but uses O(h) stack space. For a degenerate (fully skewed) BST, "
            "that is O(n) stack frames. Prefer iterative for production / constrained environments.",
            "⚖️", "yellow_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("if not root: return float('inf')", {"code": True}), " — Base case: no node here, return sentinel infinity (means 'no candidate from this direction')."])),
    N.para(N.rich([("if target == root.val: return root.val", {"code": True}), " — Exact match — absolute difference is 0, can't improve."])),
    N.para(N.rich([("if target < root.val:", {"code": True}), " — Navigate left: all values in right subtree are farther."])),
    N.para(N.rich([("child = closestValue(root.left, target)", {"code": True}), " — Recurse into only the left subtree."])),
    N.para(N.rich([("else: child = closestValue(root.right, target)", {"code": True}), " — target >= root.val: recurse right."])),
    N.para(N.rich([("if child == float('inf'): return root.val", {"code": True}), " — No child in the chosen direction — root is the only candidate."])),
    N.para(N.rich([("if abs(child - target) < abs(root.val - target): return child", {"code": True}), " — The subtree's best beats the current root."])),
    N.para(N.rich([("return root.val", {"code": True}), " — root is at least as good as any subtree candidate."])),
    N.divider(),
]

# ── Complexity ─────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution",               "Time",  "Space"],
        ["Inorder + linear scan",  "O(n)",  "O(n)"],
        ["Recursive (one child)",  "O(h)",  "O(h)"],
        ["Iterative Search ✓",     "O(h)",  "O(1)"],
    ]),
    N.para("h = tree height. O(log n) for a balanced BST; O(n) worst case for a fully skewed BST."),
    N.divider(),
]

# ── Pattern Classification ─────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Trees (BST sub-type)"])),
    N.para(N.rich([("Sub-Pattern: ", {"bold": True}), "Track Closest While Searching — navigate toward target using BST ordering, updating a running best at each node."])),
    N.callout(
        "When to recognize this pattern:\n"
        "• Problem involves a BST and asks 'find closest/nearest value'\n"
        "• Looking for floor, ceiling, predecessor, or successor in a BST\n"
        "• 'Search for X, X may not exist — find nearest match'\n"
        "• Any problem combining BST + closest/approximate search",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ───────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same BST Property sub-pattern:"),
    N.bullet(N.rich([("Closest BST Value II", {"bold": True}), " (Hard, #272) — Find k closest values; inorder walk + sliding window of size k"])),
    N.bullet(N.rich([("Search in a Binary Search Tree", {"bold": True}), " (Easy, #700) — Same BST navigation, exact target lookup"])),
    N.bullet(N.rich([("Insert into a Binary Search Tree", {"bold": True}), " (Medium, #701) — Navigate to correct position, insert at null leaf"])),
    N.bullet(N.rich([("Validate Binary Search Tree", {"bold": True}), " (Medium, #98) — Use BST ordering property to verify tree correctness"])),
    N.bullet(N.rich([("Kth Smallest Element in a BST", {"bold": True}), " (Medium, #230) — Inorder traversal exploiting sorted BST property"])),
    N.bullet(N.rich([("Delete Node in a BST", {"bold": True}), " (Medium, #450) — Navigate with BST property, restructure on deletion"])),
    N.para("These problems share the core technique: exploit BST ordering to navigate in O(h) rather than O(n)."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Trees section, BST Property sub-pattern", "📚", "gray_background"),
]

# ── Visual Explainer embed ─────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(EMBED_URL),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

print(f"Appending {len(blocks)} blocks to Notion page {PAGE_ID}...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
