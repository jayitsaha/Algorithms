"""
Notion update script for Subsets (LeetCode #78).
Run from the Algorithms directory: python3 gen_subsets.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8158-b171-cf2d87c804bc"

# ── 1. Set page properties ──
print("Setting properties ...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=78,
    pattern="Backtracking",
    subpatterns=["Include/Exclude Each Element"],
    tc="O(n · 2ⁿ)",
    sc="O(n)",
    key_insight="For each element make one binary decision (include vs. exclude); n decisions produce all 2ⁿ subsets via DFS backtracking.",
    icon="🟡",
)
print("Properties set.")

# ── 2. Wipe old body ──
print("Wiping old content ...")
deleted = N.wipe_page(PAGE_ID)
print(f"  Deleted {deleted} blocks.")

# ── 3. Rebuild body ──
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(
        "Given an integer array nums of unique elements, return all possible subsets "
        "(the power set). The solution set must not contain duplicate subsets. Return "
        "the solution in any order.\n\n"
        "Example: nums = [1, 2, 3] → [[], [1], [2], [1,2], [3], [1,3], [2,3], [1,2,3]]\n"
        "Example: nums = [0] → [[], [0]]"
    ),
    N.divider(),
]

# ── Solution 1: Include/Exclude Backtracking ──
blocks += [
    N.h2("Solution 1 — Include/Exclude Backtracking (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "The power set is every possible combination of 'take it or leave it' decisions "
            "for each element. Restated: for each element, independently decide to include "
            "or exclude it. Each unique sequence of n binary decisions yields a unique subset."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Generating subsets via nested loops fails for arbitrary n — you'd need n nested "
            "loops and can't write that statically. A 'try all bit patterns' approach (bitmask) "
            "works but is hard to explain fluently in an interview without preparation."
        ),
        N.h4("The Key Observation"),
        N.para(
            "The binary decision structure maps directly to a binary recursion tree of depth n. "
            "Each tree node branches into two children: include nums[index] or don't. "
            "Every path from root to leaf is one complete decision sequence = one unique subset. "
            "The tree has exactly 2ⁿ leaves."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. Maintain a shared path list (the current partial subset).\n"
            "2. Recurse with the current index. At each level: append nums[index] and recurse (include), "
            "then pop and recurse again (exclude).\n"
            "3. Base case: index == len(nums) → record path[:] (a copy!) and return.\n"
            "4. The outer function kicks off backtrack(0) and returns result."
        ),
        N.callout(
            "Analogy: Think of a buffet where each dish is optional. For each of the n dishes, "
            "you either take it or skip it. Every unique combination of choices is a valid plate — "
            "a subset. The DFS explores all possible plate configurations systematically.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(
        "def subsets(nums):\n"
        "    result = []\n"
        "    path = []\n"
        "\n"
        "    def backtrack(index):\n"
        "        if index == len(nums):       # Base case: all decisions made\n"
        "            result.append(path[:])   # COPY path — not a reference!\n"
        "            return\n"
        "        # Include branch\n"
        "        path.append(nums[index])\n"
        "        backtrack(index + 1)\n"
        "        # Exclude branch (backtrack)\n"
        "        path.pop()\n"
        "        backtrack(index + 1)\n"
        "\n"
        "    backtrack(0)\n"
        "    return result\n"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("result = []", {"code": True}),
                   " — Accumulate all completed subsets here."])),
    N.para(N.rich([("path = []", {"code": True}),
                   " — Shared mutable list representing the partial subset being built."])),
    N.para(N.rich([("def backtrack(index):", {"code": True}),
                   " — Inner DFS function; 'index' is the element we're currently deciding."])),
    N.para(N.rich([("if index == len(nums):", {"code": True}),
                   " — Base case: every element has been decided; path is a complete subset."])),
    N.para(N.rich([("result.append(path[:])", {"code": True}),
                   " — path[:] creates a COPY. Storing path directly gives a shared reference "
                   "that will be mutated by later backtracking steps — a silent bug."])),
    N.para(N.rich([("path.append(nums[index])", {"code": True}),
                   " — Include branch: add the current element to the partial subset."])),
    N.para(N.rich([("backtrack(index + 1)", {"code": True}),
                   " (first call) — Recurse deeper with the element included."])),
    N.para(N.rich([("path.pop()", {"code": True}),
                   " — Backtrack: undo the include to restore path to its pre-include state."])),
    N.para(N.rich([("backtrack(index + 1)", {"code": True}),
                   " (second call) — Recurse deeper with the element excluded."])),
    N.para(N.rich([("backtrack(0)", {"code": True}),
                   " — Kick off the DFS from index 0 with an empty path."])),
    N.divider(),
]

# ── Solution 2: Iterative ──
blocks += [
    N.h2("Solution 2 — Iterative / BFS-style"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Instead of DFS, think iteratively: add one element at a time and, for each new "
            "element, create a new subset for every existing subset by appending the element to it."
        ),
        N.h4("The Key Observation"),
        N.para(
            "After processing element e, the new result = old result UNION {s + [e] for every s in old result}. "
            "This doubles the result size each iteration. After n iterations: 2ⁿ subsets."
        ),
        N.callout(
            "Analogy: A photocopier that doubles your document stack. Start with one page (the empty subset). "
            "For each new element, copy the entire stack and stamp the element on every copy, then add those "
            "copies to the stack. After n elements you have 2ⁿ pages.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(
        "def subsets(nums):\n"
        "    result = [[]]             # Start: only the empty subset\n"
        "    for num in nums:          # Process each element\n"
        "        result += [s + [num]  # For each existing subset, create\n"
        "                   for s in result]  # a version with num added\n"
        "    return result\n"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("result = [[]]", {"code": True}),
                   " — Start with the one subset that always exists: the empty set."])),
    N.para(N.rich([("for num in nums:", {"code": True}),
                   " — Process elements left to right; order of output subsets changes but all are produced."])),
    N.para(N.rich([("result += [s + [num] for s in result]", {"code": True}),
                   " — For every subset s currently in result, create s + [num]. "
                   "This doubles result size on each iteration. Note: iterating over result "
                   "while extending it would be a bug — the list comprehension captures a snapshot."])),
    N.divider(),
]

# ── Solution 3: Bitmask ──
blocks += [
    N.h2("Solution 3 — Bitmask"),
    N.h3("Code"),
    N.code(
        "def subsets(nums):\n"
        "    n = len(nums)\n"
        "    result = []\n"
        "    for mask in range(1 << n):         # 0 to 2ⁿ-1\n"
        "        subset = [nums[i] for i in range(n)\n"
        "                  if mask & (1 << i)]  # bit i = include nums[i]?\n"
        "        result.append(subset)\n"
        "    return result\n"
    ),
    N.para(
        "Each integer mask from 0 to 2ⁿ-1 encodes one subset: if bit i of mask is set, "
        "include nums[i]. There are exactly 2ⁿ distinct n-bit integers, so we get exactly 2ⁿ subsets. "
        "Elegant but requires fluency to explain in an interview."
    ),
    N.divider(),
]

# ── Complexity table ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Aux Space", "Notes"],
        ["Backtracking (inc/exc)", "O(n · 2ⁿ)", "O(n)", "Stack depth n; O(n·2ⁿ) output not counted"],
        ["Iterative (BFS-style)", "O(n · 2ⁿ)", "O(n · 2ⁿ)", "All subsets in memory during construction"],
        ["Bitmask", "O(n · 2ⁿ)", "O(n)", "Same asymptotic; harder to explain"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Backtracking"])),
    N.para(N.rich([("Sub-Pattern: ", {"bold": True}), "Include/Exclude Each Element — Binary decision at each index (include or skip), DFS tree with 2ⁿ leaves."])),
    N.callout(
        "When to recognise this pattern:\n"
        "• 'Generate all subsets / power set'\n"
        "• 'Find all combinations of size k' (same template + size guard)\n"
        "• 'Count/find subsets with property X' (same recursion, different base case)\n"
        "• Problem has n items and asks for all possible selections (without ordering)",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Include/Exclude / Backtracking technique:"),
    N.bullet(N.rich([("Subsets II", {"bold": True}), " (Medium, #90) — Same structure with duplicates; sort + skip same element at each depth."])),
    N.bullet(N.rich([("Combinations", {"bold": True}), " (Medium, #77) — All subsets of exactly size k; add size guard to base case."])),
    N.bullet(N.rich([("Combination Sum", {"bold": True}), " (Medium, #39) — Elements (with repetition) summing to target; prune on excess sum."])),
    N.bullet(N.rich([("Combination Sum II", {"bold": True}), " (Medium, #40) — Each element once; duplicates in input; skip technique from Subsets II."])),
    N.bullet(N.rich([("Permutations", {"bold": True}), " (Medium, #46) — All orderings; swap-based recursion; O(n·n!)."])),
    N.bullet(N.rich([("Partition Equal Subset Sum", {"bold": True}), " (Medium, #416) — Exists subset summing to half total? Same recursion, optimised with DP."])),
    N.bullet(N.rich([("Letter Combinations of a Phone Number", {"bold": True}), " (Medium, #17) — Same DFS shape; choose one char per digit."])),
    N.para("These problems share the core pattern: binary (or k-way) decisions at each step, building a solution incrementally, recording when the base case is satisfied."),
    N.divider(),
]

# ── Embed ──
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("subsets")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.",
                    {"italic": True, "color": "gray"})])),
]

print(f"Appending {len(blocks)} blocks to Notion ...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
