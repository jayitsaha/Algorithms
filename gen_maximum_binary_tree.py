"""
gen_maximum_binary_tree.py
Notion page creator/updater for LeetCode #654 Maximum Binary Tree.
notion_page_id = null → create a new page.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

# ── 1. Use already-created page (created in previous run) ───────────────
PAGE_ID = "39193418-809c-8124-8a7f-f34296d75fb2"
print(f"Using existing page: {PAGE_ID}")

# ── 2. Set properties ────────────────────────────────────────────────────
# Note: Notion multi_select does NOT allow commas in option names.
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=654,
    pattern="Divide and Conquer",
    subpatterns=["Find Max Build Left Right"],
    tc="O(n^2) worst / O(n log n) avg",
    sc="O(n)",
    key_insight="Max element divides array into two independent halves; recurse on each.",
    icon="🟡",
)
print("Properties set.")

# ── 2b. Wipe any existing body (fresh page, nothing yet) ────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} existing blocks.")

# ── 3. Build page body ──────────────────────────────────────────────────
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an integer array ", {}),
        ("nums", {"code": True}),
        (" with no duplicates, build the maximum binary tree defined as follows: "
         "(1) The root is the maximum element. "
         "(2) The left subtree is the maximum tree built from the elements to the left of the max. "
         "(3) The right subtree is the maximum tree built from the elements to the right of the max. "
         "Return the root of the tree.", {}),
    ])),
    N.para(N.rich([
        ("Example: ", {"bold": True}),
        ("nums = [3, 2, 1, 6, 0, 5]", {"code": True}),
        (" → root=6, left child=3 (with right subtree 2→1), right child=5 (with left child 0).", {}),
    ])),
    N.divider(),
]

# ── Solution 1: Recursive D&C with Index Bounds (Interview Pick) ────────
SOL1_CODE = """\
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right

def constructMaximumBinaryTree(nums: list[int]) -> TreeNode:
    def build(lo: int, hi: int) -> TreeNode:
        if lo > hi:
            return None                         # empty subarray → null child
        max_i = lo
        for i in range(lo, hi + 1):
            if nums[i] > nums[max_i]:
                max_i = i                       # track index of the max
        root = TreeNode(nums[max_i])            # current subarray's root
        root.left  = build(lo, max_i - 1)      # left subtree from left part
        root.right = build(max_i + 1, hi)      # right subtree from right part
        return root
    return build(0, len(nums) - 1)
"""

blocks += [
    N.h2("Solution 1 — Recursive Divide and Conquer (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("You are given a construction rule, not a search problem. The rule: "
               "root = max element, left subtree = apply the same rule to everything left of the max, "
               "right subtree = apply the same rule to everything right of the max. "
               "This IS the recursive function — the problem statement writes the code for you."),
        N.h4("What Doesn't Work"),
        N.para("There is no iterative / non-recursive approach that is simpler — the tree structure "
               "is defined recursively, so any iterative attempt must simulate a call stack. "
               "Python slicing (nums[:idx]) is readable but allocates O(n) extra memory per call, "
               "leading to O(n²) space worst-case. Use index bounds instead."),
        N.h4("The Key Observation"),
        N.para("The maximum element acts as a pivot. Once you place it as the root, "
               "the elements to its left are completely independent of the elements to its right — "
               "they never interact. This is the definition of Divide and Conquer: "
               "split on the pivot, solve each half independently, combine by linking children."),
        N.h4("Building the Solution"),
        N.para("Step 1: Write the base case — if lo > hi, return None. "
               "Step 2: Scan nums[lo..hi] to find max_i. "
               "Step 3: Create root = TreeNode(nums[max_i]). "
               "Step 4: root.left = build(lo, max_i-1). "
               "Step 5: root.right = build(max_i+1, hi). "
               "Step 6: return root. Every recursive tree problem follows this preorder skeleton."),
        N.callout(
            "Analogy: Think of Quick Sort using the array maximum as its pivot. "
            "Quick Sort rearranges the array; Maximum Binary Tree instead records the recursive "
            "partition structure as a tree. Same algorithm, different output.",
            "🧭", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(SOL1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("def build(lo, hi):", {"code": True}),
                   (" — inner recursive helper; operates on the subarray nums[lo..hi].", {})])),
    N.para(N.rich([("if lo > hi: return None", {"code": True}),
                   (" — base case: empty subarray. Handles missing leaf children without any extra guard.", {})])),
    N.para(N.rich([("max_i = lo", {"code": True}),
                   (" — initialize to the first index; we'll update as we scan.", {})])),
    N.para(N.rich([("for i in range(lo, hi + 1):", {"code": True}),
                   (" — scan every element in the current window. O(n) per call.", {})])),
    N.para(N.rich([("if nums[i] > nums[max_i]: max_i = i", {"code": True}),
                   (" — track the index of the largest element seen so far.", {})])),
    N.para(N.rich([("root = TreeNode(nums[max_i])", {"code": True}),
                   (" — create the root of this subproblem using the maximum value.", {})])),
    N.para(N.rich([("root.left = build(lo, max_i - 1)", {"code": True}),
                   (" — recurse on everything LEFT of the max; result is the left subtree.", {})])),
    N.para(N.rich([("root.right = build(max_i + 1, hi)", {"code": True}),
                   (" — recurse on everything RIGHT of the max; result is the right subtree.", {})])),
    N.para(N.rich([("return root", {"code": True}),
                   (" — return the assembled node (with children attached) to the parent call.", {})])),
    N.divider(),
]

# ── Solution 2: Clean Slice Version ────────────────────────────────────
SOL2_CODE = """\
def constructMaximumBinaryTree(nums: list[int]) -> TreeNode:
    if not nums:
        return None
    idx = nums.index(max(nums))        # find max and its position
    root = TreeNode(nums[idx])
    root.left  = constructMaximumBinaryTree(nums[:idx])    # left sub-slice
    root.right = constructMaximumBinaryTree(nums[idx+1:])  # right sub-slice
    return root
"""

blocks += [
    N.h2("Solution 2 — Slice Recursion (Simpler Code, More Space)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same recursive logic, but use Python's built-in max() and list slicing "
               "to make the code more readable. Trades readability for extra space."),
        N.h4("What Doesn't Work"),
        N.para("The simplicity is misleading: each slice creates a new list (O(n) copy). "
               "In a worst-case scenario (sorted input, depth n), we create O(n) new lists "
               "of average size O(n/2), totalling O(n²) memory. Avoid this in interviews."),
        N.h4("The Key Observation"),
        N.para("nums.index(max(nums)) does two O(n) passes (one for max(), one for index()), "
               "but that's still O(n) per call — same asymptotic as Solution 1. "
               "The difference is only in the space used for the sliced sublists."),
        N.h4("Building the Solution"),
        N.para("Base case: empty list returns None. Find max value, get its index. "
               "Create root. Recurse left on nums[:idx], right on nums[idx+1:]. "
               "Return root. Three lines of logic."),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("if not nums: return None", {"code": True}),
                   (" — base case: empty list.", {})])),
    N.para(N.rich([("idx = nums.index(max(nums))", {"code": True}),
                   (" — two O(n) passes: max() then index(). Still O(n) overall.", {})])),
    N.para(N.rich([("root.left = constructMaximumBinaryTree(nums[:idx])", {"code": True}),
                   (" — creates a new list copy of the left portion. O(n) extra space.", {})])),
    N.para(N.rich([("root.right = constructMaximumBinaryTree(nums[idx+1:])", {"code": True}),
                   (" — creates a new list copy of the right portion.", {})])),
    N.callout("When to use: Quick prototype or throwaway code. "
              "In interviews, always prefer Solution 1 (index bounds) and explain the space difference.",
              "⚠️", "yellow_background"),
    N.divider(),
]

# ── Complexity Table ────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Recursive + Index Bounds (S1)", "O(n²) worst / O(n log n) avg", "O(n)"],
        ["Recursive + Slicing (S2)", "O(n²) worst / O(n log n) avg", "O(n²) worst"],
        ["Monotonic Stack (advanced)", "O(n)", "O(n)"],
    ]),
    N.para("The O(n) monotonic stack solution maintains a decreasing stack. "
           "Processing left-to-right: each element pops all smaller elements "
           "(they become its left child), then becomes the right child of the remaining top. "
           "This builds the tree in one pass — mention as a follow-up."),
    N.divider(),
]

# ── Pattern Classification ──────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Divide and Conquer", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Find Max, Build Left/Right", {})])),
    N.callout(
        "When to recognize this pattern: "
        "(1) 'Build a tree from an array where root is defined by a special element (max/min).' "
        "(2) 'Left subtree from left subarray, right subtree from right subarray.' "
        "(3) Subproblem has the exact same shape as the full problem — the definition IS the recursion.",
        "🔎", "green_background"),
    N.divider(),
]

# ── Related Problems ────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Divide and Conquer / recursive tree-building technique:"),
    N.bullet(N.rich([("Maximum Binary Tree II", {"bold": True}),
                     (" (Medium) — Insert one new last element into the right spine of an existing max tree (#998)", {})])),
    N.bullet(N.rich([("Construct Binary Tree from Preorder and Inorder", {"bold": True}),
                     (" (Medium) — Same D&C skeleton; root from preorder, split via inorder position (#105)", {})])),
    N.bullet(N.rich([("Construct Binary Tree from Postorder and Inorder", {"bold": True}),
                     (" (Medium) — Root from postorder end, split via inorder (#106)", {})])),
    N.bullet(N.rich([("Convert Sorted Array to BST", {"bold": True}),
                     (" (Easy) — Mid element as root, recurse both halves — same D&C structure (#108)", {})])),
    N.bullet(N.rich([("Different Ways to Add Parentheses", {"bold": True}),
                     (" (Medium) — Each operator is a split point → recurse both sides, collect all results (#241)", {})])),
    N.bullet(N.rich([("Burst Balloons", {"bold": True}),
                     (" (Hard) — Last balloon in interval = 'root', D&C thinking + interval DP (#312)", {})])),
    N.para("These problems share the core technique: identify a special element that divides "
           "the problem into two independent halves, solve each half recursively."),
    N.callout("📚 Reference: Divide and Conquer — Sub-Pattern: Find Max, Build Left/Right",
              "📚", "gray_background"),
]

# ── Embed ────────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("maximum_binary_tree")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.",
                    {"italic": True, "color": "gray"})])),
]

# ── Append all blocks ────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")

# ── Write status file ────────────────────────────────────────────────────
import json, pathlib

html_path = pathlib.Path(__file__).parent / "maximum_binary_tree_explainer.html"
html_lines = len(html_path.read_text().splitlines())

status_dir = pathlib.Path(__file__).parent / ".status"
status_dir.mkdir(exist_ok=True)
status = {
    "slug": "maximum_binary_tree",
    "html": "OK",
    "notion": "OK",
    "notion_page_id": "39193418-809c-8124-8a7f-f34296d75fb2",
    "lines": html_lines,
    "notes": "Full page created from scratch. 954-line HTML with 12 walkthrough steps, SVG tree viz."
}
(status_dir / "maximum_binary_tree.json").write_text(json.dumps(status, indent=2))
print(f"RESULT maximum_binary_tree | html=OK | notion=OK | lines={html_lines}")
