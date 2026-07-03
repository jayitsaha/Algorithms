"""
gen_maximum_length_of_pair_chain.py
Notion regeneration for LeetCode #646 — Maximum Length of Pair Chain
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-811c-9fc0-c95b021daf83"
SLUG = "maximum_length_of_pair_chain"

# ── 1. Set properties ──
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=646,
    pattern="Dynamic Programming",
    subpatterns=["LIS (Longest Increasing Subsequence)"],
    tc="O(n log n)",
    sc="O(1)",
    key_insight="Sort pairs by right endpoint; greedily take each pair whose left > chain_end — earliest-finish-first maximises future choices.",
    icon="🟡"
)
print("Properties set.")

# ── 2. Wipe existing body ──
print("Wiping old blocks...")
removed = N.wipe_page(PAGE_ID)
print(f"Wiped {removed} blocks.")

# ── 3. Build new body ──
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given an array of ", {}),
        ("n", {"code": True}),
        (" pairs ", {}),
        ("pairs", {"code": True}),
        (" where ", {}),
        ("pairs[i] = [left_i, right_i]", {"code": True}),
        (" and ", {}),
        ("left_i < right_i", {"code": True}),
        (". A pair ", {}),
        ("p2 = [c, d]", {"code": True}),
        (" follows a pair ", {}),
        ("p1 = [a, b]", {"code": True}),
        (" in the chain if and only if ", {}),
        ("b < c", {"code": True}),
        (". Return the length maximum length of a chain you can form.", {})
    ])),
    N.para(N.rich([
        ("Example: pairs = [[1,2],[2,3],[3,4]] → Output: 2 (chain [1,2] → [3,4]). pairs = [[1,2],[7,8],[4,5]] → Output: 3 (all three fit).", {"italic": True, "color": "gray"})
    ])),
    N.divider()
]

# ── Solution 1: Greedy ──
blocks += [
    N.h2("Solution 1 — Greedy: Sort by End, Earliest-Finish-First (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We have intervals [a, b] and want to pick the maximum number that don't overlap (with the strict inequality b < next_a). This is the classic Activity Selection / Interval Scheduling Maximization problem."),
        N.h4("What Doesn't Work"),
        N.para("Sorting by start (left) and greedily picking: a pair that starts early but ends late blocks many future pairs. Trying all subsets (2^n) is far too slow. DP works but is O(n²)."),
        N.h4("The Key Observation"),
        N.para("Among all pairs compatible with the current chain, the one that ends earliest is always at least as good as any other choice. Picking the earliest-ending pair minimizes chain_end, which maximizes future compatibility. This is the exchange argument: any optimal solution that picks pair X can swap in pair Y (where Y ends earlier) without losing chain length."),
        N.h4("Building the Solution"),
        N.para("1. Sort by right endpoint — smallest b first. 2. Track chain_end (the right of the last chosen pair). 3. Scan: if a > chain_end, take the pair (count++, chain_end = b). 4. Otherwise skip — it overlaps and our chosen pair ends earlier anyway."),
        N.callout(
            "Analogy: You're booking meeting rooms for the day. Among all unscheduled meetings that start after your last meeting ended, always pick the one that ends soonest — this leaves the afternoon most open for more meetings.",
            "🧠", "blue_background"
        )
    ]),
    N.h3("Code"),
    N.code("""def findLongestChain(pairs: list[list[int]]) -> int:
    pairs.sort(key=lambda p: p[1])   # sort by right endpoint
    chain_end = float('-inf')         # empty chain; -inf matches anything
    count = 0
    for a, b in pairs:
        if a > chain_end:             # strictly greater: new pair can extend chain
            count += 1
            chain_end = b             # update chain cursor
    return count"""),
    N.h3("Line by Line"),
    N.para(N.rich([("pairs.sort(key=lambda p: p[1])", {"code": True}), (" — Sort all pairs by their right (end) value. Earliest-finishing pairs come first. This is the invariant that makes greedy safe.", {})])),
    N.para(N.rich([("chain_end = float('-inf')", {"code": True}), (" — The current chain's right endpoint. -∞ means the chain is empty; any pair with any left value can start it.", {})])),
    N.para(N.rich([("count = 0", {"code": True}), (" — Length of the chain built so far.", {})])),
    N.para(N.rich([("for a, b in pairs:", {"code": True}), (" — Scan each pair in sorted order. Destructure into left=a and right=b.", {})])),
    N.para(N.rich([("if a > chain_end:", {"code": True}), (" — Strictly greater-than check. If the pair's left starts after the chain currently ends, it is compatible. Note: equal endpoints (a == chain_end) are NOT valid — the problem requires strict inequality.", {})])),
    N.para(N.rich([("count += 1", {"code": True}), (" — Extend the chain. This pair is now the newest link.", {})])),
    N.para(N.rich([("chain_end = b", {"code": True}), (" — Update: the chain now ends at b. Future pairs must start strictly after b.", {})])),
    N.para(N.rich([("return count", {"code": True}), (" — After scanning all pairs, count is the maximum chain length.", {})])),
    N.callout(
        "⚠️ Common mistake: using a >= chain_end instead of a > chain_end. That would allow touching pairs like [1,5] and [5,7], but the problem says b < c — strictly less than, not less-than-or-equal.",
        "⚠️", "yellow_background"
    ),
    N.divider()
]

# ── Solution 2: DP Tabulation ──
blocks += [
    N.h2("Solution 2 — DP Tabulation (Bottom-Up, LIS Recurrence)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Why Is This Dynamic Programming?"),
        N.para("The longest chain ending at pair i depends on the longest chains ending at all pairs j < i that are compatible. This is optimal substructure. A naive recursion would recompute dp(j) for many different i — overlapping subproblems. DP avoids this."),
        N.h4("The Recurrence"),
        N.para("Sort by end. dp[i] = length of the longest chain ending exactly at pair i. Base: dp[i] = 1 (every pair alone). Transition: dp[i] = max(dp[i], dp[j]+1) for all j < i where pairs[j][1] < pairs[i][0]. Answer = max(dp)."),
        N.h4("Connection to LIS"),
        N.para("This is Longest Increasing Subsequence applied to pairs instead of integers. In LIS: dp[i] = max(dp[j]+1) where nums[j] < nums[i]. Here: dp[i] = max(dp[j]+1) where pairs[j][1] < pairs[i][0]. Structurally identical — just the comparison changes."),
        N.callout(
            "Mnemonic: LIS = longest chain of numbers where each is bigger than the previous. Pair Chain = longest chain of intervals where each starts after the previous ends. Same recurrence, different comparison.",
            "🧠", "blue_background"
        )
    ]),
    N.h3("Code (Tabulation)"),
    N.code("""def findLongestChain_dp(pairs: list[list[int]]) -> int:
    pairs.sort(key=lambda p: p[1])   # sort by right endpoint
    n = len(pairs)
    dp = [1] * n                      # dp[i] = longest chain ending at pairs[i]
    for i in range(1, n):
        for j in range(i):
            if pairs[j][1] < pairs[i][0]:   # j can directly precede i
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)"""),
    N.h3("Code (Memoization — Top-Down)"),
    N.code("""from functools import lru_cache

def findLongestChain_memo(pairs: list[list[int]]) -> int:
    pairs.sort(key=lambda p: p[1])   # sort by right endpoint
    n = len(pairs)

    @lru_cache(maxsize=None)
    def dp(i):                        # longest chain starting from pairs[i]
        best = 1
        for j in range(i + 1, n):
            if pairs[j][0] > pairs[i][1]:   # j can follow i
                best = max(best, 1 + dp(j))
        return best

    return max(dp(i) for i in range(n))"""),
    N.h3("Line by Line (DP Tabulation key lines)"),
    N.para(N.rich([("dp = [1] * n", {"code": True}), (" — Every pair alone is a chain of length 1. This is the base case.", {})])),
    N.para(N.rich([("for i in range(1, n):", {"code": True}), (" — Outer loop: pairs[i] is the chain tail we are computing dp for.", {})])),
    N.para(N.rich([("for j in range(i):", {"code": True}), (" — Inner loop: check all previous pairs as potential predecessors.", {})])),
    N.para(N.rich([("if pairs[j][1] < pairs[i][0]:", {"code": True}), (" — Compatibility check: pair j must end strictly before pair i starts.", {})])),
    N.para(N.rich([("dp[i] = max(dp[i], dp[j] + 1)", {"code": True}), (" — If extending j's chain with i gives a longer chain, update dp[i].", {})])),
    N.para(N.rich([("return max(dp)", {"code": True}), (" — The answer is the best chain tail across all possible ending pairs.", {})])),
    N.divider()
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (all subsets)", "O(2ⁿ)", "O(n)"],
        ["DP Tabulation (LIS-style)", "O(n²)", "O(n)"],
        ["Memoization (Top-Down)", "O(n²)", "O(n)"],
        ["Greedy (Sort + Scan) ✓", "O(n log n)", "O(1)*"],
    ]),
    N.para(N.rich([("*O(1) extra space for the greedy scan; O(n) if the sort allocates a copy. Sort itself is the bottleneck.", {"italic": True, "color": "gray"})])),
    N.divider()
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Dynamic Programming", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("LIS (Longest Increasing Subsequence) — applied to interval endpoints instead of numeric values. The greedy shortcut is Activity Selection / Earliest Deadline First.", {})])),
    N.callout(
        "When to recognize this pattern:\n• Problem involves pairs/intervals with a 'chain' or 'sequence' condition\n• Each item must start strictly after the previous item ends\n• You can freely reorder items (no position constraint)\n• Asking for 'maximum length' or 'minimum removals' on interval-like data\n• Key signal: 'pairs [a,b] where a < b, chain where each left > previous right'",
        "🔎", "green_background"
    ),
    N.divider()
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (LIS / Greedy Interval Scheduling):"),
    N.bullet(N.rich([("Non-overlapping Intervals", {"bold": True}), (" (Medium) — Minimum pairs to remove so the rest are non-overlapping; answer = n − greedy_count. (#435)", {})])),
    N.bullet(N.rich([("Longest Increasing Subsequence", {"bold": True}), (" (Medium) — Classic LIS; same dp[i]=max(dp[j]+1) recurrence but on integers not pairs. (#300)", {})])),
    N.bullet(N.rich([("Russian Doll Envelopes", {"bold": True}), (" (Hard) — 2D LIS: sort by width ascending then height descending, LIS on heights. (#354)", {})])),
    N.bullet(N.rich([("Minimum Number of Arrows to Burst Balloons", {"bold": True}), (" (Medium) — Sort by end, count groups of overlapping balloons; greedy interval cousin. (#452)", {})])),
    N.bullet(N.rich([("Longest String Chain", {"bold": True}), (" (Medium) — Sort by word length, dp[word]=max chain ending at word; LIS on strings. (#1048)", {})])),
    N.bullet(N.rich([("Maximum Profit in Job Scheduling", {"bold": True}), (" (Hard) — Weighted interval scheduling; DP + binary search; extends this problem with profits. (#1235)", {})])),
    N.para("These problems share the core technique: sort by end/length, then use either greedy (take earliest compatible) or DP (dp[i]=max(dp[j]+1) for compatible j)."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 18.4 (Dynamic Programming → LIS). Sub-Pattern verified: Guide Section 18.4 + Analysis.", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([("Step through the greedy algorithm visually — use Next/Prev or arrow keys to see how chain_end updates and why pairs are included or skipped.", {"italic": True, "color": "gray"})]))
]

print(f"Appending {len(blocks)} blocks to Notion page...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
