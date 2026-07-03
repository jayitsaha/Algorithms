"""gen_subsets_ii.py — Notion update for Subsets II (LeetCode #90)"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-8163-ac6d-ea9db1585495"

# ── 1) Properties ──
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=90,
    pattern="Backtracking",
    subpatterns=["Sort + Skip Consecutive Dups"],
    tc="O(n · 2ⁿ)",
    sc="O(n)",
    key_insight="Sort first, then skip duplicate siblings in the loop (i > start and nums[i]==nums[i-1]).",
    icon="🟡"
)
print("Properties set.")

# ── 2) Wipe old body ──
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3) Build body ──
PROBLEM_STMT = (
    "Given an integer array nums that may contain duplicates, return all possible subsets "
    "(the power set). The solution set must not contain duplicate subsets. Return the solution "
    "in any order.\n\n"
    "Example: nums = [1,2,2] → [[], [1], [1,2], [1,2,2], [2], [2,2]]"
)

SOL1_CODE = """\
def subsetsWithDup(nums):
    nums.sort()                          # group duplicates for adjacent detection
    result, path = [], []
    def backtrack(start):
        result.append(path[:])           # every DFS node is a valid subset
        for i in range(start, len(nums)):
            if i > start and nums[i] == nums[i-1]:
                continue                 # skip duplicate SIBLING (same value, same depth)
            path.append(nums[i])
            backtrack(i + 1)
            path.pop()                   # backtrack: undo choice
    backtrack(0)
    return result
"""

SOL2_CODE = """\
def subsetsWithDup_brute(nums):
    nums.sort()
    seen, result, path = set(), [], []
    def backtrack(start):
        key = tuple(path)
        if key not in seen:
            seen.add(key)
            result.append(path[:])
        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1)
            path.pop()
    backtrack(0)
    return result  # explores all branches, deduplicates after — less efficient
"""

blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(PROBLEM_STMT),
    N.divider(),
]

# Solution 1
blocks += [
    N.h2("Solution 1 — Sort + Backtrack + Skip (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We need all unique subsets of an array that may contain duplicates. Think of it as "
            "building every possible selection: for each element, we either include it or we don't. "
            "With n elements, this gives 2^n subsets — but duplicates create identical branches."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "A naive DFS (like LeetCode #78 Subsets) would generate duplicate subsets whenever "
            "two equal values exist. For [1,2,2], choosing the first 2 and choosing the second 2 "
            "at the same DFS depth produce identical subtrees: both yield [2], [2,2], etc. "
            "Using a set to dedup after-the-fact works but wastes time exploring dead branches."
        ),
        N.h4("The Key Observation"),
        N.para(
            "If we SORT the array first, duplicates become adjacent. Then, within the for-loop "
            "at any DFS level, if we see nums[i] == nums[i-1] and i > start, we know this element "
            "is a duplicate sibling — it will produce the same subtree as the previous element. "
            "Skip it before entering the subtree."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. Sort nums.\n"
            "2. DFS with backtrack(start): on entry, add path[:] to result.\n"
            "3. Loop i from start to n-1. Before adding nums[i], check: i > start AND nums[i] == nums[i-1] → skip.\n"
            "4. Otherwise: append nums[i], recurse(i+1), pop nums[i].\n"
            "Key: i > start (not i > 0) — we only skip sibling duplicates, not child duplicates. "
            "The second 2 in [2,2] is a valid child, not a sibling duplicate."
        ),
        N.callout(
            "Analogy: Imagine you have two identical coins. At a fork in the road, taking the left "
            "coin vs the right coin leads to the same destinations. So you always take the left one "
            "and ignore the right — but once you've committed to the left path, both coins can appear "
            "in your pocket for future choices.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOL1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("nums.sort()", {"code": True}), " — Sort the array in-place. Groups equal values adjacently, enabling the skip rule."])),
    N.para(N.rich([("result, path = [], []", {"code": True}), " — result accumulates all found subsets. path is a single mutable list reused throughout the DFS."])),
    N.para(N.rich([("result.append(path[:])", {"code": True}), " — On every DFS entry (not just at leaves!), snapshot path with path[:]. Every node in the tree is a valid subset."])),
    N.para(N.rich([("for i in range(start, len(nums))", {"code": True}), " — Try each element from start onward as the next element to include."])),
    N.para(N.rich([("if i > start and nums[i] == nums[i-1]: continue", {"code": True}), " — Skip duplicate siblings. i > start ensures we only skip the 2nd+ occurrence at this depth level, not the first."])),
    N.para(N.rich([("path.append(nums[i])", {"code": True}), " — Choose nums[i]: add to current subset."])),
    N.para(N.rich([("backtrack(i + 1)", {"code": True}), " — Explore: recurse with start=i+1 so each element is used at most once per subset."])),
    N.para(N.rich([("path.pop()", {"code": True}), " — Un-choose: remove nums[i] so path returns to pre-call state, ready to try the next sibling."])),
    N.divider(),
]

# Solution 2
blocks += [
    N.h2("Solution 2 — Brute Force with Set Dedup"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same as Solution 1, but instead of pruning at the source, we explore all branches and use a set to discard duplicates afterward."),
        N.h4("What Doesn't Work"),
        N.para("This approach is correct but wastes time. For nums=[1,2,2], it fully explores the duplicate [2] branch, builds all its subsets, then discards them — extra O(n) work per duplicate group."),
        N.h4("The Key Observation"),
        N.para("Converting path to a tuple (hashable) lets us use a Python set for O(1) lookup. Since we sort first, all subset tuples are in canonical order, so equal subsets produce identical keys."),
        N.h4("Building the Solution"),
        N.para("1. Sort, then DFS as usual (no skip rule).\n2. On each entry, convert path to a tuple as the hash key.\n3. If the key is new, add to seen set AND add path[:] to result.\n4. Otherwise skip — this path was already recorded."),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("key = tuple(path)", {"code": True}), " — Convert mutable list to an immutable, hashable tuple for set membership testing."])),
    N.para(N.rich([("if key not in seen", {"code": True}), " — O(1) average lookup. If we've never seen this exact subset before, record it."])),
    N.para(N.rich([("seen.add(key); result.append(path[:])", {"code": True}), " — Mark as seen, then store a copy of the current path."])),
    N.para(N.rich([("No i > start guard", {"code": True}), " — This solution doesn't need the skip rule; it catches duplicates via the set. But it explores more nodes."])),
    N.divider(),
]

# Complexity
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space (stack)"],
        ["Sort + Skip (Solution 1)", "O(n · 2ⁿ)", "O(n)"],
        ["Brute Force + Set (Solution 2)", "O(n · 2ⁿ · n)", "O(2ⁿ) for set"],
        ["Iterative cascading", "O(n · 2ⁿ)", "O(1) stack"],
    ]),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Backtracking — DFS that builds partial solutions, recurses, and undoes (backtracks) choices."])),
    N.para(N.rich([("Sub-Pattern: ", {"bold": True}), "Sort + Skip Consecutive Dups — Sort to group duplicates, then use i > start guard to prune sibling duplicate branches in the for-loop."])),
    N.callout(
        "When to recognize this pattern:\n"
        "• Problem says 'input may contain duplicates' + 'no duplicate subsets/combinations'\n"
        "• You're doing DFS with a for-loop picking from a suffix of the array\n"
        "• You see Subsets, Combination Sum, or Permutation with the word 'II' in the title",
        "🔎", "green_background"
    ),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Sort + Skip Consecutive Dups technique:"),
    N.bullet(N.rich([("Subsets (#78)", {"bold": True}), " (Medium) — Same backtracking, no duplicates, no skip needed."])),
    N.bullet(N.rich([("Combination Sum II (#40)", {"bold": True}), " (Medium) — Same sort+skip but pick combinations summing to target, each element used once."])),
    N.bullet(N.rich([("Permutations II (#47)", {"bold": True}), " (Medium) — Permutations with dups; sort + used[] array + skip rule on adjacent equal unused elements."])),
    N.bullet(N.rich([("Combination Sum (#39)", {"bold": True}), " (Medium) — Base backtracking with unlimited reuse, no duplicates — learn this before Subsets II."])),
    N.bullet(N.rich([("Palindrome Partitioning (#131)", {"bold": True}), " (Medium) — Backtracking with palindrome condition as pruning; same choose/recurse/pop structure."])),
    N.bullet(N.rich([("Letter Combinations of a Phone Number (#17)", {"bold": True}), " (Medium) — Backtracking over character choices from a digit-to-letters map."])),
    N.para("These problems all share the DFS backtracking skeleton: choose → recurse → un-choose."),
    N.callout(
        "📚 Sub-Pattern: Sort + Skip Consecutive Dups | Classification: Analysis-based "
        "(Backtracking section)",
        "📚", "gray_background"
    ),
]

# Embed
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("subsets_ii")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
