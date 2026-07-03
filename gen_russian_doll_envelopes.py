"""gen_russian_doll_envelopes.py — Notion update for Russian Doll Envelopes (LC #354)"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81c4-82c3-f739b912855e"

# ── 1. Properties ──────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=354,
    pattern="Dynamic Programming",
    subpatterns=["DP: LIS", "Sort + LIS on Height"],
    tc="O(n log n)",
    sc="O(n)",
    key_insight="Sort by width ASC, height DESC for ties; then run O(n log n) LIS (patience sort) on heights.",
    icon="🔴",
)
print("Properties set.")

# ── 2. Wipe old content ────────────────────────────────────────
deleted = N.wipe_page(PAGE_ID)
print(f"Wiped {deleted} old blocks.")

# ── 3. Build body blocks ───────────────────────────────────────

PROB = (
    "Given a list of envelopes where envelopes[i] = [wi, hi] represents the width and height of an envelope, "
    "return the maximum number of envelopes you can Russian doll (put one inside the other). "
    "You can place envelope A inside envelope B if and only if both A's width and A's height are strictly less than B's width and B's height. "
    "Note: You cannot rotate an envelope."
)

SOL1_CODE = """\
import bisect

def maxEnvelopes(envelopes: list[list[int]]) -> int:
    # Sort: width ASC, height DESC for same width (key trick!)
    envelopes.sort(key=lambda x: (x[0], -x[1]))

    # Patience sort (LIS via binary search)
    tails = []
    for _, h in envelopes:
        pos = bisect.bisect_left(tails, h)
        if pos == len(tails):
            tails.append(h)   # extend LIS
        else:
            tails[pos] = h    # replace: better tail for this IS length

    return len(tails)
"""

SOL2_CODE = """\
def maxEnvelopes_dp(envelopes: list[list[int]]) -> int:
    envelopes.sort()  # sort by (w, h) both ascending
    n = len(envelopes)
    dp = [1] * n  # dp[i] = longest chain ending at envelope i
    for i in range(n):
        w2, h2 = envelopes[i]
        for j in range(i):
            w1, h1 = envelopes[j]
            if w1 < w2 and h1 < h2:       # j strictly fits inside i
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)
"""

blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(PROB),
    N.divider(),
]

# Solution 1
blocks += [
    N.h2("Solution 1 — Sort + LIS Binary Search (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We need the longest chain of envelopes where each is strictly smaller in BOTH dimensions. "
            "This is 2D Longest Increasing Subsequence — if we could somehow handle one dimension automatically, "
            "the problem reduces to the classic 1D LIS."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Brute force: try all 2^n subsets, check each forms a valid chain → O(2^n * n), infeasible. "
            "Plain sort by width then LIS on heights → fails for equal-width envelopes: LIS might pick "
            "[3,3],[3,5] treating them as a valid chain, but they have equal width and cannot nest."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Sort by width ASC. For envelopes with the SAME width, sort by height DESC. "
            "Now run LIS only on heights. The descending-height trick for same-width groups ensures "
            "that at most one envelope per width value can enter any increasing subsequence of heights."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. Sort: key=lambda x: (x[0], -x[1])  "
            "2. Initialize tails = []  "
            "3. For each height h, binary-search tails for bisect_left position pos  "
            "4. If pos == len(tails): append h (LIS grows by 1)  "
            "5. Else: tails[pos] = h (replace with smaller tail for this IS length)  "
            "6. Return len(tails) as the answer"
        ),
        N.callout(
            "Analogy: Think of tails as a set of piles in patience sort. Each height goes on the leftmost pile "
            "whose top card is >= h, or starts a new pile. The number of piles = LIS length. "
            "The descending-sort trick means same-width cards always decrease, so at most one card "
            "per width group gets placed.",
            "🎴", "blue_background"
        ),
    ]),
    N.h3("Why is This DP?"),
    N.para(
        "Optimal substructure: the longest chain ending at envelope i is 1 + max(chain ending at any j "
        "where j fits inside i). Each subproblem is itself a 'longest chain' problem on a smaller input."
    ),
    N.para(
        "Overlapping subproblems: many envelopes share the same compatible ancestors. Without memoization, "
        "we would recompute the same sub-chains for different 'outer' envelopes. The tails array is an "
        "O(n) compressed representation that avoids this redundancy."
    ),
    N.callout(
        "The tails array is NOT a valid nesting sequence — its elements may come from different "
        "incompatible chains. Only its LENGTH is meaningful. Never try to reconstruct the actual chain "
        "from tails; use a separate predecessor array for reconstruction.",
        "⚠️", "yellow_background"
    ),
    N.h3("Recurrence (Classic O(n²) DP)"),
    N.code(
        "# After sorting both dims ascending:\n"
        "dp[i] = 1 + max(dp[j] for j < i if w[j] < w[i] and h[j] < h[i])\n"
        "dp[i] = 1  (base: each envelope alone is a chain of 1)\n"
        "answer = max(dp)",
        "python"
    ),
    N.h3("Code"),
    N.code(SOL1_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("envelopes.sort(key=lambda x: (x[0], -x[1]))", {"code": True}),
                   " — Sort by width ascending; for equal widths, height descending. This is the crucial trick that prevents two same-width envelopes from both entering the LIS."])),
    N.para(N.rich([("tails = []", {"code": True}),
                   " — Patience-sort tails array. tails[k] = minimum possible tail of any increasing subsequence of length k+1 seen so far."])),
    N.para(N.rich([("for _, h in envelopes:", {"code": True}),
                   " — We only need heights after the sort has handled widths. Width constraint is automatically satisfied because we sorted ascending."])),
    N.para(N.rich([("pos = bisect.bisect_left(tails, h)", {"code": True}),
                   " — O(log n) binary search: find the leftmost index where tails[pos] >= h. This position tells us how long an IS we can form ending at h."])),
    N.para(N.rich([("if pos == len(tails): tails.append(h)", {"code": True}),
                   " — h is larger than every existing tail, so it extends the longest subsequence. LIS length increases by 1."])),
    N.para(N.rich([("else: tails[pos] = h", {"code": True}),
                   " — Replace the existing tail at pos with h (which is smaller or equal). This keeps the minimum possible tail for an IS of that length, making future extensions easier."])),
    N.para(N.rich([("return len(tails)", {"code": True}),
                   " — Length of tails = LIS length = maximum nesting depth."])),
    N.divider(),
]

# Solution 2
blocks += [
    N.h2("Solution 2 — Classic O(n²) DP"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "For each envelope i, think about what is the longest chain that ends with i as the outermost envelope. "
            "This depends directly on the longest chains ending at every envelope j that fits inside i."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Greedy (always pick the smallest available envelope) fails because a locally 'smallest' choice "
            "can block a longer global chain. We need to consider all possibilities."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Define dp[i] = length of the longest nesting chain ending at envelope i. "
            "Then dp[i] = 1 + max(dp[j]) for all j where envelopes[j] fits strictly inside envelopes[i]. "
            "Sort by (w,h) first so j < i implies w[j] <= w[i] — we only need to check the height condition."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Sort normally by (w,h). For each i, scan all j < i and extend dp[i] if envelopes[j] strictly fits. "
            "Return max(dp). Time O(n²), space O(n). This is intuitive but too slow for n=100,000."
        ),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("envelopes.sort()", {"code": True}),
                   " — Sort by (w,h) both ascending. This doesn't need the descending-height trick since we check both dimensions explicitly in the DP."])),
    N.para(N.rich([("dp = [1] * n", {"code": True}),
                   " — dp[i] = longest chain ending at envelope i. Starts at 1 (each envelope alone)."])),
    N.para(N.rich([("if w1 < w2 and h1 < h2:", {"code": True}),
                   " — Both dimensions strictly less — envelope j fits inside i."])),
    N.para(N.rich([("dp[i] = max(dp[i], dp[j] + 1)", {"code": True}),
                   " — Extend the chain from j to include i. Take the maximum over all valid j."])),
    N.para(N.rich([("return max(dp)", {"code": True}),
                   " — Best chain ending at any envelope."])),
    N.divider(),
]

# Complexity
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Sort + LIS Binary Search", "O(n log n)", "O(n)"],
        ["Classic DP", "O(n²)", "O(n)"],
        ["Brute Force (all subsets)", "O(2ⁿ · n)", "O(n)"],
    ]),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Dynamic Programming"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "DP: LIS (Longest Increasing Subsequence), Sort + LIS on Height"])),
    N.callout(
        "When to recognize this pattern: "
        "(1) Problem asks for longest chain where each element strictly dominates the previous. "
        "(2) Two or more numeric properties must ALL be strictly increasing. "
        "(3) You can sort on one dimension to reduce the problem to 1D LIS on another. "
        "(4) Keywords: nesting, enclosing, stacking, strictly contains, domination.",
        "🔎", "green_background"
    ),
    N.para(
        "Sub-Pattern verified: 'DP: LIS' from DSA_Patterns_and_SubPatterns_Guide.md Section 18 (Dynamic Programming). "
        "'Sort + LIS on Height' is the specific technique for this problem (2D LIS reduction)."
    ),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Sort + LIS / 2D LIS technique:"),
    N.bullet(N.rich([("Longest Increasing Subsequence", {"bold": True}), " (Medium) — Core 1D LIS; master this before Russian Doll"])),
    N.bullet(N.rich([("Maximum Height by Stacking Cuboids", {"bold": True}), " (Hard) — 3D version; sort all three dims, LIS on height"])),
    N.bullet(N.rich([("Longest Chain of Pairs", {"bold": True}), " (Medium) — [a,b] pairs chain if b_prev < a_next; same reduction pattern"])),
    N.bullet(N.rich([("Minimum Number of Arrows to Burst Balloons", {"bold": True}), " (Medium) — Sort + greedy on intervals; adjacent interval-chain reasoning"])),
    N.bullet(N.rich([("Non-overlapping Intervals", {"bold": True}), " (Medium) — Sort by end time + greedy; related 1D reduction"])),
    N.bullet(N.rich([("Box Stacking (Classic GFG/CLRS)", {"bold": True}), " (Hard) — 3D nesting with rotation choices; same Sort+LIS template"])),
    N.para("These problems share the core technique: reduce a multi-dimensional ordering constraint to 1D LIS by careful sorting."),
]

# Embed
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("russian_doll_envelopes")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

# ── 4. Append all blocks ───────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"Appended {len(blocks)} blocks to Notion page.")
print("NOTION OK", PAGE_ID)
