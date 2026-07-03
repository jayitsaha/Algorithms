"""
gen_sliding_window_maximum.py
Regenerates the Notion page for LC #239 — Sliding Window Maximum.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8140-a533-e78574fb5ed2"

# ── 1) Set page properties ──────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=239,
    pattern="Stack and Queue",
    subpatterns=["Monotonic Queue"],
    tc="O(n)",
    sc="O(k)",
    key_insight="Use a decreasing deque of indices; dominated (smaller+older) elements can be discarded immediately since they will never be a window maximum.",
    icon="🔴",
)
print("Properties set.")

# ── 2) Wipe existing body ───────────────────────────────────────────────────
print("Wiping existing page body...")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3) Build new body ───────────────────────────────────────────────────────
SOLUTION_1 = """\
from collections import deque

def maxSlidingWindow(nums, k):
    dq = deque()      # stores indices, not values
    result = []
    for i, v in enumerate(nums):
        # Step 1: Evict expired indices from front
        while dq and dq[0] <= i - k:
            dq.popleft()
        # Step 2: Remove dominated (smaller) indices from back
        while dq and nums[dq[-1]] <= v:
            dq.pop()
        # Step 3: Append current index
        dq.append(i)
        # Step 4: Record window maximum once window is full
        if i >= k - 1:
            result.append(nums[dq[0]])
    return result
"""

SOLUTION_2 = """\
def maxSlidingWindow_brute(nums, k):
    # O(n*k) — too slow for large inputs but correct baseline
    return [max(nums[i:i+k]) for i in range(len(nums) - k + 1)]
"""

blocks = []

# ── Problem statement ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an integer array ", {}),
        ("nums", {"code": True}),
        (" and an integer ", {}),
        ("k", {"code": True}),
        (", return an array of the maximum value in each contiguous sliding window of size ", {}),
        ("k", {"code": True}),
        (" as it moves from left to right across the array.", {}),
    ])),
    N.para("Example: nums = [1,3,-1,-3,5,3,6,7], k = 3 → [3,3,5,5,6,7]"),
    N.divider(),
]

# ── Solution 1 ──
blocks += [
    N.h2("Solution 1 — Monotonic Decreasing Deque (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We have a window of size k sliding over an array. At each step, one element leaves (left side) and one enters (right side). We need the maximum after every step — but re-scanning k elements each time is O(n·k), which is too slow for large n."),
        N.h4("What Doesn't Work"),
        N.para("Brute force (scan all k elements per window) is O(n·k) — ~10^9 operations for n=10^5, k=50000. A max-heap works but costs O(n log n) and requires lazy deletion of expired elements. We need something O(n)."),
        N.h4("The Key Observation"),
        N.para("When element v enters at index i, any existing element in the deque that is BOTH smaller than v AND has a smaller index (entered earlier) is permanently useless. Why? Any future window containing that older element also contains v (v came after). Since v is larger, the older element can never be the window maximum. Discard it immediately."),
        N.h4("Building the Solution"),
        N.para("We need a structure that supports O(1): remove from front (expired), remove from back (dominated), add to back (new element), peek front (current max). A deque does all four. We store INDICES so we can check window expiry. The deque values (looked up from nums) stay in decreasing order from front to back."),
        N.callout("Analogy: A talent competition queue. When a stronger performer arrives, all weaker performers who will leave before this one are dismissed immediately — they'll never win while this act is available.", "🧠", "blue_background"),
    ]),
    N.h3("🔬 Algorithm Deep-Dive: Monotonic Queue"),
    N.para("A monotonic queue (implemented via a deque) maintains elements in a specific order (increasing or decreasing) by discarding elements that violate the ordering property when a new element arrives. For maximum queries, we keep a DECREASING deque. For minimum queries, an INCREASING deque. The pattern is: O(1) amortized per element because each element is pushed once and popped at most once."),
    N.para("Invariant: After processing index i, the deque contains a subsequence of indices from [max(0,i-k+1), i] with strictly decreasing values. The front is the index of the current window maximum."),
    N.h3("Code"),
    N.code(SOLUTION_1),
    N.h3("Line by Line"),
    N.para(N.rich([("dq = deque()", {"code": True}), (" — Create a deque that stores array INDICES. Using collections.deque gives O(1) popleft; list.pop(0) would be O(n).", {})])),
    N.para(N.rich([("while dq and dq[0] <= i - k: dq.popleft()", {"code": True}), (" — Current window is [i-k+1, i]. Any front index <= i-k is expired (outside window). Evict with popleft() in O(1).", {})])),
    N.para(N.rich([("while dq and nums[dq[-1]] <= v: dq.pop()", {"code": True}), (" — Back of deque has value <= current value v. That index is dominated and permanently useless. Pop from back in O(1).", {})])),
    N.para(N.rich([("dq.append(i)", {"code": True}), (" — Add current index i to the back. Deque remains in decreasing value order because all smaller-or-equal entries were just removed.", {})])),
    N.para(N.rich([("if i >= k - 1:", {"code": True}), (" — First complete window is [0, k-1], i.e., when i == k-1. Start recording maximums from this point onward.", {})])),
    N.para(N.rich([("result.append(nums[dq[0]])", {"code": True}), (" — The front of the deque holds the index with the maximum value in the current window. Append that value.", {})])),
    N.divider(),
]

# ── Solution 2 ──
blocks += [
    N.h2("Solution 2 — Brute Force (Baseline)"),
    N.toggle_h3("💡 Intuition: Naive Scan", [
        N.h4("Reframe the Problem"),
        N.para("Simply extract each window as a slice and find its maximum."),
        N.h4("What Doesn't Work"),
        N.para("This is O(n*k). For n=10^5 and k=10^4, that's 10^9 operations. Will TLE. Only valid for very small inputs or as a starting point to explain to an interviewer."),
        N.h4("The Key Observation"),
        N.para("List slicing and max() in Python are both O(k). We iterate n-k+1 windows. Total: O((n-k+1)*k) = O(n*k)."),
        N.h4("Building the Solution"),
        N.para("One-liner using list comprehension. Clean but slow."),
    ]),
    N.h3("Code"),
    N.code(SOLUTION_2),
    N.h3("Line by Line"),
    N.para(N.rich([("range(len(nums) - k + 1)", {"code": True}), (" — There are n-k+1 valid window starting positions (0-indexed: 0 through n-k).", {})])),
    N.para(N.rich([("max(nums[i:i+k])", {"code": True}), (" — Slice the window and find its max. Each slice is O(k), making total O(n*k).", {})])),
    N.divider(),
]

# ── Complexity table ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Brute Force", "O(n·k)", "O(1) extra", "TLE for large inputs"],
        ["Monotonic Deque", "O(n) amortized", "O(k)", "Each element pushed/popped ≤ once"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Stack and Queue (Monotonic Queue sub-pattern)"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Monotonic Queue — Decreasing Deque for sliding window maximum/minimum queries"])),
    N.callout(
        "When to recognize this pattern: (1) Fixed-size sliding window + range max or min query. (2) Brute force O(n·k) is too slow. (3) A newly arrived element can permanently invalidate earlier elements. (4) Need O(1) current max/min per step. Signals: 'sliding window of size k', 'maximum/minimum in window', 'range query as window moves'.",
        "🔎", "green_background"
    ),
    N.para("Sub-Pattern source: Stack and Queue section of DSA_Patterns_and_SubPatterns_Guide.md — Monotonic Queue entry."),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Monotonic Queue / Decreasing Deque technique:"),
    N.bullet(N.rich([("Jump Game VI", {"bold": True}), " (Medium) — Maximize score with k-length jumps; apply decreasing deque directly on the DP value array"])),
    N.bullet(N.rich([("Longest Continuous Subarray With Absolute Diff ≤ Limit", {"bold": True}), " (Medium) — Use BOTH a max deque and min deque simultaneously for variable-size window"])),
    N.bullet(N.rich([("Max Value of Equation", {"bold": True}), " (Hard) — Transform to y+x form, use decreasing deque with constraint on index difference"])),
    N.bullet(N.rich([("Shortest Subarray with Sum at Least K", {"bold": True}), " (Hard) — Prefix sums + monotonic increasing deque for minimum-length subarray"])),
    N.bullet(N.rich([("Constrained Subsequence Sum", {"bold": True}), " (Hard) — DP with sliding window maximum using decreasing deque on the DP array"])),
    N.bullet(N.rich([("Daily Temperatures", {"bold": True}), " (Medium) — Monotonic decreasing stack (not deque) for 'next greater element'; same decreasing invariant"])),
    N.bullet(N.rich([("Sliding Window Minimum", {"bold": True}), " (variant) — Identical logic, flip to increasing deque: pop back when new value is smaller"])),
    N.para("These problems share the core technique: maintain a monotonic deque to answer extreme-value queries over a sliding range in O(1) amortized per step."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section: Stack and Queue → Monotonic Queue", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("sliding_window_maximum")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

# ── Append in chunks ──
print(f"Appending {len(blocks)} blocks...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
