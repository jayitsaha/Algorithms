"""
gen_permutations_ii.py — Notion IN-PLACE update for LeetCode #47 Permutations II
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81ff-9ca7-f9a9f601aedf"

# ── 1) Properties ──────────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=47,
    pattern="Backtracking",
    subpatterns=["Sort + Skip Duplicates"],
    tc="O(n · n!)",
    sc="O(n)",
    key_insight="Sort first so duplicates are adjacent; skip index i if nums[i]==nums[i-1] and nums[i-1] is an unused sibling (not ancestor).",
    icon="🟡"
)
print("Properties set.")

# ── 2) Wipe old body ───────────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3) Build new body ──────────────────────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a collection of numbers, ", {}),
        ("nums", {"code": True}),
        (", that might contain duplicates, return ", {}),
        ("all possible unique permutations", {"bold": True}),
        (" in any order.", {}),
    ])),
    N.para("Example 1: nums = [1,1,2]  →  [[1,1,2],[1,2,1],[2,1,1]]"),
    N.para("Example 2: nums = [1,2,3]  →  [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]"),
    N.para("Constraints: 1 ≤ nums.length ≤ 8, -10 ≤ nums[i] ≤ 10"),
    N.divider(),
]

# ── Solution 1 ──────────────────────────────────────────────────────────────
blocks += [
    N.h2("Solution 1 — Sort + Skip Backtracking (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to enumerate every distinct ordering of the input numbers. Think of it as filling n slots one by one: at each slot, choose one unused number; recurse to fill the rest; undo the choice and try the next option (backtracking)."),
        N.h4("What Doesn't Work"),
        N.para("Naive backtracking (LeetCode #46) generates all n! permutations without caring about duplicates. With repeated values, multiple choices at one level produce identical subtrees. Collecting all results in a set deduplicates them — but only after doing all the wasted work."),
        N.h4("The Key Observation"),
        N.para("If we SORT the input, duplicate values sit adjacent. At any recursion level, the first occurrence of a value and all subsequent identical occurrences would produce the same sub-permutations if chosen at the same position. We only need to try the first one — the rest are structurally identical."),
        N.h4("Building the Solution"),
        N.para("Sort nums. Use a boolean used[] array indexed by position (not value — two equal values have distinct indices). In the loop, before choosing index i: check if nums[i]==nums[i-1] AND used[i-1] is False. If so, skip — nums[i-1] is a sibling (not an ancestor), and its subtree was already fully explored. Otherwise, mark used[i]=True, append, recurse, then undo both (backtrack)."),
        N.callout(
            "Analogy: Think of sorting duplicate playing cards by suit then rank. When laying them face-down in a row, you never need to start with the second Jack — starting with the first Jack already covers every possible arrangement where a Jack is first.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(
        "def permuteUnique(nums):\n"
        "    nums.sort()  # CRITICAL: duplicates become adjacent\n"
        "    result = []\n"
        "    used = [False] * len(nums)\n"
        "\n"
        "    def backtrack(path):\n"
        "        if len(path) == len(nums):\n"
        "            result.append(path[:])  # copy! path is mutable\n"
        "            return\n"
        "        for i in range(len(nums)):\n"
        "            if used[i]:\n"
        "                continue\n"
        "            if i > 0 and nums[i] == nums[i-1] and not used[i-1]:\n"
        "                continue  # skip duplicate sibling\n"
        "            used[i] = True\n"
        "            path.append(nums[i])\n"
        "            backtrack(path)\n"
        "            path.pop()\n"
        "            used[i] = False\n"
        "\n"
        "    backtrack([])\n"
        "    return result"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("nums.sort()", {"code": True}), (" — Sort in-place. Duplicates become adjacent, enabling the skip condition.", {})])),
    N.para(N.rich([("used = [False] * len(nums)", {"code": True}), (" — Per-index boolean array (not per-value). Index 0 and index 1 are distinct even if nums[0]==nums[1].", {})])),
    N.para(N.rich([("if len(path) == len(nums):", {"code": True}), (" — Base case: all n positions filled. We have a complete permutation.", {})])),
    N.para(N.rich([("result.append(path[:])", {"code": True}), (" — path[:] creates a shallow copy (snapshot). Never append the live list — backtracking will mutate it.", {})])),
    N.para(N.rich([("if used[i]: continue", {"code": True}), (" — Skip if this index is already in the current path. Can't reuse a position.", {})])),
    N.para(N.rich([("if i > 0 and nums[i] == nums[i-1] and not used[i-1]: continue", {"code": True}), (" — The dedup condition. Three parts: (1) there is a previous element; (2) same value; (3) the previous one is a sibling (not an ancestor in path). All three must hold to skip.", {})])),
    N.para(N.rich([("used[i] = True; path.append(nums[i])", {"code": True}), (" — Choose: mark this index as used and add its value to the partial permutation.", {})])),
    N.para(N.rich([("backtrack(path)", {"code": True}), (" — Explore: recurse to fill the next position.", {})])),
    N.para(N.rich([("path.pop(); used[i] = False", {"code": True}), (" — Backtrack: undo both steps. Restore state exactly so the next iteration starts clean.", {})])),
    N.divider(),
]

# ── Solution 2 ──────────────────────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Brute Force with Set Deduplication"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Generate every possible arrangement and remove the duplicates afterward. Python's itertools.permutations handles the generation; converting to a set of tuples handles deduplication."),
        N.h4("What Doesn't Work"),
        N.para("This approach is correct but wasteful. It generates all n! permutations regardless of duplicates, then spends O(n·n!) space storing tuples in a set. With many duplicates (e.g., all same values), most generated permutations are thrown away."),
        N.h4("The Key Observation"),
        N.para("The stdlib itertools.permutations treats equal values as distinct if they are at different positions. Converting the resulting tuples to a set deduplicates by value, which is what we want."),
        N.h4("Building the Solution"),
        N.para("from itertools import permutations. Return list(set(permutations(nums))). Optionally convert inner tuples to lists. Simple, but no pruning occurs — all O(n!) branches are explored."),
    ]),
    N.h3("Code"),
    N.code(
        "from itertools import permutations\n"
        "\n"
        "def permuteUnique(nums):\n"
        "    # Generate all n! permutations as tuples, deduplicate via set\n"
        "    return [list(p) for p in set(permutations(nums))]"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("permutations(nums)", {"code": True}), (" — Generates all n! ordered arrangements as tuples, treating equal values at different indices as distinct.", {})])),
    N.para(N.rich([("set(...)", {"code": True}), (" — Converts iterator to set of tuples; duplicate tuples collapse into one.", {})])),
    N.para(N.rich([("list(p) for p in ...", {"code": True}), (" — Converts each tuple back to a list for the expected output format.", {})])),
    N.callout(
        "When to use this approach: Quick prototype or throwaway code. Never in an interview — it doesn't show algorithmic insight and has O(n·n!) space overhead.",
        "⚠️", "yellow_background"
    ),
    N.divider(),
]

# ── Complexity ──────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force + Set", "O(n · n!)", "O(n · n!)"],
        ["Sort + Skip Backtracking (Interview Pick)", "O(n · n!) worst case", "O(n)"],
    ]),
    N.para("Note: 'worst case' for Sort + Skip occurs when all elements are distinct (no pruning). With k identical elements in a group, that group's k! subtrees collapse to 1 — savings are dramatic for highly duplicate inputs."),
    N.divider(),
]

# ── Pattern Classification ──────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Backtracking — enumerate all valid configurations by choosing, exploring, and undoing choices.", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Sort + Skip Duplicates — sort input first so equal values are adjacent, then skip a choice at any level if the same value was already tried by a sibling at that level.", {})])),
    N.callout(
        "When to recognize this pattern:\n"
        "• Problem asks for all unique [permutations / subsets / combinations] of input with possible duplicates\n"
        "• Backtracking is the right approach (enumerate all)\n"
        "• You want to avoid post-processing deduplication (use a set at the end)\n"
        "• Output count is much smaller than n! because of repeated elements",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Sort + Skip Duplicates backtracking technique:"),
    N.bullet(N.rich([("Permutations", {"bold": True}), (" (Medium, #46) — Same backtracking template without the duplicate handling; the base case for this problem.", {})])),
    N.bullet(N.rich([("Subsets II", {"bold": True}), (" (Medium, #90) — Sort + skip for subset generation with duplicates; same skip condition, iterating forward not full range.", {})])),
    N.bullet(N.rich([("Combination Sum II", {"bold": True}), (" (Medium, #40) — Sort + skip for combinations; uses start index instead of used[] array.", {})])),
    N.bullet(N.rich([("Palindrome Partitioning", {"bold": True}), (" (Medium, #131) — Backtracking with palindrome validity as pruning; same choose/explore/undo structure.", {})])),
    N.bullet(N.rich([("Letter Combinations of a Phone Number", {"bold": True}), (" (Medium, #17) — Backtracking over character choices at each digit position.", {})])),
    N.bullet(N.rich([("N-Queens", {"bold": True}), (" (Hard, #51) — Classic backtracking; conflict checking replaces the skip condition as pruning mechanism.", {})])),
    N.bullet(N.rich([("Generate Parentheses", {"bold": True}), (" (Medium, #22) — Backtracking with validity constraint (open count ≤ n, close ≤ open) as pruning.", {})])),
    N.para("These problems all share the core pattern: build a configuration step by step, prune branches that cannot lead to valid/unique results, backtrack to try alternatives."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Backtracking section · Sub-Pattern: Sort + Skip Duplicates", "📚", "gray_background"),
]

# ── Embed ───────────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("permutations_ii")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ───────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks appended: {len(blocks)}")
