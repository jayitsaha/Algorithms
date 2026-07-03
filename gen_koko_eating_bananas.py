"""gen_koko_eating_bananas.py — Rebuild Notion page for #875 Koko Eating Bananas."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-817b-9f59-f7b79bdc8ed6"

# ── 1. Properties ──
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=875,
    pattern="Binary Search",
    subpatterns=["BS: On Answer"],
    tc="O(n log m)",
    sc="O(1)",
    key_insight="Binary search on speed k in [1, max(piles)]; feasibility = sum(ceil(p/k)) <= h.",
    icon="🟡",
)
print("Properties set.")

# ── 2. Wipe ──
deleted = N.wipe_page(PAGE_ID)
print(f"Wiped {deleted} blocks.")

# ── 3. Rebuild body ──
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para("Given an array piles where piles[i] is the number of bananas in the i-th pile, and an integer h (hours until guards return), Koko can choose a speed k (bananas/hour). Each hour she eats from at most one pile, eating at most k bananas. If a pile has fewer than k bananas she eats them all (and stops for that hour). Return the minimum integer k such that she can eat all bananas in at most h hours."),
    N.divider(),
]

# Solution 1 — Binary Search on Speed
blocks += [
    N.h2("Solution 1 — Binary Search on Speed (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need the smallest k such that sum(ceil(pile/k) for pile in piles) <= h. k is an integer in the range [1, max(piles)]. Instead of iterating over piles looking for k, we search over possible values of k."),
        N.h4("What Doesn't Work"),
        N.para("Brute force: try k=1, k=2, ..., k=max(piles) and return the first feasible k. Correct but O(n * max(piles)) — for max pile = 10^9 and n = 10^4, that's 10^13 operations. Way too slow."),
        N.h4("The Key Observation"),
        N.para("Feasibility is monotone: if speed k works, then speed k+1 also works (eating faster never hurts). The predicate feasible(k) is False for k < answer and True for k >= answer — a classic FFFTTTT step function. Binary search finds the boundary in O(log m) steps."),
        N.h4("Building the Solution"),
        N.para("Set lo=1, hi=max(piles). Repeat: pick mid=(lo+hi)//2, compute total hours at speed mid. If feasible (hours <= h): hi=mid (try slower). If infeasible: lo=mid+1 (must go faster). When lo=hi, that is the minimum feasible speed."),
        N.callout("Analogy: You are looking for the lightest backpack that lets you complete a hike. If 5kg is enough, maybe 4kg is too — check the midpoint. This is binary search on the answer space.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(
        "def minEatingSpeed(piles: list[int], h: int) -> int:\n"
        "    lo, hi = 1, max(piles)\n"
        "    while lo < hi:\n"
        "        mid = (lo + hi) // 2\n"
        "        hours = sum((p + mid - 1) // mid for p in piles)\n"
        "        if hours <= h:   # feasible — try slower\n"
        "            hi = mid\n"
        "        else:             # too slow — must go faster\n"
        "            lo = mid + 1\n"
        "    return lo\n"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("lo, hi = 1, max(piles)", {"code": True}), " — Search space: lo is the slowest conceivable speed (1 banana/hr), hi is max pile size (at this speed each pile takes exactly 1 hour, finishing in n hours which is ≤ h since h ≥ n)."])),
    N.para(N.rich([("while lo < hi:", {"code": True}), " — Loop until the range collapses to a single point (lo = hi = answer). When lo = hi, we exit and return lo."])),
    N.para(N.rich([("mid = (lo + hi) // 2", {"code": True}), " — Pick the midpoint as our candidate speed. Integer floor division ensures mid < hi when lo < hi, preventing infinite loops."])),
    N.para(N.rich([("hours = sum((p + mid - 1) // mid for p in piles)", {"code": True}), " — Compute total hours at speed mid. (p + mid - 1) // mid is exact integer ceiling division — avoids floating-point precision bugs for large pile values."])),
    N.para(N.rich([("if hours <= h: hi = mid", {"code": True}), " — Mid is feasible. We keep mid as a candidate (don't use hi = mid - 1, which would skip it) and try to find something smaller by shrinking from the right."])),
    N.para(N.rich([("else: lo = mid + 1", {"code": True}), " — Mid is infeasible (takes too long). Speed mid and everything below it is ruled out. We move lo to mid+1 to search only faster speeds."])),
    N.para(N.rich([("return lo", {"code": True}), " — At exit lo = hi = the minimum feasible speed. lo has been pushed to just past the last infeasible speed throughout the search."])),
    N.divider(),
]

# Solution 2 — Brute Force
blocks += [
    N.h2("Solution 2 — Brute Force (Linear Scan)"),
    N.toggle_h3("💡 Intuition", [
        N.h4("Reframe the Problem"),
        N.para("Simply try every possible speed from 1 upward. The first k that allows Koko to finish in h hours is the answer."),
        N.h4("Why This Works but is Too Slow"),
        N.para("Iterating k=1,2,...,max(piles) is O(max(piles)) iterations. For each, we check all n piles: O(n). Total O(n * max(piles)). For max=10^9 this is unacceptable — TLE. Binary search replaces the O(max) outer loop with O(log max)."),
    ]),
    N.h3("Code"),
    N.code(
        "def minEatingSpeed(piles: list[int], h: int) -> int:\n"
        "    for k in range(1, max(piles) + 1):\n"
        "        if sum((p + k - 1) // k for p in piles) <= h:\n"
        "            return k\n"
    ),
    N.divider(),
]

# Complexity table
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (Linear)", "O(n * m)", "O(1)"],
        ["Binary Search on Speed (optimal)", "O(n log m)", "O(1)"],
    ]),
    N.para("n = len(piles), m = max(piles). Binary search does O(log m) iterations, each O(n). log(10^9) ≈ 30, so even for huge m the search terminates in at most ~30 rounds."),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Binary Search"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "BS: On Answer (also called parametric search or binary search on the answer space)"])),
    N.callout(
        "When to recognize this pattern: 'Find minimum/maximum [value] such that [condition holds]' — when the condition is monotone over the value and the value space has clear bounds. Signals: words like 'minimum speed', 'minimum capacity', 'minimum days', 'maximum allowable'. The feasibility check must be O(n) or better.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Binary Search on Answer):"),
    N.bullet(N.rich([("Capacity to Ship Packages Within D Days", {"bold": True}), " (Medium, #1011) — Minimum ship capacity; identical template: binary search on capacity, feasibility = can all packages ship in D days"])),
    N.bullet(N.rich([("Smallest Divisor Given a Threshold", {"bold": True}), " (Medium, #1283) — Binary search on divisor value; same monotone feasibility structure"])),
    N.bullet(N.rich([("Minimum Number of Days to Make m Bouquets", {"bold": True}), " (Medium, #1482) — Binary search on day count; answer space = [1, max_day]"])),
    N.bullet(N.rich([("Split Array Largest Sum", {"bold": True}), " (Hard, #410) — Minimize the maximum subarray sum; binary search on the max value"])),
    N.bullet(N.rich([("Magnetic Force Between Two Balls", {"bold": True}), " (Medium, #1552) — Maximize minimum distance; 'rightmost False' variant of BS on answer"])),
    N.bullet(N.rich([("Minimum Speed to Arrive on Time", {"bold": True}), " (Medium, #1870) — Nearly identical to Koko but with train schedules and decimal time rounding"])),
    N.bullet(N.rich([("First Bad Version", {"bold": True}), " (Easy, #278) — Classic binary search on boundary; great warmup for the pattern"])),
    N.para("These problems all share the same core technique: binary search over the answer value space using a monotone feasibility predicate."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 9 (Binary Search) — Sub-Pattern: BS: On Answer", "📚", "gray_background"),
]

# Embed
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("koko_eating_bananas")),
    N.para(N.rich([("Step through the binary search visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
