"""
gen_longest_increasing_subsequence.py
Rebuilds the Notion page for LeetCode #300 — Longest Increasing Subsequence.
"""
import sys
sys.path.insert(0, "/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms")
import notion_lib as N

# Patch token (notion_lib.py may have a redacted placeholder)
_REAL_TOKEN = "NOTION_TOKEN_REDACTED"
N.TOKEN = _REAL_TOKEN
N._HEADERS["Authorization"] = f"Bearer {_REAL_TOKEN}"

PAGE_ID = "39193418-809c-81f8-93cd-f416ae2e93e4"

# ── 1) Set properties ─────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=300,
    pattern="Dynamic Programming",
    subpatterns=["DP: LIS", "Binary Search O(n log n)"],
    tc="O(n log n)",
    sc="O(n)",
    key_insight="Track 'tails' array where tails[i] is the smallest tail of any LIS of length i+1; binary search gives O(n log n).",
    icon="🟡",
)
print("Properties set.")

# ── 2) Wipe old body ──────────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3) Build blocks ───────────────────────────────────────────────────────────
blocks = []


def lbl(code_text, explanation):
    """Helper: para with code-annotated label + plain explanation."""
    return N.para(N.rich([
        (code_text, {"code": True}),
        (" — " + explanation, {}),
    ]))


# ── PROBLEM ───────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an integer array ", {}),
        ("nums", {"code": True}),
        (", return the length of the longest strictly increasing subsequence.\n\n"
         "A subsequence is derived from the array by deleting some (or no) elements "
         "without changing the order of remaining elements.\n\n"
         "Example:\n"
         "  Input: nums = [10, 9, 2, 5, 3, 7, 101, 18]\n"
         "  Output: 4   (one LIS: [2, 3, 7, 101])\n\n"
         "Constraints: 1 <= nums.length <= 2500, -10^4 <= nums[i] <= 10^4\n"
         "Follow-up: Can you solve it in O(n log n) time complexity?", {}),
    ])),
    N.divider(),
]

# ── SOLUTION 1: Brute Force ───────────────────────────────────────────────────
brute_code = (
    "def lengthOfLIS_brute(nums):\n"
    "    def dfs(i, prev):\n"
    "        if i == len(nums):\n"
    "            return 0\n"
    "        skip = dfs(i + 1, prev)\n"
    "        take = 0\n"
    "        if nums[i] > prev:\n"
    "            take = 1 + dfs(i + 1, nums[i])\n"
    "        return max(skip, take)\n\n"
    "    return dfs(0, float('-inf'))\n"
)

blocks += [
    N.h2("Solution 1 - Brute Force Recursion (Exponential)"),
    N.toggle_h3("Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("At each position in the array, we face a binary decision: include this element in our subsequence, or skip it. If we include it, it must be strictly greater than the last element we included. We want to find the sequence of include/skip choices that maximises total included elements."),
        N.h4("What Doesn't Work"),
        N.para("Trying every possible subsequence is 2^n. For n=25 that is 33 million checks. Exponential -- useful only to establish correctness and identify the subproblems."),
        N.h4("The Key Observation"),
        N.para("Each recursive call only needs to know two things: where we are (index i) and what the previous included value was (prev). Everything in the future depends only on these two values -- this signals overlapping subproblems and DP potential."),
        N.h4("Building the Solution"),
        N.para("Define dfs(i, prev) = length of LIS starting from index i, given last included element was prev. Base: i == len(nums) => 0. Recurse with skip or take; return max of both branches."),
        N.callout("Analogy: Choosing people for a height-increasing parade line -- at each person decide skip or include (only if taller than the last in line).", "💡", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(brute_code),
    N.h3("Line by Line"),
    lbl("def dfs(i, prev):", "recursive helper; i=current index, prev=last included value (starts as -infinity)"),
    lbl("if i == len(nums): return 0", "base case: no more elements, subsequence length contribution is 0"),
    lbl("skip = dfs(i + 1, prev)", "option A: skip nums[i] entirely, move to next index with same prev"),
    lbl("if nums[i] > prev:", "only eligible to include if strictly greater than last included"),
    lbl("take = 1 + dfs(i + 1, nums[i])", "option B: include nums[i], count it (+1) and recurse with nums[i] as new prev"),
    lbl("return max(skip, take)", "take the best of both choices"),
    N.divider(),
]

# ── SOLUTION 2: Memoization ───────────────────────────────────────────────────
memo_code = (
    "from functools import lru_cache\n\n"
    "def lengthOfLIS_memo(nums):\n"
    "    n = len(nums)\n"
    "    # prev_idx = -1 means no previous element (start fresh)\n"
    "    @lru_cache(maxsize=None)\n"
    "    def dp(i, prev_idx):\n"
    "        if i == n:\n"
    "            return 0\n"
    "        best = dp(i + 1, prev_idx)\n"
    "        if prev_idx == -1 or nums[i] > nums[prev_idx]:\n"
    "            best = max(best, 1 + dp(i + 1, i))\n"
    "        return best\n\n"
    "    return dp(0, -1)\n"
)

blocks += [
    N.h2("Solution 2 - Memoization / Top-Down DP  [O(n^2)]"),
    N.toggle_h3("Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The brute-force DFS has overlapping subproblems: dp(i=5, prev_idx=2) might be called many times from different parent calls. We memoize on (i, prev_idx) to collapse identical subproblems into a single computation."),
        N.h4("What Doesn't Work (without memo)"),
        N.para("Pure recursion re-explores the same (i, prev_idx) states exponentially. There are O(n^2) unique pairs, so memoization reduces it to O(n^2) time."),
        N.h4("The Key Observation - Overlapping Subproblems"),
        N.para("dp(i, prev_idx) depends only on i and prev_idx, NOT on the specific sequence of choices that led here. This is the hallmark of DP: optimal substructure + overlapping subproblems."),
        N.h4("Building the Solution"),
        N.para("Replace prev value with prev_idx (an integer in [-1, n-1]) so it can be used as a hashable cache key. Use @lru_cache. Same recursion as brute force, now O(n^2) time and space."),
        N.callout("Why DP? (1) Optimal substructure: LIS from index i given prev is fully determined by subproblem answers. (2) Overlapping subproblems: same (i, prev_idx) pair arises via many different call paths.", "📐", "purple_background"),
    ]),
    N.h3("Code"),
    N.code(memo_code),
    N.h3("Line by Line"),
    lbl("@lru_cache(maxsize=None)", "Python decorator that automatically memoizes (i, prev_idx) -> result in a dictionary"),
    lbl("def dp(i, prev_idx):", "i = current position; prev_idx = index of last included element, or -1 if none yet"),
    lbl("if i == n: return 0", "base case: past end of array, no more elements to consider"),
    lbl("best = dp(i + 1, prev_idx)", "skip option: don't take nums[i], keep same prev_idx"),
    lbl("if prev_idx == -1 or nums[i] > nums[prev_idx]:", "can take nums[i] if no previous element, OR if strictly greater than previous"),
    lbl("best = max(best, 1 + dp(i + 1, i))", "take option: count this element (+1), new prev_idx becomes current i"),
    lbl("return dp(0, -1)", "start from index 0 with no previous element (prev_idx = -1)"),
    N.divider(),
]

# ── SOLUTION 3: Bottom-Up Tabulation ─────────────────────────────────────────
tabulation_code = (
    "def lengthOfLIS_dp(nums):\n"
    "    n = len(nums)\n"
    "    # dp[i] = length of LIS ending exactly at index i\n"
    "    dp = [1] * n  # Every element is an LIS of length 1 by itself\n\n"
    "    for i in range(1, n):\n"
    "        for j in range(i):  # Check all previous indices\n"
    "            if nums[j] < nums[i]:\n"
    "                dp[i] = max(dp[i], dp[j] + 1)\n\n"
    "    return max(dp)\n"
)

blocks += [
    N.h2("Solution 3 - Bottom-Up DP / Tabulation  [O(n^2), Interview Pick for DP]"),
    N.toggle_h3("Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Instead of asking 'what is the LIS from index i onwards?', ask 'what is the LIS that ENDS at index i?' This reformulation lets us build forward: dp[i] = length of the longest increasing subsequence ending at nums[i]."),
        N.h4("What Doesn't Work"),
        N.para("Without fixing the endpoint, table-filling is tricky because the future depends on a variable prev. By fixing index i as the LAST element, we can scan all j < i as potential predecessors -- all already solved when we need them."),
        N.h4("The Key Observation - Fixing the Endpoint"),
        N.para("dp[i] = 1 + max(dp[j]) for all j < i where nums[j] < nums[i]. If no such j exists, dp[i] = 1. Every subproblem dp[j] for j < i is already computed when we need it for i."),
        N.h4("Building the Solution"),
        N.para("Initialize dp[i] = 1 for all i. Fill left to right. For each i, look at every j < i; if nums[j] < nums[i], try extending dp[j]. Answer is max(dp) -- the longest of all subsequences ending anywhere."),
        N.callout("State machine: dp[i] means 'I am the last element of my subsequence.' Transition: dp[i] = max over all valid predecessors j of (dp[j] + 1). Return: global max over all endpoints.", "🔐", "blue_background"),
    ]),
    N.h3("Why Is This Dynamic Programming?"),
    N.para(N.rich([
        ("Optimal Substructure: ", {"bold": True}),
        ("The LIS ending at index i is built from the LIS ending at some j < i where nums[j] < nums[i]. "
         "The optimal answer for i depends directly on optimal answers for smaller j.\n\n", {}),
        ("Overlapping Subproblems: ", {"bold": True}),
        ("dp[3] is referenced when computing dp[4], dp[5], dp[6], ... -- each needs dp[3]. "
         "Without tabulation this would be recomputed exponentially.\n\n", {}),
        ("Recurrence: ", {"bold": True}),
        ("dp[i] = max(dp[j] + 1) for all j < i where nums[j] < nums[i], else 1.\n", {}),
        ("Answer: ", {"bold": True}),
        ("max(dp[0..n-1]) -- the best endpoint anywhere in the array.", {}),
    ])),
    N.code("# Recurrence:\n# dp[i] = 1 + max(dp[j] for j in range(i) if nums[j] < nums[i])\n# Base: dp[i] = 1\n# Answer: max(dp)", "python"),
    N.h3("Code"),
    N.code(tabulation_code),
    N.h3("Line by Line"),
    lbl("dp = [1] * n", "base case: every single element is a valid LIS of length 1 by itself"),
    lbl("for i in range(1, n):", "process each element left to right (forward fill ensures all subproblems solved before use)"),
    lbl("for j in range(i):", "consider every element to the left of i as a potential predecessor"),
    lbl("if nums[j] < nums[i]:", "can only extend if strictly less (strictly increasing requirement)"),
    lbl("dp[i] = max(dp[i], dp[j] + 1)", "extend the LIS ending at j by one; keep the maximum seen"),
    lbl("return max(dp)", "longest of all possible endpoints -- NOT dp[-1] which is only the LIS ending at the last element"),
    N.callout("Common mistake: returning dp[-1] instead of max(dp). dp[-1] is the LIS ending at the LAST element, not the global longest. Example: [3,5,6,2,5,4,19,5,6,7,12] -- the LIS does not end at the last element.", "⚠️", "yellow_background"),
    N.divider(),
]

# ── SOLUTION 4: Patience Sort / Binary Search ─────────────────────────────────
patience_code = (
    "import bisect\n\n"
    "def lengthOfLIS(nums):\n"
    "    tails = []  # tails[i] = smallest tail of all LIS of length i+1\n\n"
    "    for num in nums:\n"
    "        pos = bisect.bisect_left(tails, num)\n\n"
    "        if pos == len(tails):\n"
    "            tails.append(num)   # Extends longest subsequence\n"
    "        else:\n"
    "            tails[pos] = num    # Replace: keep smallest possible tail\n\n"
    "    return len(tails)\n"
)

blocks += [
    N.h2("Solution 4 - Patience Sorting + Binary Search  [O(n log n), Optimal]"),
    N.toggle_h3("Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Think of tails[i] as: 'The smallest number that could be the (i+1)-th element of any increasing subsequence of length i+1, considering all elements processed so far.' We keep tails as small as possible, because smaller tails let more future elements extend."),
        N.h4("What Doesn't Work"),
        N.para("The O(n^2) tabulation scans all j < i for each i. Can we find the right insertion point faster? Yes -- the tails array is always strictly sorted (invariant), so binary search finds the position in O(log n)."),
        N.h4("The Key Observation - Patience Sorting"),
        N.para("Named after the card game Patience (solitaire). Deal cards left to right; place each card on the leftmost pile whose top card >= current card. If no pile qualifies, start a new one. Number of piles = LIS length. tails[i] = top of pile i."),
        N.h4("Building the Solution"),
        N.para("For each num, binary search tails for leftmost pos where tails[pos] >= num. If pos == len(tails), append (new longest). Otherwise replace tails[pos] = num (keep tail small). Replacing does NOT change len(tails) -- it only improves future extensibility."),
        N.callout("WARNING: The tails array does NOT represent an actual LIS! Elements of tails may not form a valid increasing subsequence. Only len(tails) is meaningful as the answer. To reconstruct the actual sequence, you need a separate parent[] tracking array.", "⚠️", "yellow_background"),
    ]),
    N.h3("Algorithm Deep-Dive: Patience Sorting + Binary Search"),
    N.para(N.rich([
        ("Algorithm Origin: ", {"bold": True}),
        ("Patience Sorting is a card-game strategy. The LIS connection was formalised by Aldous & Diaconis (1999). "
         "This is the standard O(n log n) LIS algorithm in competitive programming.\n\n", {}),
        ("Core Invariant: ", {"bold": True}),
        ("tails is always strictly sorted. tails[i] = minimum possible tail value of any increasing "
         "subsequence of exactly length i+1, considering all elements processed so far.\n\n", {}),
        ("Why It Works: ", {"bold": True}),
        ("If tails[pos-1] < num <= tails[pos], replacing tails[pos] = num is safe: "
         "(1) subsequences of length <= pos still have valid tails at indices < pos, "
         "(2) making tails[pos] smaller gives more future elements a chance to extend to length pos+1.\n\n", {}),
        ("Generalisations: ", {"bold": True}),
        ("Non-strictly increasing: change bisect_left to bisect_right. "
         "Longest Decreasing Subsequence: negate all elements, run LIS. "
         "Russian Doll Envelopes (2D LIS): sort by width asc / height desc, LIS on heights.\n\n", {}),
        ("Recognize when: ", {"bold": True}),
        ("'O(n log n) required for LIS', 'binary search on sorted bookkeeping array', '2D envelope/chain problem'.", {}),
    ])),
    N.h3("Code"),
    N.code(patience_code),
    N.h3("Line by Line"),
    lbl("tails = []", "the patience pile tops; tails[i] = smallest tail value of any LIS of length i+1"),
    lbl("pos = bisect.bisect_left(tails, num)", "binary search O(log n): find leftmost index where tails[pos] >= num"),
    lbl("if pos == len(tails):", "num is larger than all current tails; we found a strictly longer subsequence"),
    lbl("tails.append(num)", "extend: create a new pile / increment the LIS length by 1"),
    lbl("else: tails[pos] = num", "replace: keep the smallest possible tail for subsequences of length pos+1"),
    lbl("return len(tails)", "number of piles = LIS length. Note: tails itself may not be a valid LIS!"),
    N.divider(),
]

# ── COMPLEXITY ────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Brute Force Recursion", "O(2^n)", "O(n) stack", "Exponential -- intuition only"],
        ["Memoization (Top-Down DP)", "O(n^2)", "O(n^2)", "n^2 states x O(1) per state"],
        ["Tabulation (Bottom-Up DP)", "O(n^2)", "O(n)", "Two nested loops; clean DP interview answer"],
        ["Patience / Binary Search", "O(n log n)", "O(n)", "Optimal -- use for follow-up question"],
    ]),
    N.divider(),
]

# ── PATTERN CLASSIFICATION ────────────────────────────────────────────────────
blocks += [
    N.h2("Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Dynamic Programming", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("DP: LIS, Binary Search O(n log n) (Patience Sorting)", {})])),
    N.callout(
        N.rich([
            ("When to recognize this pattern:\n", {"bold": True}),
            ("- Problem asks for the longest subsequence with a monotone property (increasing, decreasing)\n"
             "- Elements must be taken in original order but need not be contiguous\n"
             "- 'Follow-up: can you do O(n log n)?' signals patience sort / binary search on tails\n"
             "- 2D problems (Russian Doll Envelopes) often reduce to 1D LIS on one dimension\n"
             "- 'Minimum number of chains/groups' -- often LIS dual via Dilworth's theorem", {}),
        ]),
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── RELATED PROBLEMS ──────────────────────────────────────────────────────────
blocks += [
    N.h2("Related Problems"),
    N.para("Problems using the same DP: LIS or Patience Sort technique:"),
    N.bullet(N.rich([("Russian Doll Envelopes", {"bold": True}), (" (Hard) -- Sort by width asc, height desc; LIS on heights. Direct 2D LIS reduction via patience sort.", {})])),
    N.bullet(N.rich([("Number of Longest Increasing Subsequences", {"bold": True}), (" (Medium) -- Extend LIS DP with a count[] array alongside dp[]; track ways to reach each length.", {})])),
    N.bullet(N.rich([("Increasing Triplet Subsequence", {"bold": True}), (" (Medium) -- Fixed k=3 LIS version; O(n) with just two variables (first, second) -- same patience sort idea.", {})])),
    N.bullet(N.rich([("Maximum Length of Pair Chain", {"bold": True}), (" (Medium) -- LIS on intervals sorted by start; greedy also works. Good bridge from LIS to interval scheduling.", {})])),
    N.bullet(N.rich([("Longest Arithmetic Subsequence", {"bold": True}), (" (Medium) -- DP on pairs (index, common difference); similar state design to LIS.", {})])),
    N.bullet(N.rich([("Longest Increasing Path in a Matrix", {"bold": True}), (" (Hard) -- DFS + memo on grid; each cell's LIS from it = 1 + max of valid neighbors.", {})])),
    N.bullet(N.rich([("Longest String Chain", {"bold": True}), (" (Medium) -- LIS variant where 'increasing' = predecessor has one letter removed. Sort by length, DP.", {})])),
    N.bullet(N.rich([("Delete Columns to Make Sorted III", {"bold": True}), (" (Hard) -- LIS on column subsets; same recurrence structure, different domain.", {})])),
    N.para("These problems share the core technique: defining dp[i] as the answer 'ending at i' and scanning backwards, or maintaining sorted tails array with binary search."),
    N.callout("Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 18 -- Dynamic Programming -> DP: LIS sub-pattern", "📚", "gray_background"),
    N.divider(),
]

# ── EMBED ─────────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Interactive Visual Explainer"),
    N.embed(N.embed_url_for("longest_increasing_subsequence")),
    N.para(N.rich([
        ("Step through the algorithm visually -- use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"}),
    ])),
]

# ── 4) Append all blocks ──────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK -- appended {len(blocks)} blocks to {PAGE_ID}")
