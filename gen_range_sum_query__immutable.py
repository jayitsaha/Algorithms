"""
gen_range_sum_query__immutable.py
Notion in-place update for Range Sum Query - Immutable (#303, Easy, Prefix Sum).
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-811c-802a-f2ae217525d7"

# ── 1) Properties ──────────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=303,
    pattern="Prefix Sum",
    subpatterns=["Basic Prefix Sum Query"],
    tc="O(1) per query",
    sc="O(n)",
    key_insight="Precompute prefix[k]=sum(0..k-1); then sumRange(L,R)=prefix[R+1]-prefix[L] in O(1).",
    icon="🟢",
)
print("Properties set.")

# ── 2) Wipe old content ────────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3) Build body blocks ───────────────────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an integer array ", {}),
        ("nums", {"code": True}),
        (", handle multiple queries of the form: given ", {}),
        ("left", {"code": True}),
        (" and ", {}),
        ("right", {"code": True}),
        (", return the sum of elements between indices ", {}),
        ("left", {"code": True}),
        (" and ", {}),
        ("right", {"code": True}),
        (" (inclusive). The array is immutable — it does not change after initialization.", {}),
    ])),
    N.para(N.rich([
        ("Example: nums = [-2, 0, 3, -5, 2]\n", {"code": True}),
        ("sumRange(0, 2) = 1  (−2 + 0 + 3)\n", {"code": True}),
        ("sumRange(2, 4) = 0  (3 + −5 + 2)\n", {"code": True}),
        ("sumRange(0, 4) = -2 (full array)", {"code": True}),
    ])),
    N.divider(),
]

# ── Solution 1 — Prefix Sum (Interview Pick) ───────────────────────────────────
blocks += [
    N.h2("Solution 1 — Prefix Sum (Interview Pick ★)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to answer 'what is the sum of nums[L..R]?' for many different L, R pairs. The naive approach loops through L..R each time — O(n) per query. With Q queries that's O(nQ), unacceptable for large inputs."),
        N.h4("What Doesn't Work"),
        N.para("Sorting destroys positional information (ranges require ordered indices). Hashing per-element doesn't help because we need sums over contiguous windows. A direct loop works but scales poorly."),
        N.h4("The Key Observation"),
        N.para("sum(L..R) = sum(0..R) − sum(0..L-1). If we precompute 'sum of all elements from 0 to k' for every k, then any range sum becomes one subtraction. This works because subtraction cancels the shared prefix: nums[0..L-1] appears in both terms and disappears."),
        N.h4("Building the Solution"),
        N.para("Define prefix[k] = nums[0] + nums[1] + … + nums[k-1], with prefix[0] = 0 as a sentinel. Build this in O(n) during __init__. Then sumRange(L, R) = prefix[R+1] − prefix[L]. One array lookup, one subtraction — O(1)."),
        N.callout(
            "Analogy: Think of prefix sums like odometer readings on a car. If you know the odometer at milestone L (prefix[L]) and at milestone R+1 (prefix[R+1]), the distance driven between them is simply the difference — no need to re-drive the route.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(
        "class NumArray:\n"
        "    def __init__(self, nums: list[int]):\n"
        "        n = len(nums)\n"
        "        self.prefix = [0] * (n + 1)  # sentinel: prefix[0] = 0\n"
        "        for i in range(n):\n"
        "            self.prefix[i + 1] = self.prefix[i] + nums[i]\n"
        "\n"
        "    def sumRange(self, left: int, right: int) -> int:\n"
        "        return self.prefix[right + 1] - self.prefix[left]"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("self.prefix = [0] * (n + 1)", {"code": True}), (" — Allocate n+1 slots; prefix[0]=0 is the sentinel that handles left=0 without a special case.", {})])),
    N.para(N.rich([("self.prefix[i+1] = self.prefix[i] + nums[i]", {"code": True}), (" — Running total: each prefix[i+1] stores the cumulative sum of nums[0..i]. Built left-to-right in one pass.", {})])),
    N.para(N.rich([("return self.prefix[right+1] - self.prefix[left]", {"code": True}), (" — One subtraction. prefix[right+1] includes nums[right]; prefix[left] covers nums[0..left-1]. Their difference is exactly nums[left..right].", {})])),
    N.divider(),
]

# ── Solution 2 — Brute Force ───────────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Brute Force (O(n) per query)"),
    N.toggle_h3("💡 Intuition", [
        N.h4("Reframe the Problem"),
        N.para("The simplest interpretation: just add up the elements between left and right each time sumRange is called."),
        N.h4("What Doesn't Work"),
        N.para("This is O(n) per query. For Q queries the total is O(nQ). With n=10,000 and Q=10,000 that is 10^8 operations — too slow for tight time limits."),
        N.h4("When to Use"),
        N.para("Acceptable for very few queries or in an interview as the 'brute force starting point' before you propose the optimized approach."),
    ]),
    N.h3("Code"),
    N.code(
        "class NumArray:\n"
        "    def __init__(self, nums):\n"
        "        self.nums = nums  # just store, no preprocessing\n"
        "\n"
        "    def sumRange(self, left, right):\n"
        "        return sum(self.nums[left:right + 1])  # O(n) each call"
    ),
    N.divider(),
]

# ── Complexity ─────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution",       "Init",       "Query", "Space"],
        ["Brute Force",    "O(1)",       "O(n)",  "O(1)"],
        ["Prefix Sum ★",   "O(n)",       "O(1)",  "O(n)"],
        ["Segment Tree",   "O(n log n)", "O(log n)", "O(n)"],
    ]),
    N.para("Prefix Sum is optimal for the immutable variant: amortized O(1) per query after a one-time O(n) build. Segment Tree is overkill here but necessary when updates are allowed."),
    N.divider(),
]

# ── Pattern Classification ─────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Prefix Sum (Array Manipulation)", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Basic Prefix Sum Query", {})])),
    N.callout(
        "When to recognize this pattern: Problem mentions 'multiple queries' on a fixed/immutable array asking for range sums. "
        "Also triggered by 'subarray sum equals k' (add hash map), '2D range sum' (extend to 2D prefix), or "
        "'running total' style problems.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ───────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique:"),
    N.bullet(N.rich([("Range Sum Query 2D - Immutable", {"bold": True}), (" (Medium) — 2D prefix sum with 4-corner formula; #304", {})])),
    N.bullet(N.rich([("Range Sum Query - Mutable", {"bold": True}), (" (Medium) — Array updates allowed → Fenwick Tree / Segment Tree; #307", {})])),
    N.bullet(N.rich([("Subarray Sum Equals K", {"bold": True}), (" (Medium) — Prefix sum + hash map to count subarrays summing to K in O(n); #560", {})])),
    N.bullet(N.rich([("Find Pivot Index", {"bold": True}), (" (Easy) — Left prefix equals right suffix sum; #724", {})])),
    N.bullet(N.rich([("Product of Array Except Self", {"bold": True}), (" (Medium) — Prefix/suffix products instead of sums; #238", {})])),
    N.bullet(N.rich([("Contiguous Array", {"bold": True}), (" (Medium) — Prefix sum with 0→-1 mapping for equal 0/1 subarrays; #525", {})])),
    N.bullet(N.rich([("Continuous Subarray Sum", {"bold": True}), (" (Medium) — Prefix sum modulo k + hash map; #523", {})])),
    N.para("These problems share the core technique: precompute cumulative sums (or a variant) to answer range/aggregate queries in O(1)."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 1.3 — Prefix Sum Pattern", "📚", "gray_background"),
]

# ── Interactive Visual Explainer ───────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("range_sum_query__immutable")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ──────────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
