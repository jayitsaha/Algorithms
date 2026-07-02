"""
gen_best_sightseeing_pair.py — Notion update for LeetCode #1014 Best Sightseeing Pair
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-815b-9e95-e1c5f8f517bb"
SLUG    = "best_sightseeing_pair"

# ── 1) Set properties ─────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=1014,
    pattern="Array Manipulation",
    subpatterns=["Track Best i + A[i]"],
    tc="O(n)",
    sc="O(1)",
    key_insight="Split score(i,j)=(values[i]+i)+(values[j]-j); track running max of left term.",
    icon="🟡",
)
print("Properties set.")

# ── 2) Wipe existing body ─────────────────────────────────────────────────────
removed = N.wipe_page(PAGE_ID)
print(f"Wiped {removed} old blocks.")

# ── 3) Build body blocks ──────────────────────────────────────────────────────
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given an integer array "), ("values", {"code": True}),
        (". The score of a pair (i, j) with i < j is "),
        ("values[i] + values[j] + i - j", {"code": True}),
        (". Return the maximum score of any sightseeing pair.")
    ])),
    N.divider(),
]

# ── Solution 1 — One-Pass Kadane Variant ──
blocks += [
    N.h2("Solution 1 — One-Pass Kadane Variant (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We want to maximize values[i] + values[j] + i - j over all pairs i < j. This is a 2D optimization: for every right endpoint j, find the best left endpoint i. Brute force is O(n²)."),
        N.h4("What Doesn't Work"),
        N.para("Trying every pair (i, j) is correct but O(n²). For n=50,000 that is 2.5 billion iterations — too slow. We need to avoid the inner loop."),
        N.h4("The Key Observation"),
        N.para("Rearrange the formula: score = (values[i] + i) + (values[j] - j). The first term depends only on i; the second depends only on j. They are completely independent! For a fixed j, the best i is simply the one that maximizes (values[i] + i). We can track that maximum as we scan."),
        N.h4("Building the Solution"),
        N.para("Scan j left to right. Maintain best_i = max(values[k]+k) for all k < j. At each j: (1) update ans using best_i + values[j] - j, then (2) update best_i to include j for future pairs. Order matters: update ans BEFORE best_i to enforce i < j strictly."),
        N.callout(
            "Analogy: Like stock trading — you want to maximize price[j] - price[i]. Track min price so far (that's your 'best i'). Same pattern, different formula.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(
        "def maxScoreSightseeingPair(values):\n"
        "    best_i = values[0] + 0  # best (values[i]+i) seen so far\n"
        "    ans = 0\n"
        "    for j in range(1, len(values)):\n"
        "        # Combine best left term with current right term\n"
        "        ans = max(ans, best_i + values[j] - j)\n"
        "        # Could j be a better left endpoint for future pairs?\n"
        "        best_i = max(best_i, values[j] + j)\n"
        "    return ans"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("best_i = values[0] + 0", {"code": True}), " — Initialize the best left term. For index 0: values[0] + 0. This is the only valid left endpoint before we start the loop."])),
    N.para(N.rich([("ans = 0", {"code": True}), " — Initialize the answer. We'll update this with each candidate score."])),
    N.para(N.rich([("for j in range(1, len(values))", {"code": True}), " — Scan every right endpoint j from index 1 onward (must be strictly > left endpoint)."])),
    N.para(N.rich([("ans = max(ans, best_i + values[j] - j)", {"code": True}), " — Candidate score = best left term + current right term. Rearranged: (values[i]+i) + (values[j]-j). Update ans if better."])),
    N.para(N.rich([("best_i = max(best_i, values[j] + j)", {"code": True}), " — After computing ans, check if j would be a better left endpoint. Update best_i if so. This must happen AFTER the ans update to avoid using i=j."])),
    N.para(N.rich([("return ans", {"code": True}), " — The maximum sightseeing score over all valid (i, j) pairs with i < j."])),
    N.divider(),
]

# ── Solution 2 — Brute Force ──
blocks += [
    N.h2("Solution 2 — Brute Force O(n²)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Simply try every valid pair (i, j) with i < j and compute the score directly from the formula."),
        N.h4("What Doesn't Work"),
        N.para("This approach is too slow for large n. It is useful for understanding the problem and verifying the optimal solution on small examples."),
        N.h4("The Key Observation"),
        N.para("No clever trick — just iterate all pairs. Time is O(n²), which is TLE for n > ~10,000."),
        N.h4("Building the Solution"),
        N.para("Two nested loops: outer for i from 0 to n-2, inner for j from i+1 to n-1. Compute score and track max."),
    ]),
    N.h3("Code"),
    N.code(
        "def maxScoreSightseeingPair_brute(values):\n"
        "    n, ans = len(values), 0\n"
        "    for i in range(n):\n"
        "        for j in range(i + 1, n):\n"
        "            ans = max(ans, values[i] + values[j] + i - j)\n"
        "    return ans"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("for i in range(n)", {"code": True}), " — Outer loop: every possible left endpoint."])),
    N.para(N.rich([("for j in range(i+1, n)", {"code": True}), " — Inner loop: every right endpoint strictly greater than i."])),
    N.para(N.rich([("ans = max(ans, values[i]+values[j]+i-j)", {"code": True}), " — Compute score directly from the formula and update the running maximum."])),
    N.divider(),
]

# ── Complexity table ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["One-Pass Kadane Variant (optimal)", "O(n)", "O(1)"],
        ["Brute Force", "O(n²)", "O(1)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Array Manipulation"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Track Best i + A[i] (Kadane's Algorithm variant)"])),
    N.callout(
        "When to recognize this pattern: Score formula involves two indices i < j with "
        "separable i-only and j-only terms. Formula can be rearranged to f(i) + g(j). "
        "Need to maximize over all pairs in O(n). Keywords: 'sightseeing pair', 'best pair score', "
        "'maximize values[i] + values[j] + some function of i and j'.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Kadane's Algorithm / Track Best Running Max):"),
    N.bullet(N.rich([("Maximum Subarray", {"bold": True}), " (Medium) — Classic Kadane: max subarray sum in O(n) (#53)"])),
    N.bullet(N.rich([("Best Time to Buy and Sell Stock", {"bold": True}), " (Easy) — Track min price seen so far; same running max pattern (#121)"])),
    N.bullet(N.rich([("Maximum Sum Circular Subarray", {"bold": True}), " (Medium) — Kadane + total minus min for wrap-around case (#918)"])),
    N.bullet(N.rich([("Maximum Subarray Sum with One Deletion", {"bold": True}), " (Medium) — Forward + backward Kadane to allow one element deletion (#1186)"])),
    N.bullet(N.rich([("Longest Turbulent Subarray", {"bold": True}), " (Medium) — Two-state Kadane tracking alternating increase/decrease (#978)"])),
    N.para("These problems share the core technique: track the best 'past contribution' in a single variable and combine it with the current element in one pass."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 1.6 — Kadane's Algorithm, Sub-Pattern: Track Best i + A[i]", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ──
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks appended: {len(blocks)}")
