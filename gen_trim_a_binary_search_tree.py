"""
gen_trim_a_binary_search_tree.py
Regenerate Notion page for LeetCode #669 — Trim a Binary Search Tree
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-812d-a168-fa77f1a841c6"
SLUG    = "trim_a_binary_search_tree"

# ── 1. Properties ──────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=669,
    pattern="Trees",
    subpatterns=["Recursive Trim"],
    tc="O(n)",
    sc="O(h)",
    key_insight="If node.val < low, recurse right only; if > high, recurse left only; else keep and recurse both.",
    icon="🟡",
)
print("Properties set.")

# ── 2. Wipe old body ────────────────────────────────────────────────
deleted = N.wipe_page(PAGE_ID)
print(f"Wiped {deleted} blocks.")

# ── 3. Build body ───────────────────────────────────────────────────
blocks = []

# ── Problem statement ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given the ", {}),
        ("root", {"code": True}),
        (" of a binary search tree and two integers ", {}),
        ("low", {"code": True}),
        (" and ", {}),
        ("high", {"code": True}),
        (", trim the tree so that all node values fall within [low, high]. "
         "Return the root of the trimmed tree. The result must still be a valid BST.", {}),
    ])),
    N.divider(),
]

# ══════════════════════════════════════════════════════════
# SOLUTION 1 — Recursive Trim (Interview Pick)
# ══════════════════════════════════════════════════════════
blocks += [
    N.h2("Solution 1 — Recursive Trim (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Remove every node with a value outside [low, high] and return the new BST root. "
            "The tree must remain structurally valid — no new nodes, just pointer rewiring."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "A naive approach might simply return None for out-of-range nodes. "
            "But that discards valid nodes hiding in the 'inward' subtree of an out-of-range node. "
            "If a node with value 0 is below low=1, its right child (value 2) might be perfectly valid — "
            "we must salvage it, not throw it away."
        ),
        N.h4("The Key Observation"),
        N.para(
            "The BST ordering property tells us exactly which subtree to salvage when a node is out of range: "
            "if node.val < low, the node and its entire left subtree are all too small (BST guarantees this), "
            "but the right subtree could have values >= low. "
            "If node.val > high, the node and its entire right subtree are all too large, "
            "but the left subtree might still have values <= high. "
            "This turns a complex pruning problem into a clean 3-way decision at every node."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. Base case: node is None → return None.\n"
            "2. Too small (val < low): return trim(node.right) — skip node and left, salvage right.\n"
            "3. Too large (val > high): return trim(node.left) — skip node and right, salvage left.\n"
            "4. In range: keep node, set node.left = trim(node.left), node.right = trim(node.right), return node.\n"
            "The function always returns the correct new root for that subtree."
        ),
        N.callout(
            "Analogy: You're pruning a hedge. If a branch is too far left (< low), "
            "you don't cut from the trunk — you climb the branch and check what grows off its right side first. "
            "Maybe something valid lives there.",
            "🌿", "green_background"
        ),
    ]),

    N.h3("Code"),
    N.code(
        "def trimBST(root, low, high):\n"
        "    if not root:\n"
        "        return None\n"
        "    if root.val < low:\n"
        "        return trimBST(root.right, low, high)\n"
        "    if root.val > high:\n"
        "        return trimBST(root.left, low, high)\n"
        "    root.left  = trimBST(root.left, low, high)\n"
        "    root.right = trimBST(root.right, low, high)\n"
        "    return root"
    ),

    N.h3("Line by Line"),
    N.para(N.rich([("if not root: return None", {"code": True}),
                   (" — Base case. A null node has nothing to trim; return null upward.", {})])),
    N.para(N.rich([("if root.val < low:", {"code": True}),
                   (" — Value is below range. By BST property, root.left.val ≤ root.val < low, "
                    "so the entire left subtree is also invalid. Skip this node entirely.", {})])),
    N.para(N.rich([("return trimBST(root.right, low, high)", {"code": True}),
                   (" — Salvage: recurse into the right subtree. "
                    "It starts with values > root.val and could contain values ≥ low.", {})])),
    N.para(N.rich([("if root.val > high:", {"code": True}),
                   (" — Symmetric case. root.right.val ≥ root.val > high, so entire right is invalid.", {})])),
    N.para(N.rich([("return trimBST(root.left, low, high)", {"code": True}),
                   (" — Salvage: recurse into the left subtree for values ≤ high.", {})])),
    N.para(N.rich([("root.left = trimBST(root.left, low, high)", {"code": True}),
                   (" — Node is in range; keep it. Rewire left pointer to the trimmed left subtree.", {})])),
    N.para(N.rich([("root.right = trimBST(root.right, low, high)", {"code": True}),
                   (" — Rewire right pointer to the trimmed right subtree.", {})])),
    N.para(N.rich([("return root", {"code": True}),
                   (" — Return this node as the new root of the trimmed subtree.", {})])),

    N.divider(),
]

# ══════════════════════════════════════════════════════════
# SOLUTION 2 — Iterative (O(1) space)
# ══════════════════════════════════════════════════════════
blocks += [
    N.h2("Solution 2 — Iterative Trim (O(1) Space)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Same goal — trim the BST to range [low, high] — but without using the recursion call stack. "
            "Useful when the tree could be deeply skewed (O(n) stack frames in worst case)."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "A single traversal loop can't easily handle all three cases simultaneously "
            "because we need to find the new root first before we can trim the subtrees."
        ),
        N.h4("The Key Observation"),
        N.para(
            "We can split the problem into 3 phases:\n"
            "Phase 1: Walk the root downward to find the first valid root (one where low ≤ val ≤ high).\n"
            "Phase 2: For the left spine — walk left children and bypass any child with val < low "
            "(promote its right child). Since the right child of a too-small node is closer to low, "
            "this single-direction bypass is safe.\n"
            "Phase 3: Same for right spine — bypass any right child with val > high (promote its left child)."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Each phase is a simple while loop. The key insight is that after finding a valid root, "
            "any invalid left child can only be too small (never too large — BST guarantees left < root ≤ high), "
            "and any invalid right child can only be too large (never too small)."
        ),
        N.callout(
            "The recursive version is cleaner for interviews. Choose iterative only when "
            "stack depth is explicitly a concern (very deep skewed trees).",
            "⚠️", "yellow_background"
        ),
    ]),

    N.h3("Code"),
    N.code(
        "def trimBST(root, low, high):\n"
        "    # Phase 1: find the first valid root\n"
        "    while root and (root.val < low or root.val > high):\n"
        "        root = root.right if root.val < low else root.left\n"
        "    if not root:\n"
        "        return None\n"
        "    # Phase 2: trim left subtree (remove nodes < low)\n"
        "    node = root\n"
        "    while node:\n"
        "        while node.left and node.left.val < low:\n"
        "            node.left = node.left.right\n"
        "        node = node.left\n"
        "    # Phase 3: trim right subtree (remove nodes > high)\n"
        "    node = root\n"
        "    while node:\n"
        "        while node.right and node.right.val > high:\n"
        "            node.right = node.right.left\n"
        "        node = node.right\n"
        "    return root"
    ),

    N.h3("Line by Line"),
    N.para(N.rich([("while root and (root.val < low or root.val > high):", {"code": True}),
                   (" — Walk the root downward, skipping out-of-range roots until we land on a valid one.", {})])),
    N.para(N.rich([("root = root.right if root.val < low else root.left", {"code": True}),
                   (" — Too small → move right (towards larger values); too large → move left.", {})])),
    N.para(N.rich([("while node.left and node.left.val < low:", {"code": True}),
                   (" — Phase 2 inner loop: if the left child is too small, bypass it by promoting its right child.", {})])),
    N.para(N.rich([("node.left = node.left.right", {"code": True}),
                   (" — The too-small left child is skipped. Its right subtree (closer to low) takes its place.", {})])),
    N.para(N.rich([("node = node.left", {"code": True}),
                   (" — Move deeper left to continue trimming the left spine.", {})])),
    N.para(N.rich([("Phases 3 is symmetric:", {"bold": True}),
                   (" walk right spine, bypass right children with val > high by promoting their left child.", {})])),

    N.divider(),
]

# ── Complexity table ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Recursive Trim (Interview Pick)", "O(n)", "O(h)"],
        ["Iterative Trim", "O(n)", "O(1)"],
    ]),
    N.para("h = tree height. O(log n) for balanced BST, O(n) for skewed."),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Trees", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}),
                   ("Recursive Trim (BST structural modification using ordering property)", {})])),
    N.callout(
        "When to recognize this pattern: "
        "'Filter/remove nodes from a BST based on a value condition' | "
        "'Preserve BST structure after pruning' | "
        "BST ordering lets you skip entire subtrees (not just individual nodes) | "
        "'Return the new root of a modified BST'",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (BST Property + Recursive Structure):"),
    N.bullet(N.rich([("Delete Node in a BST", {"bold": True}),
                     (" (Medium) — Remove a specific value; rewire to successor/predecessor. (#450)", {})])),
    N.bullet(N.rich([("Search in a Binary Search Tree", {"bold": True}),
                     (" (Easy) — Return subtree rooted at target; uses BST left/right navigation. (#700)", {})])),
    N.bullet(N.rich([("Validate Binary Search Tree", {"bold": True}),
                     (" (Medium) — Propagate min/max bounds downward; same invariant-passing pattern. (#98)", {})])),
    N.bullet(N.rich([("Kth Smallest Element in a BST", {"bold": True}),
                     (" (Medium) — Inorder traversal extracts sorted order; exploits BST property. (#230)", {})])),
    N.bullet(N.rich([("Range Sum of BST", {"bold": True}),
                     (" (Easy) — Prune recursion based on range; sum nodes in [low, high] only. (#938)", {})])),
    N.bullet(N.rich([("Convert BST to Greater Tree", {"bold": True}),
                     (" (Medium) — Reverse inorder accumulates suffix sums; structural BST manipulation. (#538)", {})])),
    N.bullet(N.rich([("Recover Binary Search Tree", {"bold": True}),
                     (" (Medium) — Find two swapped nodes via inorder traversal; restore BST invariant. (#99)", {})])),
    N.para("These problems all leverage the BST ordering invariant to guide traversal or skip subtrees."),
    N.callout(
        "📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Trees section → BST Property + DFS.\n"
        "Sub-Pattern: Recursive Trim — verified via analysis (problem-specific BST structural modification).",
        "📚", "blue_background"
    ),
]

# ── Interactive Visual Explainer ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ──
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
