"""
gen_constrained_subsequence_sum.py
Notion in-place rebuild for LC #1425 Constrained Subsequence Sum (Hard).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8127-a890-ed0ca03e712a"

# ── 1) Properties ──────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=1425,
    pattern="Monotonic Queue",
    subpatterns=["DP + Monotonic Deque"],
    tc="O(n)",
    sc="O(n)",
    key_insight="dp[i] = nums[i] + max(0, sliding-window-max of dp[i-k..i-1]); use monotonic deque for O(1) window max.",
    icon="🔴",
)
print("Properties set.")

# ── 2) Wipe old body ───────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3) Build body ──────────────────────────────────────────────────────────
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an integer array ", {}),
        ("nums", {"code": True}),
        (" and an integer ", {}),
        ("k", {"code": True}),
        (", return the maximum sum of a non-empty subsequence of that array such that for every two consecutive integers in the subsequence, ", {}),
        ("nums[i]", {"code": True}),
        (" and ", {}),
        ("nums[j]", {"code": True}),
        (", where ", {}),
        ("i < j", {"code": True}),
        (", the condition ", {}),
        ("j - i <= k", {"code": True}),
        (" is satisfied. A subsequence of an array is obtained by deleting some number of elements (can be zero) from the array, leaving the remaining elements in their original order.", {}),
    ])),
    N.divider(),
]

# ── Solution 1: Monotonic Deque DP (Interview Pick) ────────────────────────
blocks += [
    N.h2("Solution 1 — DP + Monotonic Deque (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We want the maximum sum over all valid subsequences. Any valid subsequence can be characterised by its last element. Define dp[i] = the maximum subsequence sum that ends at index i. Then the global answer is max(dp)."),
        N.h4("What Doesn't Work"),
        N.para("Brute force over all 2^n subsequences is exponential. Even the naive DP where we scan all k prior dp values per index is O(nk) — up to O(n^2) when k ~ n. We need a smarter way to find the window maximum."),
        N.h4("The Key Observation"),
        N.para("The transition dp[i] = nums[i] + max(0, max dp[j] for j in [i-k, i-1]) requires the maximum over a sliding window of fixed size k. That is exactly the Sliding Window Maximum problem, solvable in O(1) amortized time with a monotonic deque."),
        N.h4("Building the Solution"),
        N.para("Maintain a deque of indices with decreasing dp values (front = window max). At each i: (1) evict expired front indices (gap > k), (2) if front dp > 0 extend dp[i], (3) evict dominated back indices (dp <= dp[i]), (4) push i. Total: O(n)."),
        N.callout(
            "Analogy: Imagine a leaderboard that only shows the top score from the last k players. Every time a new player (index i) scores higher than the current tail, those tail entries drop off — they can never reclaim the lead. The front player is evicted when they are too far behind in the queue. The leaderboard front always tells you the current window best.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("🔬 Algorithm Deep-Dive: Monotonic Deque"),
    N.para(N.rich([
        ("Origin: ", {"bold": True}),
        ("The monotonic deque technique was popularised in competitive programming to compute sliding window maximum/minimum in O(n) total time (amortized O(1) per element), replacing the naive O(nk) scan. It works for any 'dp[i] depends on max dp[j] over a bounded window' pattern.", {}),
    ])),
    N.para(N.rich([
        ("Core invariant: ", {"bold": True}),
        ("The deque stores indices j1 < j2 < ... < jm such that dp[j1] > dp[j2] > ... > dp[jm] — strictly decreasing dp values in increasing index order. The front is always the window maximum.", {}),
    ])),
    N.para(N.rich([
        ("Amortized O(1): ", {"bold": True}),
        ("Every index is pushed exactly once and popped exactly once (either from the front when expired, or from the back when dominated). Total pops across all n iterations <= n. Hence O(n) total work.", {}),
    ])),
    N.para(N.rich([
        ("When to recognise: ", {"bold": True}),
        ("Any DP where dp[i] = f(nums[i], max dp[j] for j in [i-k, i-1]) or the minimum variant. Classic examples: Sliding Window Maximum (#239), Jump Game VI (#1696), this problem.", {}),
    ])),
    N.h3("Code"),
    N.code("""\
from collections import deque

def constrainedSubsetSum(nums: list[int], k: int) -> int:
    dp = nums[:]        # dp[i] = max subsequence sum ending at index i
    dq = deque()        # monotonic deque: indices with decreasing dp values

    for i in range(len(nums)):
        # Step 1: Evict expired front (gap > k)
        while dq and i - dq[0] > k:
            dq.popleft()

        # Step 2: Extend dp[i] if window max is positive
        if dq and dp[dq[0]] > 0:
            dp[i] += dp[dq[0]]

        # Step 3: Evict dominated back entries (dp[back] <= dp[i])
        while dq and dp[dq[-1]] <= dp[i]:
            dq.pop()

        # Step 4: Push current index
        dq.append(i)

    return max(dp)
"""),
    N.h3("Line by Line"),
    N.para(N.rich([("dp = nums[:]", {"code": True}), " — baseline: every index i is a valid single-element subsequence with sum nums[i]."])),
    N.para(N.rich([("dq = deque()", {"code": True}), " — empty deque; will hold indices in order of decreasing dp value."])),
    N.para(N.rich([("while dq and i - dq[0] > k:", {"code": True}), " — the front index is too far back (gap exceeds k). It can never be a valid predecessor for i or any future index, so evict permanently."])),
    N.para(N.rich([("if dq and dp[dq[0]] > 0:", {"code": True}), " — if the window max is positive, extending the subsequence helps; if negative, starting fresh at i is better (the max(0, ...) clamp)."])),
    N.para(N.rich([("dp[i] += dp[dq[0]]", {"code": True}), " — chain the best predecessor's running sum into dp[i]. Result: nums[i] + dp[best_predecessor]."])),
    N.para(N.rich([("while dq and dp[dq[-1]] <= dp[i]:", {"code": True}), " — the back index has a dp value no better than dp[i]. Since i is newer, it dominates for all future queries. Evict."])),
    N.para(N.rich([("dq.append(i)", {"code": True}), " — push current index. Deque now ends with the smallest-dp-value candidate in the window."])),
    N.para(N.rich([("return max(dp)", {"code": True}), " — the global answer is the maximum of all 'ending at i' values."])),
    N.divider(),
]

# ── Solution 2: Brute Force DP ─────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Brute Force DP O(nk)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same DP definition: dp[i] = max subsequence sum ending at i. We just compute the window max naively by scanning the k prior values."),
        N.h4("What Doesn't Work"),
        N.para("This is O(nk) time. Fine when k is small (k=1 gives standard Kadane's O(n)), but degrades to O(n^2) when k ~ n. Not acceptable for large inputs."),
        N.h4("The Key Observation"),
        N.para("The inner loop is just a linear scan for max over a window. Propose this as the starting point in an interview, then offer to optimise to O(n) with a monotonic deque."),
        N.h4("Building the Solution"),
        N.para("For each i, scan dp[max(0,i-k)..i-1] for the maximum positive value. Add it to dp[i] if positive. Return max(dp)."),
    ]),
    N.h3("Code"),
    N.code("""\
def constrainedSubsetSum_brute(nums: list[int], k: int) -> int:
    n = len(nums)
    dp = nums[:]          # single-element baseline

    for i in range(1, n):
        best = 0          # clamp at 0: restart if no positive predecessor
        for j in range(max(0, i - k), i):  # scan window [i-k, i-1]
            best = max(best, dp[j])
        dp[i] += best     # extend if best > 0; otherwise dp[i] = nums[i]

    return max(dp)
"""),
    N.h3("Line by Line"),
    N.para(N.rich([("best = 0", {"code": True}), " — if no predecessor has a positive dp, we start fresh at i (equivalent to max(0, ...) in the recurrence)."])),
    N.para(N.rich([("for j in range(max(0, i-k), i):", {"code": True}), " — scan the valid predecessor window [i-k, i-1], clamped at 0."])),
    N.para(N.rich([("dp[i] += best", {"code": True}), " — adds best (which is 0 if all predecessors were negative, meaning we restart)."])),
    N.divider(),
]

# ── Complexity ─────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force DP", "O(nk)", "O(n)"],
        ["DP + Monotonic Deque (Interview Pick)", "O(n)", "O(n)"],
        ["DP + Max-Heap (alternative)", "O(n log n)", "O(n)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ─────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Monotonic Queue"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "DP + Monotonic Deque (Sliding Window Max applied inside DP)"])),
    N.callout(
        "When to recognise this pattern: (1) 'Subsequence' problem with 'adjacent gap ≤ k' constraint. "
        "(2) DP recurrence needs max or min of dp values over a fixed-size window. "
        "(3) Naive O(k) inner scan makes the whole algorithm O(nk); monotonic deque reduces to O(n). "
        "(4) If k=1, degenerates to Kadane's Algorithm. If k≥n, any subsequence is valid.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ───────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Monotonic Queue / DP + Sliding Window Max):"),
    N.bullet(N.rich([("Sliding Window Maximum", {"bold": True}), " (Hard) — the pure sliding-window-max primitive that this problem's optimisation is built on (#239)"])),
    N.bullet(N.rich([("Jump Game VI", {"bold": True}), " (Medium) — identical recurrence: dp[i] = nums[i] + max dp[j] for j in [i-k, i-1]; no negative-clamp needed (#1696)"])),
    N.bullet(N.rich([("Maximum Subarray (Kadane)", {"bold": True}), " (Medium) — same max(0,...) restart trick but window is unbounded (k=∞); special case of this problem (#53)"])),
    N.bullet(N.rich([("Minimum Number of Coins for Fruits", {"bold": True}), " (Hard) — monotonic deque DP on bounded window intervals (#2944)"])),
    N.bullet(N.rich([("Longest Turbulent Subarray", {"bold": True}), " (Medium) — DP with bounded window transitions; similar reachability structure (#978)"])),
    N.bullet(N.rich([("Maximum Points You Can Obtain from Cards", {"bold": True}), " (Medium) — window-based DP variant on bounded subsequence sums (#1423)"])),
    N.bullet(N.rich([("Jump Game VII", {"bold": True}), " (Medium) — windowed reachability using deque; DP on boolean states (#1871)"])),
    N.para("These problems all share the same core technique: sliding window max/min inside a DP recurrence, optimised via monotonic deque."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section: Stack/Queue → Monotonic Queue. Sub-Pattern: DP + Monotonic Deque. Source: Analysis.", "📚", "gray_background"),
]

# ── Embed ──────────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("constrained_subsequence_sum")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"}),
    ])),
]

# ── Append all blocks ──────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks appended: {len(blocks)}")
