"""
gen_burst_balloons.py — Notion page creation for LeetCode #312 Burst Balloons
Run from: /Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms/
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

# Override redacted token (other gen scripts use this pattern)
N.TOKEN = "NOTION_TOKEN_REDACTED"
N._HEADERS["Authorization"] = f"Bearer {N.TOKEN}"

SLUG = "burst_balloons"
PAGE_ID = None  # No existing page — create fresh

# ─── Step 1: Create the page ───────────────────────────────────────────────
print("Creating new Notion page...")
PAGE_ID = N.create_page("Burst Balloons", 312, "Hard", "🔴")
print(f"Created page: {PAGE_ID}")

# ─── Step 2: Set properties ─────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=312,
    pattern="Dynamic Programming",
    subpatterns=["Interval DP Last Burst"],
    tc="O(n³)",
    sc="O(n²)",
    key_insight="Think 'last burst': if k is the last balloon burst in (l,r), its neighbors are always the fixed boundaries l and r — enabling clean interval subproblems.",
    icon="🔴"
)
print("Properties set.")

# ─── Step 3: Append body blocks ─────────────────────────────────────────────
print("Building body blocks...")

PROBLEM_STATEMENT = (
    "Given n balloons indexed from 0 to n-1. Each balloon has a value nums[i]. "
    "Bursting balloon i (while neighbors left and right still exist) earns "
    "nums[left] * nums[i] * nums[right] coins. If there is no left or right neighbor, "
    "treat that boundary as 1. Return the maximum coins you can collect by bursting all balloons."
)

SOL1_CODE = """\
def maxCoins(nums: list[int]) -> int:
    # Pad with virtual boundaries (value 1) at both ends
    nums = [1] + nums + [1]
    n = len(nums)

    # dp[l][r] = max coins from bursting all balloons
    # strictly inside the open interval (l, r)
    dp = [[0] * n for _ in range(n)]

    # Iterate by increasing interval length
    # (ensures sub-intervals are solved before larger ones)
    for length in range(2, n):
        for l in range(n - length):
            r = l + length
            # Try every balloon k as the LAST to be burst in (l, r)
            for k in range(l + 1, r):
                # At burst time, k's neighbors are l and r (still present)
                coins = nums[l] * nums[k] * nums[r] + dp[l][k] + dp[k][r]
                dp[l][r] = max(dp[l][r], coins)

    # Full original array sits inside interval (0, n-1)
    return dp[0][n - 1]

# Example: nums = [3, 1, 5, 8] -> 167
"""

SOL2_CODE = """\
def maxCoins(nums: list[int]) -> int:
    nums = [1] + nums + [1]
    n = len(nums)
    from functools import lru_cache

    @lru_cache(maxsize=None)
    def dp(l, r):
        \"\"\"Max coins from open interval (l, r).\"\"\"
        if r - l < 2:
            return 0  # No balloon strictly inside
        return max(
            nums[l] * nums[k] * nums[r] + dp(l, k) + dp(k, r)
            for k in range(l + 1, r)
        )

    return dp(0, n - 1)

# Same O(n^3) / O(n^2) as tabulation; call stack overhead but more intuitive.
"""

blocks = []

# ── Problem ──────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(PROBLEM_STATEMENT),
    N.callout(
        N.rich([
            ("Example: ", {"bold": True}),
            ("nums = [3,1,5,8]", {"code": True}),
            (" → Output: ", {}),
            ("167", {"bold": True}),
            (". Optimal: burst 1 (coins 3×1×5=15), burst 5 (coins 3×5×8=120), burst 3 (coins 1×3×8=24), burst 8 (coins 1×8×1=8). Total = 167.", {})
        ]),
        "💡", "blue_background"
    ),
    N.divider(),
]

# ── Solution 1: Tabulation ────────────────────────────────────────────────────
blocks += [
    N.h2("Solution 1 — Bottom-Up Tabulation (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We need to find the optimal ORDER to burst all balloons. "
            "The key difficulty: after each burst, neighbors collapse, changing what we'd earn next time. "
            "Framing this as 'which to burst first' creates shifting subproblem boundaries."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Greedy (always burst max or min value first) fails because it misses compounding effects. "
            "Brute force (try all n! orderings) is O(n!) — too slow for n > 12. "
            "Even simple recursion without memoization recomputes the same intervals exponentially often."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Flip the question: instead of 'which to burst FIRST?', ask 'which is the LAST burst in a given interval?' "
            "If balloon k is the last burst in open interval (l, r), then at the moment of bursting k, "
            "its neighbors are ALWAYS l and r — fixed, stable boundaries. "
            "This gives us the clean, reusable subproblems we need for DP."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Pad nums with 1s at both ends: nums = [1] + nums + [1]. "
            "Define dp[l][r] = max coins from bursting all balloons strictly inside the open interval (l, r). "
            "Recurrence: dp[l][r] = max over k in (l,r) of nums[l]*nums[k]*nums[r] + dp[l][k] + dp[k][r]. "
            "Subproblems dp[l][k] and dp[k][r] are independent (k hasn't been burst when solving them). "
            "Fill from small intervals to large (by length), then return dp[0][n-1]."
        ),
        N.callout(
            "Analogy: Like demolishing a building floor-by-floor. Instead of deciding which floor to tear down first (messy), "
            "ask: which floor will be the LAST standing before the final implosion? "
            "That last floor determines what's around it — and everything else was handled independently before.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOL1_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([
        ("nums = [1] + nums + [1]", {"code": True}),
        (" — Add virtual boundary sentinels. These are never burst, but act as neighbors for the outermost balloons. Eliminates edge-case index checks.", {})
    ])),
    N.para(N.rich([
        ("dp = [[0]*n for _ in range(n)]", {"code": True}),
        (" — Create n×n table. dp[l][r] = max coins inside open interval (l, r). Initially all 0 (no balloon = no coins).", {})
    ])),
    N.para(N.rich([
        ("for length in range(2, n):", {"code": True}),
        (" — Outer loop: interval length. Must start at 2 (length 1 = single boundary, no interior). Ensures smaller intervals are filled first.", {})
    ])),
    N.para(N.rich([
        ("r = l + length", {"code": True}),
        (" — Right boundary is always l + length. This pair (l, r) defines our current open interval.", {})
    ])),
    N.para(N.rich([
        ("for k in range(l+1, r):", {"code": True}),
        (" — Try each balloon k as the last to be burst in (l, r). k must be strictly inside: not l or r themselves.", {})
    ])),
    N.para(N.rich([
        ("coins = nums[l]*nums[k]*nums[r] + dp[l][k] + dp[k][r]", {"code": True}),
        (" — Coins from bursting k last (l and r are still alive as neighbors) + best from left sub-interval + best from right sub-interval.", {})
    ])),
    N.para(N.rich([
        ("dp[l][r] = max(dp[l][r], coins)", {"code": True}),
        (" — Keep the maximum over all choices of k. dp[l][r] accumulates the best pivot.", {})
    ])),
    N.para(N.rich([
        ("return dp[0][n-1]", {"code": True}),
        (" — The entire original array is inside interval (0, n-1) after padding. This is the final answer.", {})
    ])),
    N.callout(
        "Why iterating by length works: dp[l][r] needs dp[l][k] and dp[k][r] where k is inside (l,r). Both sub-intervals have strictly smaller length than r-l. "
        "By processing length 2, 3, 4... upward, all needed sub-intervals are guaranteed to be filled before we need them.",
        "⚠️", "yellow_background"
    ),
    N.divider(),
]

# ── Solution 2: Memoization ───────────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Top-Down Memoization"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Same insight as tabulation: ask 'which balloon is the last burst?' in a given interval. "
            "But here, we express this directly as recursion, letting Python's call stack handle the dependency ordering."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Pure recursion without a cache will recompute dp(l, r) exponentially many times. "
            "The same interval (l, r) is needed by many larger intervals above it."
        ),
        N.h4("The Key Observation"),
        N.para(
            "There are only O(n²) distinct (l, r) pairs. Once computed, dp(l, r) is always the same value "
            "regardless of who called it. Cache it with @lru_cache — each state computed once."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Define dp(l, r) recursively: base case r-l<2 returns 0. Otherwise try all k as last pivot, "
            "take max. Decorate with @lru_cache so repeated calls return instantly. "
            "Same recurrence as tabulation, just expressed top-down."
        ),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([
        ("@lru_cache(maxsize=None)", {"code": True}),
        (" — Auto-memoize the recursive function. Python caches result for each unique (l, r) pair. Eliminates redundant recomputation.", {})
    ])),
    N.para(N.rich([
        ("if r - l < 2: return 0", {"code": True}),
        (" — Base case: no balloon strictly inside the open interval (l, r) → 0 coins.", {})
    ])),
    N.para(N.rich([
        ("return max(nums[l]*nums[k]*nums[r] + dp(l,k) + dp(k,r) for k in range(l+1, r))", {"code": True}),
        (" — Try every possible last pivot k, return the maximum. Same recurrence as tabulation, written as a generator expression.", {})
    ])),
    N.para(N.rich([
        ("return dp(0, n-1)", {"code": True}),
        (" — Entry point: solve the full padded interval. The recursive calls fill smaller intervals on demand.", {})
    ])),
    N.divider(),
]

# ── Complexity ────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Brute Force (all orderings)", "O(n!)", "O(n)", "Try all burst sequences — feasible only n≤12"],
        ["Memoization (top-down)", "O(n³)", "O(n²)", "O(n²) unique states × O(n) pivot choices each"],
        ["Tabulation (bottom-up) ✓", "O(n³)", "O(n²)", "Same complexity, no call stack overhead — preferred"],
    ]),
    N.divider(),
]

# ── Pattern Classification ─────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Dynamic Programming", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Interval DP Last Burst", {})])),
    N.para(N.rich([
        ("Why DP? ", {"bold": True}),
        ("Optimal Substructure: once k is fixed as last burst in (l,r), the problem splits into two independent sub-intervals whose optimal values add directly. "
         "Overlapping Subproblems: the same (l,r) interval is needed by many larger intervals — memoization/tabulation avoids recomputation.", {})
    ])),
    N.callout(
        "When to recognize Interval DP: (1) sequence problem requiring all elements processed in some order; "
        "(2) adjacent elements interact (cost depends on neighbors); "
        "(3) 'first action' framing gives shifting boundaries → flip to 'last action'; "
        "(4) optimal solution for a range = optimal for two sub-ranges + combination cost. "
        "Time complexity hint: O(n³) is typical for n ≤ 500.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ───────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Interval DP technique:"),
    N.bullet(N.rich([("Matrix Chain Multiplication", {"bold": True}),
        (" (Hard) — Minimize multiplications by choosing split order; exact same O(n³) skeleton with pivot = last matrix boundary", {})])),
    N.bullet(N.rich([("Strange Printer", {"bold": True}),
        (" (Hard) — Minimum printer turns for a string; dp[l][r] = min turns for substring; LeetCode #664", {})])),
    N.bullet(N.rich([("Minimum Cost to Merge Stones", {"bold": True}),
        (" (Hard) — Merge k adjacent piles; Interval DP with feasibility check; LeetCode #1000", {})])),
    N.bullet(N.rich([("Remove Boxes", {"bold": True}),
        (" (Hard) — Remove groups for k² coins; Interval DP with extra dimension tracking grouped boxes; LeetCode #546", {})])),
    N.bullet(N.rich([("Predict the Winner", {"bold": True}),
        (" (Medium) — Two players take from ends; dp[l][r] = score advantage; same interval structure; LeetCode #486", {})])),
    N.bullet(N.rich([("Zuma Game", {"bold": True}),
        (" (Hard) — Min moves to clear a row of balls; Interval DP with grouping; LeetCode #488", {})])),
    N.bullet(N.rich([("Palindrome Partitioning II", {"bold": True}),
        (" (Hard) — Min cuts for palindrome partition; Interval DP on substrings; LeetCode #132", {})])),
    N.para("These problems all share the core pattern: fix 'last action' in an interval, decompose into independent sub-intervals, fill by increasing length."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 18 (Dynamic Programming → Interval DP). Sub-Pattern: Interval DP Last Burst", "📚", "gray_background"),
    N.divider(),
]

# ── Embed ─────────────────────────────────────────────────────────────────────
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys. "
         "Watch the dp[l][r] table fill up interval by interval, with decision panels showing each pivot comparison.",
         {"italic": True, "color": "gray"})
    ])),
]

# ─── Append all blocks ───────────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"\nPAGE_ID = {PAGE_ID}")
