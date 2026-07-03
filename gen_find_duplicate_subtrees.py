import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-814b-8ac5-dcef6c779938"

# ── Step 1: Set properties ──────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=652,
    pattern="Trees",
    subpatterns=["Serialize Subtrees + Hash"],
    tc="O(n²)",
    sc="O(n²)",
    key_insight="Serialize each subtree as a string via postorder DFS; count occurrences with a hash map; add root to result when count first reaches 2.",
    icon="🟡"
)
print("Properties set.")

# ── Step 2: Wipe old body ───────────────────────────────────────────────
deleted = N.wipe_page(PAGE_ID)
print(f"Wiped {deleted} old blocks.")

# ── Step 3: Build body blocks ───────────────────────────────────────────
blocks = []

# ── Problem ──────────────────────────────────────────────────────────────
blocks.append(N.h2("Problem"))
blocks.append(N.para(N.rich([
    ("Given the root of a binary tree, return all duplicate subtrees. "
     "For each kind of duplicate subtrees, you only need to return the root node of any one of them. "
     "Two trees are duplicate if they have the same structure with the same node values. "),
    ("root", {"code": True}),
    (" is a TreeNode. Return a list of TreeNode roots (one per unique duplicate subtree).")
])))
blocks.append(N.callout(
    N.rich([
        ("Example: root = [1,2,3,4,null,2,4,null,null,4]\n"
         "Output: [[2,4],[4]] — subtree rooted at 2 (with child 4) appears twice, leaf 4 appears three times."),
    ]),
    "📋", "gray_background"
))
blocks.append(N.divider())

# ── Solution 1 — Optimal ─────────────────────────────────────────────────
blocks.append(N.h2("Solution 1 — Postorder Serialization + Hash Map (Interview Pick)"))

blocks.append(N.toggle_h3("💡 Intuition: How to Arrive at This", [
    N.h4("Reframe the Problem"),
    N.para("We need to find subtrees that appear more than once. Two subtrees are equal iff they share the same structure AND the same values at every position. The challenge: how to compare subtrees efficiently across the whole tree."),

    N.h4("What Doesn't Work"),
    N.para("Brute force: compare every pair of subtrees using recursive isSameTree. That's O(n²) pairs × O(n) comparison = O(n³) total — too slow for large trees."),

    N.h4("The Key Observation"),
    N.para("If we could assign each unique subtree a unique name (a string fingerprint), then duplicate detection becomes: find names that appear ≥ 2 times. That's a standard O(1) hash map lookup — we already know how to do that."),

    N.h4("Building the Solution"),
    N.para(
        'Use postorder DFS (process children before the current node). At each node, build a key: '
        'f"{node.val},{left_serial},{right_serial}" where null children become "#". '
        'This key uniquely identifies the subtree. Count occurrences in a hash map. '
        'When count reaches exactly 2, add the current node to results (once only).'
    ),

    N.callout(
        '🧠 Analogy: Think of each subtree as a book. The serialization string is its ISBN. '
        'If you find two books with the same ISBN, they\'re duplicates. A librarian with a hash map '
        'can spot duplicates in one pass — no need to compare every pair of books.',
        "🧠", "blue_background"
    ),
]))

blocks.append(N.h3("Code"))
blocks.append(N.code(
    """from collections import defaultdict

def findDuplicateSubtrees(root):
    count = defaultdict(int)
    result = []

    def serialize(node):
        if node is None:
            return "#"
        left  = serialize(node.left)
        right = serialize(node.right)
        key = f"{node.val},{left},{right}"
        count[key] += 1
        if count[key] == 2:
            result.append(node)
        return key

    serialize(root)
    return result""",
    "python"
))

blocks.append(N.h3("Line by Line"))
lines = [
    ("from collections import defaultdict", "Auto-initializes missing keys to 0 — cleaner than dict.get(key, 0)."),
    ("count = defaultdict(int)", "Maps serialization string → how many times this subtree structure has appeared."),
    ("result = []", "Collects one root node per unique duplicate subtree (added when count first hits 2)."),
    ("def serialize(node):", "Postorder recursive helper — returns the unique string fingerprint for the subtree rooted at node."),
    ('if node is None: return "#"', 'Null sentinel. Critical: without this, a leaf node and a node with a null child would be indistinguishable.'),
    ("left  = serialize(node.left)", "Postorder step 1: get the left subtree's fingerprint. Recursion goes all the way down before returning."),
    ("right = serialize(node.right)", "Postorder step 2: get the right subtree's fingerprint."),
    ('key = f"{node.val},{left},{right}"', "Combine: current value + left fingerprint + right fingerprint = unique ID for this entire subtree."),
    ("count[key] += 1", "Increment the occurrence count for this serialization."),
    ("if count[key] == 2:", "Exactly 2 = the second occurrence — first time we know it's a duplicate. Using == 2 (not >= 2) so we add each duplicate exactly once."),
    ("result.append(node)", "Record this node as the root of a duplicate subtree."),
    ("return key", "Return fingerprint up the call stack — parent uses it to build its own key."),
    ("serialize(root)", "Start the postorder DFS. Return value is unused at the top level."),
    ("return result", "All duplicate subtree roots, each appearing once in the list."),
]
for code_text, explanation in lines:
    blocks.append(N.para(N.rich([
        (code_text, {"code": True, "bold": True}),
        (f" — {explanation}", {})
    ])))

blocks.append(N.divider())

# ── Solution 2 — Brute Force ─────────────────────────────────────────────
blocks.append(N.h2("Solution 2 — Brute Force: Pairwise isSameTree (Not Recommended)"))

blocks.append(N.toggle_h3("💡 Intuition: How to Arrive at This", [
    N.h4("Reframe the Problem"),
    N.para("Compare every pair of subtrees directly using the recursive tree equality check isSameTree."),
    N.h4("What Doesn't Work"),
    N.para("With n nodes we get O(n²) pairs, and each comparison is O(n). Total O(n³) — acceptable for tiny trees but unusable for n > 1000."),
    N.h4("The Key Observation"),
    N.para("This approach is correct but too slow. It's only useful as a starting point to understand the problem before deriving the serialization optimization."),
    N.h4("Building the Solution"),
    N.para("Collect all subtree roots. For every pair (i, j) where i != j, check isSameTree(nodes[i], nodes[j]). If True and nodes[i] not already in result, add it."),
]))

blocks.append(N.h3("Code"))
blocks.append(N.code(
    """def findDuplicateSubtrees_brute(root):
    def collect(node, nodes):
        if node:
            nodes.append(node)
            collect(node.left, nodes)
            collect(node.right, nodes)

    def isSameTree(a, b):
        if not a and not b: return True
        if not a or not b: return False
        return a.val == b.val and isSameTree(a.left, b.left) and isSameTree(a.right, b.right)

    nodes = []
    collect(root, nodes)
    result, seen = [], set()
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            if isSameTree(nodes[i], nodes[j]) and id(nodes[i]) not in seen:
                result.append(nodes[i])
                seen.add(id(nodes[i]))
                seen.add(id(nodes[j]))
    return result""",
    "python"
))

blocks.append(N.h3("Line by Line"))
brute_lines = [
    ("collect(node, nodes)", "Gathers all n subtree roots via any traversal order."),
    ("isSameTree(a, b)", "Recursive equality check: both null → True; one null → False; compare values and recurse on both children."),
    ("for i in range(len(nodes)): for j ...", "O(n²) pair comparisons."),
    ("isSameTree(nodes[i], nodes[j])", "O(n) comparison each. Total: O(n³)."),
    ("seen.add(id(nodes[i]))", "Avoid adding the same duplicate root multiple times using Python object id."),
]
for code_text, explanation in brute_lines:
    blocks.append(N.para(N.rich([
        (code_text, {"code": True, "bold": True}),
        (f" — {explanation}", {})
    ])))

blocks.append(N.divider())

# ── Complexity ───────────────────────────────────────────────────────────
blocks.append(N.h2("Complexity"))
blocks.append(N.table([
    ["Solution", "Time", "Space", "Notes"],
    ["Brute Force (Pairwise)", "O(n³)", "O(n)", "n² pairs × O(n) isSameTree each"],
    ["Serialization + Hash Map ✓", "O(n²)", "O(n²)", "String concat at each level; single postorder pass"],
    ["Integer ID Memoization", "O(n)", "O(n)", "Advanced: replace strings with integer IDs to avoid string cost"],
]))
blocks.append(N.callout(
    "String-building cost: at each node, building the key takes O(length of key). "
    "In the worst case (skewed tree), the root's key is O(n) long, giving O(n²) total string work. "
    "For balanced trees, it's O(n log n). The hash map stores up to n unique keys.",
    "⏱️", "gray_background"
))
blocks.append(N.divider())

# ── Pattern Classification ───────────────────────────────────────────────
blocks.append(N.h2("🏷️ Pattern Classification"))
blocks.append(N.para(N.rich([("Main Pattern: ", {"bold": True}), "Trees (DFS — Postorder)"])))
blocks.append(N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Serialize Subtrees + Hash — canonical serialization for identity-based duplicate detection"])))
blocks.append(N.callout(
    "When to recognize this pattern:\n"
    "• 'Find duplicate subtrees / subgraphs' → serialize to string + hash map\n"
    "• 'Compare tree equality across multiple positions' → serialization trick\n"
    "• 'Need a hashable key for a recursive data structure' → canonical serialization\n"
    "• Any problem where you need to group or count structurally identical objects",
    "🔎", "green_background"
))
blocks.append(N.para(
    "Note: The sub-pattern 'Serialize Subtrees + Hash' is classified based on analysis. "
    "The core technique — postorder serialization with a frequency hash map — is a specialized "
    "form of the broader Tree Serialization pattern (see also LC 297: Serialize and Deserialize Binary Tree)."
))
blocks.append(N.divider())

# ── Related Problems ─────────────────────────────────────────────────────
blocks.append(N.h2("🔗 Related Problems"))
blocks.append(N.para("Problems using the same technique (serialize + hash or postorder bottom-up propagation):"))
related = [
    ("Serialize and Deserialize Binary Tree", "Hard", "#297", "Deep dive into the exact serialization format this problem uses"),
    ("Subtree of Another Tree", "Easy", "#572", "Check if t's serialization appears among all of s's node serializations"),
    ("Count Univalue Subtrees", "Medium", "#250", "Postorder DFS returning a boolean property bottom-up to the parent"),
    ("Same Tree", "Easy", "#100", "Foundation: recursive structural equality — the building block we exploit here"),
    ("House Robber III", "Medium", "#337", "Tree DP via postorder: each call returns computed values used by parent"),
    ("Binary Tree Cameras", "Hard", "#968", "Postorder DFS returning state (covered/has-camera/needs-camera) from leaves to root"),
    ("Path Sum III", "Medium", "#437", "Hash map technique on trees — prefix sums + hash applied to paths"),
]
for name, diff, num, note in related:
    blocks.append(N.bullet(N.rich([
        (name, {"bold": True}),
        (f" ({diff}) {num}", {}),
        (f" — {note}", {"color": "gray"})
    ])))
blocks.append(N.para("These problems share the same core theme: encoding tree-structure information into a hashable form to enable O(1) lookup / comparison."))
blocks.append(N.callout(
    "📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Trees section (DFS: Postorder)\n"
    "Sub-Pattern: Serialize Subtrees + Hash · Source: Analysis",
    "📚", "gray_background"
))

# ── Embed ────────────────────────────────────────────────────────────────
blocks.append(N.divider())
blocks.append(N.h2("🎯 Interactive Visual Explainer"))
blocks.append(N.embed(N.embed_url_for("find_duplicate_subtrees")))
blocks.append(N.para(N.rich([
    ("Step through the algorithm visually — use Next/Prev or arrow keys.",
     {"italic": True, "color": "gray"})
])))

# ── Append all blocks ─────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
