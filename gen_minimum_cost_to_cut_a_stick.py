"""
gen_minimum_cost_to_cut_a_stick.py
Notion update script for LeetCode #1547 — Minimum Cost to Cut a Stick
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-81f4-8dc0-c6bc6bdd8eac"

# ── 1) Set properties ──────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=1547,
    pattern="Dynamic Programming",
    subpatterns=["Interval DP"],
    tc="O(m³)",
    sc="O(m²)",
    key_insight="Add 0 and n as sentinels; dp[i][j]=min over k of dp[i][k]+dp[k][j]+(cuts[j]-cuts[i]).",
    icon="🔴"
)
print("Properties set.")

# ── 2) Wipe existing body ─────────────────────────────────────────────────
print("Wiping existing page body...")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3) Build body blocks ──────────────────────────────────────────────────
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a wooden stick of length ", {}),
        ("n", {"code": True}),
        (" units. You are given an array ", {}),
        ("cuts", {"code": True}),
        (" of cut positions. Each cut on a stick piece of length ", {}),
        ("L", {"code": True}),
        (" costs exactly ", {}),
        ("L", {"code": True}),
        (". Return the minimum total cost to make all the cuts.", {}),
    ])),
    N.para(N.rich([
        ("Example: n=7, cuts=[1,3,4,5]. Answer: 16.", {}),
        (" Optimal order: cut at 3 (cost 7) → cut at 5 in [3,7] (cost 4) → cut at 1 in [0,3] (cost 3) → cut at 4 in [3,5] (cost 2). Total = 16.", {"italic": True, "color": "gray"}),
    ])),
    N.divider(),
]

# Solution 1 — Bottom-Up Interval DP
blocks += [
    N.h2("Solution 1 — Bottom-Up Interval DP (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to make a set of cuts on a stick. The cost of each cut equals the current length of the piece being cut — so the order matters. We want to find the optimal ordering of cuts to minimize total cost."),
        N.h4("What Doesn't Work"),
        N.para("A greedy approach (e.g., always cut the middle or smallest piece) fails because local optimality doesn't imply global optimality. Trying all permutations of m cuts is O(m!) — far too slow for m up to 100."),
        N.h4("The Key Observation"),
        N.para("After any cut splits an interval [L, R] at position k, the two resulting sub-sticks [L,k] and [k,R] are fully independent. This is optimal substructure. The cost of the first cut is always (R−L) — the current full piece length. So dp[i][j] = min cost for all cuts between cuts[i] and cuts[j]."),
        N.h4("Building the Solution"),
        N.para("1) Add 0 and n as sentinels to cuts, then sort. 2) Define dp[i][j] = min cost for interval [cuts[i], cuts[j]]. 3) Base case: adjacent indices (j=i+1) → dp=0, no cuts. 4) Transition: try each k as the 'first cut', taking minimum. 5) Iterate by increasing interval length so sub-problems are ready."),
        N.callout("Analogy: Matrix Chain Multiplication — same template. 'First cut in interval' = 'parenthesization point'. The sentinel trick = extending boundaries to unify edge handling.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(
        "def minCost(n: int, cuts: list[int]) -> int:\n"
        "    cuts = sorted([0] + cuts + [n])  # add sentinels, e.g. [0,1,3,4,5,7]\n"
        "    m = len(cuts)\n"
        "    dp = [[0] * m for _ in range(m)]\n"
        "    for length in range(2, m):         # iterate by interval length\n"
        "        for i in range(m - length):    # left boundary\n"
        "            j = i + length             # right boundary\n"
        "            dp[i][j] = float('inf')\n"
        "            for k in range(i + 1, j):  # try each interior k as first cut\n"
        "                cost = cuts[j] - cuts[i]  # full piece length\n"
        "                dp[i][j] = min(dp[i][j], dp[i][k] + dp[k][j] + cost)\n"
        "    return dp[0][m - 1]"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("cuts = sorted([0] + cuts + [n])", {"code": True}), (" — Insert boundary sentinels and sort. Every sub-problem is now uniformly dp[i][j] between two known positions.", {})])),
    N.para(N.rich([("dp = [[0]*m for _ in range(m)]", {"code": True}), (" — Initialize entire table to 0. Adjacent cells (j==i+1) remain 0 as the base case: no cuts possible between adjacent positions.", {})])),
    N.para(N.rich([("for length in range(2, m)", {"code": True}), (" — Outer loop over interval length. length=2 means one interior cut possible; we build up to the full stick.", {})])),
    N.para(N.rich([("j = i + length", {"code": True}), (" — Right boundary of current interval.", {})])),
    N.para(N.rich([("dp[i][j] = float('inf')", {"code": True}), (" — Reset before taking minimum across all possible first cuts.", {})])),
    N.para(N.rich([("for k in range(i+1, j)", {"code": True}), (" — Try each interior position k as the 'first cut' made in this interval.", {})])),
    N.para(N.rich([("cost = cuts[j] - cuts[i]", {"code": True}), (" — The current piece length — this is always the cost of any cut within this interval (regardless of which position k we choose).", {})])),
    N.para(N.rich([("dp[i][j] = min(..., dp[i][k] + dp[k][j] + cost)", {"code": True}), (" — Left sub-problem + right sub-problem + cost of this cut. We take the minimum over all k.", {})])),
    N.para(N.rich([("return dp[0][m-1]", {"code": True}), (" — The answer: minimum cost for the full stick from position 0 to n.", {})])),
    N.divider(),
]

# Solution 2 — Top-Down Memoization
blocks += [
    N.h2("Solution 2 — Top-Down Memoization"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same subproblem definition as bottom-up: dp(i,j) = min cost to make all cuts between cuts[i] and cuts[j]. This time we express it recursively."),
        N.h4("What Doesn't Work"),
        N.para("Naive recursion without memoization recomputes the same sub-intervals many times. For m=22 cuts, this would time out."),
        N.h4("The Key Observation"),
        N.para("Python's lru_cache transparently handles memoization. The recursive formulation is often easier to derive from the recurrence than the iterative version, and lru_cache handles cache invalidation automatically."),
        N.h4("Building the Solution"),
        N.para("Define dp(i,j) recursively: if j-i==1 return 0 (base case). Otherwise return min over k in (i+1..j-1) of dp(i,k)+dp(k,j)+(cuts[j]-cuts[i])."),
        N.callout("Top-down is great for interviews when you've derived the recurrence and want to code quickly. Bottom-up is preferred if you need to optimize space.", "💡", "green_background"),
    ]),
    N.h3("Code"),
    N.code(
        "from functools import lru_cache\n\n"
        "def minCost(n: int, cuts: list[int]) -> int:\n"
        "    cuts = sorted([0] + cuts + [n])\n\n"
        "    @lru_cache(maxsize=None)\n"
        "    def dp(i, j):\n"
        "        if j - i == 1:\n"
        "            return 0  # base case: adjacent, no cuts between them\n"
        "        return min(\n"
        "            dp(i, k) + dp(k, j) + cuts[j] - cuts[i]\n"
        "            for k in range(i + 1, j)\n"
        "        )\n\n"
        "    return dp(0, len(cuts) - 1)"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("@lru_cache(maxsize=None)", {"code": True}), (" — Memoizes all (i,j) calls so each is computed at most once.", {})])),
    N.para(N.rich([("if j - i == 1: return 0", {"code": True}), (" — Base case: no positions exist strictly between two adjacent cut indices, so no cut is needed and cost is 0.", {})])),
    N.para(N.rich([("dp(i,k) + dp(k,j) + cuts[j] - cuts[i]", {"code": True}), (" — Recurrence: left part + right part + current piece length. Python's min() over a generator finds the optimal k.", {})])),
    N.divider(),
]

# Why is this DP?
blocks += [
    N.h2("Why is This Dynamic Programming?"),
    N.para(N.rich([("Optimal Substructure: ", {"bold": True}), ("Once cut k splits interval [i,j], sub-problems [i,k] and [k,j] are fully independent. Min cost for [i,j] = min cost for [i,k] + min cost for [k,j] + cost of this cut. We can solve each independently.", {})])),
    N.para(N.rich([("Overlapping Subproblems: ", {"bold": True}), ("Interval [2,5] may be needed by both dp[0,5] and dp[1,5]. Without memoization, recomputed exponentially many times. DP stores each of the O(m²) answers once, computed in O(m) each.", {})])),
    N.code(
        "# The Recurrence Relation\n"
        "# cuts_aug = sorted([0] + cuts + [n])    (m = len(cuts_aug))\n"
        "# Base case:  dp[i][j] = 0              when j == i+1\n"
        "# Transition: dp[i][j] = min over k in (i+1 .. j-1) of:\n"
        "#                 dp[i][k] + dp[k][j] + (cuts_aug[j] - cuts_aug[i])"
    ),
    N.callout("Same template as Matrix Chain Multiplication and Burst Balloons. If you've seen either of those, this problem is immediately recognizable.", "🔑", "purple_background"),
    N.divider(),
]

# Complexity
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (all permutations)", "O(m! · m)", "O(m)"],
        ["Top-Down Memoization", "O(m³)", "O(m²)"],
        ["Bottom-Up Interval DP", "O(m³)", "O(m²)"],
    ]),
    N.para("m = len(cuts) + 2 (after adding sentinels). O(m²) states, each taking O(m) to fill → O(m³) total."),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Dynamic Programming", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Interval DP — solve sub-problems defined by left/right boundaries of a sequence, building from smallest intervals up to the full range.", {})])),
    N.callout(
        "When to recognize this pattern:\n"
        "• Problem asks for min/max cost of performing operations on a sequence\n"
        "• The cost depends on the current boundaries (not fixed positions)\n"
        "• After any split, the two parts are fully independent\n"
        "• You choose the ORDER of operations (not just whether to include each)\n"
        "• Keywords: 'minimum cost to cut/merge/burst/print' on a range",
        "🔎", "green_background"
    ),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Interval DP technique:"),
    N.bullet(N.rich([("Burst Balloons", {"bold": True}), (" (Hard) — Interval DP; choose which balloon to burst last in each interval. Direct analog.", {})])),
    N.bullet(N.rich([("Palindrome Partitioning II", {"bold": True}), (" (Hard) — Interval DP; minimum cuts to partition string into palindromes.", {})])),
    N.bullet(N.rich([("Strange Printer", {"bold": True}), (" (Hard) — Interval DP; minimum print turns for a string.", {})])),
    N.bullet(N.rich([("Minimum Cost to Merge Stones", {"bold": True}), (" (Hard) — Interval DP; merge piles optimally.", {})])),
    N.bullet(N.rich([("Stone Game V", {"bold": True}), (" (Hard) — Interval DP; split array and maximize score.", {})])),
    N.bullet(N.rich([("Zuma Game", {"bold": True}), (" (Hard) — Interval DP; minimum moves to destroy all balls.", {})])),
    N.bullet(N.rich([("Matrix Chain Multiplication", {"bold": True}), (" (Classic) — The original Interval DP problem; identical template.", {})])),
    N.para("These problems share the same core technique: define dp[i][j] as the optimal cost for a contiguous range, try every split point k, and fill by increasing interval length."),
    N.callout("Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 18 (Dynamic Programming) → DP: Interval sub-pattern", "📚", "gray_background"),
]

# Embed
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("minimum_cost_to_cut_a_stick")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})
    ])),
]

# ── 4) Append all blocks ──────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks to Notion page...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
