"""
gen_optimal_account_balancing.py
Regeneration script for LeetCode #465 — Optimal Account Balancing (Hard)
Pattern: Dynamic Programming / Bitmask DP on Debts
notion_page_id: null → create fresh page
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notion_lib as N

PAGE_ID = "39293418-809c-81fe-a995-fb8bb5c5de9e"  # already created in prior run

# Override token (notion_lib.py was redacted; token is still valid)
N.TOKEN = "NOTION_TOKEN_REDACTED"
N._HEADERS["Authorization"] = f"Bearer {N.TOKEN}"

# ── Step 0: Create page ──────────────────────────────────────────────────────
if PAGE_ID is None:
    PAGE_ID = N.create_page("Optimal Account Balancing", 465, "Hard", "🔴")
    print(f"Created new Notion page: {PAGE_ID}")

# ── Step 1: Set properties ───────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=465,
    pattern="Dynamic Programming",
    subpatterns=["Bitmask DP on Debts"],
    tc="O(3^n)",
    sc="O(2^n)",
    key_insight="Reduce to net balances; partition into zero-sum subsets; each k-person group costs k-1 transactions. Bitmask DP over all 2^n subsets with sub-mask enumeration.",
    icon="🔴"
)
print("Properties set.")

# ── Step 2: Wipe old body (fresh page so nothing to wipe, but safe to call) ──
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── Step 3: Build body blocks ─────────────────────────────────────────────────
SOLUTION_1 = """\
def minTransfers(transactions):
    # Step 1: Compute net balances
    bal = {}
    for u, v, w in transactions:
        bal[u] = bal.get(u, 0) - w   # u paid out w
        bal[v] = bal.get(v, 0) + w   # v received w

    # Step 2: Extract non-zero balances
    debts = [v for v in bal.values() if v != 0]
    n = len(debts)

    # Step 3: Bitmask DP — dp[mask] = min transactions to settle group
    INF = float('inf')
    dp = [INF] * (1 << n)
    dp[0] = 0  # empty group: 0 transactions

    for mask in range(1, 1 << n):
        # Enumerate all non-empty sub-masks of mask
        sub = mask
        while sub:
            # Compute sum of this sub-mask
            s_sum = sum(debts[i] for i in range(n) if sub & (1 << i))
            if s_sum == 0:  # zero-sum subgroup found
                k = bin(sub).count('1')  # group size
                # k people need k-1 transactions; combine with solved remainder
                dp[mask] = min(dp[mask], dp[mask ^ sub] + k - 1)
            sub = (sub - 1) & mask  # classic sub-mask enumeration

    # Answer: min transactions to settle all n people
    return dp[(1 << n) - 1]
"""

SOLUTION_2 = """\
def minTransfers(transactions):
    # Compute net balances (same as Solution 1)
    bal = {}
    for u, v, w in transactions:
        bal[u] = bal.get(u, 0) - w
        bal[v] = bal.get(v, 0) + w
    debts = [v for v in bal.values() if v != 0]

    def dfs(idx):
        # Skip people already settled
        while idx < len(debts) and debts[idx] == 0:
            idx += 1
        if idx == len(debts):
            return 0  # everyone settled

        res = float('inf')
        # Try settling debts[idx] against every other person with opposite sign
        for j in range(idx + 1, len(debts)):
            if debts[j] * debts[idx] < 0:  # one positive, one negative
                debts[j] += debts[idx]      # idx transfers to j (clears idx)
                res = min(res, 1 + dfs(idx + 1))
                debts[j] -= debts[idx]      # backtrack
        return res

    return dfs(0)
"""

SOLUTION_GREEDY = """\
import heapq
def minTransfers_greedy(transactions):
    # Greedy: always match largest creditor with largest debtor
    # WARNING: This is NOT optimal — shown here for comparison only
    bal = {}
    for u, v, w in transactions:
        bal[u] = bal.get(u, 0) - w
        bal[v] = bal.get(v, 0) + w

    pos = sorted([v for v in bal.values() if v > 0], reverse=True)
    neg = sorted([v for v in bal.values() if v < 0])

    count = 0
    i, j = 0, 0
    while i < len(pos) and j < len(neg):
        amt = min(pos[i], -neg[j])
        pos[i] -= amt
        neg[j] += amt
        count += 1
        if pos[i] == 0: i += 1
        if neg[j] == 0: j += 1
    return count  # may be suboptimal!
"""

blocks = []

# ── Problem Statement ──────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        "You are given a list of transactions where each transaction is represented as ",
        ("transactions[i] = [from_i, to_i, amount_i]", {"code": True}),
        ", indicating that person ",
        ("from_i", {"code": True}),
        " gave ",
        ("amount_i", {"code": True}),
        " dollars to person ",
        ("to_i", {"code": True}),
        ". Return the minimum number of transactions required to settle all the debts."
    ])),
    N.para("Example: transactions = [[0,1,10],[1,0,1],[1,2,5],[0,3,5]]"),
    N.para("Net balances: P0=+4, P1=-4, P2=+5, P3=-5. Answer: 2 (P1→P0 $4, P3→P2 $5)."),
    N.callout("Key reduction: The original transaction graph is irrelevant. Only each person's net balance matters. Creditors have positive balance (are owed), debtors have negative (owe). The problem is then to partition non-zero balances into zero-sum groups and settle each group in (group_size - 1) transactions.", "💡", "green_background"),
    N.divider(),
]

# ── Solution 1: Bitmask DP ─────────────────────────────────────────────────────
blocks += [
    N.h2("Solution 1 — Bitmask DP (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Forget the individual transactions. After summing up, each person has a net balance: positive = creditor (is owed money), negative = debtor (owes money). The balances always sum to zero globally. We need to find the minimum number of direct payments to make everyone's balance zero."),
        N.h4("What Doesn't Work"),
        N.para("Greedy (always match the largest creditor with the largest debtor) seems natural but fails. Example: balances [+3, +3, -4, -2]. Greedy: match +3 and -4 (1 tx, +3 and -2 remain). Then match +3 and -2 (1 tx, +1 remains with nothing to cancel) — STUCK. Optimal: [+3, -2, -1 split] and [+3, -4, +1 split] might be better. Greedy misses globally optimal partitions."),
        N.h4("The Key Observation"),
        N.para("A group of people can settle among themselves if and only if their net balances sum to zero. Within such a zero-sum group of k people, you always need exactly k-1 transactions (chain: person 1 pays person 2, 2 pays 3, ..., k-1 pays k). So the problem reduces to: find the partition of people into zero-sum groups that minimizes the total (group_size - 1) across all groups — equivalently, maximize the number of zero-sum groups (more groups = fewer transactions per group)."),
        N.h4("Building the Solution"),
        N.para("With n ≤ 12 people, we have 2^n ≤ 4096 subsets. We use Bitmask DP: dp[mask] = minimum transactions to settle the people indicated by mask. For each mask, we enumerate all zero-sum sub-masks s using the classic (s-1)&mask trick, and update dp[mask] = min(dp[mask ^ s] + popcount(s) - 1). The sub-mask enumeration visits O(3^n) total pairs."),
        N.callout("Analogy: Think of it like splitting a dinner bill. If 4 friends owe/are-owed [+4, -4, +5, -5], the best strategy is to pair them: friend 0 and friend 1 settle between themselves (1 payment), friend 2 and friend 3 settle between themselves (1 payment). Total: 2. Rather than one big chain of 4 people (3 payments).", "🧠", "blue_background"),
    ]),
    N.h3("🔬 Algorithm Deep-Dive: Bitmask DP + Sub-Mask Enumeration"),
    N.para(N.rich([
        ("Bitmask DP", {"bold": True}),
        " is a technique for problems where the state is which subset of n elements (n <= 20) have been 'used'. A bitmask is an integer whose i-th bit represents whether element i is in the set. There are 2^n possible subsets. The sub-mask enumeration trick ",
        ("for s=m; s>0; s=(s-1)&m", {"code": True}),
        " visits all 2^popcount(m) non-empty sub-masks of m in O(3^n) total across all m (each element is in: outer mask only, sub-mask, or neither -- 3 choices)."
    ])),
    N.code("# Sub-mask enumeration template\nm = some_mask\nsub = m\nwhile sub > 0:\n    # process sub as a subset of m\n    sub = (sub - 1) & m  # next sub-mask, or 0 when done\n\n# Total work across all masks: O(3^n)\n# Because sum_{m} 2^popcount(m) = 3^n (binomial expansion)", "python"),
    N.para("Why it works: (sub-1) flips the lowest set bit of sub to 0 and sets all lower bits to 1. ANDing with m strips any bits not in m. When sub becomes 0, the loop ends (0 is the empty sub-mask, not enumerated)."),
    N.h3("Code"),
    N.code(SOLUTION_1, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("bal = {}", {"code": True}), " — net balance dictionary. We build it from all transactions: u (payer) decrements, v (recipient) increments."])),
    N.para(N.rich([("debts = [v for v in bal.values() if v != 0]", {"code": True}), " — extract only non-zero balances. People with balance 0 are already settled and don't participate."])),
    N.para(N.rich([("dp = [INF] * (1 << n)", {"code": True}), " — 2^n states. dp[mask] = minimum transactions to settle exactly the people in mask. Initialize all to INF."])),
    N.para(N.rich([("dp[0] = 0", {"code": True}), " — base case: the empty group needs 0 transactions."])),
    N.para(N.rich([("for mask in range(1, 1 << n):", {"code": True}), " — iterate all non-empty subsets from smallest (0001) to largest (1111...1)."])),
    N.para(N.rich([("sub = mask", {"code": True}), " then ", ("while sub:", {"code": True}), " — enumerate all non-empty sub-masks of mask using the (sub-1)&mask trick."])),
    N.para(N.rich([("s_sum == 0", {"code": True}), " — this sub-group's balances sum to zero, meaning they can settle among themselves without outside help."])),
    N.para(N.rich([("k = bin(sub).count('1')", {"code": True}), " — count people in the zero-sum group. A group of k people needs k-1 transactions."])),
    N.para(N.rich([("dp[mask] = min(dp[mask], dp[mask ^ sub] + k - 1)", {"code": True}), " — mask ^ sub removes sub's bits from mask, giving the 'remaining' people. The total cost = cost to settle remaining + (k-1) for this group."])),
    N.para(N.rich([("sub = (sub - 1) & mask", {"code": True}), " — advance to next sub-mask. When sub=0 after this, all sub-masks have been visited."])),
    N.para(N.rich([("return dp[(1 << n) - 1]", {"code": True}), " — the all-ones mask means 'settle everyone'. This is our answer."])),
    N.divider(),
]

# ── Solution 2: DFS Backtracking ───────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — DFS Backtracking"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("After computing net balances, think of it as: pick any unsettled person (idx), try making them pay or be paid by every other person with opposite sign. After one transaction involving idx, recurse on the remaining balances."),
        N.h4("What Doesn't Work"),
        N.para("Trying all possible pairings naively is O(n!) — too slow for large n. But for n ≤ 12, with good pruning (only match opposite signs), it runs acceptably."),
        N.h4("The Key Observation"),
        N.para("Once person at idx has their balance set to zero (by transferring to person j), we move on to idx+1. We try all valid recipients j (opposite sign) and take the min. The key: debts[j] += debts[idx] accumulates the merged balance onto j, clearing idx. Backtrack by undoing this."),
        N.h4("Building the Solution"),
        N.para("Skip already-settled (zero balance) people. For the first non-zero person, try pairing with each opposite-sign person, recurse, backtrack. Return 1 + dfs(next person). Base case: all settled → return 0."),
        N.callout("Trade-off: DFS is simpler to derive in an interview (no bitmask machinery needed). Bitmask DP is cleaner to analyze and proves O(3^n) rigorously. In practice, both work for n ≤ 12.", "🧠", "yellow_background"),
    ]),
    N.h3("Code"),
    N.code(SOLUTION_2, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("while idx < len(debts) and debts[idx] == 0: idx += 1", {"code": True}), " — skip people whose balance was cleared in previous recursive calls."])),
    N.para(N.rich([("if idx == len(debts): return 0", {"code": True}), " — all people processed (settled). Zero more transactions needed."])),
    N.para(N.rich([("if debts[j] * debts[idx] < 0:", {"code": True}), " — one is positive, one is negative. Only opposite-sign pairs can mutually reduce balances."])),
    N.para(N.rich([("debts[j] += debts[idx]", {"code": True}), " — person idx clears their balance by transferring to j. Idx's balance is now conceptually zero; j absorbs the remainder."])),
    N.para(N.rich([("res = min(res, 1 + dfs(idx + 1))", {"code": True}), " — 1 transaction (idx → j) plus recursively settling everyone from idx+1 onward."])),
    N.para(N.rich([("debts[j] -= debts[idx]", {"code": True}), " — backtrack: undo the transfer, restoring debts[j] to its original value for the next iteration."])),
    N.divider(),
]

# ── Complexity Table ───────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Greedy (max-match)", "O(n log n)", "O(n)", "Fast but NOT optimal"],
        ["DFS Backtracking (Sol 2)", "O(n!)", "O(n)", "Correct; pruning helps; simpler to derive"],
        ["Bitmask DP (Sol 1) ✓", "O(3^n)", "O(2^n)", "Optimal & clean; n ≤ 12 → ~531K ops"],
    ]),
    N.divider(),
]

# ── Why is this DP? ────────────────────────────────────────────────────────────
blocks += [
    N.h2("Why is This Dynamic Programming?"),
    N.para(N.rich([("Optimal Substructure:", {"bold": True}), " The optimal settlement of the full group decomposes into settling independent zero-sum sub-groups. Once we choose a zero-sum subset s to settle among themselves, the remaining people (mask ^ s) can be settled independently — no shared transactions. Cost = cost(s) + cost(remainder). This is the classic DP decomposition."])),
    N.para(N.rich([("Overlapping Subproblems:", {"bold": True}), " The same subset (e.g., {P0, P1}) can appear as a 'remaining debt group' in many different decompositions of larger masks. The dp array memoizes each subset's optimal cost, avoiding recomputation."])),
    N.h3("The Recurrence"),
    N.code("# State: dp[mask] = min transactions to settle all people in mask\n# (mask is settleable only if sum(debts[i] for i in mask) == 0)\n\n# Base case:\ndp[0] = 0  # empty group: no transactions\n\n# Recurrence: for each mask, try every zero-sum sub-mask s\n# dp[mask] = min over all zero-sum s ⊆ mask:\n#             dp[mask ^ s] + popcount(s) - 1\n#\n# Why popcount(s) - 1?\n# A zero-sum group of k people always settles in k-1 transactions (chain).\n# This is a LOWER BOUND: you can't settle k people with k != 1 non-zero\n# balances in fewer than k-1 transactions (each transaction reduces\n# the count of non-zero balances by at most 1, but at least one per tx).", "python"),
    N.callout("State machine view: Each person starts in state UNSETTLED. After being included in a zero-sum sub-group that is settled, they move to SETTLED. The DP finds the optimal 'settlement order' (partition into groups) that minimizes total transactions.", "🔐", "blue_background"),
    N.divider(),
]

# ── Pattern Classification ─────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Dynamic Programming"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Bitmask DP on Debts (Guide Section 18 + 18.8)"])),
    N.callout("When to recognize this pattern: Small n (≤ 20) with 'which subset have we processed?' state; partition/assignment problems; any problem where dp[mask] encodes the state of n binary choices and transitions involve sub-masks.", "🔎", "green_background"),
    N.divider(),
]

# ── Related Problems ───────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Bitmask DP / Subset Partition DP):"),
    N.bullet(N.rich([("Partition to K Equal Sum Subsets", {"bold": True}), " (Medium) — dp[mask] = can we assign elements in mask to k equal-sum buckets? Same zero-sum group logic (#698)"])),
    N.bullet(N.rich([("Minimum Number of Work Sessions to Finish Tasks", {"bold": True}), " (Medium) — dp[mask] = min sessions; similar subset partitioning with capacity constraint (#1986)"])),
    N.bullet(N.rich([("Campus Bikes II", {"bold": True}), " (Medium) — dp[bike_mask] = min Manhattan distance; bitmask over bikes (#1066)"])),
    N.bullet(N.rich([("Shortest Path Visiting All Nodes", {"bold": True}), " (Hard) — BFS with (node, visited_mask) state; bitmask DP for graph coverage (#847)"])),
    N.bullet(N.rich([("Travelling Salesman Problem", {"bold": True}), " (Hard) — dp[mask][city] = min cost to visit all cities in mask ending at city; canonical bitmask DP"])),
    N.bullet(N.rich([("Maximum Score Words Formed by Letters", {"bold": True}), " (Hard) — enumerate subsets of words; bitmask over words (#1255)"])),
    N.bullet(N.rich([("Fair Distribution of Cookies", {"bold": True}), " (Medium) — backtracking or bitmask DP to distribute cookies into k groups (#2305)"])),
    N.para("These problems all share the same core technique: represent which elements have been 'assigned' as a bitmask and build up optimal solutions from smaller subsets."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 18 (Dynamic Programming → 18.8 Bitmask DP). Problem 'Optimal Account Balancing' listed in Section 18 general table with sub-pattern 'Bitmask DP on Debts'.", "📚", "gray_background"),
    N.divider(),
]

# ── Interactive Visual Explainer embed ────────────────────────────────────────
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("optimal_account_balancing")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

# ── Append all blocks ─────────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Page URL: https://www.notion.so/{PAGE_ID.replace('-', '')}")
