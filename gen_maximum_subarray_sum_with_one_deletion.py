import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-8169-9eeb-d2aba906b4ea"

# ── 1. Set properties ──────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=1186,
    pattern="Array Manipulation",
    subpatterns=["Kadane's Algorithm", "Forward + Backward Kadane"],
    tc="O(n)",
    sc="O(n)",
    key_insight="Precompute fwd[i] (best subarray ending at i) and bwd[i] (best starting at i); bridge across each deletion with fwd[i-1]+bwd[i+1].",
    icon="🟡"
)
print("Properties set OK")

# ── 2. Wipe old body ───────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks")

# ── 3. Rebuild body ────────────────────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Return the maximum sum of a non-empty subarray of "),
        ("arr", {"code": True}),
        (" with at most one element deleted. An element can only be deleted once. If there is only one element, return it without deletion.")
    ])),
    N.para(N.rich([
        ("Example: "),
        ("arr = [1, -2, 3, 4, -1, 3]", {"code": True}),
        (" → "),
        ("10", {"bold": True}),
        (" (delete -2: subarray [1,3,4,-1,3]=10, or delete -1: subarray [3,4,3]=10)")
    ])),
    N.divider(),
]

# Solution 1 — Forward + Backward Kadane
blocks += [
    N.h2("Solution 1 — Forward + Backward Kadane (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We want the best subarray sum where we can erase one value. Think of it as: if I erase element at position i, I need the best left segment ending at i-1 and the best right segment starting at i+1. Joining those two gives the best answer when deleting i."),
        N.h4("What Doesn't Work"),
        N.para("Brute force: try all n possible deletion positions, run Kadane's each time → O(n²). Too slow for large arrays. We need a way to precompute 'best left side' and 'best right side' for every index simultaneously."),
        N.h4("The Key Observation"),
        N.para("Kadane's algorithm naturally gives us fwd[i] = best subarray ending at i. If we run it backwards, we get bwd[i] = best subarray starting at i. With both precomputed, evaluating any deletion is O(1): fwd[i-1] + bwd[i+1]."),
        N.h4("Building the Solution"),
        N.para("1. Forward Kadane left→right: fwd[i] = max(arr[i], fwd[i-1]+arr[i]). "
               "2. Backward Kadane right→left: bwd[i] = max(arr[i], bwd[i+1]+arr[i]). "
               "3. Initialize ans = max(fwd) — no-deletion case is mandatory. "
               "4. Sweep i from 1 to n-2: ans = max(ans, fwd[i-1]+bwd[i+1])."),
        N.callout(
            "Analogy: Think of fwd[] and bwd[] as two spotlights shining from each end. "
            "For any index i, the left spotlight's reach is fwd[i-1] and the right spotlight's reach is bwd[i+1]. "
            "Deleting i bridges the two beams.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("🔬 Algorithm Deep-Dive: Kadane's Algorithm"),
    N.para(N.rich([
        ("Kadane's Algorithm", {"bold": True}),
        (" was published by Joseph B. Kadane in 1984. It finds the maximum-sum contiguous subarray of a 1-D array in O(n) time and O(1) space. It solves a class of problems of the form: 'find the optimal contiguous window ending at each position'.")
    ])),
    N.code(
        "# Core Kadane's (forward)\n"
        "best_ending_here = arr[0]\n"
        "global_max = arr[0]\n"
        "for num in arr[1:]:\n"
        "    best_ending_here = max(num, best_ending_here + num)  # restart or extend\n"
        "    global_max = max(global_max, best_ending_here)",
        "python"
    ),
    N.para(N.rich([
        ("Core invariant: ", {"bold": True}),
        ("At each step, "),
        ("best_ending_here", {"code": True}),
        (" = maximum sum of any subarray ending at the current index. "
         "This is maintained by the recurrence: extend the previous best (best_ending_here + num) "
         "or restart fresh (num alone), whichever is larger. "
         "The key insight is that a negative prefix can never help a future subarray — restart.")
    ])),
    N.para(N.rich([
        ("Generalization to this problem: ", {"bold": True}),
        ("Run Kadane's twice — once forward to answer 'best ending at i', once backward to answer 'best starting at i'. "
         "Then bridge across a deletion. This pattern extends to k deletions via k+1 state DP.")
    ])),
    N.h3("Code"),
    N.code(
        "def maximumSum(arr):\n"
        "    n = len(arr)\n"
        "    # Phase 1: Forward Kadane\n"
        "    fwd = [0] * n\n"
        "    fwd[0] = arr[0]\n"
        "    for i in range(1, n):\n"
        "        fwd[i] = max(arr[i], fwd[i-1] + arr[i])\n"
        "    # Phase 2: Backward Kadane\n"
        "    bwd = [0] * n\n"
        "    bwd[-1] = arr[-1]\n"
        "    for i in range(n-2, -1, -1):\n"
        "        bwd[i] = max(arr[i], bwd[i+1] + arr[i])\n"
        "    # Phase 3: No-deletion case\n"
        "    ans = max(fwd)\n"
        "    # Phase 4: Try every interior deletion\n"
        "    for i in range(1, n-1):\n"
        "        ans = max(ans, fwd[i-1] + bwd[i+1])\n"
        "    return ans",
        "python"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("fwd = [0]*n; fwd[0] = arr[0]", {"code": True}), " — Allocate forward array. Base case: best subarray ending at index 0 is arr[0] alone."])),
    N.para(N.rich([("fwd[i] = max(arr[i], fwd[i-1] + arr[i])", {"code": True}), " — Kadane's transition: either restart at arr[i] (fresh start is better) or extend the best subarray ending at i-1 by appending arr[i]."])),
    N.para(N.rich([("bwd[-1] = arr[-1]", {"code": True}), " — Base case for backward pass: best subarray starting at the last index is that element alone."])),
    N.para(N.rich([("bwd[i] = max(arr[i], bwd[i+1] + arr[i])", {"code": True}), " — Symmetric Kadane's going right-to-left: restart at arr[i] or extend rightward into bwd[i+1]."])),
    N.para(N.rich([("ans = max(fwd)", {"code": True}), " — Initialize answer with no-deletion case. CRITICAL: deletion is optional, so we must cover zero-deletion scenario first."])),
    N.para(N.rich([("for i in range(1, n-1):", {"code": True}), " — Only interior indices. Deleting index 0 or n-1 just yields a shorter subarray already covered by max(fwd)."])),
    N.para(N.rich([("ans = max(ans, fwd[i-1] + bwd[i+1])", {"code": True}), " — Bridge formula: best left segment (ending at i-1) + best right segment (starting at i+1) = best result when deleting element i."])),
    N.divider(),
]

# Solution 2 — State Machine DP
blocks += [
    N.h2("Solution 2 — State Machine DP (O(1) Space)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("At each position in the array, we are in one of two states: (A) we haven't used our deletion yet, or (B) we've already deleted exactly one element somewhere in our current window. Can we encode this with just two variables?"),
        N.h4("What Doesn't Work"),
        N.para("Trying to track the deletion position explicitly would require O(n) state. We need something that captures 'best result with or without deletion used' without storing where the deletion happened."),
        N.h4("The Key Observation"),
        N.para("Two rolling variables suffice: dp0 = best subarray sum ending here with no deletion used; dp1 = best subarray sum ending here with exactly one deletion used. The recurrences link them cleanly."),
        N.h4("Building the Solution"),
        N.para("For each new element x: "
               "dp1 = max(dp0, dp1 + x) — either delete x right now (dp0, the best without deletion, then skip x) OR extend a window that already used its deletion (dp1 + x). "
               "dp0 = max(x, dp0 + x) — standard Kadane: restart or extend, no deletion. "
               "CRITICAL: update dp1 BEFORE dp0 to use the old dp0 value."),
        N.callout("Update order is crucial: dp1 must see the OLD dp0. If you update dp0 first, dp1's 'delete x' option would consume the already-updated value, creating an off-by-one in which element was 'deleted'.", "⚠️", "yellow_background"),
    ]),
    N.h3("Code"),
    N.code(
        "def maximumSum(arr):\n"
        "    # dp0: best ending here with 0 deletions used\n"
        "    # dp1: best ending here with 1 deletion used\n"
        "    dp0 = dp1 = arr[0]\n"
        "    ans = arr[0]\n"
        "    for x in arr[1:]:\n"
        "        dp1 = max(dp0, dp1 + x)   # delete x OR extend after prev deletion\n"
        "        dp0 = max(x, dp0 + x)     # Kadane's: restart or extend, no deletion\n"
        "        ans = max(ans, dp0, dp1)  # global best from both states\n"
        "    return ans",
        "python"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("dp0 = dp1 = arr[0]", {"code": True}), " — Both states start equal: with one element and zero deletions, both states are just arr[0]. (We haven't had a chance to delete anything yet.)"])),
    N.para(N.rich([("dp1 = max(dp0, dp1 + x)", {"code": True}), " — Two ways to be in 'one deletion used' state: (1) delete x right now — take dp0 (old, no deletion) and skip x; (2) x is NOT the deleted element — extend dp1 by adding x. Uses OLD dp0!"])),
    N.para(N.rich([("dp0 = max(x, dp0 + x)", {"code": True}), " — Standard Kadane's for the no-deletion state: restart at x alone or extend the previous best."])),
    N.para(N.rich([("ans = max(ans, dp0, dp1)", {"code": True}), " — Track global maximum across both states and all positions."])),
    N.divider(),
]

# Complexity
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (try all deletions)", "O(n²)", "O(1)"],
        ["Forward + Backward Kadane", "O(n)", "O(n)"],
        ["State Machine DP (dp0/dp1)", "O(n)", "O(1)"],
    ]),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Array Manipulation (Kadane's Algorithm variant)"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Forward + Backward Kadane; State Machine DP (2-state)"])),
    N.callout(
        "When to recognize this pattern: "
        "'Max/min subarray sum with at most one element removed/skipped' | "
        "'Best contiguous segment bridging a gap' | "
        "You need BOTH best-ending-at-i and best-starting-at-i for the same array | "
        "Two passes of Kadane's (one per direction) allow O(1) per-deletion query",
        "🔎", "green_background"
    ),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Kadane's Algorithm family):"),
    N.bullet(N.rich([("Maximum Subarray", {"bold": True}), " (Medium) — Classic Kadane's, no deletion allowed (#53)"])),
    N.bullet(N.rich([("Maximum Sum Circular Subarray", {"bold": True}), " (Medium) — Kadane's on circular array via complement trick; max of direct and 'total - min subarray' (#918)"])),
    N.bullet(N.rich([("Maximum Product Subarray", {"bold": True}), " (Medium) — Track both max and min at each step; negatives can flip to become maximums (#152)"])),
    N.bullet(N.rich([("K-Concatenation Maximum Sum", {"bold": True}), " (Medium) — Kadane's combined with prefix/suffix sums for repeated arrays (#1191)"])),
    N.bullet(N.rich([("Longest Turbulent Subarray", {"bold": True}), " (Medium) — Kadane's variant tracking alternating sign changes (#978)"])),
    N.bullet(N.rich([("Maximum Absolute Sum of Any Subarray", {"bold": True}), " (Medium) — Run max Kadane's and min Kadane's simultaneously (#1749)"])),
    N.para("These problems all share the core Kadane's technique: at each step decide to restart or extend, maintaining a rolling optimal."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 1.6 (Array Manipulation → Kadane's Algorithm). Sub-Pattern: Forward + Backward Kadane.", "📚", "gray_background"),
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("maximum_subarray_sum_with_one_deletion")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys. "
         "Watch fwd[] and bwd[] build up, then see each deletion evaluated.",
         {"italic": True, "color": "gray"})
    ])),
]

N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
