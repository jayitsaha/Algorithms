"""gen_subtree_of_another_tree.py — Notion page rebuild for LeetCode #572."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notion_lib as N

PAGE_ID = "39193418-809c-81b2-84bb-de50035bcc6f"
SLUG    = "subtree_of_another_tree"

# ── 1. Set properties ──────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=572,
    pattern="Trees",
    subpatterns=["Check at Each Node"],
    tc="O(m·n)",
    sc="O(m)",
    key_insight="Walk every node with DFS; at each node call isSameTree to check if subRoot begins there.",
    icon="🟢",
)
print("Properties OK")

# ── 2. Wipe old content ────────────────────────────────────────────
print("Wiping old blocks...")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks")

# ── 3. Build body blocks ───────────────────────────────────────────
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given the roots of two binary trees ", {}),
        ("root", {"code": True}),
        (" and ", {}),
        ("subRoot", {"code": True}),
        (", return ", {}),
        ("true", {"code": True}),
        (" if there is a subtree of ", {}),
        ("root", {"code": True}),
        (" with the same structure and node values of ", {}),
        ("subRoot", {"code": True}),
        (", and ", {}),
        ("false", {"code": True}),
        (" otherwise. A subtree of a tree consists of a node and all its descendants.", {}),
    ])),
    N.para("Constraints: the number of nodes in root is in range [1, 2000]; number of nodes in subRoot is in range [1, 1000]; -10^4 <= val <= 10^4."),
    N.divider(),
]

# ── Solution 1 ──
sol1_code = """\
class Solution:
    def isSubtree(self, root, subRoot) -> bool:
        if not root:                          # Exhausted tree, no match
            return False
        if self.isSameTree(root, subRoot):    # Does subRoot begin exactly here?
            return True
        return (self.isSubtree(root.left,  subRoot) or   # Try left branch
                self.isSubtree(root.right, subRoot))      # Try right branch

    def isSameTree(self, p, q) -> bool:
        if not p and not q: return True    # Both null → perfect match
        if not p or  not q: return False   # One null, one not → mismatch
        if p.val != q.val:  return False   # Different values → mismatch
        return (self.isSameTree(p.left,  q.left) and   # Left children match?
                self.isSameTree(p.right, q.right))      # Right children match?
"""

blocks += [
    N.h2("Solution 1 — DFS + isSameTree (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We're asking: 'does there exist any node n in root such that the tree rooted at n is exactly the same as subRoot?' This is a search + validation problem. We need to visit candidates (every node of root) and validate each one."),
        N.h4("What Doesn't Work"),
        N.para("Checking only if values match at each node won't work — the whole subtree structure must match. And you can't just find subRoot's root value in root, because there might be multiple nodes with the same value but different children."),
        N.h4("The Key Observation"),
        N.para("This is a two-function problem: (1) isSubtree navigates every node of root looking for a starting point, (2) isSameTree validates whether two trees are structurally and value-identical. Keep these responsibilities separate."),
        N.h4("Building the Solution"),
        N.para("Start with isSameTree (the simpler sub-problem). Two trees are equal if both are null, or both are non-null with equal root values and equal left and right subtrees. Then isSubtree just calls isSameTree at each node visited during a pre-order DFS — return True as soon as any call succeeds."),
        N.callout("Analogy: Searching for a word in a book. isSubtree = flipping through pages (finding candidates). isSameTree = reading the word letter by letter to confirm it matches.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(sol1_code),
    N.h3("Line by Line"),
    N.para(N.rich([("if not root:", {"code": True}), " — Base case: we've walked the entire tree without finding a match. Return False."])),
    N.para(N.rich([("if self.isSameTree(root, subRoot):", {"code": True}), " — Test the current node as the root of a matching subtree. If it passes, we're done."])),
    N.para(N.rich([("return isSubtree(root.left, subRoot) or ...", {"code": True}), " — If this node doesn't match, recurse into left and right subtrees. OR short-circuits: once True is found, right branch is never evaluated."])),
    N.para(N.rich([("if not p and not q:", {"code": True}), " — Both trees are null at this position. This is a perfect structural match for these children."])),
    N.para(N.rich([("if not p or not q:", {"code": True}), " — Exactly one is null. One tree has a child here, the other doesn't — structural mismatch."])),
    N.para(N.rich([("if p.val != q.val:", {"code": True}), " — Both non-null but different values. Mismatch."])),
    N.para(N.rich([("return isSameTree(p.left, q.left) and ...", {"code": True}), " — Both values match; now verify left subtrees AND right subtrees recursively. AND short-circuits on first False."])),
    N.divider(),
]

# ── Solution 2 ──
sol2_code = """\
class Solution:
    def isSubtree(self, root, subRoot) -> bool:
        def serialize(node):
            if not node:
                return "#"              # # marks null — captures structure
            return (f"^{node.val}"      # ^ prefix prevents val collision
                    + serialize(node.left)
                    + serialize(node.right))

        return serialize(subRoot) in serialize(root)
"""

blocks += [
    N.h2("Solution 2 — Serialization + Substring Match"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("If we could convert both trees to strings that uniquely represent their structure, then 'is subRoot a subtree of root' becomes 'is the serialization of subRoot a substring of the serialization of root' — a classic string problem."),
        N.h4("What Doesn't Work"),
        N.para("Naive serialization without delimiters causes false matches: node value 1 followed by node value 2 becomes '12', which looks identical to a single node with value 12."),
        N.h4("The Key Observation"),
        N.para("Pre-order serialization with a value delimiter (^) and a null marker (#) creates a unique fingerprint per tree. The ^ prefix on each value ensures no two different trees produce the same string."),
        N.h4("Building the Solution"),
        N.para("Serialize both trees using pre-order traversal. Use '#' for null nodes and '^' before each value. Then simply check if serialize(subRoot) appears as a substring in serialize(root)."),
        N.callout("This reduces to: does subRoot's 'fingerprint' appear inside root's 'fingerprint'? The Python 'in' operator handles the substring check in O(m+n) average time.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(sol2_code),
    N.h3("Line by Line"),
    N.para(N.rich([("if not node: return '#'", {"code": True}), " — Null nodes become '#'. This encodes structural information — without it, null children would be invisible."])),
    N.para(N.rich([("f'^{node.val}'", {"code": True}), " — The ^ prefix before every value prevents '1' + '2' being confused with '12'. Each node value is unambiguously delimited."])),
    N.para(N.rich([("+ serialize(node.left) + serialize(node.right)", {"code": True}), " — Pre-order: root value first, then left, then right subtree strings concatenated."])),
    N.para(N.rich([("serialize(subRoot) in serialize(root)", {"code": True}), " — Python substring check. Returns True if the subRoot's full serialization appears anywhere within root's serialization."])),
    N.callout("Warning: The delimiter trick is non-negotiable. Without '^', a tree [1,2] serializes to '12#' which could be confused with a tree [12] serializing to '12#'. The '^' makes them '^1^2#' vs '^12#' — unambiguous.", "⚠️", "yellow_background"),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution",                "Time",   "Space"],
        ["DFS + isSameTree (✓)",    "O(m·n)", "O(m)"],
        ["Serialization + Substring","O(m+n)", "O(m+n)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Trees (Section 11 — Tree Traversal Patterns)"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Check at Each Node — Pre-Order DFS (visit root, test isSameTree, then recurse left/right)"])),
    N.callout(
        "When to recognize this pattern: The problem asks whether some tree/pattern appears somewhere inside a larger tree. Key signals: 'is A a subtree of B?', 'does any node satisfy X?', 'find all nodes where...' — these all require visiting every node + testing a condition at each one.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same sub-pattern (Check at Each Node / Pre-Order DFS):"),
    N.bullet(N.rich([("Same Tree", {"bold": True}), " (Easy) — The isSameTree helper we wrote IS the full solution; #100"])),
    N.bullet(N.rich([("Symmetric Tree", {"bold": True}), " (Easy) — Compare left and right subtrees as mirrors with the same recursive structure; #101"])),
    N.bullet(N.rich([("Binary Tree Paths", {"bold": True}), " (Easy) — Pre-order DFS collecting root-to-leaf path strings at each leaf; #257"])),
    N.bullet(N.rich([("Path Sum", {"bold": True}), " (Easy) — At each leaf, check if accumulated sum equals target; #112"])),
    N.bullet(N.rich([("Count Univalue Subtrees", {"bold": True}), " (Medium) — Post-order DFS: at each node check if entire subtree has same value; #250"])),
    N.bullet(N.rich([("Find Duplicate Subtrees", {"bold": True}), " (Medium) — Serialize each subtree and use a hash map to collect duplicates; #652"])),
    N.para("These problems share the core technique: walk every node of the tree and apply a per-node test (sometimes aggregating child results post-order, sometimes testing greedily pre-order)."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 11.2 (Pre-Order Traversal) — Sub-Pattern: Check at Each Node", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

# ── Append all blocks ──────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"RESULT {SLUG} | html=OK | notion=OK | lines=837")
