"""
gen_count_subarrays_with_fixed_bounds.py
Notion in-place update for LC #2444 Count Subarrays With Fixed Bounds
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8131-a33f-e1581cff7248"

# 1) Set properties
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=2444,
    pattern="Two Pointers",
    subpatterns=["Three Pointers Tracking"],
    tc="O(n)",
    sc="O(1)",
    key_insight="Track last bad (out-of-range), last minK, last maxK positions; valid left ends per right end = max(0, min(min_pos, max_pos) - bad_pos).",
    icon="🔴"
)
print("Properties set.")

# 2) Wipe old content
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# 3) Rebuild body
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an integer array ", {}),
        ("nums", {"code": True}),
        (" and two integers ", {}),
        ("minK", {"code": True}),
        (" and ", {}),
        ("maxK", {"code": True}),
        (", a fixed-bound subarray is a contiguous subarray where the minimum equals exactly ", {}),
        ("minK", {"code": True}),
        (" and the maximum equals exactly ", {}),
        ("maxK", {"code": True}),
        (". Return the count of all such subarrays.", {}),
    ])),
    N.divider(),
]

# Solution 1 — Brute Force
blocks += [
    N.h2("Solution 1 — Brute Force (O(n²))"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to count contiguous subarrays where the minimum is exactly minK and the maximum is exactly maxK. The simplest way is to try every possible left endpoint, extend the right endpoint one step at a time, and check the running min and max."),
        N.h4("What Doesn't Work Naively"),
        N.para("Checking all O(n²) pairs by recomputing min and max from scratch each time would be O(n³). However, by maintaining a running min and max as we extend the right endpoint, we can reduce this to O(n²). Still too slow for n = 10⁵."),
        N.h4("The Key Observation"),
        N.para("Once the running maximum exceeds maxK, extending the right endpoint further will only increase the max further — never bring it back below maxK. So we can break early when max > maxK."),
        N.h4("Building the Solution"),
        N.para("For each left endpoint l: initialize running lo = hi = nums[l]. Extend right. If hi > maxK, break. If lo == minK and hi == maxK, increment count."),
        N.callout("Analogy: Like checking every window in a building from each floor — you can stop when you're too high up.", "🔭", "gray_background"),
    ]),
    N.h3("Code"),
    N.code("""def countSubarrays_brute(nums, minK, maxK):
    n, ans = len(nums), 0
    for l in range(n):
        lo, hi = nums[l], nums[l]
        for r in range(l, n):
            lo = min(lo, nums[r])
            hi = max(hi, nums[r])
            if hi > maxK:
                break          # can't improve — max only grows
            if lo == minK and hi == maxK:
                ans += 1
    return ans"""),
    N.h3("Line by Line"),
    N.para(N.rich([("for l in range(n):", {"code": True}), (" — fix each left endpoint; O(n) choices.", {})])),
    N.para(N.rich([("lo, hi = nums[l], nums[l]", {"code": True}), (" — initialize running min and max to the first element of this window.", {})])),
    N.para(N.rich([("for r in range(l, n):", {"code": True}), (" — extend the right end of the window.", {})])),
    N.para(N.rich([("if hi > maxK: break", {"code": True}), (" — once max exceeds maxK, all further extensions also exceed it; early exit.", {})])),
    N.para(N.rich([("if lo == minK and hi == maxK:", {"code": True}), (" — both bounds exactly met; this subarray is valid.", {})])),
    N.divider(),
]

# Solution 2 — Optimal Three Pointers
blocks += [
    N.h2("Solution 2 — Three Pointers Tracking (O(n), O(1)) ⭐ Interview Pick"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Instead of checking every subarray, ask: for each right endpoint r, how many valid left endpoints l exist? If we can answer this in O(1), the total becomes O(n)."),
        N.h4("What Doesn't Work"),
        N.para("A standard two-pointer/sliding window shrinks the window when a constraint is violated — but here we have TWO constraints (min and max bounds) that interact non-trivially. A window valid for min might not be valid for max."),
        N.h4("The Key Observation"),
        N.para("Elements outside [minK, maxK] are hard walls — no valid subarray can cross them. For a right endpoint r, valid left endpoints l must: (1) be strictly after the most recent wall (bad_pos), (2) be at or before the most recent minK occurrence (min_pos), and (3) be at or before the most recent maxK occurrence (max_pos). The count is max(0, min(min_pos, max_pos) − bad_pos)."),
        N.h4("Building the Solution"),
        N.para("Track three integers: bad_pos, min_pos, max_pos — all starting at −1. In one sweep, update them as we see wall elements, minK elements, and maxK elements. Add the formula result to ans at each step."),
        N.callout("Analogy: Three bookmark ribbons in a book — the 'red warning ribbon' (last bad element), the 'blue ribbon' (last minK), and the 'green ribbon' (last maxK). Count the pages between red and the earlier of blue/green.", "📚", "blue_background"),
    ]),
    N.h3("Code"),
    N.code("""def countSubarrays(nums, minK, maxK):
    ans = 0
    bad_pos = min_pos = max_pos = -1
    for r, x in enumerate(nums):
        if x < minK or x > maxK:
            bad_pos = r
        if x == minK:
            min_pos = r
        if x == maxK:
            max_pos = r
        ans += max(0, min(min_pos, max_pos) - bad_pos)
    return ans"""),
    N.h3("Line by Line"),
    N.para(N.rich([("bad_pos = min_pos = max_pos = -1", {"code": True}), (" — initialize all bookmarks to −1 (before the array).", {})])),
    N.para(N.rich([("for r, x in enumerate(nums):", {"code": True}), (" — single left-to-right sweep.", {})])),
    N.para(N.rich([("if x < minK or x > maxK:", {"code": True}), (" — element outside [minK, maxK] is a wall; update bad_pos.", {})])),
    N.para(N.rich([("if x == minK:", {"code": True}), (" — NOT elif! Update min_pos. Using if allows minK==maxK case to update both.", {})])),
    N.para(N.rich([("if x == maxK:", {"code": True}), (" — track most recent maxK occurrence.", {})])),
    N.para(N.rich([("ans += max(0, min(min_pos, max_pos) - bad_pos)", {"code": True}), (" — count valid left ends for this r. max(0,...) handles cases where no valid left end exists yet.", {})])),
    N.divider(),
]

# Complexity
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force", "O(n²)", "O(1)"],
        ["Three Pointers (optimal)", "O(n)", "O(1)"],
    ]),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Two Pointers", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Three Pointers Tracking (last bad, last minK, last maxK)", {})])),
    N.callout(
        N.rich([("When to recognize this pattern: ", {"bold": True}),
                ('Count subarrays with BOTH a minimum and maximum exact constraint; elements outside range act as hard resets; need "most recent occurrence" of multiple event types.', {})]),
        "🔎", "green_background"
    ),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique:"),
    N.bullet(N.rich([("Number of Subarrays with Bounded Maximum", {"bold": True}), (" (Medium) — Count subarrays with max in [L, R]; same wall + counting idea (#795)", {})])),
    N.bullet(N.rich([("Subarray Product Less Than K", {"bold": True}), (" (Medium) — Sliding window counting valid subarrays from each right end (#713)", {})])),
    N.bullet(N.rich([("Count Subarrays Where Max Element Appears at Least K Times", {"bold": True}), (" (Medium) — Counting by tracking positions of extreme elements (#2962)", {})])),
    N.bullet(N.rich([("Longest Subarray of 1s After Deleting One Element", {"bold": True}), (" (Medium) — Sliding window with a single bad_pos bookmark (#1493)", {})])),
    N.bullet(N.rich([("Count of Subarrays With Score Less Than K", {"bold": True}), (" (Hard) — Counting valid subarrays using sliding window (#2302)", {})])),
    N.para("These problems share the core idea: counting subarrays by tracking boundary positions per right endpoint."),
    N.divider(),
]

# Embed
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("count_subarrays_with_fixed_bounds")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
