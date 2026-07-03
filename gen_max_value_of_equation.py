"""
gen_max_value_of_equation.py
Notion in-place update for LeetCode #1499 — Max Value of Equation.
Pattern: Monotonic Queue / Monotonic Deque Optimization. Difficulty: Hard.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notion_lib as N

PAGE_ID = "39193418-809c-816d-8e30-e85f869e2ff0"
SLUG = "max_value_of_equation"

# ── 1. Set properties ──────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=1499,
    pattern="Monotonic Queue",
    subpatterns=["Monotonic Deque Optimization"],
    tc="O(n)",
    sc="O(n)",
    key_insight="Split y_i + y_j + x_j - x_i as (y_i - x_i) + (y_j + x_j); use monotonic deque for sliding window max of (y_i - x_i).",
    icon="🔴"
)
print("Properties set.")

# ── 2. Wipe old content ─────────────────────────────────────────
print("Wiping existing blocks...")
deleted = N.wipe_page(PAGE_ID)
print(f"Deleted {deleted} blocks.")

# ── 3. Build body blocks ────────────────────────────────────────
blocks = []

# ── Problem statement ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given an array ", {}),
        ("points", {"code": True}),
        (" containing the coordinates of points on a 2D plane, sorted by the x-values, where ", {}),
        ("points[i] = [xi, yi]", {"code": True}),
        (". The cost of connecting two points ", {}),
        ("[xi, yi]", {"code": True}),
        (" and ", {}),
        ("[xj, yj]", {"code": True}),
        (" is ", {}),
        ("yi + yj + |xi - xj|", {"code": True}),
        (". Find the maximum value of ", {}),
        ("yi + yj + |xi - xj|", {"code": True}),
        (" where ", {}),
        ("xi < xj", {"code": True}),
        (" and ", {}),
        ("xj - xi <= k", {"code": True}),
        (". It is guaranteed that there exists at least one pair of points that satisfy the constraint.", {}),
    ])),
    N.divider(),
]

# ── Solution 1: Monotonic Deque (Interview Pick) ──
SOLUTION1_CODE = """\
from collections import deque

def findMaxValueOfEquation(points, k):
    dq = deque()          # stores (y - x, x) pairs, decreasing by y-x
    ans = float('-inf')
    for xj, yj in points:
        # Evict front: x-distance exceeds k -> permanently stale
        while dq and xj - dq[0][1] > k:
            dq.popleft()
        # Query: front holds max (y_i - x_i) among valid left candidates
        if dq:
            ans = max(ans, dq[0][0] + yj + xj)
        # Evict back: dominated by current point (lower score, expires sooner)
        while dq and dq[-1][0] <= yj - xj:
            dq.pop()
        # Insert current point as candidate for future right partners
        dq.append((yj - xj, xj))
    return ans"""

blocks += [
    N.h2("Solution 1 — Monotonic Deque Optimization (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("For each pair (i, j) with i < j and xj - xi <= k, compute yi + yj + |xi - xj| and return the maximum. The points are sorted by x, so for i < j we always have xj >= xi, making |xi - xj| = xj - xi. No absolute value needed!"),
        N.h4("What Doesn't Work"),
        N.para("Brute force: try every pair (i, j) — O(n^2) which TLEs for n = 10^5. We need to avoid re-examining every prior point for each j."),
        N.h4("The Key Observation"),
        N.para("Rewrite: yi + yj + xj - xi = (yi - xi) + (yj + xj). The right term (yj + xj) is fixed per j. So for each j, we just need the maximum (yi - xi) among all valid left partners i with xj - xi <= k. That's a sliding window maximum — the window slides right as j increases, and old points that fall outside (xj - xi > k) can never be used again."),
        N.h4("Building the Solution"),
        N.para("Sliding window maximum = monotonic deque. Maintain a deque of (y-x, x) pairs in decreasing order of y-x. The front is always the current maximum. For each new j: (1) evict front if too far (stale), (2) query front for the best left partner, (3) evict back entries dominated by current (lower value AND expires sooner), (4) push current. O(n) total since each point enters/exits deque at most once."),
        N.callout(
            "Analogy: Think of the deque as a 'candidate pool'. When a better candidate arrives, all older worse candidates are thrown out — they can never win over the new one. Only the front (best remaining) is ever used to answer queries.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("🔬 Algorithm Deep-Dive: Monotonic Deque"),
    N.para("The monotonic deque (or monotone queue) is a double-ended queue that maintains its elements in sorted order (increasing or decreasing). It enables O(1) amortized sliding window maximum/minimum queries."),
    N.code("""\
# Sliding Window Maximum Template (monotonic deque)
from collections import deque

def sliding_window_max(arr, k):
    dq = deque()   # stores indices, values decrease from front to back
    result = []
    for i, val in enumerate(arr):
        # Remove indices outside window
        while dq and i - dq[0] >= k:
            dq.popleft()
        # Remove dominated back entries
        while dq and arr[dq[-1]] <= val:
            dq.pop()
        dq.append(i)
        if i >= k - 1:
            result.append(arr[dq[0]])
    return result"""),
    N.para(N.rich([
        ("Core invariant: ", {"bold": True}),
        ("The deque always contains indices of elements in decreasing order of value. The front is the index of the current window maximum. When a new element is added, all smaller elements at the back are evicted because they are permanently dominated — the new element has a higher value AND won't expire before them. Front eviction handles window boundary (oldest-first expiry)."),
    ])),
    N.para(N.rich([
        ("When to recognize: ", {"bold": True}),
        ('"Find max/min in a sliding window of size k" or "for each j, find optimal i in range [j-k, j-1]" or any objective that splits into a sliding window query on one variable plus a per-element term.'),
    ])),
    N.h3("Code"),
    N.code(SOLUTION1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("dq = deque()", {"code": True}), (" — Monotonic deque storing (y-x, x) pairs. Decreasing order by first element (y-x = contribution value). Front = max contributor among valid points.", {})])),
    N.para(N.rich([("ans = float('-inf')", {"code": True}), (" — Running maximum of the equation value across all valid (i,j) pairs seen so far.", {})])),
    N.para(N.rich([("for xj, yj in points:", {"code": True}), (" — Iterate left to right. Points are pre-sorted by x, so xj is non-decreasing. We use j as the right partner in each pair.", {})])),
    N.para(N.rich([("while dq and xj - dq[0][1] > k:", {"code": True}), (" — Check if the FRONT entry's x-coordinate is too far left. dq[0][1] is the stored x_i. If x_j - x_i > k, the front point is outside the valid window and can never pair with j or any future point (x only increases). Evict it.", {})])),
    N.para(N.rich([("dq.popleft()", {"code": True}), (" — O(1) removal from front. May run multiple times if several old entries are stale.", {})])),
    N.para(N.rich([("if dq:", {"code": True}), (" — After evicting stale entries, if the deque is non-empty, the front is the best valid left partner.", {})])),
    N.para(N.rich([("ans = max(ans, dq[0][0] + yj + xj)", {"code": True}), (" — dq[0][0] is (y_i - x_i) for the best left partner. Adding (y_j + x_j) gives the full equation value. Update running max.", {})])),
    N.para(N.rich([("while dq and dq[-1][0] <= yj - xj:", {"code": True}), (" — Back eviction: if the BACK entry's value (y-x) is <= current point's value, it's dominated. Current point has a higher contribution AND a larger x (expires later). Back entry is useless forever.", {})])),
    N.para(N.rich([("dq.pop()", {"code": True}), (" — O(1) removal from back. Maintains the decreasing invariant.", {})])),
    N.para(N.rich([("dq.append((yj - xj, xj))", {"code": True}), (" — Insert current point as a future left-partner candidate. The pair stores contribution value (y-x) and x-coordinate (for validity checks).", {})])),
    N.para(N.rich([("return ans", {"code": True}), (" — Maximum over all valid pairs found during the scan.", {})])),
    N.divider(),
]

# ── Solution 2: Brute Force ──
SOLUTION2_CODE = """\
def findMaxValueOfEquation_brute(points, k):
    ans = float('-inf')
    n = len(points)
    for j in range(n):
        for i in range(j):
            xi, yi = points[i]
            xj, yj = points[j]
            if xj - xi <= k:        # distance constraint
                val = yi + yj + xj - xi  # no abs needed since sorted
                ans = max(ans, val)
    return ans"""

blocks += [
    N.h2("Solution 2 — Brute Force O(n²)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Try every pair of points (i, j) with i < j. For each pair, check if the x-distance is at most k, and if so compute the equation value."),
        N.h4("What Doesn't Work"),
        N.para("This is O(n^2) — for n=10^5, that's 10^10 operations. Completely intractable for the given constraints. Use this to understand correctness, then optimize."),
        N.h4("The Key Observation"),
        N.para("Since points are sorted by x, for i < j we always have xj >= xi so |xi - xj| = xj - xi. The inner loop can break early once xj - xi > k (remaining points are even further), but worst case is still O(n^2)."),
        N.h4("Building the Solution"),
        N.para("Simple nested loops. O(n^2) time, O(1) space. Present this first in an interview to show you understand the problem, then propose the deque optimization."),
    ]),
    N.h3("Code"),
    N.code(SOLUTION2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("for j in range(n):", {"code": True}), (" — Outer loop: j is the right partner (larger x).", {})])),
    N.para(N.rich([("for i in range(j):", {"code": True}), (" — Inner loop: i is the left partner (smaller x). O(n) per j -> O(n^2) total.", {})])),
    N.para(N.rich([("if xj - xi <= k:", {"code": True}), (" — Only consider pairs within x-distance k. Since sorted, xj - xi is always non-negative.", {})])),
    N.para(N.rich([("val = yi + yj + xj - xi", {"code": True}), (" — Equation value. xj - xi = |xi - xj| since xj >= xi (sorted).", {})])),
    N.divider(),
]

# ── Complexity table ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Brute Force", "O(n^2)", "O(1)", "TLE for n=10^5"],
        ["Monotonic Deque (Optimal)", "O(n)", "O(n)", "Each point pushed/popped at most once"],
    ]),
    N.divider(),
]

# ── Pattern classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Monotonic Queue", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Monotonic Deque Optimization (sliding window maximum applied to DP/equation decomposition)", {})])),
    N.callout(
        "When to recognize this pattern: (1) Objective can be split into f(i) + g(j) where f(i) is the 'left contribution' and g(j) is the 'right contribution'. (2) Valid left partners form a sliding window (i.e., xj - xi <= k or index distance <= k). (3) You need the maximum or minimum of f(i) over the window. (4) Input is sorted or naturally ordered. Signal keywords: 'sorted by x', 'distance at most k', 'maximize yi + yj + |xi - xj|'.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Monotonic Deque / Sliding Window Maximum technique:"),
    N.bullet(N.rich([("Sliding Window Maximum", {"bold": True}), (" (Hard) — The canonical deque template. dq stores indices of elements in decreasing order; front = window max.", {})])),
    N.bullet(N.rich([("Jump Game VI", {"bold": True}), (" (Medium) — DP + deque: dp[i] = max(dp[j] for j in [i-k, i-1]) + a[i]. Identical deque structure applied to DP transitions.", {})])),
    N.bullet(N.rich([("Constrained Subsequence Sum", {"bold": True}), (" (Hard) — dp[i] = max(dp[j] for j in [i-k, i-1]) + nums[i]. Direct monotonic deque on DP array.", {})])),
    N.bullet(N.rich([("Shortest Subarray with Sum at Least K", {"bold": True}), (" (Hard) — Prefix sums + deque. Evict from front when prefix condition is met; maintain increasing prefix sum order.", {})])),
    N.bullet(N.rich([("Longest Continuous Subarray With Abs Diff <= Limit", {"bold": True}), (" (Medium) — Two deques (max and min deque) to track window range; shrink window when |max - min| > limit.", {})])),
    N.bullet(N.rich([("Maximum Earnings From Taxi", {"bold": True}), (" (Medium) — DP over events sorted by end time with sliding window max; same formula split pattern.", {})])),
    N.para("These problems share the core pattern: split the objective, use a sliding window with deque-maintained max/min, O(n) total."),
    N.callout("Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section: Stack/Queue Patterns → Monotonic Queue / Deque sub-pattern. Also related to Heap sub-pattern (Top K) as an alternative O(n log n) approach.", "📚", "gray_background"),
]

# ── Interactive visual explainer ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

# ── 4. Append all blocks ────────────────────────────────────────
print(f"Appending {len(blocks)} blocks to Notion...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
