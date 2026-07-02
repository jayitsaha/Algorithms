"""
gen_max_consecutive_ones_iii.py
Regenerates the Notion page for LeetCode #1004 Max Consecutive Ones III IN-PLACE.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81bc-8966-d78d82b0e567"

# ─── 1) Properties ───────────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=1004,
    pattern="Sliding Window",
    subpatterns=["Count Zeros <= K"],
    tc="O(n)",
    sc="O(1)",
    key_insight="Reframe: flip ≤ k zeros = find longest subarray with ≤ k zeros. Variable sliding window.",
    icon="🟡"
)
print("  Properties OK")

# ─── 2) Wipe old body ─────────────────────────────────────────────────────────
print("Wiping old page body...")
deleted = N.wipe_page(PAGE_ID)
print(f"  Deleted {deleted} blocks")

# ─── 3) Build new body ───────────────────────────────────────────────────────
blocks = []

# ── Problem ──────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a binary array ", {}),
        ("nums", {"code": True}),
        (" and an integer ", {}),
        ("k", {"code": True}),
        (", return the maximum number of consecutive 1s in the array if you can flip at most ", {}),
        ("k", {"code": True}),
        (" 0s.", {}),
    ])),
    N.para("Constraints: 1 ≤ nums.length ≤ 10⁵, nums[i] is 0 or 1, 0 ≤ k ≤ nums.length."),
    N.divider(),
]

# ── Solution 1 — Sliding Window (Interview Pick) ──────────────────────────────
sol1_code = """\
def longestOnes(nums: list, k: int) -> int:
    left = 0          # left boundary of the window
    zeros = 0         # zeros currently inside the window [left, right]
    max_len = 0       # best valid window length seen so far
    for right in range(len(nums)):
        if nums[right] == 0:
            zeros += 1        # new element is a zero — consume one flip budget
        while zeros > k:      # window invalid: too many zeros, shrink left
            if nums[left] == 0:
                zeros -= 1    # evicting a zero — restore flip budget
            left += 1
        max_len = max(max_len, right - left + 1)  # valid window — record size
    return max_len"""

blocks += [
    N.h2("Solution 1 — Variable Sliding Window (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "The problem says 'flip at most k zeros.' A flip makes a 0 behave like a 1 inside "
            "a consecutive run. So the question is really: what is the longest contiguous subarray "
            "that contains at most k zeros? The length of that subarray equals the longest run of "
            "ones achievable by flipping those zeros. We never need to actually modify the array."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "The brute-force approach tries every pair (i, j) as a window start and end, counts "
            "zeros in nums[i..j], and records the maximum length when zeros ≤ k. This is O(n²) "
            "and times out for n = 10⁵. The key inefficiency: when we move i forward by 1, we "
            "recount zeros in the remaining window from scratch."
        ),
        N.h4("The Key Observation"),
        N.para(
            "As we expand right, zeros only increases. As we shrink left, zeros only decreases. "
            "We never need to backtrack left — all windows starting before our current left have "
            "already been evaluated. This monotonic behavior is the heart of the sliding window pattern."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Maintain [left, right] as our window. Expand right one step at a time. If adding "
            "nums[right] causes zeros > k, shrink left until zeros ≤ k again. After each "
            "expand+shrink cycle, the window is guaranteed valid — record its length. "
            "Each element is added once (right scan) and removed at most once (left scan) → O(n)."
        ),
        N.callout(
            "Analogy: Imagine a sliding ruler over a sequence of lights (1=on, 0=off). You have "
            "a battery pack that can power k off-lights temporarily. You want the longest span "
            "of lights you can illuminate at once. Slide the ruler right — whenever your battery "
            "is overwhelmed (too many off-lights), shrink from the left until you're within budget again.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(sol1_code),
    N.h3("Line by Line"),
    N.para(N.rich([("left = 0", {"code": True}), " — Left boundary of the window. Starts at index 0. Only ever moves forward (never backward)."])),
    N.para(N.rich([("zeros = 0", {"code": True}), " — Count of zeros currently inside the window [left, right]. Exactly tracks how many flip credits we've consumed."])),
    N.para(N.rich([("max_len = 0", {"code": True}), " — Best valid window length seen so far. Updated after every expand-shrink cycle."])),
    N.para(N.rich([("for right in range(len(nums)):", {"code": True}), " — Expand the window by moving right one step at a time. Right is the new right boundary."])),
    N.para(N.rich([("if nums[right] == 0: zeros += 1", {"code": True}), " — If the incoming element is a zero, we consume one flip budget. If it's a 1, no action needed."])),
    N.para(N.rich([("while zeros > k:", {"code": True}), " — The window is now invalid (too many zeros). Shrink left in a loop — a single step might remove a 1, leaving zeros still > k."])),
    N.para(N.rich([("if nums[left] == 0: zeros -= 1", {"code": True}), " — If we're evicting a zero from the left, restore one flip budget. If we're evicting a 1, zeros is unchanged."])),
    N.para(N.rich([("left += 1", {"code": True}), " — Move the left boundary one step right. After this, the evicted element is no longer in the window."])),
    N.para(N.rich([("max_len = max(max_len, right - left + 1)", {"code": True}), " — Window [left, right] is now valid (≤ k zeros). right - left + 1 is its length. Update best if larger."])),
    N.para(N.rich([("return max_len", {"code": True}), " — After right has swept the entire array, max_len holds the answer."])),
    N.divider(),
]

# ── Solution 2 — Brute Force ─────────────────────────────────────────────────
sol2_code = """\
def longestOnes_brute(nums: list, k: int) -> int:
    n, best = len(nums), 0
    for i in range(n):
        zeros = 0
        for j in range(i, n):
            if nums[j] == 0:
                zeros += 1
            if zeros > k:
                break           # budget exceeded — no point extending further
            best = max(best, j - i + 1)
    return best"""

blocks += [
    N.h2("Solution 2 — Brute Force O(n²)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same reframe: find the longest subarray with at most k zeros."),
        N.h4("What Doesn't Work"),
        N.para("This approach is correct but slow. For each starting index i, we scan rightward until zeros exceed k. Every starting position independently rescans the same range."),
        N.h4("The Key Observation"),
        N.para("When we increment i by 1, we discard work done in the previous inner loop — we're re-scanning elements already visited. The sliding window avoids this by reusing the previous window state."),
        N.h4("Building the Solution"),
        N.para("For each i, walk j from i to n-1, counting zeros. Break when zeros > k. Record j - i + 1. Simple to implement but O(n²) total work."),
    ]),
    N.h3("Code"),
    N.code(sol2_code),
    N.h3("Line by Line"),
    N.para(N.rich([("for i in range(n):", {"code": True}), " — Try every starting index as the left boundary of the window."])),
    N.para(N.rich([("zeros = 0", {"code": True}), " — Reset zero count for each new starting index."])),
    N.para(N.rich([("for j in range(i, n):", {"code": True}), " — Extend right boundary from i to n-1."])),
    N.para(N.rich([("if zeros > k: break", {"code": True}), " — Budget exceeded — any further extension from this i is invalid. Move to next i."])),
    N.para(N.rich([("best = max(best, j - i + 1)", {"code": True}), " — Record valid window length."])),
    N.divider(),
]

# ── Complexity ────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (nested loops)", "O(n²)", "O(1)"],
        ["Sliding Window (optimal)", "O(n)", "O(1)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Sliding Window (DSA Guide Section 1.5 — Variable/Dynamic Window)"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Count Zeros ≤ K — maintain a counter of 'bad' elements (zeros) in the window; shrink when budget exceeded"])),
    N.callout(
        "When to recognize this pattern: binary or integer array + 'at most k' budget + "
        "maximize length + contiguous subarray. Any time you can reframe a problem as "
        "'longest subarray with at most k of some element', reach for the variable sliding window.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Count Zeros ≤ K / Variable Sliding Window technique:"),
    N.bullet(N.rich([("Max Consecutive Ones", {"bold": True}), " (Easy) — k=0 variant; find the longest existing run of 1s without any flips (#485)"])),
    N.bullet(N.rich([("Max Consecutive Ones II", {"bold": True}), " (Medium) — Same problem fixed at k=1; identical sliding window algorithm (#487)"])),
    N.bullet(N.rich([("Longest Subarray of 1s After Deleting One Element", {"bold": True}), " (Medium) — k=1 but must delete exactly one element (even a 1); slight variation (#1493)"])),
    N.bullet(N.rich([("Longest Repeating Character Replacement", {"bold": True}), " (Medium) — Sliding window where 'bad' elements are non-majority characters; track freq map (#424)"])),
    N.bullet(N.rich([("Fruit Into Baskets", {"bold": True}), " (Medium) — Longest subarray with at most 2 distinct values; same expand/shrink template (#904)"])),
    N.bullet(N.rich([("Minimum Swaps to Group All 1s Together II", {"bold": True}), " (Medium) — Fixed-size window equal to total ones; minimize zeros inside (#2134)"])),
    N.para("These problems share the same core technique: maintain a window invariant via a counter, expand right greedily, shrink left when the invariant is violated."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 1.5 — Sliding Window (Variable Window / Count Zeros ≤ K)", "📚", "gray_background"),
]

# ── Embed ─────────────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("max_consecutive_ones_iii")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ─── 4) Append all blocks ─────────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks to Notion page...")
N.append_blocks(PAGE_ID, blocks)
print("  Blocks OK")
print(f"\nNOTION OK {PAGE_ID}")
