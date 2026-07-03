"""
gen_magnetic_force_between_two_balls.py
Rebuilds the Notion page for LeetCode #1552 – Magnetic Force Between Two Balls.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81fd-b037-d006eeb41d87"
SLUG    = "magnetic_force_between_two_balls"

# ── Step 1: Set properties ──────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=1552,
    pattern="Binary Search",
    subpatterns=["Binary Search on Distance"],
    tc="O(n log n + n log D)",
    sc="O(1)",
    key_insight="Binary search the minimum gap d; greedily verify placement feasibility in O(n).",
    icon="🟡",
)
print("Properties set.")

# ── Step 2: Wipe old content ────────────────────────────────────────────────
print("Wiping old page body...")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── Step 3: Build new body ──────────────────────────────────────────────────
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You have ", {}),
        ("n", {"code": True}),
        (" baskets at fixed integer positions along a number line and ", {}),
        ("m", {"code": True}),
        (" balls to place — one ball per basket, but you choose which ", {}),
        ("m", {"code": True}),
        (" of the ", {}),
        ("n", {"code": True}),
        (" baskets to use. The magnetic force between two balls equals their distance. "
         "Return the largest minimum magnetic force (minimum pairwise distance) among any "
         "valid placement of all ", {}),
        ("m", {"code": True}),
        (" balls.", {}),
    ])),
    N.divider(),
]

# ── Solution 1 (Optimal) ──────────────────────────────────────────────────
blocks += [
    N.h2("Solution 1 — Binary Search on Distance (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We are not choosing positions one by one — we are choosing a target quality "
            "metric: 'can all balls be placed so the minimum gap is at least d?' "
            "Reframing as a feasibility question over a numeric range unlocks binary search."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Enumerating all C(n,m) subsets of baskets is exponential — n=100 000, m=50 000 "
            "gives ~10^29999 possibilities. No greedy formula directly picks which m baskets "
            "to use, because the optimal choice depends on the global arrangement."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Feasibility is monotone in d: if we can place m balls with gap ≥ d, "
            "we can also place them with any gap d' < d (same placement, relaxed constraint). "
            "This monotone structure [True, True, True, False, False] is exactly what binary "
            "search requires. We don't search FOR positions — we search FOR the best gap value."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. Sort positions (O(n log n)). "
            "2. Set lo=1 (min gap), hi=max-min (max gap). "
            "3. Binary search: for each mid, run greedy checker can_place(mid) in O(n). "
            "4. If feasible: record ans=mid, push lo=mid+1 (try larger). "
            "5. If infeasible: push hi=mid-1. "
            "6. Return ans (last recorded feasible mid)."
        ),
        N.callout(
            "Analogy: Imagine tuning a dial from 'tight' to 'loose'. At some threshold "
            "the balls stop fitting. Binary search finds that threshold — the largest "
            "setting where they still fit.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(
        "def maxDistance(position: list[int], m: int) -> int:\n"
        "    position.sort()\n"
        "\n"
        "    def can_place(d: int) -> bool:\n"
        "        count = 1\n"
        "        last = position[0]\n"
        "        for pos in position[1:]:\n"
        "            if pos - last >= d:\n"
        "                count += 1\n"
        "                last = pos\n"
        "                if count == m:\n"
        "                    return True\n"
        "        return count >= m\n"
        "\n"
        "    lo, hi = 1, position[-1] - position[0]\n"
        "    ans = 0\n"
        "    while lo <= hi:\n"
        "        mid = (lo + hi) // 2\n"
        "        if can_place(mid):\n"
        "            ans = mid\n"
        "            lo = mid + 1\n"
        "        else:\n"
        "            hi = mid - 1\n"
        "    return ans",
        "python"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("position.sort()", {"code": True}),
                   (" — Sort so the greedy scan always visits positions in increasing order. Required for correctness.", {})])),
    N.para(N.rich([("count = 1; last = position[0]", {"code": True}),
                   (" — Always place the first ball at the leftmost basket. count tracks how many balls have been placed.", {})])),
    N.para(N.rich([("if pos - last >= d:", {"code": True}),
                   (" — This basket is far enough from the last placed ball. Greedy: take the earliest valid basket to maximise room for future balls.", {})])),
    N.para(N.rich([("count += 1; last = pos", {"code": True}),
                   (" — Place a ball here. Update the last placed position.", {})])),
    N.para(N.rich([("if count == m: return True", {"code": True}),
                   (" — Early exit: all balls placed — no need to scan further.", {})])),
    N.para(N.rich([("return count >= m", {"code": True}),
                   (" — After scanning all positions, did we manage to place all m balls?", {})])),
    N.para(N.rich([("lo, hi = 1, position[-1] - position[0]", {"code": True}),
                   (" — Binary search range. lo=1: smallest conceivable gap. hi=max-min: largest conceivable gap.", {})])),
    N.para(N.rich([("if can_place(mid): ans = mid; lo = mid + 1", {"code": True}),
                   (" — Feasible: record this gap as the best so far, then try a LARGER gap (push lo up). This is the 'find last True' template.", {})])),
    N.para(N.rich([("else: hi = mid - 1", {"code": True}),
                   (" — Not feasible: gap too large, search smaller half.", {})])),
    N.para(N.rich([("return ans", {"code": True}),
                   (" — The largest gap for which can_place returned True.", {})])),
    N.divider(),
]

# ── Solution 2 (Brute Force) ──────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Brute Force (All Subsets)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Try every possible selection of m baskets out of n. For each selection, compute the minimum pairwise distance (minimum adjacent gap in the sorted subset). Keep the maximum over all selections."),
        N.h4("What Doesn't Work"),
        N.para("C(n,m) subsets — exponential. For n=20, m=10 this is C(20,10)=184,756. For n=100,000 it is astronomically large. This is only usable for tiny inputs."),
        N.h4("The Key Observation"),
        N.para("This establishes correctness — it is the ground truth. Use it to verify the binary search approach on small examples during an interview."),
        N.h4("Building the Solution"),
        N.para("Enumerate all combinations, sort each, compute min gap, track max."),
    ]),
    N.h3("Code"),
    N.code(
        "from itertools import combinations\n"
        "\n"
        "def maxDistance_brute(position: list[int], m: int) -> int:\n"
        "    best = 0\n"
        "    for subset in combinations(sorted(position), m):\n"
        "        min_gap = min(subset[i+1] - subset[i] for i in range(m - 1))\n"
        "        best = max(best, min_gap)\n"
        "    return best  # O(C(n,m) * m) — infeasible for large n",
        "python"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("combinations(sorted(position), m)", {"code": True}),
                   (" — Generate every C(n,m) subset of m positions.", {})])),
    N.para(N.rich([("min(...)", {"code": True}),
                   (" — Minimum adjacent gap in this sorted subset = the weakest magnetic force for this placement.", {})])),
    N.para(N.rich([("best = max(best, min_gap)", {"code": True}),
                   (" — Track the best (largest minimum gap) across all placements.", {})])),
    N.divider(),
]

# ── Complexity ────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (subsets)", "O(C(n,m) · m)", "O(m)"],
        ["Binary Search on Distance ✓", "O(n log n + n log D)", "O(1)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Binary Search", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Binary Search on Distance (BS on Answer variant)", {})])),
    N.callout(
        "When to recognise this pattern:\n"
        "• Problem says 'maximise the minimum' or 'minimise the maximum'\n"
        "• The answer is a numeric value in a bounded range\n"
        "• You can verify feasibility for a given answer in O(n) or O(n log n)\n"
        "• The feasibility function is monotone (if d works, all d' < d also work)",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Binary Search on Answer / Distance):"),
    N.bullet(N.rich([("Koko Eating Bananas", {"bold": True}), (" (Medium) — BS on eating speed; greedy hours checker — the 'minimise maximum' twin of this problem (#875)", {})])),
    N.bullet(N.rich([("Capacity to Ship Packages Within D Days", {"bold": True}), (" (Medium) — BS on ship capacity; greedy day count (#1011)", {})])),
    N.bullet(N.rich([("Split Array Largest Sum", {"bold": True}), (" (Hard) — Minimise maximum subarray sum; BS on max; greedy partition (#410)", {})])),
    N.bullet(N.rich([("Minimum Number of Days to Make m Bouquets", {"bold": True}), (" (Medium) — BS on blooming day; greedy consecutive flower count (#1482)", {})])),
    N.bullet(N.rich([("Find K-th Smallest Pair Distance", {"bold": True}), (" (Hard) — BS on distance value; count pairs with gap ≤ mid (#719)", {})])),
    N.bullet(N.rich([("Minimum Speed to Arrive on Time", {"bold": True}), (" (Medium) — BS on speed; greedy ceiling-sum check (#1870)", {})])),
    N.bullet(N.rich([("Aggressive Cows (SPOJ/GFG)", {"bold": True}), (" (Medium) — Classic 'spread m cows in n stalls to maximise minimum gap' — essentially identical problem", {})])),
    N.para("These problems all share the same core technique: binary search on the answer value with a greedy O(n) feasibility checker."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 9 (Binary Search → BS on Answer)", "📚", "gray_background"),
]

# ── Interactive Visual Explainer ──────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the binary search algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ─────────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks to Notion page...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
