"""
gen_house_robber_ii.py — Notion IN-PLACE update for House Robber II (LC 213).
Run from: /Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms/
"""
import notion_lib as N

PAGE_ID = "39193418-809c-8113-adb7-ee148e9f78bf"
SLUG = "house_robber_ii"

# ─── 1. Properties ───────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=213,
    pattern="Dynamic Programming",
    subpatterns=["Two Passes: Exclude First/Last"],
    tc="O(n)",
    sc="O(1)",
    key_insight="Break the circular constraint into two linear DP passes: exclude last house, then exclude first. Take the max.",
    icon="🟡",
)
print("Properties set.")

# ─── 2. Wipe old body ────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ─── 3. Build body blocks ─────────────────────────────────────────
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are a robber on a ", {}),
        ("circular", {"bold": True}),
        (" street of ", {}),
        ("n", {"code": True}),
        (" houses. Each house ", {}),
        ("nums[i]", {"code": True}),
        (" has some money. Adjacent houses share a security alarm — robbing two neighbors triggers it. Because the street is ", {}),
        ("circular", {"italic": True}),
        (", house 0 and house n-1 are also neighbors. Return the maximum amount you can rob without activating any alarm.", {}),
    ])),
    N.para(N.rich([
        ("Example: ", {"bold": True}),
        ("nums = [2, 7, 9, 3, 1]", {"code": True}),
        (" → Output: ", {}),
        ("11", {"bold": True}),
        (" (rob houses 0 and 2: 2+9=11; house 4 excluded so no circular alarm).", {}),
    ])),
    N.divider(),
]

# ── Solution 1 — Two-Pass Bottom-Up DP ──
solution1_code = """def rob(nums: list[int]) -> int:
    if len(nums) == 1:
        return nums[0]          # single house: trivially return it

    def rob_linear(arr):
        \"\"\"House Robber I on any sub-array — O(n) time, O(1) space.\"\"\"
        pprev, prev = 0, 0      # best loot through i-2 and i-1
        for num in arr:
            curr = max(prev, pprev + num)   # skip house OR rob it
            pprev, prev = prev, curr        # slide rolling window
        return prev             # prev holds the final answer

    pass_a = rob_linear(nums[:-1])   # exclude last house → house 0 may be robbed
    pass_b = rob_linear(nums[1:])    # exclude first house → house n-1 may be robbed
    return max(pass_a, pass_b)       # best of both circular scenarios"""

blocks += [
    N.h2("Solution 1 — Two-Pass Bottom-Up DP (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("You need to pick a subset of houses to rob — no two adjacent — but the houses form a ring, so the first and last are also adjacent. What makes this hard is that picking house 0 constrains what you can pick at the end, and vice versa."),
        N.h4("What Doesn't Work"),
        N.para("Running House Robber I on the full circular array doesn't work — the recurrence doesn't know that house 0 and house n-1 are neighbors. Skipping both endpoints (nums[1..n-2]) is also wrong: it misses plans that include house 0 or house n-1 as the best choice."),
        N.h4("The Key Observation"),
        N.para("In any valid robbery plan, house 0 and house n-1 are mutually exclusive — you'll never rob both. Therefore, the optimal answer comes from either: (A) a plan that includes house 0 but not house n-1, or (B) a plan that includes house n-1 but not house 0. We can solve each scenario independently as a linear (non-circular) problem."),
        N.h4("Building the Solution"),
        N.para("Pass A: run rob_linear on nums[0..n-2] (house n-1 removed). Pass B: run rob_linear on nums[1..n-1] (house 0 removed). Return max(pass_a, pass_b). Each pass is the classic House Robber I recurrence with O(1) space rolling variables pprev and prev."),
        N.callout("Analogy: It's like deciding whether to start counting calories from Monday or Tuesday when your diet week loops around — you try both starting points and keep the better weekly total.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(solution1_code),
    N.h3("Line by Line"),
    N.para(N.rich([("if len(nums) == 1:", {"code": True}), (" — Edge case: a single house has no neighbor, return it directly.", {})])),
    N.para(N.rich([("def rob_linear(arr):", {"code": True}), (" — Inner helper that solves the linear (non-circular) House Robber I on any sub-array.", {})])),
    N.para(N.rich([("pprev, prev = 0, 0", {"code": True}), (" — Rolling DP state. pprev = best loot through i-2; prev = best loot through i-1. Both start at 0 (nothing robbed yet).", {})])),
    N.para(N.rich([("curr = max(prev, pprev + num)", {"code": True}), (" — The core recurrence: skip house i (keep prev) or rob it (pprev + num, since i-1 can't be robbed).", {})])),
    N.para(N.rich([("pprev, prev = prev, curr", {"code": True}), (" — Slide the window: yesterday's prev becomes pprev, today's curr becomes prev.", {})])),
    N.para(N.rich([("return prev", {"code": True}), (" — After the loop, prev holds the maximum achievable loot for the full arr.", {})])),
    N.para(N.rich([("pass_a = rob_linear(nums[:-1])", {"code": True}), (" — Exclude house n-1 (last). This range allows house 0 to be robbed freely.", {})])),
    N.para(N.rich([("pass_b = rob_linear(nums[1:])", {"code": True}), (" — Exclude house 0 (first). This range allows house n-1 to be robbed freely.", {})])),
    N.para(N.rich([("return max(pass_a, pass_b)", {"code": True}), (" — Every valid circular plan is covered by one of the two passes; take the best.", {})])),
    N.callout("Why is this correct? Because the two passes are exhaustive: any optimal solution either includes house 0 (covered by Pass A, which excludes the conflicting house n-1) or does not include house 0 (covered by Pass B, which may include house n-1). No valid plan is missed.", "✅", "green_background"),
    N.divider(),
]

# ── Solution 2 — Top-Down Memoization ──
solution2_code = """from functools import lru_cache

def rob(nums: list[int]) -> int:
    if len(nums) == 1:
        return nums[0]

    def rob_range(lo: int, hi: int) -> int:
        @lru_cache(maxsize=None)
        def dp(i: int) -> int:
            if i > hi:
                return 0                        # base: no more houses
            skip = dp(i + 1)                    # don't rob house i
            rob  = nums[i] + dp(i + 2)          # rob house i; skip i+1
            return max(skip, rob)
        result = dp(lo)
        dp.cache_clear()                        # reset for next call
        return result

    # Pass A: houses 0..n-2 | Pass B: houses 1..n-1
    return max(rob_range(0, len(nums) - 2),
               rob_range(1, len(nums) - 1))"""

blocks += [
    N.h2("Solution 2 — Top-Down Memoization"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Define dp(i) = maximum loot from house i to the end of the current range. At each house, we choose to skip or rob — the same binary decision as the bottom-up version, but expressed as top-down recursion."),
        N.h4("What Doesn't Work"),
        N.para("Naive recursion (without memoization) recomputes dp(i) exponentially — 2^n calls for an n-element range. We need to cache results."),
        N.h4("The Key Observation"),
        N.para("With @lru_cache, each (i) state is computed exactly once. The two-pass structure is identical to Solution 1 — we just call rob_range twice with different lo/hi bounds."),
        N.h4("Building the Solution"),
        N.para("dp(i) = max(dp(i+1), nums[i]+dp(i+2)). Base case: dp(i) = 0 when i > hi. Memoize with lru_cache. Call for Pass A (lo=0, hi=n-2) and Pass B (lo=1, hi=n-1). Clear cache between passes."),
    ]),
    N.h3("Code"),
    N.code(solution2_code),
    N.h3("Line by Line"),
    N.para(N.rich([("def dp(i):", {"code": True}), (" — Recursive function: returns max loot from house i to hi.", {})])),
    N.para(N.rich([("if i > hi: return 0", {"code": True}), (" — Base case: past the range boundary, no money to collect.", {})])),
    N.para(N.rich([("skip = dp(i + 1)", {"code": True}), (" — Option A: skip house i, move to the next house.", {})])),
    N.para(N.rich([("rob = nums[i] + dp(i + 2)", {"code": True}), (" — Option B: rob house i (i+1 is adjacent, skip it), jump to i+2.", {})])),
    N.para(N.rich([("dp.cache_clear()", {"code": True}), (" — Critical: clear the memoization cache so Pass B starts fresh. Without this, Pass B inherits stale cache entries from Pass A's different index range.", {})])),
    N.callout("When to use memoization over tabulation: Memoization is easier to derive from the recurrence definition and handles sparse state spaces well. Use it when first working out the recurrence; switch to tabulation for interview or production code where stack depth and O(n) space are concerns.", "💡", "gray_background"),
    N.divider(),
]

# ── Why Is This DP? ──
blocks += [
    N.h2("🧠 Why Is This Dynamic Programming?"),
    N.para(N.rich([
        ("Optimal Substructure: ", {"bold": True}),
        ("The best loot from houses 0..i depends only on the best from 0..i-1 and 0..i-2. No future house can retroactively change what we decided at house i. This allows us to build the solution incrementally.", {}),
    ])),
    N.para(N.rich([
        ("Overlapping Subproblems: ", {"bold": True}),
        ("A recursive solution without memoization would recompute dp(3) from multiple paths in the decision tree (e.g., skip-skip-rob vs rob-skip-rob). Memoization or tabulation removes this redundancy.", {}),
    ])),
    N.code("# Recurrence (House Robber I — used in each pass):\n# dp[i] = max(dp[i-1],          # skip house i\n#              dp[i-2] + nums[i]) # rob house i\n#\n# Space-optimized with rolling variables:\n# prev  → dp[i-1]\n# pprev → dp[i-2]\n# curr  → dp[i]", lang="python"),
    N.callout("State Machine View: At any house, you are in one of two implicit states — 'just robbed i-1 (can't rob i)' or 'did not rob i-1 (can rob i)'. The rolling variables prev and pprev encode exactly this two-state machine.", "🔧", "blue_background"),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Two-Pass Bottom-Up DP (Interview Pick)", "O(n)", "O(1)"],
        ["Top-Down Memoization", "O(n)", "O(n) stack + cache"],
        ["Brute Force (all valid subsets)", "O(2^n)", "O(n)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Dynamic Programming", {})])),
    N.para(N.rich([("Sub-Pattern: ", {"bold": True}), ("Two Passes: Exclude First/Last — breaks a circular DP into two linear sub-problems by fixing which endpoint is excluded, then solving each with the base DP recurrence.", {})])),
    N.callout(
        "When to recognize this pattern:\n"
        "• Problem involves a circular array with an adjacency/conflict constraint\n"
        "• 'Maximize or minimize' subject to non-adjacent selections\n"
        "• You know how to solve the linear version — just run it twice\n"
        "• Signal phrases: 'arranged in a circle', 'first and last are neighbors'",
        "🔎", "green_background"
    ),
    N.para(N.rich([
        ("Sub-pattern verified in DSA_Patterns_and_SubPatterns_Guide.md Section 18 (Dynamic Programming). ", {"italic": True}),
    ])),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique or closely related DP patterns:"),
    N.bullet(N.rich([("House Robber I", {"bold": True}), (" (Easy) — The linear foundation; master this before tackling Robber II. LC 198.", {})])),
    N.bullet(N.rich([("House Robber III", {"bold": True}), (" (Medium) — Houses on a binary tree; post-order DP at each node chooses rob-or-skip. LC 337.", {})])),
    N.bullet(N.rich([("Delete and Earn", {"bold": True}), (" (Medium) — Reduce to Robber I: bucket values and treat each bucket as a 'house'. LC 740.", {})])),
    N.bullet(N.rich([("Maximum Sum Circular Subarray", {"bold": True}), (" (Medium) — Circular Kadane's algorithm; same two-case decomposition idea. LC 918.", {})])),
    N.bullet(N.rich([("Paint House", {"bold": True}), (" (Medium) — Adjacent color exclusion DP; same non-adjacent constraint but with state colors. LC 256.", {})])),
    N.bullet(N.rich([("Jump Game VI", {"bold": True}), (" (Medium) — DP with sliding window max; non-adjacent jump optimization. LC 1696.", {})])),
    N.para("These problems share the core technique: rolling-variable DP to maximize a sum under an adjacency exclusion constraint, with a circular variant handled by the two-pass reduction."),
    N.callout("Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 18: Dynamic Programming → Two Passes: Exclude First/Last", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

# ─── 4. Append blocks ────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks appended: {len(blocks)}")
