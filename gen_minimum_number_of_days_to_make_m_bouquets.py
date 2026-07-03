"""
Notion page builder for:
  Minimum Number of Days to Make m Bouquets (LC #1482)
  Notion page ID: 39193418-809c-81b4-83b6-ed777e23c72b
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-81b4-83b6-ed777e23c72b"
SLUG    = "minimum_number_of_days_to_make_m_bouquets"

# ── 1. Properties ──────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=1482,
    pattern="Binary Search",
    subpatterns=["Binary Search on Days"],
    tc="O(n log(max(bloomDay)))",
    sc="O(1)",
    key_insight="Binary search on the answer day; canMake(d) greedily counts consecutive bouquets in O(n).",
    icon="🟡"
)
print("Properties set.")

# ── 2. Wipe old body ────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3. Build body ───────────────────────────────────────────
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given an integer array "), ("bloomDay", {"code": True}),
        (", and integers "), ("m", {"code": True}), (" and "), ("k", {"code": True}),
        (". You want to make "), ("m", {"code": True}),
        (" bouquets. To make a bouquet, you need to use "), ("k", {"code": True}),
        (" adjacent bloomed flowers from the garden. The garden consists of "), ("n", {"code": True}),
        (" flowers, the "), ("i", {"code": True}), ("-th flower will bloom in the "), ("bloomDay[i]", {"code": True}),
        ("-th day. Return the minimum number of days you need to wait to be able to make "),
        ("m", {"code": True}), (" bouquets from the garden. If it is impossible to make "),
        ("m", {"code": True}), (" bouquets, return "), ("-1", {"code": True}), (".")
    ])),
    N.divider(),
]

# ── Solution 1: Binary Search on Days (Optimal) ──
SOL1_CODE = """\
def minDays(bloomDay: list[int], m: int, k: int) -> int:
    n = len(bloomDay)
    if m * k > n:          # Impossible: not enough flowers ever
        return -1
    lo, hi = 1, max(bloomDay)
    ans = hi               # Worst-case fallback (always valid after early-exit guard)
    while lo <= hi:
        mid = (lo + hi) // 2
        if canMake(bloomDay, m, k, mid):
            ans = mid      # Valid! Try to do better with fewer days
            hi = mid - 1
        else:
            lo = mid + 1   # Not enough flowers; need more days
    return ans

def canMake(bloomDay: list[int], m: int, k: int, day: int) -> bool:
    \"\"\"O(n): can we form m bouquets of k consecutive bloomed flowers by `day`?\"\"\"
    bouquets = streak = 0
    for d in bloomDay:
        if d <= day:       # This flower has bloomed by target day
            streak += 1
        else:
            streak = 0     # Gap breaks consecutive run
        if streak == k:    # Completed a full bouquet
            bouquets += 1
            streak = 0     # Used these k flowers; start fresh
    return bouquets >= m
"""

blocks += [
    N.h2("Solution 1 — Binary Search on Days (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Instead of directly computing the answer, ask: 'Given day d, can I form m bouquets?' A flower is available on day d iff bloomDay[i] ≤ d. We need m non-overlapping groups of k consecutive available flowers. This feasibility check is O(n)."),
        N.h4("What Doesn't Work"),
        N.para("Brute force tries every day from 1 to max(bloomDay), running the O(n) check each time. That's O(n × max) — with max up to 10^9, this times out entirely."),
        N.h4("The Key Observation"),
        N.para("The feasibility function canMake(d) is monotone: once day d works, day d+1 also works (same flowers bloomed plus possibly more). There is a threshold T: for all d < T it fails, for all d ≥ T it succeeds. Binary search finds T in O(log(max)) feasibility queries."),
        N.h4("Building the Solution"),
        N.para("Set lo=1, hi=max(bloomDay). Each iteration: mid = (lo+hi)//2. If canMake(mid) is True, record ans=mid and shrink hi=mid-1 (search for a smaller valid day). If False, set lo=mid+1. When lo > hi, ans holds the minimum valid day."),
        N.callout(
            "Analogy: Imagine a light switch that flips from OFF to ON at threshold T. You don't know T, but you can test any position. Binary search: test the midpoint, recurse into the half where the switch flips.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOL1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("if m * k > n", {"code": True}), (" — Early impossibility check. A garden of n flowers can never provide m×k flowers for bouquets, regardless of how long you wait. Return -1 immediately.")])),
    N.para(N.rich([("lo, hi = 1, max(bloomDay)", {"code": True}), (" — Search range over possible days. lo=1 (nothing blooms before day 1). hi=max(bloomDay) (every flower has bloomed). Critical: hi is max(bloomDay), NOT n — bloom days can be up to 10^9.")])),
    N.para(N.rich([("ans = hi", {"code": True}), (" — Initialize answer to worst case (all flowers bloomed). The loop refines it downward. After the early-exit guard, hi is always a valid day (if m*k ≤ n).")])),
    N.para(N.rich([("mid = (lo + hi) // 2", {"code": True}), (" — Candidate day to evaluate.")])),
    N.para(N.rich([("if canMake(..., mid)", {"code": True}), (" — Run the O(n) feasibility check. If we can make m bouquets by day mid, record it and try smaller days (hi = mid-1).")])),
    N.para(N.rich([("else: lo = mid + 1", {"code": True}), (" — Day mid is not enough; we need more days for more flowers to bloom. Search right half.")])),
    N.para(N.rich([("if d <= day: streak += 1", {"code": True}), (" — This flower has bloomed; extend the consecutive run of available flowers.")])),
    N.para(N.rich([("else: streak = 0", {"code": True}), (" — Gap in bloomed flowers. Any bouquet being formed here is broken. Reset streak.")])),
    N.para(N.rich([("if streak == k", {"code": True}), (" — We have exactly k consecutive bloomed flowers. Claim a bouquet. Reset streak (these flowers are used; they cannot be shared with the next bouquet).")])),
    N.para(N.rich([("return bouquets >= m", {"code": True}), (" — Did we accumulate enough bouquets? If yes, this day is feasible.")])),
    N.divider(),
]

# ── Solution 2: Brute Force ──
SOL2_CODE = """\
def minDays_brute(bloomDay: list[int], m: int, k: int) -> int:
    if m * k > len(bloomDay):
        return -1
    for day in range(1, max(bloomDay) + 1):   # Try every day from 1 onward
        if canMake(bloomDay, m, k, day):       # O(n) check
            return day                         # First valid day is the minimum
    return -1
"""

blocks += [
    N.h2("Solution 2 — Brute Force Linear Scan (Too Slow)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The simplest approach: try every day from 1 upward and return the first day that works."),
        N.h4("What Doesn't Work"),
        N.para("This is O(n × max(bloomDay)). For n=10^5 and max=10^9, that is 10^14 operations — far too slow."),
        N.h4("The Key Observation"),
        N.para("This approach is correct but inefficient. It establishes the feasibility check pattern that the binary search solution reuses."),
        N.h4("Building the Solution"),
        N.para("Iterate day from 1 to max(bloomDay). On the first day where canMake returns True, that is the answer. Useful for small inputs or to verify the binary search against."),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("for day in range(1, max(bloomDay) + 1)", {"code": True}), (" — Try every candidate day sequentially. For large max(bloomDay), this is the bottleneck.")])),
    N.para(N.rich([("if canMake(..., day): return day", {"code": True}), (" — The first valid day is the minimum — canMake is monotone, so no need to continue.")])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force", "O(n × max(bloomDay))", "O(1)"],
        ["Binary Search on Days", "O(n log(max(bloomDay)))", "O(1)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Binary Search")])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Binary Search on Days (a variant of Binary Search on Answer)")])),
    N.callout(
        "When to recognize this pattern: The problem asks for a minimum/maximum X such that a condition holds. The condition is monotone in X (once True, always True for larger X). Checking the condition for a given X is efficient (O(n) or O(n log n)). Binary search the answer range [lo, hi], track the leftmost True.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Binary Search on Answer):"),
    N.bullet(N.rich([("Koko Eating Bananas", {"bold": True}), (" (Medium) — Binary search on eating speed; feasibility = all piles done in h hours. (#875)")])),
    N.bullet(N.rich([("Capacity To Ship Packages Within D Days", {"bold": True}), (" (Medium) — Binary search on ship capacity; feasibility = greedy pack into D days. (#1011)")])),
    N.bullet(N.rich([("Split Array Largest Sum", {"bold": True}), (" (Hard) — Binary search on max subarray sum; feasibility = can we partition into ≤ m parts? (#410)")])),
    N.bullet(N.rich([("Magnetic Force Between Two Balls", {"bold": True}), (" (Medium) — Binary search on minimum gap; feasibility = place m balls with at least mid gap. (#1552)")])),
    N.bullet(N.rich([("Valid Perfect Square", {"bold": True}), (" (Easy) — Binary search on the answer (perfect square root). (#367)")])),
    N.bullet(N.rich([("Find Minimum in Rotated Sorted Array", {"bold": True}), (" (Medium) — Classic binary search variant; finding the pivot. (#153)")])),
    N.bullet(N.rich([("Aggressive Cows (SPOJ)", {"bold": True}), (" (Hard) — Prototype of BS-on-answer: maximum minimum gap between cows in stalls.")])),
    N.para("These problems all share the pattern: binary search the answer space + O(n) greedy feasibility check."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 9 — Binary Search", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([("Step through the binary search visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
