"""
gen_russian_doll_envelopes.py — Notion rebuild for Russian Doll Envelopes (LC #354)
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81c4-82c3-f739b912855e"

# ─── Step 1: Set page properties ────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=354,
    pattern="Dynamic Programming",
    subpatterns=["Sort + LIS (Binary Search)", "DP: LIS"],
    tc="O(n log n)",
    sc="O(n)",
    key_insight="Sort by (width ASC, height DESC for ties), then find LIS on heights — same-width envelopes appear in decreasing height order so at most one per group enters the chain.",
    icon="🔴"
)
print("Properties set.")

# ─── Step 2: Wipe existing body ─────────────────────────────────────────────
print("Wiping existing body...")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ─── Step 3: Build body blocks ──────────────────────────────────────────────
BRUTE_CODE = """\
def maxEnvelopes_brute(envelopes):
    # Try every possible subset of envelopes
    # Check if they form a valid nesting chain
    from itertools import permutations
    n = len(envelopes)
    best = 1
    for length in range(2, n + 1):
        for perm in permutations(range(n), length):
            chain = [envelopes[i] for i in perm]
            valid = all(chain[k][0] < chain[k+1][0] and chain[k][1] < chain[k+1][1]
                        for k in range(len(chain) - 1))
            if valid:
                best = max(best, length)
    return best

# Time:  O(n! * n) -- factorial, completely impractical
# Space: O(n)
"""

N2_CODE = """\
def maxEnvelopes_dp(envelopes):
    # Sort by both dimensions ascending -- safe for O(n^2) since we check both
    envelopes.sort()
    n = len(envelopes)
    # dp[i] = length of longest valid chain ending at envelope i
    dp = [1] * n
    for i in range(n):
        for j in range(i):
            w1, h1 = envelopes[j]
            w2, h2 = envelopes[i]
            # j strictly fits inside i?
            if w1 < w2 and h1 < h2:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)

# Time:  O(n^2) -- two nested loops over envelopes
# Space: O(n) -- dp array of length n
"""

MEMO_CODE = """\
from functools import lru_cache

def maxEnvelopes_memo(envelopes):
    # Sort by (width ASC, height ASC) for memoization
    envelopes = sorted(envelopes)
    n = len(envelopes)

    @lru_cache(maxsize=None)
    def dp(i):
        # Longest chain starting at envelope i (i is the innermost)
        best = 1
        for j in range(i + 1, n):
            w1, h1 = envelopes[i]
            w2, h2 = envelopes[j]
            if w1 < w2 and h1 < h2:
                best = max(best, 1 + dp(j))
        return best

    return max(dp(i) for i in range(n))

# Time:  O(n^2) -- each dp(i) computed once, O(n) work each
# Space: O(n) -- memoization cache + recursion stack
"""

OPTIMAL_CODE = """\
import bisect

def maxEnvelopes(envelopes):
    # TRICK: sort width ASC, but for same width sort height DESC
    # Same-width heights appear DECREASING -> LIS picks at most one per group
    envelopes.sort(key=lambda x: (x[0], -x[1]))

    # Patience sort tails array for O(n log n) LIS
    # tails[k] = smallest possible ending height for IS of length k+1
    tails = []

    for _, h in envelopes:
        # Binary search: find first position where tails[pos] >= h
        pos = bisect.bisect_left(tails, h)

        if pos == len(tails):
            # h is larger than all tails -- EXTEND the LIS
            tails.append(h)
        else:
            # Record smaller tail for IS of length pos+1 (more extensible)
            tails[pos] = h

    # len(tails) = LIS length = max nesting depth
    return len(tails)

# Time:  O(n log n) -- sort O(n log n) + n * O(log n) binary searches
# Space: O(n) -- tails array
"""

blocks = []

# ── Problem ──────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        "Given an array of envelopes where ",
        ("envelopes[i] = [w_i, h_i]", {"code": True}),
        ", representing the width and height of an envelope, return the maximum number of envelopes you can Russian doll (put one inside the other). ",
        "Envelope A fits inside envelope B if and only if both ",
        ("A.width < B.width", {"code": True}),
        " AND ",
        ("A.height < B.height", {"code": True}),
        " (strictly less than on both dimensions)."
    ])),
    N.para(N.rich([
        ("Example: ", {"bold": True}),
        ("envelopes = [[5,4],[6,4],[6,7],[2,3]]", {"code": True}),
        " => Output: ",
        ("3", {"code": True}),
        ". The maximum chain is [2,3] -> [5,4] -> [6,7]."
    ])),
    N.divider(),
]

# ── Solution 1: Brute Force ──────────────────────────────────────────────────
blocks += [
    N.h2("Solution 1 -- Brute Force (Try All Orderings)"),
    N.toggle_h3("Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need the longest sequence of envelopes where each one strictly fits inside the next on both width and height. This is like finding the longest chain where every link satisfies a two-dimensional 'fits inside' relationship."),
        N.h4("What Doesn't Work (and Why We'd Try It First)"),
        N.para("The most obvious approach: try every possible ordering of every subset of envelopes, check if each ordering forms a valid nesting chain, track the maximum length. This is guaranteed correct but catastrophically slow at O(n! * n)."),
        N.h4("The Key Observation"),
        N.para("For a subset to form a valid chain, there is exactly one valid ordering (sorted by width, then height). So we only need to check subsets, not permutations. Still exponential O(2^n), but this observation clarifies why sorting is useful."),
        N.h4("Building the Solution"),
        N.para("Generate all subsets. For each subset, sort it by (width, height). Check if every adjacent pair satisfies the strict < condition on both dimensions. Return the maximum valid subset length."),
        N.callout("Analogy: Trying every possible way to stack Russian dolls by hand and checking if each stacking is valid.", "💡", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(BRUTE_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("for length in range(2, n+1)", {"code": True}), " -- Try chains of lengths 2 to n."])),
    N.para(N.rich([("for perm in permutations(range(n), length)", {"code": True}), " -- Try every ordered selection of `length` envelope indices."])),
    N.para(N.rich([("valid = all(...)", {"code": True}), " -- Check every consecutive pair: w[k] < w[k+1] AND h[k] < h[k+1]."])),
    N.para(N.rich([("best = max(best, length)", {"code": True}), " -- Track the longest valid chain seen."])),
    N.divider(),
]

# ── Solution 2: Classic O(n^2) DP ─────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 -- Classic DP Tabulation O(n^2) (Understand the Recurrence)"),
    N.toggle_h3("Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("This is the Longest Increasing Subsequence (LIS) problem extended to 2D. For 1D LIS we define dp[i] = longest IS ending at index i. Here: dp[i] = longest valid nesting chain ending at envelope i."),
        N.h4("What Doesn't Work (and Why DP Helps)"),
        N.para("Brute force checks all orderings. DP eliminates redundancy: if we already know the best chain ending at each earlier envelope, we only need to check which earlier envelopes fit inside envelope i and take the best."),
        N.h4("The Key Observation -- Optimal Substructure"),
        N.para("The longest chain ending at envelope i is 1 plus the max dp[j] over all j where envelope j strictly fits inside i. Optimal subproblem solutions (best chain ending at j) compose directly into optimal solutions for larger problems."),
        N.h4("Building the Solution"),
        N.para("Sort by (width, height) both ASC to enable the O(n^2) scan. Fill dp left to right. Return max(dp)."),
        N.callout("For each envelope, ask: 'What is the longest chain if I use this envelope as the outermost?' Check all valid predecessors.", "💡", "blue_background"),
    ]),
    N.h3("Why is This Dynamic Programming?"),
    N.para(N.rich([("Optimal Substructure: ", {"bold": True}), "The longest chain ending at envelope i optimally depends on the longest chains ending at all valid predecessors j. Optimal sub-solutions compose to give the optimal overall solution."])),
    N.para(N.rich([("Overlapping Subproblems: ", {"bold": True}), "Many envelopes share the same set of valid predecessors. Without the dp[] cache, we would recompute identical sub-chains repeatedly."])),
    N.code("# The Recurrence:\n# dp[i] = 1 + max(dp[j] for all j < i where w[j] < w[i] and h[j] < h[i])\n# dp[i] = 1  (base: each envelope alone is a chain of length 1)\n# answer  = max(dp)", "plain text"),
    N.h3("Code"),
    N.code(N2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("envelopes.sort()", {"code": True}), " -- Sort by (w, h) both ASC; for O(n^2) DP we check both dimensions explicitly so this simpler sort is fine."])),
    N.para(N.rich([("dp = [1] * n", {"code": True}), " -- Every envelope alone forms a valid chain of length 1 (base case)."])),
    N.para(N.rich([("for i in range(n)", {"code": True}), " -- Consider each envelope i as the outermost (largest) envelope of its chain."])),
    N.para(N.rich([("for j in range(i)", {"code": True}), " -- Try all earlier envelopes j as potential predecessors (the innermost of i's chain)."])),
    N.para(N.rich([("if w1 < w2 and h1 < h2", {"code": True}), " -- Check the strict 2D nesting condition: j fits strictly inside i."])),
    N.para(N.rich([("dp[i] = max(dp[i], dp[j] + 1)", {"code": True}), " -- Extend the best chain ending at j by one (add i as the new outermost)."])),
    N.para(N.rich([("return max(dp)", {"code": True}), " -- The answer is the longest chain ending at any single envelope."])),
    N.divider(),
]

# ── Solution 3: Memoization (Top-Down) ───────────────────────────────────────
blocks += [
    N.h2("Solution 3 -- Top-Down Memoization (Recursive + lru_cache)"),
    N.toggle_h3("Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same recurrence as Solution 2, but computed recursively. dp(i) = longest chain starting at envelope i as the innermost. For each j > i where i fits inside j, recurse into dp(j) and take the max."),
        N.h4("The Key Observation"),
        N.para("lru_cache ensures each dp(i) is computed once. The recursion naturally flows from the smallest (innermost) envelopes outward to the largest."),
        N.h4("Building the Solution"),
        N.para("Sort envelopes. Define dp(i) recursively with lru_cache. Return max(dp(i) for all i)."),
        N.callout("Memoization is DP 'top-down': solve from the goal backward to base cases, caching results to avoid recomputation.", "💡", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(MEMO_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("@lru_cache(maxsize=None)", {"code": True}), " -- Python decorator caching function results. Any dp(i) with the same i returns the cached answer instantly."])),
    N.para(N.rich([("def dp(i)", {"code": True}), " -- Returns the longest chain starting at envelope i (i is the innermost of the chain)."])),
    N.para(N.rich([("for j in range(i+1, n)", {"code": True}), " -- Look at all larger-indexed envelopes (sorted, so potentially larger envelopes)."])),
    N.para(N.rich([("best = max(best, 1 + dp(j))", {"code": True}), " -- Chain: envelope i inside j, then whatever dp(j) found recursively."])),
    N.para(N.rich([("return max(dp(i) for i in range(n))", {"code": True}), " -- Try every starting point as the innermost envelope."])),
    N.callout("Both O(n^2) approaches (tabulation and memoization) produce the same time complexity. The O(n log n) patience sort below is needed for large inputs (n up to 100,000).", "⚠️", "yellow_background"),
    N.divider(),
]

# ── Solution 4: Optimal Sort + Patience Sort LIS ─────────────────────────────
blocks += [
    N.h2("Solution 4 -- Sort + Patience Sort LIS O(n log n) -- Interview Pick"),
    N.toggle_h3("Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("After sorting by width, the width constraint is handled for consecutive elements. We then need the Longest Increasing Subsequence on heights. But same-width envelopes can never nest (width is not strictly less), so we need a sorting trick to exclude them."),
        N.h4("What Doesn't Work -- Why O(n^2) Is Insufficient"),
        N.para("For n up to 100,000 (LC #354 constraints), O(n^2) exceeds the time limit. We need the O(n log n) LIS algorithm using binary search on a 'tails' array."),
        N.h4("The Key Observation -- The Same-Width Trick"),
        N.para("Sort by (width ASC, height DESC for ties). Within any group of same-width envelopes, their heights appear in DECREASING order in our sorted array. An increasing subsequence can pick at most one element from a decreasing sequence. So LIS on the resulting heights automatically excludes invalid same-width pairs."),
        N.h4("The Patience Sort LIS"),
        N.para("Maintain tails[] where tails[k] = smallest possible ending height for an IS of length k+1. For each height h: binary search for leftmost pos where tails[pos] >= h. If pos == len(tails): append (LIS grows). Else: replace tails[pos] = h (better tail, same length). Return len(tails)."),
        N.callout("Patience sort analogy: deal cards onto piles, always placing on the leftmost pile whose top >= current card, or start a new pile. Number of piles = LIS length.", "💡", "blue_background"),
    ]),
    N.h3("Algorithm Deep-Dive: Patience Sort LIS"),
    N.para(N.rich([("Origin: ", {"bold": True}), "Based on patience sorting (card game analysis). O(n log n) LIS via binary search was established by Fredman (1975) and is part of standard algorithms curricula."])),
    N.para(N.rich([("Core Invariant: ", {"bold": True}), "After processing any prefix, tails is strictly increasing where tails[k] holds the minimum possible ending value for any IS of length k+1 seen so far."])),
    N.para(N.rich([("Why It Works: ", {"bold": True}), "The replace operation never decreases any IS length -- it only records that the same length is achievable with a smaller (better) tail. The sorted property enables O(log n) binary search. Each append strictly increases the count."])),
    N.para(N.rich([("Recognize When: ", {"bold": True}), "Problem asks for LIS length. Constraints: n up to 10^5. Keywords: 'longest increasing', 'maximum chain', 'nested sequence', 'strictly greater than previous'."])),
    N.h3("Code"),
    N.code(OPTIMAL_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("import bisect", {"code": True}), " -- Python's built-in binary search module."])),
    N.para(N.rich([("envelopes.sort(key=lambda x: (x[0], -x[1]))", {"code": True}), " -- Sort by width ASC; for same width, negate height to sort height DESC. This single line is the critical trick."])),
    N.para(N.rich([("tails = []", {"code": True}), " -- Patience sort tails array. Length at end = LIS length. Never shrinks."])),
    N.para(N.rich([("for _, h in envelopes:", {"code": True}), " -- Discard width (handled by sort). Only process heights for LIS."])),
    N.para(N.rich([("pos = bisect.bisect_left(tails, h)", {"code": True}), " -- O(log n) binary search: first index where tails[pos] >= h. If h > all, pos = len(tails)."])),
    N.para(N.rich([("if pos == len(tails): tails.append(h)", {"code": True}), " -- h extends the LIS. Start a new 'pile'. LIS length +1."])),
    N.para(N.rich([("else: tails[pos] = h", {"code": True}), " -- Record smaller tail for IS of length pos+1. Same IS length, but more extensible for future elements."])),
    N.para(N.rich([("return len(tails)", {"code": True}), " -- len(tails) = number of piles = LIS length = max nesting depth."])),
    N.callout("Common Mistake: thinking tails is a valid nesting sequence. It is NOT. tails[k] may come from a completely different chain than tails[k-1]. Only the length matters, not the elements.", "⚠️", "yellow_background"),
    N.divider(),
]

# ── Complexity ────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Brute Force (all orderings)", "O(n! * n)", "O(n)", "Never use"],
        ["Classic DP tabulation", "O(n^2)", "O(n)", "Good for understanding recurrence"],
        ["Memoization top-down", "O(n^2)", "O(n)", "Same as tabulation, recursive"],
        ["Sort + Patience Sort LIS", "O(n log n)", "O(n)", "Interview pick -- required for n=10^5"],
    ]),
    N.divider(),
]

# ── Pattern Classification ────────────────────────────────────────────────────
blocks += [
    N.h2("Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Dynamic Programming"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "DP: LIS (Longest Increasing Subsequence) -- specifically the O(n log n) Patience Sort variant. Sort + LIS is the 2D generalization technique."])),
    N.para(N.rich([("Why DP: ", {"bold": True}), "Optimal substructure (best chain ending at i depends on best chains ending at valid predecessors j) plus overlapping subproblems (multiple envelopes share the same valid predecessors -- dp[j] is reused for many i)."])),
    N.callout(
        "When to recognize this pattern:\n"
        "- 'Maximum length chain where each element satisfies some relation with the previous'\n"
        "- 2D version: 'one object fits inside another on multiple dimensions'\n"
        "- Keywords: 'Russian doll', 'nest', 'strictly increasing in both X and Y'\n"
        "- LIS signal: n up to 10^5 and you need O(n log n)",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ───────────────────────────────────────────────────────────
blocks += [
    N.h2("Related Problems"),
    N.para("Problems using the same LIS / patience sort technique:"),
    N.bullet(N.rich([("Longest Increasing Subsequence (#300)", {"bold": True}), " (Medium) -- The 1D version of this exact problem. Solve this first; Russian Doll Envelopes extends it to 2D with the sorting trick."])),
    N.bullet(N.rich([("Maximum Length of Pair Chain (#646)", {"bold": True}), " (Medium) -- Given pairs [a, b] where b < next a, find the longest chain. Sort by second element and apply greedy or LIS."])),
    N.bullet(N.rich([("Increasing Triplet Subsequence (#334)", {"bold": True}), " (Medium) -- Special case: LIS of length exactly 3. Solved with three-variable tracking, no full DP needed."])),
    N.bullet(N.rich([("Longest Divisible Subset (#368)", {"bold": True}), " (Medium) -- LIS variant where 'increasing' means divisibility. Same DP recurrence, different comparator."])),
    N.bullet(N.rich([("Number of Longest Increasing Subsequences (#673)", {"bold": True}), " (Medium) -- Count (not just find length of) all LIS sequences. O(n^2) DP with length and count arrays."])),
    N.bullet(N.rich([("Minimum Number of Arrows to Burst Balloons (#452)", {"bold": True}), " (Medium) -- Interval scheduling variant. Sort by end coordinate, greedy interval merging."])),
    N.bullet(N.rich([("Delete Columns to Make Sorted III (#960)", {"bold": True}), " (Hard) -- Minimum column deletions so remaining columns form LIS across all rows."])),
    N.bullet(N.rich([("Longest String Chain (#1048)", {"bold": True}), " (Medium) -- LIS on words where predecessor = word with one letter removed. Sort by length, apply LIS-style DP."])),
    N.para("These problems share the core technique: define a 'compatible predecessor' relation, sort to enable efficient lookup, then apply LIS (O(n^2) DP or O(n log n) patience sort)."),
    N.callout("Reference: DSA_Patterns_and_SubPatterns_Guide.md -- Section 18: Dynamic Programming, DP: LIS sub-pattern.", "📚", "gray_background"),
]

# ── Interactive Explainer ─────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("Interactive Visual Explainer"),
    N.embed(N.embed_url_for("russian_doll_envelopes")),
    N.para(N.rich([
        ("Step through the algorithm visually -- use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ─── Step 4: Append all blocks ───────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks to Notion page...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
