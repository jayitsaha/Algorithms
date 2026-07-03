"""
gen_best_time_to_buy_and_sell_stock_iv.py
Regenerates the Notion page for Best Time to Buy and Sell Stock IV (LC #188).
Uses notion_lib for all API calls.
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-8137-9f19-c91f24e3dcfd"
SLUG = "best_time_to_buy_and_sell_stock_iv"

print(f"[1/4] Setting properties on {PAGE_ID}...")
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=188,
    pattern="Dynamic Programming",
    subpatterns=["DP: State Machine", "K Transactions DP"],
    tc="O(kn)",
    sc="O(k)",
    key_insight="Track hold[j] and cash[j] for each of k transaction slots; iterate j high-to-low per day to avoid double-counting a transaction in one day.",
    icon="🔴"
)
print("   Properties set OK.")

print("[2/4] Wiping old page body...")
wiped = N.wipe_page(PAGE_ID)
print(f"   Wiped {wiped} blocks.")

print("[3/4] Building new page body...")
blocks = []

# ── Problem ──────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an integer ", {}),
        ("k", {"code": True}),
        (" and an integer array ", {}),
        ("prices", {"code": True}),
        (" where ", {}),
        ("prices[i]", {"code": True}),
        (" is the price of a stock on day ", {}),
        ("i", {"code": True}),
        (", find the maximum profit you can achieve. You may complete at most ", {}),
        ("k", {"code": True}),
        (" transactions. Note: you may not engage in multiple transactions simultaneously (you must sell before you buy again).", {})
    ])),
    N.divider(),
]

# ── Solution 1: Optimal 1D State Machine DP ──────────────────
blocks += [
    N.h2("Solution 1 — K-State Machine DP, Rolling Arrays (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We have a budget of k transactions and a sequence of prices. On any given day, for any transaction slot j, we are in one of two states: HOLD (stock in hand, waiting to sell) or CASH (no stock, can buy or wait). We want the maximum total profit across all completed transactions."),
        N.h4("What Doesn't Work"),
        N.para("Greedy fails because k is a hard budget — grabbing every upward move would overspend. Brute force trying all buy/sell combos is O(2^n). A naive 2D DP table of size k×n works but costs O(kn) space — avoidable with rolling arrays."),
        N.h4("The Key Observation"),
        N.para("At any day, for each transaction slot j, we only need two numbers: the best profit achievable if we are HOLDING (hold[j]) and the best profit if we are in CASH (cash[j]). Everything else about past history is encoded in these numbers. This is the State Machine insight: history collapses to current state."),
        N.h4("Building the Solution"),
        N.para("For each new price, we update hold[j] = max(hold[j], cash[j-1] - price): either we kept holding, or we bought today using profit from j-1 prior transactions. Then cash[j] = max(cash[j], hold[j] + price): either we stayed in cash, or we sold today completing the j-th transaction. Critical: iterate j from k down to 1 so cash[j-1] is always yesterday's value — preventing a double-use of a transaction in one day."),
        N.callout(
            N.rich([("Analogy: ", {"bold": True}), ("Think of k 'coupon books', each with one buy-sell pair. On each day, for each remaining coupon j, you decide: 'Should I use this coupon to buy (if I haven't yet) or sell (if I am holding)?' You always check higher coupons first so they don't steal from lower-coupon profits computed the same day.", {})]),
            "🧠", "blue_background"
        ),
    ]),
]

blocks += [
    N.h3("🔬 DP Deep-Dive: Why is This Dynamic Programming?"),
    N.para(N.rich([
        ("Optimal Substructure: ", {"bold": True}),
        ("Today's best HOLD[j] is max('keep yesterday's hold' vs 'buy today from yesterday's CASH[j-1]'). Yesterday's optimal values are all we need — no earlier history matters. ", {}),
        ("Overlapping Subproblems: ", {"bold": True}),
        ("A naive recursive solution would recompute 'best profit with j transactions up to day i' exponentially many times. Memoization (or tabulation) computes each (j, day) pair exactly once.", {})
    ])),
    N.code(
        "# Recurrence relations — the heart of the algorithm\n"
        "# hold[j] = best profit if HOLDING after using j buy operations\n"
        "# cash[j] = best profit if NOT HOLDING after completing j sell operations\n"
        "#\n"
        "# On each new price:\n"
        "hold[j] = max(hold[j],       cash[j-1] - price)  # keep holding OR buy today\n"
        "cash[j] = max(cash[j],       hold[j]   + price)  # stay cash    OR sell today\n"
        "#\n"
        "# Key: j goes from k DOWN to 1 each day\n"
        "# This ensures cash[j-1] is yesterday's value when computing hold[j]\n"
        "# — prevents buying AND selling the same transaction on the same day",
        "python"
    ),
    N.h3("Code"),
    N.code(
        "def maxProfit(k: int, prices: list[int]) -> int:\n"
        "    n = len(prices)\n"
        "    if n == 0 or k == 0:\n"
        "        return 0\n"
        "\n"
        "    # Special case: unlimited transactions (greedy)\n"
        "    if k >= n // 2:\n"
        "        return sum(max(prices[i] - prices[i-1], 0) for i in range(1, n))\n"
        "\n"
        "    # DP arrays of size k+1\n"
        "    hold = [-float('inf')] * (k + 1)  # hold[j]: best profit holding, j buys started\n"
        "    cash = [0] * (k + 1)              # cash[j]: best profit not holding, j txns done\n"
        "\n"
        "    for price in prices:\n"
        "        for j in range(k, 0, -1):      # high-to-low: preserve yesterday's cash[j-1]\n"
        "            hold[j] = max(hold[j], cash[j-1] - price)  # keep or buy\n"
        "            cash[j] = max(cash[j], hold[j] + price)    # stay or sell\n"
        "\n"
        "    return cash[k]  # at most k completed transactions",
        "python"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("n = len(prices)", {"code": True}), (" — number of trading days.", {})])),
    N.para(N.rich([("if n == 0 or k == 0: return 0", {"code": True}), (" — edge case guard: no prices means no profit, no transactions allowed means no profit.", {})])),
    N.para(N.rich([("if k >= n // 2:", {"code": True}), (" — with n prices, at most n//2 non-overlapping transactions are possible. When k exceeds this, we effectively have unlimited transactions, so we use O(n) greedy instead of O(kn) DP.", {})])),
    N.para(N.rich([("hold = [-inf] * (k+1)", {"code": True}), (" — initialize all hold states to −∞ (impossible to be holding before any price seen). Index 0 is unused but keeps indexing clean.", {})])),
    N.para(N.rich([("cash = [0] * (k+1)", {"code": True}), (" — initialize all cash states to 0. ", {}), ("cash[0] = 0", {"code": True}), (" is the permanent baseline: buying into the first transaction comes 'from' 0 completed transactions.", {})])),
    N.para(N.rich([("for price in prices:", {"code": True}), (" — scan prices left to right; each iteration updates our DP states for that day's price.", {})])),
    N.para(N.rich([("for j in range(k, 0, -1):", {"code": True}), (" — the critical inner loop direction. High-to-low ensures ", {}), ("cash[j-1]", {"code": True}), (" is still yesterday's value when used to compute ", {}), ("hold[j]", {"code": True}), (".", {})])),
    N.para(N.rich([("hold[j] = max(hold[j], cash[j-1] - price)", {"code": True}), (" — either keep the stock I'm already holding (profit stays same), or buy today at this price using the best profit from j-1 completed transactions.", {})])),
    N.para(N.rich([("cash[j] = max(cash[j], hold[j] + price)", {"code": True}), (" — either stay in cash (no action), or sell today (add today's price to my hold profit, completing the j-th transaction).", {})])),
    N.para(N.rich([("return cash[k]", {"code": True}), (" — maximum profit achievable with at most k completed buy-sell transactions.", {})])),
    N.divider(),
]

# ── Solution 2: 2D DP for clarity ──────────────────────────
blocks += [
    N.h2("Solution 2 — 2D DP Table (Conceptually Clearer)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Before optimizing to 1D arrays, think in terms of a 2D table: dp[j][0] = best profit after at most j transactions, currently NOT holding; dp[j][1] = best profit after at most j transactions, currently HOLDING. Fill row by row (j=1..k) for each day."),
        N.h4("What Doesn't Work"),
        N.para("This approach is correct but uses O(kn) space for the full table. For large k and n, this can cause memory issues. The 1D rolling array solution is preferred in interviews."),
        N.h4("The Key Observation"),
        N.para("The 2D table makes the recurrence visually obvious and is easier to explain from scratch. Once you have it, the 1D optimization is a straightforward 'rolling array' observation."),
        N.h4("Building the Solution"),
        N.para("Initialize dp[0][*] = 0 (0 transactions = 0 profit). For each j and each day, apply the same recurrences. The 2D layout shows clearly how each cell depends only on the same row's previous day and row j-1's previous day."),
    ]),
    N.h3("Code"),
    N.code(
        "def maxProfit_2d(k: int, prices: list[int]) -> int:\n"
        "    n = len(prices)\n"
        "    if n == 0 or k == 0:\n"
        "        return 0\n"
        "    if k >= n // 2:\n"
        "        return sum(max(prices[i]-prices[i-1], 0) for i in range(1, n))\n"
        "\n"
        "    # dp[j][0] = best profit, j txns completed, not holding\n"
        "    # dp[j][1] = best profit, j-th txn started (holding)\n"
        "    dp = [[0, -float('inf')] for _ in range(k + 1)]\n"
        "\n"
        "    for price in prices:\n"
        "        for j in range(k, 0, -1):\n"
        "            dp[j][1] = max(dp[j][1], dp[j-1][0] - price)  # buy\n"
        "            dp[j][0] = max(dp[j][0], dp[j][1] + price)    # sell\n"
        "\n"
        "    return dp[k][0]",
        "python"
    ),
    N.divider(),
]

# ── Solution 3: Top-Down Memoization ──────────────────────
blocks += [
    N.h2("Solution 3 — Top-Down DP (Memoization)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("A recursive formulation: dp(day, transactions_left, holding) = max profit from 'day' onwards, with 'transactions_left' remaining, and 'holding' indicating if we hold a stock. This naturally expresses the problem but leads to exponential recomputation without memoization."),
        N.h4("What Doesn't Work"),
        N.para("Pure recursion without memoization is O(2^n * k). With memoization the state space is O(n * k * 2) = O(nk) — same as tabulation but with function call overhead."),
        N.h4("The Key Observation"),
        N.para("Top-down is easier to write from the recurrence and is useful when not all states are visited (sparse k). Bottom-up (tabulation) is generally preferred in practice for its cache efficiency."),
        N.h4("Building the Solution"),
        N.para("Base cases: day=n → 0 profit, transactions_left=0 → 0 profit. Recursive cases: if holding, we can sell (add price, reduce transactions_left) or hold (recurse to next day). If not holding, we can buy (subtract price) or wait."),
    ]),
    N.h3("Code"),
    N.code(
        "from functools import lru_cache\n"
        "\n"
        "def maxProfit_memo(k: int, prices: list[int]) -> int:\n"
        "    n = len(prices)\n"
        "    if k >= n // 2:\n"
        "        return sum(max(prices[i]-prices[i-1], 0) for i in range(1, n))\n"
        "\n"
        "    @lru_cache(maxsize=None)\n"
        "    def dp(day, txns_left, holding):\n"
        "        if day == n or txns_left == 0:\n"
        "            return 0  # No more days or budget\n"
        "        # Option 1: do nothing today\n"
        "        result = dp(day + 1, txns_left, holding)\n"
        "        if holding:\n"
        "            # Option 2: sell today (uses one transaction)\n"
        "            result = max(result, prices[day] + dp(day+1, txns_left-1, False))\n"
        "        else:\n"
        "            # Option 2: buy today (no transaction count change yet)\n"
        "            result = max(result, -prices[day] + dp(day+1, txns_left, True))\n"
        "        return result\n"
        "\n"
        "    return dp(0, k, False)",
        "python"
    ),
    N.divider(),
]

# ── Complexity ────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["1D State Machine DP (Interview Pick)", "O(kn)", "O(k)"],
        ["2D DP Table", "O(kn)", "O(kn)"],
        ["Top-Down Memoization", "O(kn)", "O(kn) + call stack"],
    ]),
    N.divider(),
]

# ── Pattern Classification ────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Dynamic Programming", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("DP: State Machine, K Transactions DP", {})])),
    N.callout(
        N.rich([
            ("When to recognize this pattern: ", {"bold": True}),
            ('"at most k transactions", "buy and sell", "maximize profit over days" — whenever you see a fixed budget of buy-sell operations over a time sequence, think State Machine DP with k slots. Signals also include: the problem has a simpler k=1 or k=unlimited variant, or the constraint k causes you to need to track how many you have remaining.', {})
        ]),
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ─────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same State Machine DP technique:"),
    N.bullet(N.rich([("Best Time to Buy and Sell Stock III", {"bold": True}), (" (Hard) — k=2 fixed; use four named variables hold1, cash1, hold2, cash2", {})])),
    N.bullet(N.rich([("Best Time to Buy and Sell Stock II", {"bold": True}), (" (Medium) — k unlimited; the greedy escape hatch used in this solution", {})])),
    N.bullet(N.rich([("Best Time to Buy and Sell Stock I", {"bold": True}), (" (Easy) — k=1; one-pass: track min price seen so far", {})])),
    N.bullet(N.rich([("Best Time to Buy and Sell Stock with Cooldown", {"bold": True}), (" (Medium) — unlimited k but add a 'resting' 3rd state after sell", {})])),
    N.bullet(N.rich([("Best Time to Buy and Sell Stock with Transaction Fee", {"bold": True}), (" (Medium) — unlimited k but subtract fee at sell: cash = hold + price − fee", {})])),
    N.bullet(N.rich([("Paint House II", {"bold": True}), (" (Hard) — k-state DP across n days, same structural idea with k color choices", {})])),
    N.bullet(N.rich([("Maximum Profit in Job Scheduling", {"bold": True}), (" (Hard) — DP with k non-overlapping intervals, related budget structure", {})])),
    N.para("These problems all share the core technique: track states per 'budget unit' and use recurrences to find the globally optimal sequence of decisions."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 18 — Dynamic Programming → DP: State Machine", "📚", "gray_background"),
]

# ── Interactive Visual Explainer ─────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

print(f"   Built {len(blocks)} blocks total. Appending to Notion...")
N.append_blocks(PAGE_ID, blocks)
print("   Blocks appended OK.")

print("[4/4] Verifying block count...")
count = len(N.get_children(PAGE_ID))
print(f"   Page now has {count} blocks.")
print(f"\nNOTION OK {PAGE_ID}")
