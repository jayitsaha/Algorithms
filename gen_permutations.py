"""gen_permutations.py — Notion in-place update for Permutations (LeetCode #46)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81e5-baac-c4d5f6f24e06"

# ── 1) Properties ──────────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=46,
    pattern="Backtracking",
    subpatterns=["Swap or Used Array"],
    tc="O(n · n!)",
    sc="O(n)",
    key_insight="Use a start pointer to partition nums into locked vs available zones; swap an element in, recurse, swap back to undo.",
    icon="🟡",
)
print("Properties set.")

# ── 2) Wipe old body ───────────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3) Rebuild body ────────────────────────────────────────────────────────────
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an array of distinct integers ", {}),
        ("nums", {"code": True}),
        (", return all possible permutations. You can return the answer in any order.", {}),
    ])),
    N.para("Example: nums = [1,2,3] → [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]. "
           "For n distinct elements there are exactly n! total permutations. "
           "All elements are guaranteed to be unique (no duplicates)."),
    N.divider(),
]

# Solution 1 — Swap-based Backtracking (Interview Pick)
SOL1_CODE = """\
def permute(nums):
    result = []
    def backtrack(start):
        if start == len(nums):        # base case: all positions filled
            result.append(nums[:])    # append a COPY, not a reference!
            return
        for i in range(start, len(nums)):
            nums[start], nums[i] = nums[i], nums[start]   # choose
            backtrack(start + 1)                           # explore
            nums[start], nums[i] = nums[i], nums[start]   # undo
    backtrack(0)
    return result
"""

blocks += [
    N.h2("Solution 1 — Backtracking with Swap (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need every possible ordering of all n elements. Think of it as filling positions 0, 1, ..., n-1 one at a time. At each position, choose one of the remaining unused elements to place there. After all positions are filled, record the arrangement. Then undo the last choice and try another."),
        N.h4("What Doesn't Work"),
        N.para("A brute-force approach of generating all n! orderings and deduplicating doesn't simplify the problem — we still must enumerate all n! arrangements. A greedy approach (always pick smallest) only produces one permutation. We cannot avoid exploring all branches."),
        N.h4("The Key Observation"),
        N.para("We can partition the nums array into two zones using a 'start' index. Elements at 0..start-1 are already locked in their final positions. Elements at start..n-1 are still available. To 'try' element nums[i], swap it to position start (moving it into the locked zone), recurse, then swap it back (restoring the available zone). This avoids a separate 'used' data structure entirely."),
        N.h4("Building the Solution"),
        N.para("Step 1: If start == n, all positions filled — append nums[:] (a copy!) to result and return. Step 2: For each i in range(start, n), swap nums[start] with nums[i] (choose), recurse with start+1 (explore), swap back (undo). The choose and undo lines are identical because swapping is its own inverse."),
        N.callout("Analogy: Think of seats in a row. You fill seat 0 with any available person, fill the rest recursively, then 'unseat' them and try the next person. The swap trick is like a label swap — no new data structures needed.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(SOL1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("result = []", {"code": True}), " — accumulator for all completed permutations."])),
    N.para(N.rich([("def backtrack(start):", {"code": True}), " — 'start' is the index of the position we are currently filling."])),
    N.para(N.rich([("if start == len(nums):", {"code": True}), " — base case: every index 0..n-1 has been filled."])),
    N.para(N.rich([("result.append(nums[:])", {"code": True}), " — COPY the array. Never append nums directly — it will be mutated by future backtracking steps."])),
    N.para(N.rich([("for i in range(start, len(nums)):", {"code": True}), " — try each element in the available zone (index start to n-1) as the next choice."])),
    N.para(N.rich([("nums[start], nums[i] = nums[i], nums[start]", {"code": True}), " — CHOOSE: swap element at index i to position start, locking it in."])),
    N.para(N.rich([("backtrack(start + 1)", {"code": True}), " — EXPLORE: fill the remaining positions start+1..n-1."])),
    N.para(N.rich([("nums[start], nums[i] = nums[i], nums[start]", {"code": True}), " — UNDO: the same swap restores the array. Swapping twice is the identity."])),
    N.para(N.rich([("backtrack(0)", {"code": True}), " — kick off: start filling from position 0."])),
    N.divider(),
]

# Solution 2 — Used-array
SOL2_CODE = """\
def permute(nums):
    result, path = [], []
    used = [False] * len(nums)
    def backtrack():
        if len(path) == len(nums):
            result.append(path[:])   # copy current path
            return
        for i, num in enumerate(nums):
            if used[i]:
                continue             # skip already-placed elements
            used[i] = True           # choose
            path.append(num)
            backtrack()              # explore
            used[i] = False          # undo
            path.pop()
    backtrack()
    return result
"""

blocks += [
    N.h2("Solution 2 — Used-Array + Path (More Readable)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Instead of partitioning the array in-place, maintain a separate boolean 'used' array and build the current permutation in a 'path' list. This separates concerns: used[] tracks which elements are taken, path holds the current arrangement being built."),
        N.h4("What Doesn't Work"),
        N.para("Without the 'used' array, we'd try every element at every position (including already-placed ones), generating duplicates and incorrect results."),
        N.h4("The Key Observation"),
        N.para("At each recursion level, iterate over ALL elements. Skip those already in the path (used[i] == True). Add the chosen element, mark it used, recurse, then unmark it and remove it from path. This is the most explicit and readable form of the choose-explore-undo pattern."),
        N.h4("Building the Solution"),
        N.para("Base case: len(path) == n. Loop over all elements, skip if used. Mark used, append to path, recurse, unmark, pop. The undo must reverse BOTH changes: used[i] = False AND path.pop()."),
        N.callout("Trade-off: This approach uses O(n) extra space for used[] and O(n) for path, whereas the swap approach uses only the O(n) recursion stack. For an interview, the swap version is preferred for space efficiency.", "⚖️", "yellow_background"),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("result, path = [], []", {"code": True}), " — result collects finished permutations; path is the current one being built."])),
    N.para(N.rich([("used = [False] * len(nums)", {"code": True}), " — tracks which indices are currently in the path."])),
    N.para(N.rich([("if used[i]: continue", {"code": True}), " — skip elements already included in the current path."])),
    N.para(N.rich([("used[i] = True; path.append(num)", {"code": True}), " — CHOOSE: mark element i as used and add it to the current path."])),
    N.para(N.rich([("used[i] = False; path.pop()", {"code": True}), " — UNDO: both changes must be reversed in order to backtrack cleanly."])),
    N.divider(),
]

# Complexity
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Aux Space"],
        ["Swap (in-place)", "O(n · n!)", "O(n) stack only"],
        ["Used-array + path", "O(n · n!)", "O(n) × 3"],
        ["Note: output space", "O(n · n!)", "unavoidable"],
    ]),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Backtracking"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Swap or Used Array"])),
    N.callout(
        "When to recognize this pattern: The problem asks for ALL possible arrangements, "
        "combinations, or subsets. Output size is exponential (n! or 2ⁿ). "
        "You need to make a sequence of choices, explore consequences, and undo — classic backtracking. "
        "Signal words: 'all possible', 'every arrangement', 'enumerate all', 'list all solutions'.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same backtracking (choose-explore-undo) framework:"),
    N.bullet(N.rich([("Permutations II", {"bold": True}), " (Medium) — Same but with duplicates; sort first, skip duplicate choices at each level with 'if i > start and nums[i] == nums[i-1]: continue'"])),
    N.bullet(N.rich([("Combinations", {"bold": True}), " (Medium) — Choose k from n unordered; pass 'start' to avoid revisiting earlier elements"])),
    N.bullet(N.rich([("Subsets", {"bold": True}), " (Medium) — Include or exclude each element; collect result at every depth, not just leaves"])),
    N.bullet(N.rich([("Letter Combinations of a Phone Number", {"bold": True}), " (Medium) — One character per digit from a mapping; branching factor varies by key"])),
    N.bullet(N.rich([("Combination Sum", {"bold": True}), " (Medium) — Unlimited reuse allowed; prune when sum exceeds target"])),
    N.bullet(N.rich([("N-Queens", {"bold": True}), " (Hard) — Backtracking with diagonal/row/column conflict pruning; much deeper pruning than permutations"])),
    N.bullet(N.rich([("Next Permutation", {"bold": True}), " (Medium) — Find the single next lexicographic ordering in O(n) — no recursion, no enumeration"])),
    N.para("These problems all share the core backtracking template: choose from available options, explore consequences, undo the choice."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Backtracking section (Swap or Used Array sub-pattern)", "📚", "gray_background"),
]

# Embed
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("permutations")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── 4) Append all blocks ───────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK — appended {len(blocks)} blocks to {PAGE_ID}")
