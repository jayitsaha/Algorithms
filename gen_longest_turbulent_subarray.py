"""
Notion updater for Longest Turbulent Subarray (#978).
Runs in-place: wipes the existing page body and rebuilds it with full educational content.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8121-8124-fc9fd3f23ebd"

# ── 1) Set properties ──────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=978,
    pattern="Kadane's Algorithm",
    subpatterns=["Two State Kadane (Inc/Dec)"],
    tc="O(n)",
    sc="O(1)",
    key_insight="Track two states — inc (turbulent window ending in up-step) and dec (ending in down-step); each step transitions between states via tuple-swap Kadane.",
    icon="🟡"
)
print("Properties set.")

# ── 2) Wipe existing body ──────────────────────────────────────────────────────
deleted = N.wipe_page(PAGE_ID)
print(f"Wiped {deleted} old blocks.")

# ── 3) Build new body ─────────────────────────────────────────────────────────
blocks = []

# ── Problem Statement ──────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an integer array arr, return the length of the maximum size turbulent subarray of arr.\n\n"
         "A subarray is turbulent if the comparison sign flips between each adjacent pair of elements in the subarray:\n"
         "  • arr[i-1] < arr[i] > arr[i+1]  (up-down-up), OR\n"
         "  • arr[i-1] > arr[i] < arr[i+1]  (down-up-down).\n\n"
         "Constraints: 1 ≤ arr.length ≤ 4×10⁴, 0 ≤ arr[i] ≤ 10⁹.", {})
    ])),
    N.divider(),
]

# ── Solution 1: Two-State Kadane (Interview Pick) ─────────────────────────────
sol1_code = """\
def maxTurbulenceSize(arr: list[int]) -> int:
    n = len(arr)
    if n < 2:
        return n
    inc = dec = 1   # inc: best turbulent length ending in up-step
                    # dec: best turbulent length ending in down-step
    ans = 1
    for i in range(1, n):
        if arr[i] > arr[i-1]:
            inc, dec = dec + 1, 1  # up extends a dec-window; reset dec
        elif arr[i] < arr[i-1]:
            inc, dec = 1, inc + 1  # down extends an inc-window; reset inc
        else:
            inc = dec = 1          # equal kills turbulence; full reset
        ans = max(ans, inc, dec)
    return ans"""

blocks += [
    N.h2("Solution 1 — Two-State Kadane (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We want the longest subarray where the sign of consecutive differences (+, −, 0) strictly alternates. Equal adjacent elements produce sign=0 which breaks turbulence. So we're really asking: how long can + and − signs alternate without a repeat or zero?"),
        N.h4("What Doesn't Work"),
        N.para("Brute force checks every (i, j) subarray pair and scans for turbulence: O(n²) or O(n³). With n up to 40,000 this is too slow. A sliding window with just one length variable fails because extension depends on the direction of the current step, not just the length."),
        N.h4("The Key Observation"),
        N.para("Classic Kadane tracks 'best subarray ending here'. Here, 'ending here' has two variants: ending in an up-step (arr[i] > arr[i-1]) or a down-step (arr[i] < arr[i-1]). An up-step can only extend a down-ending window (because down then up = alternating). A down-step can only extend an up-ending window. Equal steps reset both."),
        N.h4("Building the Solution"),
        N.para("Maintain inc = best turbulent length ending at i with an up-step; dec = ending with a down-step. Transitions: if up → inc, dec = dec+1, 1 (using tuple unpacking to avoid old-value bug). If down → inc, dec = 1, inc+1. If equal → inc = dec = 1. Update ans = max(ans, inc, dec)."),
        N.callout("Analogy: Think of a yo-yo. It can only go up after going down, and down after going up. If it stops moving (equal) or goes the same direction twice, the 'turbulent run' resets. We track the best up-ending and down-ending yo-yo runs simultaneously.", "🧠", "blue_background"),
    ]),
    N.h3("🔬 Algorithm Deep-Dive: Two-State Kadane"),
    N.para(N.rich([
        ("Kadane's Algorithm", {"bold": True}),
        (" (Kadane, 1984) finds the maximum subarray sum in O(n) time by maintaining a running 'best ending here' value. The key invariant: at each step, we either extend the previous subarray or start fresh.\n\n"
         "Two-State Kadane generalizes this to settings where 'ending here' has multiple types. Instead of one running value, we maintain one per type. Transitions between types are determined by the nature of the current element. This pattern appears in:\n"
         "  • Maximum Product Subarray: types are 'max-ending-here' and 'min-ending-here'\n"
         "  • Stock with Transaction Fee: types are 'holding' and 'cash'\n"
         "  • Longest Turbulent Subarray: types are 'inc' and 'dec'\n\n"
         "Core invariant: inc = length of best turbulent window ending at i with last step going up; dec = last step going down. At every i, both invariants hold.", {})
    ])),
    N.h3("Code"),
    N.code(sol1_code),
    N.h3("Line by Line"),
    N.para(N.rich([("inc = dec = 1", {"code": True}), (" — Both states start at 1. A single element is always a valid turbulent subarray.", {})])),
    N.para(N.rich([("ans = 1", {"code": True}), (" — Global best answer; minimum possible is 1.", {})])),
    N.para(N.rich([("for i in range(1, n):", {"code": True}), (" — Scan from index 1; each iteration compares arr[i] to arr[i-1].", {})])),
    N.para(N.rich([("if arr[i] > arr[i-1]:", {"code": True}), (" — Step goes up (sign +).", {})])),
    N.para(N.rich([("    inc, dec = dec + 1, 1", {"code": True}), (" — Tuple unpacking: new inc = old dec + 1 (up extends a down-window); new dec = 1 (can't continue a down-run going up). Both right-hand sides evaluated before assignment.", {})])),
    N.para(N.rich([("elif arr[i] < arr[i-1]:", {"code": True}), (" — Step goes down (sign −).", {})])),
    N.para(N.rich([("    inc, dec = 1, inc + 1", {"code": True}), (" — Symmetric: new dec = old inc + 1; new inc = 1.", {})])),
    N.para(N.rich([("else:", {"code": True}), (" — Equal elements (sign 0). Any turbulent window including this equal boundary is invalid.", {})])),
    N.para(N.rich([("    inc = dec = 1", {"code": True}), (" — Full reset: both states return to single-element window.", {})])),
    N.para(N.rich([("ans = max(ans, inc, dec)", {"code": True}), (" — Best ending here could be in either state; take the max of both.", {})])),
    N.divider(),
]

# ── Solution 2: Brute Force ───────────────────────────────────────────────────
sol2_code = """\
def maxTurbulenceSize_brute(arr: list[int]) -> int:
    n = len(arr)
    ans = 1
    for i in range(n):
        for j in range(i + 1, n):
            # Check if arr[i..j] is turbulent
            turbulent = True
            for k in range(i, j):
                if arr[k] == arr[k+1]:
                    turbulent = False
                    break
                if k > i:
                    prev_up = arr[k-1] < arr[k]
                    curr_up = arr[k] < arr[k+1]
                    if prev_up == curr_up:
                        turbulent = False
                        break
            if turbulent:
                ans = max(ans, j - i + 1)
    return ans"""

blocks += [
    N.h2("Solution 2 — Brute Force (For Reference)"),
    N.toggle_h3("💡 Intuition: Enumerate All Subarrays", [
        N.h4("Reframe the Problem"),
        N.para("Try every possible subarray (i, j) and explicitly verify whether it is turbulent by scanning consecutive pairs within it."),
        N.h4("What Doesn't Work"),
        N.para("Three nested loops means O(n³) in the worst case, or O(n²) if you optimize by stopping early. With n=40,000 this produces ~1.6 billion operations — guaranteed TLE."),
        N.h4("The Key Observation"),
        N.para("This approach works correctly but is impractical. Its value is as a reference to verify the Two-State Kadane on small examples."),
        N.h4("Building the Solution"),
        N.para("Outer loops fix start i and end j. Inner loop checks consecutive pair signs within [i..j]. Track turbulence as a flag."),
    ]),
    N.h3("Code"),
    N.code(sol2_code),
    N.h3("Line by Line"),
    N.para(N.rich([("for i in range(n): for j in range(i+1, n):", {"code": True}), (" — Enumerate all O(n²) subarrays.", {})])),
    N.para(N.rich([("for k in range(i, j):", {"code": True}), (" — Scan within the subarray checking alternating signs.", {})])),
    N.para(N.rich([("if arr[k] == arr[k+1]:", {"code": True}), (" — Zero-sign step immediately breaks turbulence.", {})])),
    N.para(N.rich([("prev_up == curr_up:", {"code": True}), (" — Two consecutive same-direction steps break turbulence.", {})])),
    N.divider(),
]

# ── Complexity Table ──────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Brute Force", "O(n²) – O(n³)", "O(1)", "Correct but TLE; use for reference only"],
        ["Two-State Kadane (Interview Pick)", "O(n)", "O(1)", "Single pass; four scalar variables"],
    ]),
    N.divider(),
]

# ── Pattern Classification ────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Kadane's Algorithm", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Two State Kadane (Inc/Dec)", {})])),
    N.callout(
        "When to recognize this pattern: (1) Problem asks for longest subarray satisfying a local constraint. "
        "(2) The constraint is purely about adjacent pairs (local). "
        "(3) Extension depends on the TYPE of the last step, not just the length. "
        "Two or more Kadane states, one per step-type — transitions between them per element.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Two-State (or multi-state) Kadane technique:"),
    N.bullet(N.rich([("Maximum Subarray", {"bold": True}), (" (Easy, LC 53) — Classic single-state Kadane; the direct ancestor of this pattern.", {})])),
    N.bullet(N.rich([("Maximum Product Subarray", {"bold": True}), (" (Medium, LC 152) — Two-state Kadane (max-product, min-product); handles sign flips.", {})])),
    N.bullet(N.rich([("Wiggle Subsequence", {"bold": True}), (" (Medium, LC 376) — Nearly identical alternating-sign condition but on subsequences; greedy two-state.", {})])),
    N.bullet(N.rich([("Best Time to Buy and Sell Stock II", {"bold": True}), (" (Medium, LC 122) — State-machine DP (hold/cash); same simultaneous-state-update idea.", {})])),
    N.bullet(N.rich([("Longest Mountain in Array", {"bold": True}), (" (Medium, LC 845) — Two-pass (ascending then descending) local constraint.", {})])),
    N.bullet(N.rich([("Count Subarrays With Fixed Bounds", {"bold": True}), (" (Hard, LC 2444) — Running-start tracking with conditional resets; generalizes Kadane reset idea.", {})])),
    N.para("These problems share the core insight: track what's best 'ending here' in each possible state, and use element-driven transitions between states."),
    N.callout("Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 1.6 Kadane's Algorithm / Two-State Kadane (Inc/Dec)", "📚", "gray_background"),
]

# ── Embed ─────────────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("longest_turbulent_subarray")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ─────────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks appended: {len(blocks)}")
