"""
gen_contains_duplicate_iii.py
Notion IN-PLACE update for LeetCode #220 Contains Duplicate III.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-819a-b1d4-e0b81434a0c3"

# ── 1. Properties ─────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=220,
    pattern="Sorting",
    subpatterns=["Bucket Sort + Sliding Window"],
    tc="O(n)",
    sc="O(k)",
    key_insight="Divide value space into buckets of size (t+1); same-bucket values are auto-within-t, check only 3 buckets per element.",
    icon="🔴"
)
print("Properties set.")

# ── 2. Wipe old body ──────────────────────────────────────────────────
print("Wiping old blocks...")
deleted = N.wipe_page(PAGE_ID)
print(f"Deleted {deleted} blocks.")

# ── 3. Rebuild body ───────────────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an integer array ", {}),
        ("nums", {"code": True}),
        (" and two integers ", {}),
        ("indexDiff", {"code": True}),
        (" (k) and ", {}),
        ("valueDiff", {"code": True}),
        (" (t), return ", {}),
        ("True", {"code": True}),
        (" if there exist two distinct indices ", {}),
        ("i", {"code": True}),
        (" and ", {}),
        ("j", {"code": True}),
        (" such that ", {}),
        ("|i − j| ≤ k", {"code": True}),
        (" and ", {}),
        ("|nums[i] − nums[j]| ≤ t", {"code": True}),
        (", otherwise return ", {}),
        ("False", {"code": True}),
        (".", {}),
    ])),
    N.para("Constraints: 2 ≤ nums.length ≤ 10⁵, -10⁹ ≤ nums[i] ≤ 10⁹, 1 ≤ indexDiff ≤ 10⁵, 0 ≤ valueDiff ≤ 10⁹."),
    N.divider(),
]

# ── SOLUTION 1: Bucket Sort + Sliding Window ──────────────────────────
blocks += [
    N.h2("Solution 1 — Bucket Sort + Sliding Window (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We have a sliding window of the last k elements. For each new element, we need to know: 'does any element in this window have a value within t of mine?' The naive O(k) scan leads to O(n·k) total — too slow. We need O(1) per query."),
        N.h4("What Doesn't Work"),
        N.para("A simple hash set lets us find exact duplicates in O(1), but doesn't handle 'within t' proximity. Sorting the whole array loses positional information. A brute-force scan of the window is O(k) per element."),
        N.h4("The Key Observation"),
        N.para("If we partition the number line into 'buckets' of width (t+1), any two values in the SAME bucket differ by at most t — guaranteed, no check needed. Adjacent buckets might also qualify (verify actual diff). Buckets 2+ away are provably too far apart (differ by > t)."),
        N.h4("Building the Solution"),
        N.para("Map each value x to bucket bid = x // (t+1). Maintain a dict of {bid: value} for the current window. For each new x: check bid, bid-1, bid+1 in the dict. If hit → True. Insert x into dict. Evict the element that left the window (delete its bucket entry). At most one value per bucket at any time — if two values were in the same bucket simultaneously, we'd have returned True when inserting the second one."),
        N.callout("Analogy: Think of price ranges in a market. Bucket 0 = items costing $0–$3, bucket 1 = $4–$7, etc. (with t=3, w=4). If two items are in the same price bucket, they're within $3 of each other automatically. You only need to glance at your own bucket and the two adjacent ones.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code("""\
def containsNearbyAlmostDuplicate(nums, indexDiff, valueDiff):
    if valueDiff < 0:
        return False          # impossible constraint

    buckets = {}              # bid -> value in that bucket
    w = valueDiff + 1         # bucket width: same-bucket diff <= valueDiff

    for i, x in enumerate(nums):
        bid = x // w          # Python floor division; correct for negatives

        # Same bucket: guaranteed |diff| <= valueDiff, no check needed
        if bid in buckets:
            return True

        # Left neighbor: actual check required
        if bid - 1 in buckets and abs(x - buckets[bid - 1]) <= valueDiff:
            return True

        # Right neighbor: actual check required
        if bid + 1 in buckets and abs(x - buckets[bid + 1]) <= valueDiff:
            return True

        # Insert x (at most 1 value per bucket enforced by early returns above)
        buckets[bid] = x

        # Slide window: evict element that left the k-sized window
        if i >= indexDiff:
            del buckets[nums[i - indexDiff] // w]

    return False
"""),
    N.h3("Line by Line"),
    N.para(N.rich([("if valueDiff < 0: return False", {"code": True}), (" — Edge case guard. A negative valueDiff is impossible (absolute difference is always ≥ 0), so immediately return False.", {})])),
    N.para(N.rich([("w = valueDiff + 1", {"code": True}), (" — Bucket width. A bucket of this width contains exactly w consecutive integers, any two differing by at most w−1 = valueDiff.", {})])),
    N.para(N.rich([("bid = x // w", {"code": True}), (" — Compute bucket ID using Python floor division. For x=5, w=4: bid=1. For x=−3, w=4: bid=−1 (correctly, since Python floors toward −∞).", {})])),
    N.para(N.rich([("if bid in buckets: return True", {"code": True}), (" — Same bucket means same range of size w. Max diff between any two values in the bucket is w−1 = valueDiff. Return True without checking the actual difference.", {})])),
    N.para(N.rich([("if bid-1 in buckets and abs(x - buckets[bid-1]) <= valueDiff", {"code": True}), (" — Left neighbor might have a value close to x. The bucket boundary could be right next to x, so we verify. Can't skip the abs() check here.", {})])),
    N.para(N.rich([("buckets[bid] = x", {"code": True}), (" — Insert x into its bucket. Because we return True on any collision, there can be at most one value per bucket at any moment.", {})])),
    N.para(N.rich([("if i >= indexDiff: del buckets[nums[i - indexDiff] // w]", {"code": True}), (" — Eviction: the element at index i−indexDiff just fell outside the window. Remove its bucket entry so it can't cause false positives in future lookups.", {})])),
    N.divider(),
]

# ── SOLUTION 2: Sorted Set ────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Sorted Set / BST (O(n log k), good fallback)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Instead of partitioning the value space into buckets, maintain the window in a sorted data structure. Then finding a value in [x−t, x+t] is a binary search."),
        N.h4("What Doesn't Work"),
        N.para("A plain list would require O(k) linear scan. A heap doesn't support arbitrary removal efficiently."),
        N.h4("The Key Observation"),
        N.para("A balanced BST (or Python's SortedList) supports insertion, deletion, and range queries in O(log k). Binary search for x−t gives the first value that could qualify, then check if it's ≤ x+t."),
        N.h4("Building the Solution"),
        N.para("Maintain a SortedList of the current window. For each new x: binary-search for x−t (first value ≥ x−t), check if it's ≤ x+t. If so, return True. Add x. If window > k, remove the oldest element."),
    ]),
    N.h3("Code"),
    N.code("""\
from sortedcontainers import SortedList

def containsNearbyAlmostDuplicate(nums, indexDiff, valueDiff):
    window = SortedList()
    for i, x in enumerate(nums):
        # Find leftmost value >= x - valueDiff
        pos = window.bisect_left(x - valueDiff)
        # Check if that value is also <= x + valueDiff
        if pos < len(window) and window[pos] <= x + valueDiff:
            return True
        window.add(x)
        if len(window) > indexDiff:
            window.remove(nums[i - indexDiff])
    return False
"""),
    N.h3("Line by Line"),
    N.para(N.rich([("window.bisect_left(x - valueDiff)", {"code": True}), (" — O(log k) binary search for the insertion point of x−valueDiff. Returns the index of the leftmost value ≥ (x−valueDiff).", {})])),
    N.para(N.rich([("window[pos] <= x + valueDiff", {"code": True}), (" — The value at pos is ≥ x−t. If it's also ≤ x+t, it's in the range [x−t, x+t], satisfying the valueDiff constraint.", {})])),
    N.para(N.rich([("window.remove(nums[i - indexDiff])", {"code": True}), (" — O(log k) removal by value. Keeps window size exactly indexDiff.", {})])),
    N.divider(),
]

# ── SOLUTION 3: Brute Force ───────────────────────────────────────────
blocks += [
    N.h2("Solution 3 — Brute Force (O(n·k), for understanding only)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("For each element at index i, check every element in the window [i−k, i−1]. If any satisfies |diff| ≤ t, return True."),
        N.h4("What Doesn't Work"),
        N.para("This is O(n·k) which is O(n²) when k approaches n. Exceeds time limit for n=10⁵."),
        N.h4("The Key Observation"),
        N.para("Every pair within the window is checked. No optimization. Useful only for verifying correctness of the faster solutions."),
    ]),
    N.h3("Code"),
    N.code("""\
def containsNearbyAlmostDuplicate(nums, indexDiff, valueDiff):
    n = len(nums)
    for i in range(n):
        # Only look ahead up to indexDiff steps
        for j in range(i + 1, min(i + indexDiff + 1, n)):
            if abs(nums[i] - nums[j]) <= valueDiff:
                return True
    return False
"""),
    N.divider(),
]

# ── Complexity table ──────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force", "O(n·k)", "O(1)"],
        ["Sorted Set (BST)", "O(n log k)", "O(k)"],
        ["Bucket Sort + Sliding Window (optimal)", "O(n)", "O(k)"],
    ]),
    N.divider(),
]

# ── Pattern classification ────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Sorting (bucket sort partitioning the value space)", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Bucket Sort + Sliding Window — divide value axis into equal-width buckets; maintain last k elements in a bucket map to answer O(1) proximity queries.", {})])),
    N.callout(
        "When to recognize this pattern: (1) Sliding window of size k for index constraint. (2) Value proximity query: 'is any element within t?' needed for each new element. (3) Integer values with a natural bucket size (t+1). (4) O(1) per element required (BST gives O(log k) if bucket trick not known).",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related problems ──────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (bucket sort / sliding window value proximity):"),
    N.bullet(N.rich([("Contains Duplicate", {"bold": True}), (" (Easy) — Any exact duplicate in the whole array; simplest version of this family.", {})])),
    N.bullet(N.rich([("Contains Duplicate II", {"bold": True}), (" (Medium) — Exact duplicate within k indices; this problem with valueDiff=0.", {})])),
    N.bullet(N.rich([("Longest Consecutive Sequence", {"bold": True}), (" (Medium) — Hash set partitioning of integer value space; O(n) via bucket-like grouping.", {})])),
    N.bullet(N.rich([("Maximum Gap", {"bold": True}), (" (Hard) — Pigeonhole + bucket sort on value range; find max gap between sorted elements in O(n).", {})])),
    N.bullet(N.rich([("Sliding Window Maximum", {"bold": True}), (" (Hard) — Monotonic deque for O(1) window queries; same sliding window concept, different data structure.", {})])),
    N.bullet(N.rich([("Find K-th Smallest Pair Distance", {"bold": True}), (" (Hard) — Binary search on value distance combined with sliding window counting.", {})])),
    N.para("These problems share the core theme: use the value threshold itself to define a natural partition (bucket width), then answer proximity queries in O(1) rather than O(k)."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Sorting section, Bucket Sort sub-pattern. Sub-pattern classification: Bucket Sort + Sliding Window (Analysis).", "📚", "gray_background"),
]

# ── Embed ─────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("contains_duplicate_iii")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

# ── Append all ────────────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks to Notion...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
