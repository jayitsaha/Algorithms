"""
gen_minimum_distance_between_bst_nodes.py
Notion page creation for LeetCode #783 — Minimum Distance Between BST Nodes
notion_page_id: null → create fresh page
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

# ── Step 0: Page was already created in a prior attempt ──────────
PAGE_ID = "39293418-809c-81d2-81a6-f6733cd018fb"
print(f"Using existing page: {PAGE_ID}")

# ── Step 1: Set properties ────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=783,
    pattern="Trees",
    subpatterns=["In-order - Track Prev"],
    tc="O(n)",
    sc="O(h)",
    key_insight="In-order BST traversal is sorted; min diff is always between adjacent values in that sorted sequence.",
    icon="🟢"
)
print("Properties set.")

# ── Step 2: Build body blocks ─────────────────────────────────────
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given the root of a Binary Search Tree, return the minimum difference between the values of any two different nodes. The tree contains unique integer values. This is also LeetCode #530 (Minimum Absolute Difference in BST) — identical problem.\n\n"),
        ("Example 1: ", {"bold": True}),
        ("root = [4,2,6,1,3] → Output: 1  (adjacent sorted values 1,2,3,4,6 — minimum gap = 1)\n"),
        ("Example 2: ", {"bold": True}),
        ("root = [1,0,48,null,null,12,49] → Output: 1  (gap between 0 and 1)"),
    ])),
    N.divider(),
]

# Solution 1 — Recursive In-Order (Interview Pick)
blocks += [
    N.h2("Solution 1 — Recursive In-Order with Prev (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need the minimum absolute difference between any two node values. A naive approach checks all pairs — O(n²). Can we do better by exploiting the BST structure?"),
        N.h4("What Doesn't Work"),
        N.para("A generic DFS or BFS doesn't help — they visit nodes in tree order, not value order. Checking all node pairs is O(n²). Even sorting collected values costs O(n log n) and wastes the BST property."),
        N.h4("The Key Observation"),
        N.para("A BST's in-order traversal (Left → Root → Right) visits nodes in strictly ascending sorted order. The minimum gap between any two nodes must occur between adjacent values in this sorted sequence — because any non-adjacent gap is a sum of adjacent gaps and thus ≥ the smallest adjacent gap."),
        N.h4("Building the Solution"),
        N.para("Run an in-order traversal. At each node, compare its value with the previously visited node's value (prev). Compute diff = node.val − prev (always positive since sorted). Track the running minimum. Update prev = node.val. One pass through all n nodes: O(n) time, O(h) space."),
        N.callout("Analogy: Walking a sorted list left-to-right. The minimum step between any two elements is always between neighbors — you'd never find a smaller gap by skipping elements.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(
        "def minDiffInBST(root):\n"
        "    min_diff = float('inf')\n"
        "    prev = [None]  # mutable container for closure\n"
        "\n"
        "    def inorder(node):\n"
        "        nonlocal min_diff\n"
        "        if not node:\n"
        "            return\n"
        "        inorder(node.left)              # 1) go left (smaller values)\n"
        "        if prev[0] is not None:         # skip diff on first node\n"
        "            diff = node.val - prev[0]   # always positive (sorted)\n"
        "            min_diff = min(min_diff, diff)\n"
        "        prev[0] = node.val              # 2) record this node as previous\n"
        "        inorder(node.right)             # 3) go right (larger values)\n"
        "\n"
        "    inorder(root)\n"
        "    return min_diff\n"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("min_diff = float('inf')", {"code": True}), " — Sentinel meaning 'no minimum found yet'. Will be replaced on first comparison."])),
    N.para(N.rich([("prev = [None]", {"code": True}), " — Mutable list allows the nested inorder() to write to it without needing a global. prev[0] stores the last visited node's value."])),
    N.para(N.rich([("if not node: return", {"code": True}), " — Base case. A null node terminates this branch of recursion."])),
    N.para(N.rich([("inorder(node.left)", {"code": True}), " — Recurse left FIRST. In-order = Left→Root→Right. This ensures we reach smaller values before processing the current node."])),
    N.para(N.rich([("if prev[0] is not None:", {"code": True}), " — Skip the diff check for the very first node visited (the leftmost, smallest node). It has no predecessor."])),
    N.para(N.rich([("diff = node.val - prev[0]", {"code": True}), " — No abs() needed: in sorted order, node.val > prev[0] always. diff is always positive."])),
    N.para(N.rich([("min_diff = min(min_diff, diff)", {"code": True}), " — Update running minimum if this consecutive gap is smaller."])),
    N.para(N.rich([("prev[0] = node.val", {"code": True}), " — Record this node as the 'previous' for the next node we visit in sorted order."])),
    N.para(N.rich([("inorder(node.right)", {"code": True}), " — Recurse right after processing the current node. Right subtree has all larger values."])),
    N.divider(),
]

# Solution 2 — Iterative Stack
blocks += [
    N.h2("Solution 2 — Iterative In-Order with Explicit Stack"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same logic as the recursive approach — produce values in sorted in-order, compare adjacent pairs. But use an explicit stack instead of the call stack."),
        N.h4("What Doesn't Work"),
        N.para("For very deep/skewed BSTs (e.g., all nodes in a right-leaning chain), recursive in-order will hit Python's recursion limit (~1000 calls). The iterative version avoids this."),
        N.h4("The Key Observation"),
        N.para("The call stack in recursion is implicitly doing the same thing as an explicit stack: 'push this node, go left, come back, process node, go right.' We can replicate this loop structure explicitly."),
        N.h4("Building the Solution"),
        N.para("Use a while loop. At each iteration: (a) descend left as far as possible, pushing every node onto the stack. (b) Pop the top node — this is the next node in sorted order. (c) Compare with prev, update min_diff, set prev. (d) Move curr to the right child."),
        N.callout("This is the canonical iterative in-order traversal pattern. Memorize it — it appears across many BST problems.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(
        "def minDiffInBST(root):\n"
        "    stack, prev, min_diff = [], None, float('inf')\n"
        "    curr = root\n"
        "    while curr or stack:\n"
        "        while curr:                 # descend left as far as possible\n"
        "            stack.append(curr)\n"
        "            curr = curr.left\n"
        "        curr = stack.pop()          # process leftmost unvisited node\n"
        "        if prev is not None:\n"
        "            min_diff = min(min_diff, curr.val - prev)\n"
        "        prev = curr.val\n"
        "        curr = curr.right           # next: process right subtree\n"
        "    return min_diff\n"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("while curr or stack:", {"code": True}), " — Continue while there are nodes to descend into (curr) or nodes waiting to be processed (stack)."])),
    N.para(N.rich([("while curr:", {"code": True}), " — Push every node along the leftmost path. When curr becomes null, we've reached the smallest unprocessed node."])),
    N.para(N.rich([("curr = stack.pop()", {"code": True}), " — This is the next node in sorted order. Pop it and process: compare with prev, update min_diff."])),
    N.para(N.rich([("curr = curr.right", {"code": True}), " — After processing, move to the right subtree. The outer while loop will then descend left again from this new position."])),
    N.divider(),
]

# Complexity table
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Recursive In-Order + Prev", "O(n)", "O(h) — h=height, log n balanced, n skewed"],
        ["Iterative Stack In-Order", "O(n)", "O(h) — same, no recursion limit risk"],
        ["Brute Force (all pairs)", "O(n²)", "O(n)"],
    ]),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Trees (Section 11 — Tree Traversals)"])),
    N.para(N.rich([("Sub-Pattern: ", {"bold": True}), "In-order, Track Prev (Section 11.3 — In-Order Traversal, BST sorted sequence)"])),
    N.callout(
        "When to recognize this pattern:\n"
        "• Problem involves a BST and asks for a min/max property between node values\n"
        "• You need consecutive sorted values without storing all of them\n"
        "• Keywords: 'minimum difference', 'validate BST', 'k-th smallest' in a BST\n"
        "• BST structure can replace an explicit sort step",
        "🔎", "green_background"
    ),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same In-Order + Track Prev technique:"),
    N.bullet(N.rich([("Minimum Absolute Difference in BST", {"bold": True}), " (Easy, #530) — Identical problem, different name. Same exact solution."])),
    N.bullet(N.rich([("Validate Binary Search Tree", {"bold": True}), " (Medium, #98) — In-order, check each value is strictly greater than prev. Same prev-tracking pattern."])),
    N.bullet(N.rich([("Kth Smallest Element in a BST", {"bold": True}), " (Medium, #230) — In-order traversal, decrement counter K; return node.val when K reaches 0."])),
    N.bullet(N.rich([("Binary Search Tree Iterator", {"bold": True}), " (Medium, #173) — Controlled in-order with an explicit stack; yields next sorted value on demand."])),
    N.bullet(N.rich([("Two Sum IV - Input is a BST", {"bold": True}), " (Easy, #653) — In-order to sorted list, then two-pointer for pair summing to target."])),
    N.bullet(N.rich([("Find Mode in Binary Search Tree", {"bold": True}), " (Easy, #501) — In-order + track prev to find mode without extra hash map."])),
    N.bullet(N.rich([("Convert BST to Greater Tree", {"bold": True}), " (Medium, #538) — Reverse in-order (Right→Root→Left) with a running cumulative sum."])),
    N.para("These problems share the same core technique: exploit BST in-order = sorted order, carry a prev pointer, avoid storing all node values."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 11.3 — In-Order Traversal (Left-Root-Right)", "📚", "gray_background"),
]

# Embed
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("minimum_distance_between_bst_nodes")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Step 3: Append all blocks ─────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")

# ── Step 4: Write status file ─────────────────────────────────────
import json, pathlib
status_dir = pathlib.Path(__file__).parent / ".status"
status_dir.mkdir(exist_ok=True)
html_path = pathlib.Path(__file__).parent / "minimum_distance_between_bst_nodes_explainer.html"
html_lines = len(html_path.read_text().splitlines())
status = {
    "slug": "minimum_distance_between_bst_nodes",
    "html": "OK",
    "notion": "OK",
    "notion_page_id": PAGE_ID,
    "lines": html_lines,
    "notes": "Fresh page created. Recursive + iterative in-order solutions. 13-step interactive walkthrough with BST SVG visualization."
}
status_file = status_dir / "minimum_distance_between_bst_nodes.json"
status_file.write_text(json.dumps(status, indent=2))
print(f"RESULT minimum_distance_between_bst_nodes | html=OK | notion=OK | lines={html_lines}")
