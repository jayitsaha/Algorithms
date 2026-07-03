"""gen_fair_distribution_of_cookies.py — Notion regeneration for LeetCode #2305"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8194-941a-c10d071c3658"

# 1) Set properties
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=2305,
    pattern="Dynamic Programming",
    subpatterns=["Backtracking", "DP: Bitmask"],
    tc="O(k^n) with pruning",
    sc="O(n + k)",
    key_insight="Backtrack bag-by-bag assigning to k children; prune when child total ≥ current best or duplicate total exists (symmetry).",
    icon="🟡"
)
print("Properties set.")

# 2) Wipe existing body
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# 3) Build body
blocks = []

# ── Problem Statement ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an integer array "), ("cookies", {"code": True}),
        (" where "), ("cookies[i]", {"code": True}),
        (" is the number of cookies in the "), ("i", {"code": True}),
        ("-th bag, and an integer "), ("k", {"code": True}),
        (" (the number of children), distribute all "), ("n", {"code": True}),
        (" bags so that the "),
        ("unfairness", {"bold": True}),
        (" — the maximum cookies any child receives — is minimized. Each bag must go to exactly one child (cannot split). Return the minimum possible unfairness."),
    ])),
    N.callout(
        N.rich([("Example: "), ("cookies=[8,15,10,20,8], k=2", {"code": True}),
                (" → ans=31 (Child A: [8,10,20]=38 wait... optimal is [15,8,8]=31 and [20,10]=30 → max=31). "
                 "Small n (≤8) signals exhaustive search is viable.")]),
        "💡", "blue_background"
    ),
    N.divider(),
]

# ── Solution 1: Backtracking with Pruning ──
blocks += [
    N.h2("Solution 1 — Backtracking with Pruning (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Partition n bags into k groups to minimize the maximum group sum. Each bag is indivisible and must go to exactly one child. We want the 'fairest' partition."),
        N.h4("What Doesn't Work"),
        N.para("Greedy (always give the current bag to the child with fewest cookies) doesn't guarantee the global optimum — local greediness fails because a bag given now affects all future assignments. Sorting + greedy also fails; counterexamples exist for k > 2."),
        N.h4("The Key Observation"),
        N.para("n ≤ 8 is tiny. k^n = 8^8 ≈ 16 million at worst — feasible. The search space is all ways to assign n bags to k children. We can exhaustively explore it if we prune aggressively. Two pruning rules collapse the space enormously: (1) value prune: skip if child's total already meets or beats current best answer; (2) symmetry prune: if two children have the same current total, assigning the current bag to either produces identical futures — try only one."),
        N.h4("Building the Solution"),
        N.para("Maintain bags[k] = current total per child. Recurse: for bag i, try assigning it to each child j. Add, recurse, then subtract (backtrack). At leaf (i == n), update ans = min(ans, max(bags)). Pruning cuts most branches before reaching leaves."),
        N.callout("Analogy: Distributing halloween candy bags to kids. You hand them one bag at a time, trying each kid. If one kid already has more candy than your best distribution found so far, skip giving them more — it can only get worse.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(
        '''def distributeCookies(cookies: list[int], k: int) -> int:
    bags = [0] * k        # each child's current total
    ans = float('inf')    # best unfairness found

    def backtrack(i: int):
        nonlocal ans
        if i == len(cookies):            # all bags assigned
            ans = min(ans, max(bags))
            return
        seen = set()                     # symmetry pruning
        for j in range(k):
            if bags[j] in seen:          # skip duplicate total
                continue
            if bags[j] >= ans:           # value prune
                continue
            seen.add(bags[j])
            bags[j] += cookies[i]        # assign bag i to child j
            backtrack(i + 1)
            bags[j] -= cookies[i]        # BACKTRACK: undo assignment

    backtrack(0)
    return ans''',
        "python"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("bags = [0] * k", {"code": True}), " — One slot per child; tracks how many cookies each child currently holds in this partial assignment."])),
    N.para(N.rich([("ans = float('inf')", {"code": True}), " — Best (minimum) unfairness discovered so far. Starts at infinity so any complete assignment beats it."])),
    N.para(N.rich([("if i == len(cookies):", {"code": True}), " — Base case: all n bags have been assigned. Compute unfairness and update ans."])),
    N.para(N.rich([("ans = min(ans, max(bags))", {"code": True}), " — max(bags) is this assignment's unfairness. Record if it's the best seen."])),
    N.para(N.rich([("seen = set()", {"code": True}), " — Tracks child totals we've already tried for THIS bag. If two children have the same total, they're interchangeable — only try one."])),
    N.para(N.rich([("if bags[j] in seen: continue", {"code": True}), " — Symmetry prune: skip children with already-seen totals. Saves huge portions of the search space."])),
    N.para(N.rich([("if bags[j] >= ans: continue", {"code": True}), " — Value prune: if this child's total already matches or exceeds our best answer, adding more cookies can only make things worse. Skip."])),
    N.para(N.rich([("bags[j] += cookies[i]", {"code": True}), " — Assign bag i to child j. This is the 'choose' step of backtracking."])),
    N.para(N.rich([("backtrack(i + 1)", {"code": True}), " — Recurse: assign the next bag."])),
    N.para(N.rich([("bags[j] -= cookies[i]", {"code": True}), " — CRITICAL: undo the assignment before trying the next child. Without this, the state is corrupted for the next iteration."])),
    N.divider(),
]

# ── Why This is DP (Backtracking) ──
blocks += [
    N.h2("Why This is a Backtracking / DP Problem"),
    N.para(N.rich([
        ("Optimal Substructure: ", {"bold": True}),
        ("The optimal unfairness for assigning bags [i..n-1] to k children with current totals bags[0..k-1] depends only on bags and i — not on how we got there. Each subproblem feeds into the next.")
    ])),
    N.para(N.rich([
        ("Overlapping Subproblems (Bitmask DP angle): ", {"bold": True}),
        ("In the bitmask DP formulation, dp[j][mask] = minimum unfairness distributing the subset mask among j children. The same (j, mask) pair can be reached via many different orderings of bag assignments — without memoization, we'd recompute it exponentially often.")
    ])),
    N.divider(),
]

# ── Solution 2: Bitmask DP ──
blocks += [
    N.h2("Solution 2 — Bitmask DP (Polynomial Alternative)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("With n ≤ 8, we can represent any subset of bags as a bitmask (integer where bit i = 1 means bag i is included). There are 2^n = 256 subsets at most."),
        N.h4("The Key Observation"),
        N.para("Define dp[j][mask] = minimum unfairness when we distribute all bags in subset mask among exactly j children. We build up from j=1 to k. For j children and mask, enumerate all submasks sub of mask (give sub to child j, and distribute mask XOR sub among j-1 children). The unfairness contribution from child j is total[sub]; the rest is dp[j-1][mask XOR sub]. Take the max of both parts and minimize over all sub."),
        N.h4("Building the Solution"),
        N.para("Precompute total[mask] = sum of cookies[i] for each i in mask. Then fill dp[j][mask] bottom-up. The answer is dp[k][(1<<n)-1] (all bags among k children)."),
    ]),
    N.h3("Code"),
    N.code(
        '''def distributeCookies(cookies: list[int], k: int) -> int:
    n = len(cookies)
    # Precompute sum for every subset
    total = [0] * (1 << n)
    for mask in range(1 << n):
        for i in range(n):
            if (mask >> i) & 1:
                total[mask] += cookies[i]

    INF = float('inf')
    # dp[j][mask] = min unfairness distributing mask among j children
    dp = [[INF] * (1 << n) for _ in range(k + 1)]
    dp[0][0] = 0  # 0 children, 0 bags -> unfairness 0

    for j in range(1, k + 1):
        for mask in range(1 << n):
            sub = mask
            while sub:               # enumerate all submasks of mask
                prev = mask ^ sub    # bags NOT given to child j
                if dp[j-1][prev] < INF:
                    dp[j][mask] = min(dp[j][mask],
                                      max(dp[j-1][prev], total[sub]))
                sub = (sub - 1) & mask   # next submask trick

    return dp[k][(1 << n) - 1]''',
        "python"
    ),
    N.h3("Recurrence Relation"),
    N.code(
        '''dp[j][mask] = min over all submasks sub of mask:
    max(dp[j-1][mask XOR sub],  total[sub])

# Give submask `sub` to child j
# Remaining bags (mask XOR sub) handled by j-1 children optimally
# Unfairness = max of the two halves
# Base: dp[0][0] = 0  (no children, no bags -> 0)''',
        "python"
    ),
    N.callout("The submask enumeration trick `sub = (sub-1) & mask` iterates through all non-zero submasks of mask in O(2^popcount(mask)) time. Summed over all masks, total work is O(3^n) — because each element is either in sub, in mask-sub, or not in mask (3 choices per element).", "🔎", "green_background"),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Backtracking + Pruning (Interview Pick)", "O(k^n) with heavy pruning", "O(n + k)"],
        ["Bitmask DP", "O(3^n × k)", "O(k × 2^n)"],
        ["Brute Force (no pruning)", "O(k^n)", "O(n + k)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Dynamic Programming"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Backtracking (primary), DP: Bitmask (alternative)"])),
    N.callout(
        N.rich([("When to recognize this pattern: ", {"bold": True}),
                ("n is very small (≤ 15); items must be partitioned into k groups without splitting; "
                 "objective is 'minimize the maximum' (minimax/load-balancing); "
                 "greedy fails due to non-local dependencies; exhaustive search with pruning is feasible.")]),
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique:"),
    N.bullet(N.rich([("Partition to K Equal Sum Subsets", {"bold": True}),
                     " (Medium) — Same backtracking; target sum = total/k. (#698)"])),
    N.bullet(N.rich([("Minimum Number of Work Sessions to Finish the Tasks", {"bold": True}),
                     " (Medium) — Bitmask DP: dp[mask] = min sessions. (#1986)"])),
    N.bullet(N.rich([("Find Minimum Time to Finish All Jobs", {"bold": True}),
                     " (Hard) — Identical structure + binary search on answer. (#1723)"])),
    N.bullet(N.rich([("Campus Bikes II", {"bold": True}),
                     " (Hard) — Bitmask DP assignment: workers to bikes. (#1066)"])),
    N.bullet(N.rich([("Partition Equal Subset Sum", {"bold": True}),
                     " (Medium) — 0/1 knapsack DP; simpler 2-group partition. (#416)"])),
    N.bullet(N.rich([("Travelling Salesman Problem (TSP)", {"bold": True}),
                     " (Hard) — Canonical bitmask DP: visit all cities minimizing cost."])),
    N.bullet(N.rich([("Maximum Students Taking Exam", {"bold": True}),
                     " (Hard) — Bitmask DP over rows of seats. (#1349)"])),
    N.para("These problems share the core technique: exhaustive search over exponentially many subsets, made tractable by bitmask representation and/or backtracking with pruning."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 18 (Dynamic Programming → DP: Bitmask)", "📚", "gray_background"),
    N.divider(),
]

# ── Embed ──
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("fair_distribution_of_cookies")),
    N.para(N.rich([
        ("Step through the backtracking algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
print(f"Total blocks appended: {len(blocks)}")
