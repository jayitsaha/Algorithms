"""
Notion update script for: Longest Arithmetic Subsequence (#1027)
Run from: /Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms/
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-81a8-bd31-ce3e06306f00"
SLUG = "longest_arithmetic_subsequence"

# ── 1) Set properties ────────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=1027,
    pattern="Dynamic Programming",
    subpatterns=["dp[i][diff] length"],
    tc="O(n²)",
    sc="O(n²)",
    key_insight="State dp[i][d]=length of longest AP ending at i with diff d; extend via dp[j].get(d,1)+1 for all j<i.",
    icon="🟡"
)
print("Properties set.")

# ── 2) Wipe existing body ────────────────────────────────────────────────────
print("Wiping old blocks...")
removed = N.wipe_page(PAGE_ID)
print(f"Removed {removed} blocks.")

# ── 3) Build body blocks ─────────────────────────────────────────────────────
print("Building blocks...")
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an integer array "),
        ("nums", {"code": True}),
        (", return the length of the longest arithmetic subsequence in "),
        ("nums", {"code": True}),
        (". A subsequence is arithmetic if the difference between consecutive elements is constant. A subsequence preserves order but need not use consecutive elements."),
    ])),
    N.para(N.rich([
        ("Example 1: "),
        ("nums = [3, 6, 9, 12]", {"code": True}),
        (" → Output: "),
        ("4", {"bold": True}),
        (" (sequence [3,6,9,12] with diff=3)"),
    ])),
    N.para(N.rich([
        ("Example 2: "),
        ("nums = [9, 4, 7, 2, 10]", {"code": True}),
        (" → Output: "),
        ("3", {"bold": True}),
        (" (sequence [4,7,10] with diff=3, using indices 1,2,4)"),
    ])),
    N.callout(
        N.rich([
            ("Constraints: ", {"bold": True}),
            ("2 ≤ nums.length ≤ 1000; 0 ≤ nums[i] ≤ 500. Answer is always ≥ 2.")
        ]),
        "📌", "gray_background"
    ),
    N.divider(),
]

# ── Solution 1: DP Tabulation (Interview Pick) ──
blocks += [
    N.h2("Solution 1 — DP Tabulation / Bottom-Up (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We want the longest subsequence where the gap between consecutive chosen elements is always the same constant. The moment you fix a 'last element' and a 'common difference,' the chain is characterized. So ask: what is the longest chain ending at each position, for every possible difference?"),
        N.h4("What Doesn't Work"),
        N.para("Brute force fixes a start index and a difference, then scans right — O(n³). It re-computes every chain from scratch. Greedy (pick nearest element with correct diff) fails because the optimal subsequence may skip nearer elements to pick farther ones that extend a longer chain."),
        N.h4("The Key Observation"),
        N.para("Two numbers determine a unique difference. If position j has a chain of length L with difference d, and nums[i] − nums[j] = d, then position i can extend that chain to length L+1. We store this: dp[i][d] = L+1. This is the dp[i][diff] DP pattern — analogous to LIS but parameterized by difference instead of 'must be increasing.'"),
        N.h4("Building the Solution"),
        N.para("1. dp = list of empty dicts, one per position.\n2. For each pair (j < i): d = nums[i] - nums[j]. dp[i][d] = dp[j].get(d, 1) + 1. The default of 1 means 'j alone is length 1; adding i makes it 2.'\n3. Track the global max throughout. Return it."),
        N.callout("Analogy: Relay race. Each runner i asks all prior runners j: 'Were you running at my pace d? If so, take your baton count and add one.' dp[j][d] records how many legs runner j's team has run at pace d.", "🧠", "blue_background"),
    ]),
    N.h3("Why Is This Dynamic Programming?"),
    N.para(N.rich([
        ("Optimal Substructure: ", {"bold": True}),
        ("The longest AP ending at i with diff d = 1 + (longest AP ending at some j < i with same d where nums[i]−nums[j]=d). Big problem solved by smaller ones."),
    ])),
    N.para(N.rich([
        ("Overlapping Subproblems: ", {"bold": True}),
        ("dp[j][d] is queried by every later i where nums[i]−nums[j]=d. Many i's will share the same j-and-d pair. Without memoization, these recomputations blow up exponentially."),
    ])),
    N.h3("Recurrence Relation"),
    N.code(
        "State: dp[i][d] = length of longest AP ending at index i with common difference d\n\n"
        "Transition:\n"
        "  For each pair (j, i) with j < i:\n"
        "      d = nums[i] - nums[j]\n"
        "      dp[i][d] = dp[j].get(d, 1) + 1\n\n"
        "Base case: dp[i] = {} (no chains known initially)\n"
        "Answer: max over all i, d of dp[i][d]   (initialized to 2)",
        "plain text"
    ),
    N.h3("Code"),
    N.code(
        "def longestArithSeqLength(nums: list) -> int:\n"
        "    n = len(nums)\n"
        "    dp = [dict() for _ in range(n)]  # dp[i]: diff -> chain length\n"
        "    ans = 2                           # min answer: any 2 elements\n"
        "    for i in range(1, n):\n"
        "        for j in range(i):\n"
        "            d = nums[i] - nums[j]\n"
        "            dp[i][d] = dp[j].get(d, 1) + 1\n"
        "            ans = max(ans, dp[i][d])\n"
        "    return ans\n",
        "python"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("dp = [dict() for _ in range(n)]", {"code": True}), (" — One empty dictionary per position. dp[i] will hold all (difference → length) pairs for subsequences ending at i.")])),
    N.para(N.rich([("ans = 2", {"code": True}), (" — Initialize to 2 because any two elements form an arithmetic subsequence. Guaranteed lower bound given constraints.")])),
    N.para(N.rich([("for i in range(1, n)", {"code": True}), (" — Outer loop: i is the 'current endpoint' we're building chains toward. We start at 1 because i=0 has no j to look back at.")])),
    N.para(N.rich([("for j in range(i)", {"code": True}), (" — Inner loop: j is the 'previous element' candidate. We check all positions before i.")])),
    N.para(N.rich([("d = nums[i] - nums[j]", {"code": True}), (" — The common difference if i directly follows j in the arithmetic sequence.")])),
    N.para(N.rich([("dp[i][d] = dp[j].get(d, 1) + 1", {"code": True}), (" — Extend the best chain ending at j with difference d by 1. Default 1 means 'j is alone, adding i makes length 2.'")])),
    N.para(N.rich([("ans = max(ans, dp[i][d])", {"code": True}), (" — Update global best if this chain is the longest seen so far.")])),
    N.callout(
        N.rich([
            ("⚠️ Critical Default: ", {"bold": True}),
            ("Use "),
            ("dp[j].get(d, 1)", {"code": True}),
            (", NOT "),
            ("dp[j].get(d, 0)", {"code": True}),
            (". If j has no chain for d, j itself is a valid element (length 1). Adding i gives 2. Default 0 would give 1 — wrong! This is the most common implementation bug.")
        ]),
        "⚠️", "yellow_background"
    ),
    N.divider(),
]

# ── Solution 2: DP Memoization (Top-Down) ──
blocks += [
    N.h2("Solution 2 — DP Memoization / Top-Down"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The recurrence dp(i, d) = 1 + max(dp(j, d)) for j < i where nums[i]-nums[j]=d maps naturally to recursion with memoization. Think: 'to know the best chain ending at i with diff d, recursively ask j for its best chain.'"),
        N.h4("What Doesn't Work"),
        N.para("Pure recursion without memoization recomputes dp(j, d) every time a different i needs it — exponential blowup."),
        N.h4("The Key Observation"),
        N.para("lru_cache automatically memoizes calls. Once dp(j, d) is computed, all future calls with the same (j, d) return immediately. This collapses the exponential tree into an O(n²) DAG."),
        N.h4("Building the Solution"),
        N.para("Define dp(i, d): look back at all j < i where nums[i]-nums[j]=d, recursively get dp(j, d)+1, take the max. Base: return 1 if no valid j found. Seed by calling dp(i, nums[i]-nums[j]) for all pairs."),
        N.callout("Top-down is easier to derive from the recurrence directly. Bottom-up (Solution 1) is easier to implement without recursion overhead.", "💡", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(
        "def longestArithSeqLength(nums: list) -> int:\n"
        "    from functools import lru_cache\n"
        "    n = len(nums)\n"
        "\n"
        "    @lru_cache(maxsize=None)\n"
        "    def dp(i, d):\n"
        "        # Best chain length ending at index i with difference d\n"
        "        best = 1  # i alone\n"
        "        for j in range(i):\n"
        "            if nums[i] - nums[j] == d:\n"
        "                best = max(best, dp(j, d) + 1)\n"
        "        return best\n"
        "\n"
        "    ans = 2\n"
        "    for i in range(n):\n"
        "        for j in range(i):\n"
        "            ans = max(ans, dp(i, nums[i] - nums[j]))\n"
        "    return ans\n",
        "python"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("@lru_cache(maxsize=None)", {"code": True}), (" — Python decorator that caches all (i, d) calls. First call computes; subsequent calls return the cached value. This is the memoization layer.")])),
    N.para(N.rich([("best = 1", {"code": True}), (" — Base case: i alone is a chain of length 1 (before any extension).")])),
    N.para(N.rich([("if nums[i] - nums[j] == d:", {"code": True}), (" — Only extend from j if j's value is exactly d less than nums[i], meaning j can directly precede i.")])),
    N.para(N.rich([("best = max(best, dp(j, d) + 1)", {"code": True}), (" — Recursively get the best chain ending at j, then extend by 1. Takes the max over all valid j.")])),
    N.callout(
        N.rich([
            ("⚠️ Recursion Limit Warning: ", {"bold": True}),
            ("Python's default recursion limit is 1000. For n=1000 (the problem constraint), this approach may hit the limit. Use "),
            ("sys.setrecursionlimit(10000)", {"code": True}),
            (" or prefer the iterative bottom-up Solution 1 in interviews.")
        ]),
        "⚠️", "yellow_background"
    ),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Brute Force (3 loops)", "O(n³)", "O(1)", "TLE for n=1000"],
        ["DP Tabulation (bottom-up)", "O(n²)", "O(n·D)", "D = distinct diffs per pos; Interview pick"],
        ["DP Memoization (top-down)", "O(n²)", "O(n²)", "Recursion overhead; limit risk in Python"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Dynamic Programming")])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("dp[i][diff] length — DP with dictionary state keyed by the derived property (common difference)")])),
    N.callout(
        N.rich([
            ("When to recognize this pattern: ", {"bold": True}),
            ("• 'Longest subsequence with constant X between consecutive elements'\n"
             "• State requires both position AND a derived key (difference, ratio, XOR)\n"
             "• Every pair (i, j) must be examined → O(n²) is the expected complexity\n"
             "• Similar to LIS but with a parameterized comparison instead of just '>'")
        ]),
        "🔎", "green_background"
    ),
    N.para(N.rich([
        ("Note: The 'dp[i][diff] length' sub-pattern is closely related to LIS (dp[i] = scalar) but extends it by adding a dictionary key dimension for the structural property. Not explicitly listed as its own sub-pattern in the guide — classified from analysis as a LIS variant.", {"italic": True})
    ])),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same dp[i][key] technique or closely related DP over pairs:"),
    N.bullet(N.rich([("Longest Increasing Subsequence", {"bold": True}), (" (Medium) — Special case: dp[i] = max length of increasing subseq ending at i; difference is implicitly >0 (#300)")])),
    N.bullet(N.rich([("Arithmetic Slices II — Subsequence", {"bold": True}), (" (Hard) — Count ALL arithmetic subsequences (not just longest) using the exact same dp[i][d] framework; sum counts instead of max length (#446)")])),
    N.bullet(N.rich([("Arithmetic Slices", {"bold": True}), (" (Medium) — Count contiguous arithmetic subarrays; simpler O(n) DP on adjacent differences — no subsequence jumping (#413)")])),
    N.bullet(N.rich([("Longest Fibonacci Subsequence", {"bold": True}), (" (Medium) — Same look-back DP but state is keyed by (prev, curr) pair instead of a single difference; dict-of-dicts (#873)")])),
    N.bullet(N.rich([("Number of Longest Increasing Subsequence", {"bold": True}), (" (Medium) — Track both length and count arrays in the LIS skeleton; same O(n²) pair comparison (#673)")])),
    N.bullet(N.rich([("Number of Arithmetic Triplets", {"bold": True}), (" (Easy) — Simpler variant: count index triplets (i<j<k) with fixed given difference k; O(n) with a set (#2367)")])),
    N.para("These problems share the core technique: for each pair (j, i), compute a key from the pair and look up/update a stored state at j with that key."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 18 (Dynamic Programming). Sub-pattern 'dp[i][diff] length' is a LIS variant with parameterized key.", "📚", "gray_background"),
    N.divider(),
]

# ── Interactive Visual Explainer ──
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys. Watch the dp table fill in as each (j, i) pair is processed and chains extend.", {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ──
print(f"Appending {len(blocks)} blocks...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
