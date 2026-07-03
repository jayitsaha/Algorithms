"""
gen_two_sum_iv__input_is_a_bst.py
Regenerates the Notion page for LeetCode #653 Two Sum IV - Input is a BST.
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-815c-9817-fd4a2abc5b4f"
SLUG = "two_sum_iv__input_is_a_bst"

# ── 1) Properties ──
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=653,
    pattern="Trees",
    subpatterns=["In-order + Two Pointers"],
    tc="O(n)",
    sc="O(n)",
    key_insight="BST in-order traversal yields a sorted array; then classic two-pointer Two Sum solves in O(n).",
    icon="🟢"
)
print("Properties set.")

# ── 2) Wipe old body ──
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3) Build body ──
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given the "), ("root", {"code": True}),
        (" of a Binary Search Tree and an integer "), ("k", {"code": True}),
        (", return "), ("True", {"code": True}),
        (" if there exist two elements in the BST such that their sum equals "),
        ("k", {"code": True}), ("."),
        (" The two elements must be distinct (different nodes). "
         "Example: BST with values [2,3,4,6,7], k=9 → True (2+7=9). "
         "BST with same values, k=28 → False (max sum=13).")
    ])),
    N.divider(),
]

# ── Solution 1: In-Order + Two Pointers ──
blocks += [
    N.h2("Solution 1 — In-Order Traversal + Two Pointers (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("This is the Two Sum problem disguised as a tree question. We need two distinct node values that add up to k. The question is: can we exploit the BST's sorted structure?"),
        N.h4("What Doesn't Work"),
        N.para("Brute force: for every node u, search the tree for a node v where u.val + v.val = k. That's O(n²) — too slow. A hash set works in O(n) but doesn't demonstrate any BST knowledge."),
        N.h4("The Key Observation"),
        N.para("A BST visited in in-order (left → root → right) always yields values in strictly ascending sorted order. This is the fundamental BST property. And once you have a sorted sequence, Two Sum is solvable in O(n) with two pointers from both ends."),
        N.h4("Building the Solution"),
        N.para("Step 1: in-order DFS to collect all node values into list nums (O(n)). "
               "Step 2: set L=0, R=len-1. While L < R: compute s=nums[L]+nums[R]. "
               "If s==k return True; if s<k move L right (need bigger); if s>k move R left (need smaller). "
               "Return False if pointers cross."),
        N.callout("Analogy: Imagine BST values printed on sorted cards, face-down. In-order traversal flips them left-to-right in order. Then you slide two fingers in from both ends until they find a pair or meet.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(
        "def findTarget(root, k):\n"
        "    nums = []\n"
        "    def inorder(node):\n"
        "        if not node: return\n"
        "        inorder(node.left)\n"
        "        nums.append(node.val)\n"
        "        inorder(node.right)\n"
        "    inorder(root)\n"
        "    L, R = 0, len(nums) - 1\n"
        "    while L < R:\n"
        "        s = nums[L] + nums[R]\n"
        "        if s == k: return True\n"
        "        elif s < k: L += 1\n"
        "        else: R -= 1\n"
        "    return False"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("nums = []", {"code": True}), " — Initialize empty list; will hold BST values in sorted order after traversal."])),
    N.para(N.rich([("def inorder(node):", {"code": True}), " — Inner recursive helper: performs left → node → right DFS."])),
    N.para(N.rich([("if not node: return", {"code": True}), " — Base case: null node (leaf's child) — stop recursing."])),
    N.para(N.rich([("inorder(node.left)", {"code": True}), " — Visit all smaller values first (left subtree) before current node."])),
    N.para(N.rich([("nums.append(node.val)", {"code": True}), " — Append current node after its entire left subtree — guarantees sorted position."])),
    N.para(N.rich([("inorder(node.right)", {"code": True}), " — Visit all larger values after current node (right subtree)."])),
    N.para(N.rich([("inorder(root)", {"code": True}), " — Execute traversal; after this, nums is a sorted array of all BST values."])),
    N.para(N.rich([("L, R = 0, len(nums) - 1", {"code": True}), " — Two pointers: L at smallest (index 0), R at largest (last index)."])),
    N.para(N.rich([("while L < R:", {"code": True}), " — Continue while pointers are at different positions (never use same element twice)."])),
    N.para(N.rich([("s = nums[L] + nums[R]", {"code": True}), " — Compute the current candidate pair sum."])),
    N.para(N.rich([("if s == k: return True", {"code": True}), " — Found the pair! Return immediately."])),
    N.para(N.rich([("elif s < k: L += 1", {"code": True}), " — Sum too small: advance L right to get a bigger left value."])),
    N.para(N.rich([("else: R -= 1", {"code": True}), " — Sum too big: move R left to get a smaller right value."])),
    N.para(N.rich([("return False", {"code": True}), " — Pointers crossed, all pairs exhausted — no valid pair exists."])),
    N.divider(),
]

# ── Solution 2: Hash Set DFS ──
blocks += [
    N.h2("Solution 2 — Hash Set DFS"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("For each node value v, we need to know if k-v exists somewhere else in the tree. If we've already visited the complement, we have our answer."),
        N.h4("What Doesn't Work"),
        N.para("Checking for the complement by re-traversing the tree from root every time costs O(n) per node = O(n²) total. We need O(1) lookup."),
        N.h4("The Key Observation"),
        N.para("A hash set gives O(1) membership check. As we DFS, before inserting a value, check if its complement is already in the set. If yes — those two nodes form the answer pair."),
        N.h4("Building the Solution"),
        N.para("DFS (any order). At each node with value v: if k-v is in seen → return True; else add v to seen, recurse left AND right. Return left OR right result."),
        N.callout("This approach works on ANY binary tree, not just a BST. The in-order approach is BST-specific.", "💡", "green_background"),
    ]),
    N.h3("Code"),
    N.code(
        "def findTarget(root, k):\n"
        "    seen = set()\n"
        "    def dfs(node):\n"
        "        if not node: return False\n"
        "        if k - node.val in seen:\n"
        "            return True\n"
        "        seen.add(node.val)\n"
        "        return dfs(node.left) or dfs(node.right)\n"
        "    return dfs(root)"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("seen = set()", {"code": True}), " — Hash set storing all node values visited so far."])),
    N.para(N.rich([("if not node: return False", {"code": True}), " — Null node: no values here, return False."])),
    N.para(N.rich([("if k - node.val in seen:", {"code": True}), " — Check if complement was previously visited (O(1) lookup)."])),
    N.para(N.rich([("seen.add(node.val)", {"code": True}), " — Record this value before recursing to children."])),
    N.para(N.rich([("return dfs(node.left) or dfs(node.right)", {"code": True}), " — Short-circuit: if left subtree finds pair, don't search right."])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (nested DFS)", "O(n²)", "O(h)"],
        ["Hash Set DFS", "O(n)", "O(n)"],
        ["In-Order + Two Pointers (Optimal)", "O(n)", "O(n)"],
        ["BST Iterator Approach (Advanced)", "O(n)", "O(h)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Trees"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "In-order + Two Pointers; also BST Property / DFS: Inorder"])),
    N.callout(
        "When to recognize this pattern: "
        "Problem involves 'Two Sum' on a BST → in-order traversal converts BST to sorted array; "
        "then two-pointer scan finds the pair in O(n). "
        "More generally: any BST operation that would be easy on a sorted array → consider in-order as bridge.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (In-order traversal + Two Pointers / BST):"),
    N.bullet(N.rich([("Two Sum", {"bold": True}), " (Easy) — Classic hash set or sort + two pointers on array (#1)"])),
    N.bullet(N.rich([("Two Sum II - Input Array Is Sorted", {"bold": True}), " (Medium) — Direct two-pointer scan; the exact inner loop of this problem (#167)"])),
    N.bullet(N.rich([("Kth Smallest Element in a BST", {"bold": True}), " (Medium) — In-order traversal, count to k-th element (#230)"])),
    N.bullet(N.rich([("Validate Binary Search Tree", {"bold": True}), " (Medium) — In-order must yield strictly increasing sequence (#98)"])),
    N.bullet(N.rich([("Minimum Absolute Difference in BST", {"bold": True}), " (Easy) — In-order to compare adjacent sorted pairs (#530)"])),
    N.bullet(N.rich([("3Sum", {"bold": True}), " (Medium) — Sort + two pointers extended to triplets; natural follow-up (#15)"])),
    N.bullet(N.rich([("Find Mode in BST", {"bold": True}), " (Easy) — In-order traversal to track most frequent element (#501)"])),
    N.para("These problems share the core technique: exploit BST sorted order via in-order traversal, then apply array-based algorithms."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Trees section (DFS: Inorder, BST Property)", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})]))
]

# ── Append ──
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
