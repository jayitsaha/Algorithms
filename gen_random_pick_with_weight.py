"""
gen_random_pick_with_weight.py
Notion IN-PLACE update for LC #528 Random Pick with Weight
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8163-b81f-ec51c893f255"

# ── 1. Set properties ──────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=528,
    pattern="Binary Search",
    subpatterns=["Prefix Sum + Binary Search"],
    tc="O(log n) per pick",
    sc="O(n)",
    key_insight="Convert weights to prefix sums; binary search the sorted array for the first entry exceeding a random float.",
    icon="🟡",
)
print("Properties set.")

# ── 2. Wipe old content ────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3. Build body ──────────────────────────────────────────────────────────
blocks = []

# ── Problem ────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given a 0-indexed array of positive integers ", {}),
        ("w", {"code": True}),
        (" where ", {}),
        ("w[i]", {"code": True}),
        (" describes the weight of the ", {}),
        ("i", {"code": True}),
        ("th index.\n\nImplement the ", {}),
        ("Solution", {"code": True}),
        (" class:\n• ", {}),
        ("Solution(int[] w)", {"code": True}),
        (" — initializes the object with the array ", {}),
        ("w", {"code": True}),
        (".\n• ", {}),
        ("int pickIndex()", {"code": True}),
        (" — returns a random index in the range ", {}),
        ("[0, w.length - 1]", {"code": True}),
        (" where the probability of picking index ", {}),
        ("i", {"code": True}),
        (" is ", {}),
        ("w[i] / sum(w)", {"code": True}),
        (".\n\nExample: w=[1,3], pickIndex returns 0 with prob 1/4 and 1 with prob 3/4.", {}),
    ])),
    N.divider(),
]

# ── Solution 1 — Prefix Sum + Binary Search ────────────────────────────────
sol1_code = """\
import random, bisect

class Solution:
    def __init__(self, w: list[int]):
        # Build prefix sum array in one pass — O(n)
        self.prefix = []
        total = 0
        for wt in w:
            total += wt
            self.prefix.append(total)
        # prefix[i] = w[0] + w[1] + ... + w[i]
        # = right boundary of segment i on the weighted number line [0, total)

    def pickIndex(self) -> int:
        # Pick a uniformly random real in [0, total_weight)
        target = random.uniform(0, self.prefix[-1])
        # Binary search: find leftmost index where prefix[i] > target
        # That segment is the one our random point landed in
        return bisect.bisect_right(self.prefix, target)

# Time:  __init__ O(n),  pickIndex O(log n)
# Space: O(n) for the prefix array
"""

sol1_line_by_line = [
    ("import random, bisect", "Import the random module for uniform sampling and bisect for binary search."),
    ("self.prefix = []", "Initialize an empty list to hold cumulative weight sums."),
    ("total = 0", "Running sum starts at 0 — will accumulate each weight."),
    ("for wt in w:", "Iterate over each weight in the input array — one pass, O(n)."),
    ("total += wt", "Add current weight to running total — this is the right boundary of segment i."),
    ("self.prefix.append(total)", "Append the cumulative sum. After the loop, prefix[i] = sum(w[0..i])."),
    ("target = random.uniform(0, self.prefix[-1])", "Generate a uniformly random float in [0, total_weight). This is the random dart throw."),
    ("return bisect.bisect_right(self.prefix, target)", "Find the insertion point after any equal values — the first prefix entry strictly greater than target. That is the segment index we landed in."),
]

blocks += [
    N.h2("Solution 1 — Prefix Sum + Binary Search (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need weighted random sampling: pick index i with probability w[i]/total. The challenge is doing this efficiently for many picks without O(sum(w)) space."),
        N.h4("What Doesn't Work"),
        N.para("Naive expansion: copy index i into a pool w[i] times, then random.choice. O(1) pick but O(sum(w)) space and O(sum(w)) init — if weights reach 10⁵, we'd need 10⁸ slots. Too much."),
        N.h4("The Key Observation"),
        N.para("Each index's weight is a segment width on a number line [0, total_weight). A uniformly random point on that line lands in segment i with probability exactly w[i]/total. We don't need to materialize the expanded pool — just store the segment boundaries (prefix sums)."),
        N.h4("Building the Solution"),
        N.para("1. Build prefix = [w[0], w[0]+w[1], ..., total]. This is O(n) space.\n2. To pick: generate target = random.uniform(0, total). Find the leftmost prefix[i] that is strictly greater than target — that is our segment. Binary search on the sorted prefix array gives O(log n)."),
        N.callout("Analogy: Imagine a colour-coded number line. Blue covers 0–1, purple covers 1–4, cyan covers 4–6. Throw a dart at the line. It lands in purple (1–4) 3/6 = 50% of the time. Prefix sums encode the colour boundaries; binary search finds the colour.", "🎯", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(sol1_code),
    N.h3("Line by Line"),
]
for line, explanation in sol1_line_by_line:
    blocks.append(N.para(N.rich([
        (line, {"code": True, "bold": True}),
        (" — " + explanation, {}),
    ])))

blocks.append(N.divider())

# ── Solution 2 — Expand to flat pool ─────────────────────────────────────
sol2_code = """\
import random

class Solution:
    def __init__(self, w: list[int]):
        # Expand each index i by w[i] copies into a flat pool
        # e.g., w=[1,3,2] -> pool=[0, 1,1,1, 2,2]
        self.pool = []
        for i, wt in enumerate(w):
            self.pool.extend([i] * wt)

    def pickIndex(self) -> int:
        return random.choice(self.pool)  # O(1) pick — just index a random position

# Time:  __init__ O(n + sum(w)),  pickIndex O(1)
# Space: O(sum(w)) — catastrophic if weights are large
"""

blocks += [
    N.h2("Solution 2 — Expand to Flat Pool (Brute Force)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The most direct approach: make the number of copies of each index exactly proportional to its weight, then pick uniformly at random."),
        N.h4("What Doesn't Work"),
        N.para("If w[i] can be up to 10⁵ and n is large, sum(w) can be 10⁸. Building and storing a pool of that size exhausts memory and takes too long to construct."),
        N.h4("The Key Observation"),
        N.para("This approach is pedagogically valuable — it makes the probability argument crystal clear. Every position in the pool is equally likely; index i appears w[i] times out of sum(w) total. But it wastes space."),
        N.h4("Building the Solution"),
        N.para("Iterate through w, extend the pool with w[i] copies of i. Call random.choice on the pool. Correct but impractical for large weights."),
    ]),
    N.h3("Code"),
    N.code(sol2_code),
    N.h3("Line by Line"),
    N.para(N.rich([("self.pool = []", {"code": True, "bold": True}), (" — Initialize empty pool list.", {})])),
    N.para(N.rich([("self.pool.extend([i] * wt)", {"code": True, "bold": True}), (" — Append w[i] copies of index i. After all iterations, pool has sum(w) entries.", {})])),
    N.para(N.rich([("return random.choice(self.pool)", {"code": True, "bold": True}), (" — Uniform pick from the pool. Each index i appears w[i] times, so prob = w[i]/sum(w). Correct but O(sum(w)) space.", {})])),
    N.divider(),
]

# ── Complexity ─────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Init Time", "pickIndex Time", "Space"],
        ["Expand to flat pool", "O(n + sum(w))", "O(1)", "O(sum(w))"],
        ["Prefix Sum + Binary Search (Optimal)", "O(n)", "O(log n)", "O(n)"],
        ["Alias Method (advanced)", "O(n)", "O(1)", "O(n)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ─────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Binary Search — O(log n) search on sorted prefix array.", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Prefix Sum + Binary Search — build cumulative sums during init, binary-search the sorted prefix to find which segment a random value falls in.", {})])),
    N.callout(
        "When to recognize this pattern: (1) 'pick randomly with probability proportional to weight', (2) 'map a value to a range defined by running totals', (3) any weighted-sampling or load-balancing problem. If construction cost is acceptable and each query must be O(log n), reach for prefix sums + binary search.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ────────────────────────────────────────────────────────
related = [
    ("Koko Eating Bananas", "Medium", "#875", "Binary search on answer space (eating speed) — same 'find leftmost valid' binary search pattern"),
    ("Capacity to Ship Packages Within D Days", "Medium", "#1011", "Binary search on capacity; prefix sums used internally to validate feasibility"),
    ("Find First and Last Position of Element in Sorted Array", "Medium", "#34", "Two binary searches (lower/upper bound) on a sorted array"),
    ("Range Sum Query - Immutable", "Easy", "#303", "Build prefix sums once in init, query any range in O(1)"),
    ("Subarray Sum Equals K", "Medium", "#560", "Prefix sums + hash map to count qualifying subarrays — same prefix-sum build step"),
    ("K Closest Elements", "Medium", "#658", "Binary search to find optimal left boundary, then expand window — same bisect pattern"),
    ("Random Pick Index", "Medium", "#398", "Related weighted pick variant using reservoir sampling for equal-weight duplicates"),
]

blocks.append(N.h2("🔗 Related Problems"))
blocks.append(N.para("Problems using the same technique (Prefix Sum + Binary Search):"))
for name, diff, num, note in related:
    blocks.append(N.bullet(N.rich([
        (name, {"bold": True}),
        (f" ({diff}, {num})", {}),
        (f" — {note}", {"color": "gray"}),
    ])))
blocks.append(N.para("These problems all share the core technique: build a prefix/cumulative structure in O(n), then use binary search to find the correct index/bucket in O(log n)."))
blocks.append(N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 9 (Binary Search), Sub-Pattern: Prefix Sum + Binary Search", "📚", "gray_background"))

# ── Embed ──────────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("random_pick_with_weight")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"}),
    ])),
]

# ── Append all blocks ───────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
