"""
gen_candy.py — Notion IN-PLACE update for Candy (LC #135)
Run from the Algorithms directory: python3 gen_candy.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81e2-998e-e0d8061da1a4"

# ── Step 1: Set properties ──────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=135,
    pattern="Greedy",
    subpatterns=["Two Passes Left/Right"],
    tc="O(n)",
    sc="O(n)",
    key_insight="Solve left-neighbour and right-neighbour constraints independently in one pass each, then take element-wise max.",
    icon="🔴",
)
print("Properties set.")

# ── Step 2: Wipe existing body ──────────────────────────────────────────────
print("Wiping old body...")
removed = N.wipe_page(PAGE_ID)
print(f"Removed {removed} blocks.")

# ── Step 3: Build new body ──────────────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("There are ", {}),
        ("n", {"code": True}),
        (" children standing in a line. Each child has a ", {}),
        ("ratings[i]", {"code": True}),
        (" value. You must give each child at least 1 candy. Children with a higher rating than an adjacent neighbour must receive ", {}),
        ("strictly more", {"bold": True}),
        (" candies than that neighbour. Return the minimum number of candies required.", {}),
    ])),
    N.divider(),
]

# Solution 1 — Two-Pass Greedy (Interview Pick)
sol1_code = """def candy(ratings: list[int]) -> int:
    n = len(ratings)
    left = [1] * n                       # left[i]: min candies for left-neighbour constraint
    for i in range(1, n):
        if ratings[i] > ratings[i - 1]:  # strictly higher than left neighbour
            left[i] = left[i - 1] + 1   # must beat left by exactly 1 (greedy minimum)
    right = [1] * n                      # right[i]: min candies for right-neighbour constraint
    for i in range(n - 2, -1, -1):       # right-to-left pass
        if ratings[i] > ratings[i + 1]:  # strictly higher than right neighbour
            right[i] = right[i + 1] + 1 # must beat right by exactly 1
    return sum(max(l, r) for l, r in zip(left, right))  # max satisfies both"""

blocks += [
    N.h2("Solution 1 — Two-Pass Greedy (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We must assign a minimum positive integer to each child such that, wherever one child has a strictly higher rating than a neighbour, they must hold strictly more candies. Think of it as: each child has two potential demands — one from the left, one from the right — and we must satisfy both simultaneously."),
        N.h4("What Doesn't Work"),
        N.para("A single left-to-right pass only satisfies left-neighbour constraints. A strictly decreasing sequence like [5,4,3,2,1] would leave all values at 1 even though child 0 should get 5, child 1 should get 4, etc. You cannot propagate right-to-left corrections in a single left-to-right sweep."),
        N.h4("The Key Observation"),
        N.para("The left-neighbour constraint and the right-neighbour constraint are causally independent. Left constraints propagate left-to-right; right constraints propagate right-to-left. Solve each separately with a single greedy scan, then take the element-wise maximum — the minimum value that dominates both lower bounds at every position."),
        N.h4("Building the Solution"),
        N.para("1. Left pass (L→R): start left[i]=1 for all i. If ratings[i] > ratings[i-1], set left[i] = left[i-1]+1 (greedy: give exactly one more than needed). 2. Right pass (R→L): start right[i]=1 for all i. If ratings[i] > ratings[i+1], set right[i] = right[i+1]+1. 3. Answer = sum of max(left[i], right[i])."),
        N.callout("Analogy: Think of two independent judges — one walking left-to-right, one right-to-left — each assigning the minimum candy to satisfy their local rule. The child must satisfy both judges; take the stricter verdict (max) at every seat.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(sol1_code),
    N.h3("Line by Line"),
    N.para(N.rich([("n = len(ratings)", {"code": True}), " — number of children."])),
    N.para(N.rich([("left = [1] * n", {"code": True}), " — initialize every child's left-pass candy count to 1 (the minimum allowed)."])),
    N.para(N.rich([("for i in range(1, n):", {"code": True}), " — scan left-to-right starting at index 1 (index 0 has no left neighbour)."])),
    N.para(N.rich([("if ratings[i] > ratings[i - 1]:", {"code": True}), " — strictly higher than left neighbour? (equal doesn't count)"])),
    N.para(N.rich([("left[i] = left[i - 1] + 1", {"code": True}), " — greedy: give exactly one more than the left neighbour had — the minimum needed."])),
    N.para(N.rich([("right = [1] * n", {"code": True}), " — initialize right-pass array with all 1s independently."])),
    N.para(N.rich([("for i in range(n - 2, -1, -1):", {"code": True}), " — right-to-left scan; start at n-2 because index n-1 (last) has no right neighbour."])),
    N.para(N.rich([("if ratings[i] > ratings[i + 1]:", {"code": True}), " — strictly higher than right neighbour?"])),
    N.para(N.rich([("right[i] = right[i + 1] + 1", {"code": True}), " — give exactly one more than the right neighbour — greedy minimum."])),
    N.para(N.rich([("return sum(max(l, r) ...)", {"code": True}), " — for each position, take the max of both constraints (tightest lower bound), then sum."])),
    N.divider(),
]

# Solution 2 — Brute Force
sol2_code = """def candy_brute(ratings: list[int]) -> int:
    n = len(ratings)
    candies = [1] * n
    changed = True
    while changed:           # repeat until no constraint is violated
        changed = False
        for i in range(n - 1):
            if ratings[i] > ratings[i+1] and candies[i] <= candies[i+1]:
                candies[i] = candies[i+1] + 1
                changed = True
    return sum(candies)     # O(n^2) worst case on strictly decreasing input"""

blocks += [
    N.h2("Solution 2 — Brute Force (Repeated Scans)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The most direct approach: keep scanning and fixing violations until there are none left. A violation is any pair where a higher-rated child doesn't have more candies than its neighbour."),
        N.h4("What Doesn't Work for Optimality"),
        N.para("This is correct but slow. On a strictly decreasing input of size n, each pass of the outer loop fixes only one index. You need O(n) passes of O(n) each = O(n^2) total."),
        N.h4("The Key Observation"),
        N.para("This is essentially bubble sort applied to constraint satisfaction. The two-pass approach is the insight that eliminates the outer loop by separating directions."),
        N.callout("Use this in the interview to motivate the two-pass solution: show brute force first, then explain why two directed passes are equivalent to 'convergence in one sweep per direction.'", "💡", "yellow_background"),
    ]),
    N.h3("Code"),
    N.code(sol2_code),
    N.h3("Line by Line"),
    N.para(N.rich([("candies = [1] * n", {"code": True}), " — start every child at the minimum (1 candy)."])),
    N.para(N.rich([("while changed:", {"code": True}), " — keep iterating until a full pass produces no updates (converged)."])),
    N.para(N.rich([("if ratings[i] > ratings[i+1] and candies[i] <= candies[i+1]:", {"code": True}), " — violation found: higher-rated child doesn't beat neighbour."])),
    N.para(N.rich([("candies[i] = candies[i+1] + 1", {"code": True}), " — fix violation by giving one more than the neighbour."])),
    N.para(N.rich([("return sum(candies)", {"code": True}), " — O(n^2) worst case; correct but too slow for large inputs."])),
    N.divider(),
]

# Complexity table
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (repeated scans)", "O(n²)", "O(n)"],
        ["Two-Pass Greedy (optimal)", "O(n)", "O(n)"],
        ["Single-Pass Slope Counting (bonus)", "O(n)", "O(1)"],
    ]),
    N.divider(),
]

# Pattern classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Greedy"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Two Passes Left/Right — decompose bidirectional local constraints into two independent directed passes, then combine results with element-wise max."])),
    N.callout(
        "When to recognize this pattern:\n"
        "• Problem has local constraints that flow in two opposite directions (e.g., 'beat left neighbour' AND 'beat right neighbour')\n"
        "• Each directional constraint alone is solvable greedily in one linear scan\n"
        "• You need a minimum total subject to per-element lower bounds from both directions\n"
        "• Keywords: 'higher rated must get more than adjacent', 'each element must dominate its neighbours'",
        "🔎", "green_background"
    ),
    N.divider(),
]

# Related problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same or closely related technique:"),
    N.bullet(N.rich([("Trapping Rain Water", {"bold": True}), " (Hard) — left-max[] and right-max[] arrays combined at each position; identical two-pass structure. (#42)"])),
    N.bullet(N.rich([("Product of Array Except Self", {"bold": True}), " (Medium) — left-product and right-product merged; same decompose-then-combine approach. (#238)"])),
    N.bullet(N.rich([("Jump Game II", {"bold": True}), " (Medium) — greedy minimum jumps; local greedy decisions yield global optimum. (#45)"])),
    N.bullet(N.rich([("Gas Station", {"bold": True}), " (Medium) — greedy feasibility scan; running sum determines the valid start. (#134)"])),
    N.bullet(N.rich([("Partition Labels", {"bold": True}), " (Medium) — greedy interval merging using a last-occurrence precompute + one-pass merge. (#763)"])),
    N.bullet(N.rich([("Largest Rectangle in Histogram", {"bold": True}), " (Hard) — left-boundary and right-boundary per bar, combined; uses monotonic stack instead of arrays. (#84)"])),
    N.bullet(N.rich([("Container With Most Water", {"bold": True}), " (Medium) — two-pointer greedy: always move the shorter wall inward. (#11)"])),
    N.para("These problems share the core technique: precompute a quantity for each element from the left, precompute from the right, then combine at each position."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 16 (Greedy) · Sub-Pattern: Two Passes Left/Right", "📚", "gray_background"),
]

# Embed section
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("candy")),
    N.para(N.rich([
        ("Step through the two-pass algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Step 4: Append all blocks ───────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
