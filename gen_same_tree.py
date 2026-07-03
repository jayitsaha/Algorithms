"""
gen_same_tree.py — Notion page builder for LeetCode #100 Same Tree.
notion_page_id: null → create fresh page.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

# ── Step 0: Create the page (no existing page_id) ──────────────────
PAGE_ID = N.create_page("Same Tree", 100, "Easy", "🟢")
print(f"Created page: {PAGE_ID}")

# ── Step 1: Set properties ─────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=100,
    pattern="Trees",
    subpatterns=["DFS Preorder on Two Trees"],
    tc="O(n)",
    sc="O(h)",
    key_insight="Simultaneously DFS both trees: return True only if root values match AND both subtrees are the same.",
    icon="🟢",
)
print("Properties set.")

# ── Step 2: Build body blocks ──────────────────────────────────────
blocks = []

# Problem section
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given the roots of two binary trees ", {}),
        ("p", {"code": True}),
        (" and ", {}),
        ("q", {"code": True}),
        (", return ", {}),
        ("true", {"code": True}),
        (" if the trees are structurally identical, "
         "and the nodes have the same value. Return ", {}),
        ("false", {"code": True}),
        (" otherwise.", {}),
    ])),
    N.divider(),
]

# ── Solution 1: Recursive DFS ──────────────────────────────────────
blocks += [
    N.h2("Solution 1 — Recursive DFS (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to verify that two trees are structurally and value-identical "
               "at every node. The question reduces to: 'At each corresponding pair of "
               "positions, do both trees have the same thing?' — either both have a node "
               "with the same value, or both have nothing (null)."),
        N.h4("What Doesn't Work"),
        N.para("A naive approach might collect all values from both trees into lists and "
               "compare them. But [1,2,3] in preorder for tree A could come from a "
               "completely different structure than [1,2,3] from tree B. Structure matters — "
               "so we must compare position by position, not just value sets."),
        N.h4("The Key Observation"),
        N.para("'Same tree' has a perfect recursive definition: two trees are the same if "
               "(a) their roots have the same value, (b) their left subtrees are the same "
               "tree, and (c) their right subtrees are the same tree. This IS the algorithm "
               "— no extra insight needed. The recursive definition maps directly to code."),
        N.h4("Building the Solution"),
        N.para("1. Define base cases: both null → True (empty match), exactly one null → "
               "False (structural mismatch), values differ → False. "
               "2. Recursive case: values match, so return whether BOTH children pairs also "
               "match. The AND short-circuits — left mismatch skips right evaluation entirely."),
        N.callout(
            "Analogy: Imagine two parallel tour guides walking identical buildings floor by floor. "
            "At each room they check: 'Same room number here?' If ever one guide is in a room "
            "and the other hits a wall — mismatch. If both hit walls simultaneously — perfect match.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(
        "def isSameTree(p, q):\n"
        "    # Base case 1: both subtrees are empty -> identical\n"
        "    if p is None and q is None:\n"
        "        return True\n"
        "    # Base case 2: exactly one is None -> structural mismatch\n"
        "    if p is None or q is None:\n"
        "        return False\n"
        "    # Both exist but values differ\n"
        "    if p.val != q.val:\n"
        "        return False\n"
        "    # Values match -> check both subtrees\n"
        "    return (isSameTree(p.left, q.left)\n"
        "        and isSameTree(p.right, q.right))\n"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("if p is None and q is None:", {"code": True}),
                   (" — Both subtrees are empty. Empty trees are trivially identical. "
                    "Return True. This is the 'success leaf' of every recursion.", {})])),
    N.para(N.rich([("if p is None or q is None:", {"code": True}),
                   (" — Exactly one is None. One tree has a node where the other has a "
                    "gap. Structural mismatch — return False immediately.", {})])),
    N.para(N.rich([("if p.val != q.val:", {"code": True}),
                   (" — Both exist but carry different values. This pair fails — return "
                    "False. No need to check any descendants.", {})])),
    N.para(N.rich([("return isSameTree(p.left, q.left) and isSameTree(p.right, q.right)", {"code": True}),
                   (" — Values match here. Recurse on both child pairs. Python's ", {}),
                   ("and", {"code": True}),
                   (" short-circuits: if left subtrees differ, right is never evaluated.", {})])),
    N.divider(),
]

# ── Solution 2: Iterative BFS ──────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Iterative BFS (Stack-Safe for Deep Trees)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("For trees with millions of nodes in a skewed chain (linked-list shaped), "
               "the recursive call stack may hit Python's recursion limit (~1000 frames by "
               "default). We need the same comparison logic but without growing the call stack."),
        N.h4("What Doesn't Work"),
        N.para("The recursive solution is elegant but fragile for pathological inputs. "
               "Any deep recursion can cause RecursionError in Python. In production systems, "
               "this is not acceptable."),
        N.h4("The Key Observation"),
        N.para("We can simulate the recursion explicitly using a queue. Instead of the call "
               "stack holding (p, q) pairs, we put them in a deque. We process pairs one at a "
               "time — same logic as the recursive version, but iteratively. BFS processes "
               "level by level, which is fine since we check all pairs regardless of order."),
        N.h4("Building the Solution"),
        N.para("Seed the queue with the root pair. While the queue is non-empty, pop a pair "
               "and apply the same three checks: both null (continue), one null (False), "
               "values differ (False). If all pass, enqueue both child pairs."),
        N.callout(
            "Use this variant when: the interviewer asks about very deep/skewed trees, "
            "or you need to avoid Python's recursion limit in production.",
            "💡", "green_background"
        ),
    ]),
    N.h3("Code"),
    N.code(
        "from collections import deque\n\n"
        "def isSameTree(p, q):\n"
        "    queue = deque([(p, q)])       # seed with root pair\n"
        "    while queue:\n"
        "        n1, n2 = queue.popleft()  # next pair to compare\n"
        "        if n1 is None and n2 is None:\n"
        "            continue              # both null -> this pair OK\n"
        "        if n1 is None or n2 is None:\n"
        "            return False          # structural mismatch\n"
        "        if n1.val != n2.val:\n"
        "            return False          # value mismatch\n"
        "        # Enqueue child pairs for later comparison\n"
        "        queue.append((n1.left,  n2.left))\n"
        "        queue.append((n1.right, n2.right))\n"
        "    return True                   # all pairs verified\n"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("queue = deque([(p, q)])", {"code": True}),
                   (" — Initialize queue with the root pair. Each entry is a tuple of "
                    "two corresponding nodes.", {})])),
    N.para(N.rich([("n1, n2 = queue.popleft()", {"code": True}),
                   (" — Dequeue the next pair to compare. FIFO order = BFS = level by level.", {})])),
    N.para(N.rich([("if n1 is None and n2 is None: continue", {"code": True}),
                   (" — Both null: this pair is fine, skip it and continue processing queue.", {})])),
    N.para(N.rich([("queue.append((n1.left, n2.left))", {"code": True}),
                   (" — Enqueue left child pair for future comparison. Same for right.", {})])),
    N.para(N.rich([("return True", {"code": True}),
                   (" — Queue exhausted without finding any mismatch — all pairs verified.", {})])),
    N.divider(),
]

# ── Complexity table ──────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Recursive DFS (Interview Pick)", "O(n)", "O(h)", "h=height; O(log n) balanced, O(n) skewed"],
        ["Iterative BFS", "O(n)", "O(w)", "w=max width; up to O(n/2)=O(n) for complete tree"],
    ]),
    N.divider(),
]

# ── Pattern classification ────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Trees", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}),
                   ("Compare Root, Left, Right (Simultaneous Preorder DFS)", {})])),
    N.callout(
        "When to recognize this pattern:\n"
        "• 'Are these two trees identical / symmetric / mirrors?'\n"
        "• 'Does tree A contain tree B as a subtree?'\n"
        "• 'Merge / compare two trees node by node'\n"
        "• Any problem requiring parallel traversal of two tree structures",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related problems ──────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (simultaneous tree DFS):"),
    N.bullet(N.rich([("Symmetric Tree", {"bold": True}),
                     (" (Easy) — Mirror check: is tree symmetric around its center? (#101)", {})])),
    N.bullet(N.rich([("Subtree of Another Tree", {"bold": True}),
                     (" (Easy) — Run isSameTree at every node of the larger tree (#572)", {})])),
    N.bullet(N.rich([("Merge Two Binary Trees", {"bold": True}),
                     (" (Easy) — Simultaneous DFS, sum overlapping nodes instead of comparing (#617)", {})])),
    N.bullet(N.rich([("Flip Equivalent Binary Trees", {"bold": True}),
                     (" (Medium) — Same tree comparison but children may be swapped (#951)", {})])),
    N.bullet(N.rich([("Leaf-Similar Trees", {"bold": True}),
                     (" (Easy) — Check if leaf value sequences match between two trees (#872)", {})])),
    N.bullet(N.rich([("Count Good Nodes in Binary Tree", {"bold": True}),
                     (" (Medium) — Single-tree DFS tracking max value on root-to-node path (#1448)", {})])),
    N.para("These problems share the core technique: recursive/iterative simultaneous traversal "
           "of two tree structures, checking correspondence at each node pair."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Trees Section "
              "(DFS Preorder / Compare Root, Left, Right)", "📚", "gray_background"),
]

# ── Embed section ─────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("same_tree")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.",
                    {"italic": True, "color": "gray"})])),
]

# ── Append all blocks ─────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")

# ── Write status file ─────────────────────────────────────────────
import json
status_dir = "/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms/.status"
os.makedirs(status_dir, exist_ok=True)
html_path = "/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms/same_tree_explainer.html"
html_lines = sum(1 for _ in open(html_path))
status = {
    "slug": "same_tree",
    "notion_page_id": PAGE_ID,
    "html": "OK",
    "notion": "OK",
    "lines": html_lines,
    "notes": "Fresh page created. 13-step interactive DFS walkthrough. Recursive + iterative BFS solutions."
}
with open(f"{status_dir}/same_tree.json", "w") as f:
    json.dump(status, f, indent=2)
print(f"RESULT same_tree | html=OK | notion=OK | lines={html_lines}")
