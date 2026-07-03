"""
gen_check_completeness_of_a_binary_tree.py
Notion page generator for LeetCode #958 — Check Completeness of a Binary Tree
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

SLUG = "check_completeness_of_a_binary_tree"
NAME = "Check Completeness of a Binary Tree"
NUMBER = 958
DIFFICULTY = "Medium"
ICON = "🟡"
PATTERN = "Trees"
SUBPATTERNS = ["BFS: Level Order"]
TC = "O(n)"
SC = "O(n)"
KEY_INSIGHT = "BFS with null children enqueued; first null sets found_null flag; any real node after that flag is a violation"

# ── Step 0: Create or retrieve page ──────────────────────────
PAGE_ID = None  # null → create fresh
if PAGE_ID is None:
    print("Creating new Notion page...")
    PAGE_ID = N.create_page(NAME, NUMBER, DIFFICULTY, ICON)
    print(f"Created page: {PAGE_ID}")

# ── Step 1: Set properties ────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty=DIFFICULTY,
    number=NUMBER,
    pattern=PATTERN,
    subpatterns=SUBPATTERNS,
    tc=TC,
    sc=SC,
    key_insight=KEY_INSIGHT,
    icon=ICON,
)
print("Properties set.")

# ── Step 2: No wipe needed — fresh page ──────────────────────
# N.wipe_page(PAGE_ID) not needed since we just created it

# ── Step 3: Build body blocks ─────────────────────────────────
print("Building body blocks...")

SOLUTION_1_CODE = """\
from collections import deque

def isCompleteTree(root) -> bool:
    queue = deque([root])
    found_null = False
    while queue:
        curr = queue.popleft()
        if curr is None:
            found_null = True
        else:
            if found_null:
                return False
            queue.append(curr.left)
            queue.append(curr.right)
    return True\
"""

SOLUTION_2_CODE = """\
def isCompleteTree(root) -> bool:
    def count_nodes(node):
        if not node: return 0
        return 1 + count_nodes(node.left) + count_nodes(node.right)
    n = count_nodes(root)

    def check(node, idx):
        if not node: return True
        if idx > n: return False
        return check(node.left, 2*idx) and check(node.right, 2*idx+1)

    return check(root, 1)\
"""

blocks = []

# ── Problem ──────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        "Given the ", ("root", {"code": True}), " of a binary tree, determine if it is a complete binary tree. "
        "In a complete binary tree, every level is fully filled except possibly the last level, "
        "which is filled from left to right with no gaps."
    ])),
    N.divider(),
]

# ── Solution 1 ───────────────────────────────────────────────
blocks += [
    N.h2("Solution 1 — BFS with Null-Sentinel (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to verify that the tree has a specific shape: every level filled left to right with no internal gaps. "
               "The question becomes: is there any 'hole' in the tree when we read it level by level from left to right?"),
        N.h4("What Doesn't Work"),
        N.para("A naive DFS comparing left and right subtree heights at each node fails for asymmetric trees. "
               "Height comparison alone cannot detect gaps in the middle of a level — it only catches level-count mismatches."),
        N.h4("The Key Observation"),
        N.para("BFS visits nodes in the exact same order as the completeness definition: level by level, left to right. "
               "If we also enqueue null children (not just real ones), nulls appear in the queue at exactly the positions "
               "where the tree has empty slots. A real node appearing AFTER any null means there is a gap."),
        N.h4("Building the Solution"),
        N.para("Use a deque. Enqueue the root. While the queue is non-empty: dequeue curr. "
               "If curr is None, set found_null = True. "
               "If curr is a real node and found_null is True, return False (gap detected). "
               "Otherwise, enqueue curr.left and curr.right (both, unconditionally). "
               "If the loop completes with no violation, return True."),
        N.callout("Analogy: Imagine filling seats in a theater row by row, left to right. A complete binary tree is like a sold-out show where you can only have empty seats at the far-right end of the last row. BFS checks each 'seat' in order — the moment you see an empty seat followed by an occupied one, the theater (tree) is not complete.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(SOLUTION_1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("queue = deque([root])", {"code": True}), " — Initialize BFS queue with the root. Using deque for O(1) popleft."])),
    N.para(N.rich([("found_null = False", {"code": True}), " — Two-state flag. False = NORMAL mode, True = NULL_SEEN mode."])),
    N.para(N.rich([("curr = queue.popleft()", {"code": True}), " — Dequeue the front element. Critically, this may be None if a null slot was enqueued."])),
    N.para(N.rich([("if curr is None:", {"code": True}), " — Check if we dequeued an empty slot."])),
    N.para(N.rich([("found_null = True", {"code": True}), " — Mark that we have seen the first gap. From here, only more nulls are acceptable."])),
    N.para(N.rich([("if found_null: return False", {"code": True}), " — Real node encountered AFTER a null = gap in tree = not complete."])),
    N.para(N.rich([("queue.append(curr.left)", {"code": True}), " — Enqueue left child unconditionally. If None, that null slot goes into the queue in the correct position."])),
    N.para(N.rich([("queue.append(curr.right)", {"code": True}), " — Same for right child. This is what makes the sentinel work."])),
    N.para(N.rich([("return True", {"code": True}), " — No violation during the entire BFS. Tree is complete."])),
    N.divider(),
]

# ── Solution 2 ───────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Node Count + DFS Index Check"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("A complete binary tree maps perfectly to a 1-indexed array (heap representation): root at index 1, "
               "left child at 2i, right child at 2i+1. If the tree has n nodes and every node's index satisfies index ≤ n, "
               "there are no gaps — the tree is complete."),
        N.h4("What Doesn't Work"),
        N.para("This approach requires counting all nodes first (O(n) traversal), then a second O(n) DFS with index checks. "
               "Total is O(n) time but uses two passes."),
        N.h4("The Key Observation"),
        N.para("In a complete binary tree of n nodes, every node's 1-indexed position must be ≤ n. "
               "If any node has index > n, it means there is a gap somewhere before it — a slot at a smaller index is unfilled."),
        N.h4("Building the Solution"),
        N.para("Count all n nodes with a DFS. Then do a second DFS: at each node, pass its 1-indexed position. "
               "If position > n, return False. If null, return True. Recurse on both children with 2*idx and 2*idx+1."),
    ]),
    N.h3("Code"),
    N.code(SOLUTION_2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("count_nodes(node)", {"code": True}), " — Recursively count all nodes in the tree. This is O(n)."])),
    N.para(N.rich([("check(node, idx)", {"code": True}), " — DFS with the 1-indexed heap position of each node."])),
    N.para(N.rich([("if idx > n: return False", {"code": True}), " — Index beyond total count means this slot would be past all occupied positions — a gap exists."])),
    N.para(N.rich([("check(node.left, 2*idx)", {"code": True}), " — Left child in a heap array is at index 2*parent."])),
    N.para(N.rich([("check(node.right, 2*idx+1)", {"code": True}), " — Right child in a heap array is at index 2*parent+1."])),
    N.divider(),
]

# ── Complexity ───────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["BFS Null-Sentinel (Interview Pick)", "O(n)", "O(n) — queue width"],
        ["Node Count + DFS Index", "O(n)", "O(log n) — recursion stack"],
        ["Height-based Binary Search", "O(log²n)", "O(log n)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Trees"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "BFS: Level Order · Special constraint: No Node After Null"])),
    N.callout(
        "When to recognize this pattern: Problem involves validating the SHAPE of a binary tree. "
        "'Left-to-right fill' or 'level completeness' signals BFS level-order traversal. "
        "Null-sentinel trick applies whenever you need to detect gaps in level-order positions.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same BFS Level Order technique:"),
    N.bullet(N.rich([("Count Complete Tree Nodes", {"bold": True}), " (Medium) — Uses completeness property for O(log²n) node count (#222)"])),
    N.bullet(N.rich([("Binary Tree Level Order Traversal", {"bold": True}), " (Medium) — Standard BFS collecting per-level results (#102)"])),
    N.bullet(N.rich([("Binary Tree Right Side View", {"bold": True}), " (Medium) — BFS, take last node per level (#199)"])),
    N.bullet(N.rich([("Populating Next Right Pointers in Each Node", {"bold": True}), " (Medium) — BFS on complete binary tree specifically (#116)"])),
    N.bullet(N.rich([("Maximum Width of Binary Tree", {"bold": True}), " (Medium) — BFS with positional index tracking, same null-position idea (#662)"])),
    N.bullet(N.rich([("Average of Levels in Binary Tree", {"bold": True}), " (Easy) — BFS per level, compute mean (#637)"])),
    N.para("These problems all share BFS level-order traversal as the core technique, adapted for different per-level queries."),
]

# ── Embed ─────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([("Step through the BFS algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

# ── Append all blocks ─────────────────────────────────────────
print(f"Appending {len(blocks)} blocks to page {PAGE_ID}...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")

# Print the page ID so we can record it
print(f"PAGE_ID={PAGE_ID}")
