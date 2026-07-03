"""
gen_unique_binary_search_trees_ii.py
Rebuild the Notion page for LeetCode #95 — Unique Binary Search Trees II
Pattern: Dynamic Programming / Generate Trees Recursively
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notion_lib as N

PAGE_ID = "39193418-809c-814f-b381-ed88c21dd62e"

# ── 1) Properties ──────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=95,
    pattern="Dynamic Programming",
    subpatterns=["Generate Trees Recursively"],
    tc="O(n^2 * C(n))",
    sc="O(n * C(n))",
    key_insight="For each root r in [lo,hi], BST property forces left=generate(lo,r-1) and right=generate(r+1,hi); memoize on (lo,hi) to avoid recomputing identical subranges.",
    icon="🟡",
)
print("Properties set.")

# ── 2) Wipe old body ───────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3) Build new body ──────────────────────────────────────────────────────
blocks = []

# ── PROBLEM ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an integer ", {}),
        ("n", {"code": True}),
        (", return all structurally unique BSTs (binary search trees) which have exactly ", {}),
        ("n", {"code": True}),
        (" nodes with values ", {}),
        ("1", {"code": True}),
        (" to ", {}),
        ("n", {"code": True}),
        (". Return the answer in any order.", {}),
    ])),
    N.para(N.rich([
        ("Example: ", {"bold": True}),
        ("n = 3", {"code": True}),
        (" -> 5 unique BSTs. Catalan(3) = 5.", {}),
    ])),
    N.callout(
        N.rich([
            ("Constraints: ", {"bold": True}),
            ("1 <= n <= 8. Output can be large: C(8) = 1430 distinct trees.", {}),
        ]),
        "📌", "gray_background"
    ),
    N.divider(),
]

# ── SOLUTION 1 — Recursion with Memoization ────────────────────────────────
sol1_code = """\
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def generateTrees(n: int):
    memo = {}                               # Cache: (lo, hi) -> list[TreeNode]

    def generate(lo, hi):
        if (lo, hi) in memo:               # Already solved this subrange
            return memo[(lo, hi)]
        if lo > hi:                         # Empty range: one option -- "no node"
            return [None]                  # [None], NOT [] (see warning below)

        trees = []
        for root_val in range(lo, hi + 1): # Try each value as the root
            lefts  = generate(lo, root_val - 1)   # All BSTs for left subtree
            rights = generate(root_val + 1, hi)    # All BSTs for right subtree
            for L in lefts:                        # Cartesian product
                for R in rights:
                    node = TreeNode(root_val, L, R)
                    trees.append(node)

        memo[(lo, hi)] = trees             # Cache before returning
        return trees

    return generate(1, n)
"""

blocks += [
    N.h2("Solution 1 -- Recursion with Memoization (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We need every valid arrangement of nodes 1..n into a BST. "
            "A BST is defined recursively: a root divides remaining values into "
            "a left group (smaller) and right group (larger). So this problem "
            "is inherently recursive -- pick a root, recurse on each side, combine results."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Brute-force: generate all permutations and insert each into a BST. "
            "That is O(n! * n) work and produces duplicate structures (many permutations "
            "yield the same tree shape). We would waste enormous effort deduplicating."
        ),
        N.h4("The Key Observation"),
        N.para(
            "For a BST with values lo..hi and root r: the BST property forces "
            "the left subtree to contain exactly {lo..r-1} and the right subtree "
            "to contain exactly {r+1..hi}. No choice needed -- the constraint partitions "
            "for free. So: generate(lo, hi) = union over all roots r of "
            "{ TreeNode(r, L, R) for L in generate(lo, r-1) for R in generate(r+1, hi) }."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Step 1: Define generate(lo, hi) returning all BSTs using values lo..hi.\n"
            "Step 2: Base case -- lo > hi means empty subtree. Return [None] (not [] -- see warning).\n"
            "Step 3: For each root r in lo..hi, get all left trees and all right trees.\n"
            "Step 4: Cartesian product: every (L, R) pair forms one valid BST.\n"
            "Step 5: Notice generate(2, 4) may be called multiple times for different roots. "
            "Add memo = {} keyed on (lo, hi) to cache results -- this is the memoization step."
        ),
        N.callout(
            "Analogy: Building all LEGO car configurations. Pick any tire as the 'center axle' (root). "
            "The left compartment can hold only smaller parts (left subtree), right only larger. "
            "Build all left configs, all right configs, then combine every pairing.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Algorithm Deep-Dive: Recursive Enumeration with Memoization"),
    N.para(
        "This problem uses Divide and Conquer with Memoization (top-down DP). "
        "It is not a 'counting' DP -- we must build actual tree nodes, so time is bounded by output size."
    ),
    N.para(
        "Core invariant: generate(lo, hi) returns the complete, correct list of all distinct BSTs "
        "whose node values are exactly the integers lo, lo+1, ..., hi. This invariant holds for any "
        "subrange, which is why memoization on (lo, hi) is valid -- the result depends only on the range, "
        "not on which larger problem triggered the call."
    ),
    N.para(
        "Why memoization works: Because 1..n are consecutive integers, the range [lo, hi] uniquely "
        "identifies the set of values. The same range [2, 4] produces identical BSTs whether called "
        "from root=1 or root=5. This is the 'overlapping subproblems' property that makes DP applicable."
    ),
    N.para(
        "Catalan connection: The number of distinct BSTs on n nodes equals the nth Catalan number "
        "C(n) = C(2n,n)/(n+1). C(1)=1, C(2)=2, C(3)=5, C(4)=14, C(5)=42. "
        "This grows exponentially, so time complexity is O(n^2 * C(n)) -- unavoidable for enumeration."
    ),
    N.h3("Code"),
    N.code(sol1_code),
    N.h3("Line by Line"),
    N.para(N.rich([("memo = {}", {"code": True}), " -- Initialize the memoization cache. Keys are (lo, hi) tuples; values are lists of TreeNode roots."])),
    N.para(N.rich([("def generate(lo, hi)", {"code": True}), " -- Inner recursive function. Returns all valid BSTs using integers lo through hi."])),
    N.para(N.rich([("if (lo, hi) in memo", {"code": True}), " -- Cache hit: we already computed this subrange. Return immediately (O(1) lookup)."])),
    N.para(N.rich([("if lo > hi: return [None]", {"code": True}), " -- Base case: empty range. Return [None] (one option: no node). Crucial for Cartesian product to work correctly."])),
    N.para(N.rich([("for root_val in range(lo, hi+1)", {"code": True}), " -- Try each integer as the root. BST property will handle partitioning automatically."])),
    N.para(N.rich([("lefts = generate(lo, root_val - 1)", {"code": True}), " -- Recursively get all BSTs for values to the left of root (all must be < root_val by BST property)."])),
    N.para(N.rich([("rights = generate(root_val + 1, hi)", {"code": True}), " -- Recursively get all BSTs for values to the right of root (all > root_val)."])),
    N.para(N.rich([("for L in lefts: for R in rights:", {"code": True}), " -- Cartesian product: every combination of a left tree and right tree forms one valid BST with this root."])),
    N.para(N.rich([("node = TreeNode(root_val, L, R)", {"code": True}), " -- Build one complete BST node. L or R may be None (leaf children), which is valid."])),
    N.para(N.rich([("memo[(lo, hi)] = trees", {"code": True}), " -- Store result BEFORE returning. Any future call with same (lo, hi) gets instant answer."])),
    N.para(N.rich([("return generate(1, n)", {"code": True}), " -- Kick off with the full range [1, n]. Returns all distinct BSTs."])),
    N.callout(
        N.rich([
            ("Why [None] not []?\n", {"bold": True}),
            ("Returning [] would make the Cartesian product loops iterate zero times -- "
             "meaning nodes with an empty left or right subtree would never be created. "
             "Returning [None] says 'one valid option: attach nothing here,' so the loop "
             "still runs once with L=None or R=None, correctly producing leaf nodes.", {}),
        ]),
        "⚠️", "yellow_background"
    ),
    N.divider(),
]

# ── SOLUTION 2 — Pure Recursion (No Memoization) ──────────────────────────
sol2_code = """\
def generateTrees(n: int):
    def generate(lo, hi):
        if lo > hi:
            return [None]            # Same base case -- always return [None]
        trees = []
        for r in range(lo, hi + 1):
            for L in generate(lo, r - 1):      # Recomputes overlapping ranges
                for R in generate(r + 1, hi):  # Same here -- no caching
                    trees.append(TreeNode(r, L, R))
        return trees
    return generate(1, n)
"""

blocks += [
    N.h2("Solution 2 -- Pure Recursion (Baseline, No Memoization)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Identical recursive logic to Solution 1 -- pick every root, recurse on both sides, "
            "combine via Cartesian product. This is the starting recursive solution with no optimization."
        ),
        N.h4("What Doesn't Work at Scale"),
        N.para(
            "For n=8, generate(2,4) may be called dozens of times from different root choices. "
            "Without caching, we redo the same work repeatedly. Still correct -- just slower."
        ),
        N.h4("The Key Observation"),
        N.para(
            "This version is best for interviews as a starting point before optimization. "
            "State it first, identify the overlapping subproblems, then add memo = {} as the upgrade."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Identical to Solution 1, minus the memo dict. Use this as the 'naive baseline' to "
            "present before the memoized version. Interviewers appreciate seeing the thought process."
        ),
    ]),
    N.h3("Code"),
    N.code(sol2_code),
    N.h3("Line by Line"),
    N.para("Every line is identical to Solution 1 except the memo dictionary is absent. The generate function recomputes each (lo, hi) subrange fresh every time it is called."),
    N.para(N.rich([("Complexity:", {"bold": True}), " Same asymptotic bounds as Solution 1 but with higher constant factor -- identical subranges are computed multiple times rather than cached. Stack depth is O(n)."])),
    N.divider(),
]

# ── COMPLEXITY TABLE ────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Recursion + Memoization (Interview Pick)", "O(n^2 * C(n))", "O(n * C(n))"],
        ["Pure Recursion (Baseline)", "O(n^2 * C(n)) repeated subproblems", "O(n) stack"],
    ]),
    N.para(
        "C(n) = nth Catalan number = C(2n,n)/(n+1). "
        "n=3->5, n=4->14, n=5->42, n=6->132, n=7->429, n=8->1430. "
        "The output size itself grows as 4^n / n^(3/2), so any algorithm that builds "
        "all trees is necessarily super-polynomial in n."
    ),
    N.divider(),
]

# ── WHY IS THIS DP ──────────────────────────────────────────────────────────
blocks += [
    N.h2("Why is This Dynamic Programming?"),
    N.para(
        "Two pillars of DP both apply here:"
    ),
    N.para(N.rich([
        ("1. Optimal Substructure: ", {"bold": True}),
        ("generate(lo, hi) can be built entirely from generate(lo, r-1) and generate(r+1, hi) "
         "for each root r. The full solution is the Cartesian product of sub-solutions.", {}),
    ])),
    N.para(N.rich([
        ("2. Overlapping Subproblems: ", {"bold": True}),
        ("The same range [lo, hi] is requested from multiple parent calls. Without memoization, "
         "we recompute the same list of trees many times.", {}),
    ])),
    N.callout(
        N.rich([
            ("Recurrence Relation:\n", {"bold": True}),
            ("generate(lo, hi) = [] if lo > hi else\n"
             "  [ TreeNode(r, L, R)\n"
             "    for r in range(lo, hi+1)\n"
             "    for L in generate(lo, r-1)\n"
             "    for R in generate(r+1, hi) ]\n"
             "\n"
             "Base case: generate(lo, hi) = [None] when lo > hi", {}),
        ]),
        "📐", "blue_background"
    ),
    N.divider(),
]

# ── PATTERN CLASSIFICATION ──────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Dynamic Programming", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Generate Trees Recursively (Memoized Enumeration)", {})])),
    N.callout(
        N.rich([
            ("When to recognize this pattern:\n", {"bold": True}),
            ("• Problem asks to RETURN ALL structures (not count them)\n"
             "• The structure has natural recursive decomposition (trees, parentheses, subsets)\n"
             "• Subproblems are identified by a compact key (here: (lo, hi) range)\n"
             "• Output size is exponential -- computation bounded by Catalan / Fibonacci numbers\n"
             "• Cartesian product of sub-results appears naturally", {}),
        ]),
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── RELATED PROBLEMS ─────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same recursive enumeration + memoization technique:"),
    N.bullet(N.rich([("Unique Binary Search Trees (LeetCode #96)", {"bold": True}), (" (Medium) -- Count BSTs only, classic DP O(n^2): dp[i] = sum dp[j-1]*dp[i-j]", {})])),
    N.bullet(N.rich([("Generate Parentheses (LeetCode #22)", {"bold": True}), (" (Medium) -- Generate all valid parenthesis strings; similar recursive branching", {})])),
    N.bullet(N.rich([("Different Ways to Add Parentheses (LeetCode #241)", {"bold": True}), (" (Medium) -- Exact same pattern: pick operator as 'root', recurse on both sides, Cartesian product", {})])),
    N.bullet(N.rich([("Scramble String (LeetCode #87)", {"bold": True}), (" (Hard) -- Memoized recursion on string ranges, similar (lo, hi) keying", {})])),
    N.bullet(N.rich([("All Possible Full Binary Trees (LeetCode #894)", {"bold": True}), (" (Medium) -- Generate all full binary trees with n nodes; identical structural pattern", {})])),
    N.bullet(N.rich([("Letter Combinations of a Phone Number (LeetCode #17)", {"bold": True}), (" (Medium) -- Cartesian product of digit-mapped letters, same enumeration spirit", {})])),
    N.bullet(N.rich([("Subsets II (LeetCode #90)", {"bold": True}), (" (Medium) -- Enumerate all subsets with backtracking; overlapping subproblems handled by pruning", {})])),
    N.para(
        "These problems share the core technique: recursive decomposition into independent subproblems, "
        "Cartesian product of sub-results to build full solutions, and memoization keyed on a compact "
        "identifier (range, prefix length, or bitmask) to avoid exponential redundancy."
    ),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md -- Section 18: Dynamic Programming (DP: Tree / Generate All Structures)", "📚", "gray_background"),
    N.divider(),
]

# ── EMBED ────────────────────────────────────────────────────────────────────
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("unique_binary_search_trees_ii")),
    N.para(N.rich([
        ("Step through the algorithm visually -- use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"}),
    ])),
]

# ── Append all blocks ────────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
