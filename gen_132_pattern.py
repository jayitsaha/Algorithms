"""
gen_132_pattern.py — Notion update for LeetCode #456: 132 Pattern
Run from the Algorithms directory: python3 gen_132_pattern.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81b5-a992-db35edc3c9db"

# ── 1. Set properties ──────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=456,
    pattern="Stack and Queue",
    subpatterns=["Monotonic Stack (Next Greater)", "Reverse + Track Second Max"],
    tc="O(n)",
    sc="O(n)",
    key_insight="Scan right-to-left with a monotonic decreasing stack; popped values become valid '2' candidates tracked in 'third'.",
    icon="🟡"
)
print("Properties set.")

# ── 2. Wipe old body ───────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3. Rebuild body ────────────────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an array of ", {}),
        ("n", {"code": True}),
        (" integers ", {}),
        ("nums", {"code": True}),
        (", return ", {}),
        ("true", {"code": True}),
        (" if there is a ", {}),
        ("132 pattern", {"bold": True}),
        (" in ", {}),
        ("nums", {"code": True}),
        (".  A 132 pattern is a subsequence of three integers ", {}),
        ("nums[i]", {"code": True}),
        (", ", {}),
        ("nums[j]", {"code": True}),
        (" and ", {}),
        ("nums[k]", {"code": True}),
        (" such that ", {}),
        ("i < j < k", {"code": True}),
        (" and ", {}),
        ("nums[i] < nums[k] < nums[j]", {"code": True}),
        (".  The name '132' refers to the shape: smallest (the '1'), largest (the '3'), then middle (the '2') — in positional order.", {})
    ])),
    N.divider(),
]

# ── Solution 1: Monotonic Stack (Optimal / Interview Pick) ─────────────
blocks += [
    N.h2("Solution 1 — Monotonic Stack, Right-to-Left (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need three indices i < j < k where the values are 'valley → peak → middle': nums[i] is smallest, nums[j] is largest, nums[k] is in between. The '132' name is just the relative value ordering of these three positions."),
        N.h4("What Doesn't Work"),
        N.para("Brute force tries all O(n³) triplets — too slow for n = 2×10⁵. Precomputing prefix minimums reduces the search for the '1' to O(1) per j, but we still scan all k values, giving O(n²). We need to eliminate that inner loop."),
        N.h4("The Key Observation"),
        N.para("Scan RIGHT-TO-LEFT. When processing index i, all valid j and k positions (which must be to the right of i) are already processed. If we can summarize the best possible '2' value from all right-side pairs into a single number, checking whether nums[i] can be the '1' becomes a one-line comparison: nums[i] < third?"),
        N.h4("Building the Solution"),
        N.para("Maintain a monotonic decreasing stack of candidate '3' values. When nums[i] is larger than the stack top, pop it — the popped value is smaller than nums[i], making nums[i] the '3' and the popped value a valid '2'. Track the largest popped value in 'third' (the best '2' we've seen). At each i, if nums[i] < third, we found the '1' — done."),
        N.callout(
            "Analogy: Imagine looking at a mountain range from right to left. The stack keeps track of the tallest peaks we've seen. Whenever we find a peak taller than the stack top, we 'retire' the shorter peak — it becomes a valley candidate. The tallest retired valley is 'third'. If we find a point shorter than that valley, the pattern is complete.",
            "🏔️", "blue_background"
        )
    ]),
    N.h3("Code"),
    N.code("""def find132pattern(nums: list[int]) -> bool:
    third = float('-inf')       # best "2" value found; -inf = none yet
    stack = []                  # monotonic decreasing: candidate "3" values
    for i in range(len(nums) - 1, -1, -1):   # scan right-to-left
        if nums[i] < third:     # nums[i] is the "1"; pattern confirmed
            return True
        while stack and nums[i] > stack[-1]:  # nums[i] beats stack top
            third = max(third, stack.pop())   # popped value is a valid "2"
        stack.append(nums[i])   # push as candidate "3" for future "1" check
    return False"""),
    N.h3("Line by Line"),
    N.para(N.rich([("third = float('-inf')", {"code": True}), ("  — Initialize the best '2' value to -∞. Before any pops, no valid (3, 2) pair has been found, so -∞ ensures the check nums[i] < third never fires prematurely.", {})])),
    N.para(N.rich([("stack = []", {"code": True}), ("  — Empty monotonic stack. Will hold candidate '3' values in strictly decreasing order (bottom to top).", {})])),
    N.para(N.rich([("for i in range(len(nums) - 1, -1, -1):", {"code": True}), ("  — Scan from the rightmost element to the leftmost. When we process index i, all positions j > i and k > i are already in the stack or have been popped.", {})])),
    N.para(N.rich([("if nums[i] < third:", {"code": True}), ("  — Check if the current element can be the '1'. If it is smaller than our confirmed '2' (third), we have all three pieces. Return True immediately.", {})])),
    N.para(N.rich([("while stack and nums[i] > stack[-1]:", {"code": True}), ("  — Pop smaller elements. Each popped element forms a valid (j=current i, k=popped index) pair where nums[j] > nums[k]. This makes the popped value a candidate '2'.", {})])),
    N.para(N.rich([("third = max(third, stack.pop())", {"code": True}), ("  — Keep the largest '2' ever seen. A larger '2' is better because it is easier for future '1' candidates (left side) to be smaller than it.", {})])),
    N.para(N.rich([("stack.append(nums[i])", {"code": True}), ("  — After all pops, push the current element as a candidate '3' for elements further to the left that we will process next.", {})])),
    N.para(N.rich([("return False", {"code": True}), ("  — Scanned all elements without finding nums[i] < third — no 132 pattern exists.", {})])),
    N.divider(),
]

# ── Solution 2: Brute Force ────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Brute Force, Three Nested Loops (O(n³))"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The simplest reading of the problem: try every possible combination of three indices and check the condition directly."),
        N.h4("What Doesn't Work"),
        N.para("For n = 2×10⁵, there are approximately 10¹⁵ triplets — computationally impossible. This solution is only valid for very small inputs (n < ~500)."),
        N.h4("The Key Observation"),
        N.para("For each pair (i, j), nums[k] must satisfy: nums[i] < nums[k] < nums[j]. This directly translates to a three-loop check with no tricks needed."),
        N.h4("Building the Solution"),
        N.para("Loop i from 0 to n-3, j from i+1 to n-2, k from j+1 to n-1. Check nums[i] < nums[k] < nums[j]. Return True if found, False at the end."),
    ]),
    N.h3("Code"),
    N.code("""def find132pattern_brute(nums: list[int]) -> bool:
    n = len(nums)
    for i in range(n - 2):
        for j in range(i + 1, n - 1):
            for k in range(j + 1, n):
                if nums[i] < nums[k] < nums[j]:
                    return True
    return False"""),
    N.h3("Line by Line"),
    N.para(N.rich([("for i in range(n - 2):", {"code": True}), ("  — The '1' position; must leave room for j and k.", {})])),
    N.para(N.rich([("for j in range(i + 1, n - 1):", {"code": True}), ("  — The '3' position (highest value), must come after i and leave room for k.", {})])),
    N.para(N.rich([("for k in range(j + 1, n):", {"code": True}), ("  — The '2' position (middle value), must come after j.", {})])),
    N.para(N.rich([("if nums[i] < nums[k] < nums[j]:", {"code": True}), ("  — Direct 132 pattern check: lowest < middle < highest.", {})])),
    N.divider(),
]

# ── Complexity table ───────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (3 loops)", "O(n³)", "O(1)"],
        ["Prefix Min + 2 loops", "O(n²)", "O(n)"],
        ["Monotonic Stack (optimal)", "O(n)", "O(n)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ─────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Stack and Queue — Monotonic Stack variant", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Monotonic Stack (Next Greater) · Reverse + Track Second Max", {})])),
    N.callout(
        "When to recognize this pattern: (1) 'Find subsequence of k elements with specific value-ordering constraints' — scan from the direction that leaves only 1 constraint to check. (2) 'Detect pattern among three elements at distinct positions' — monotonic stack collapses 2 of the 3 roles into tracked state. (3) 'Efficiently discard candidates that can no longer improve the answer' — monotonic structure.",
        "🔎", "green_background"
    ),
    N.para("Note: 'Reverse + Track Second Max' is a specialized sub-pattern of the Monotonic Stack family, specific to 3-element pattern detection via right-to-left scan."),
    N.divider(),
]

# ── Related Problems ───────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same monotonic stack technique:"),
    N.bullet(N.rich([("Daily Temperatures", {"bold": True}), (" (Medium) — Next greater temperature using stack of indices; same pop-when-larger logic. #739", {})])),
    N.bullet(N.rich([("Next Greater Element I", {"bold": True}), (" (Easy) — Foundational next-greater template with HashMap + stack. #496", {})])),
    N.bullet(N.rich([("Increasing Triplet Subsequence", {"bold": True}), (" (Medium) — The 123 pattern (ascending triplet) using two-variable greedy in O(n). #334", {})])),
    N.bullet(N.rich([("Largest Rectangle in Histogram", {"bold": True}), (" (Hard) — Monotonic increasing stack tracks previous-smaller boundaries for each bar. #84", {})])),
    N.bullet(N.rich([("Remove K Digits", {"bold": True}), (" (Medium) — Greedy monotonic stack: pop larger digits to build the smallest number. #402", {})])),
    N.bullet(N.rich([("Sum of Subarray Minimums", {"bold": True}), (" (Medium) — Monotonic stack to find previous/next smaller elements for each position. #907", {})])),
    N.para("These problems share the core technique: maintain a monotonic structure that efficiently discards elements that can no longer be optimal, reducing the search space from O(n²) to O(n)."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section: Stack/Queue → Monotonic Stack: Next Greater", "📚", "gray_background"),
]

# ── Embed ──────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("132_pattern")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})
    ]))
]

# ── Append all blocks ──────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK — {len(blocks)} blocks appended to {PAGE_ID}")
