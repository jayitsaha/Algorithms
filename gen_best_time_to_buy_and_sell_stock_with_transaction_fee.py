"""
gen_best_time_to_buy_and_sell_stock_with_transaction_fee.py
Notion page builder for LeetCode 714 — Best Time to Buy and Sell Stock with Transaction Fee
DP sub-pattern: State Machine (States: hold and cash)
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

SLUG = "best_time_to_buy_and_sell_stock_with_transaction_fee"
NAME = "Best Time to Buy and Sell Stock with Transaction Fee"
NUMBER = 714
DIFFICULTY = "Medium"
ICON = "🟡"
PATTERN = "Dynamic Programming"
SUBPATTERNS = ["States hold and cash"]

# ── Step 1: create page (notion_page_id is null in the record) ──────────────
PAGE_ID = N.create_page(NAME, NUMBER, DIFFICULTY, ICON)
print(f"Created page: {PAGE_ID}")

# ── Step 2: set properties ───────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty=DIFFICULTY,
    number=NUMBER,
    pattern=PATTERN,
    subpatterns=SUBPATTERNS,
    tc="O(n)",
    sc="O(1)",
    key_insight="Track two states per day — holding stock (hold) or in cash — and pick max of keep/transition at each price.",
    icon=ICON,
)
print("Properties set.")

# ── Step 3: build body blocks ─────────────────────────────────────────────────
blocks = []

# ── PROBLEM ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given an array ", {}),
        ("prices", {"code": True}),
        (" where ", {}),
        ("prices[i]", {"code": True}),
        (" is the price of a given stock on the ", {}),
        ("i", {"code": True}),
        ("-th day, and an integer ", {}),
        ("fee", {"code": True}),
        (" representing a transaction fee.\n\n"
         "Find the maximum profit you can achieve. You may complete as many transactions as you "
         "like, but you need to pay the transaction fee for each transaction. You may not hold more "
         "than one share of the stock at a time (i.e., you must sell the stock before you buy again).\n\n"
         "Note: The transaction fee is only charged once per buy-sell pair.", {}),
    ])),
    N.divider(),
]

# ── SOLUTION 1 — Greedy (Peak-Valley with fee) ────────────────────────────────
blocks += [
    N.h2("Solution 1 — Greedy / Valley-Peak Scan"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("With unlimited transactions but a per-trade fee, we want to collect every profitable "
               "price rise that overcomes the fee — but do so efficiently without double-counting. "
               "Think of it as: should I extend the current holding streak, or start fresh?"),
        N.h4("What Doesn't Work"),
        N.para("Brute-force recursion tries every buy/sell pair — O(n²) or worse. Greedy "
               '"buy every dip, sell every peak" over-counts fee because you may buy and sell '
               "multiple times over a single profitable run."),
        N.h4("The Key Observation"),
        N.para("If prices[i] - prices[i-1] > fee, it's worth collecting that profit now. "
               "We can model each day's price change as a potential micro-transaction and greedily "
               "accumulate gains exceeding the fee, adjusting the basis when we would 'extend' a run."),
        N.h4("Building the Solution"),
        N.para("Track a buy price (basis). For each day:\n"
               "• If today's price > basis + fee → sell (collect profit), reset basis to today's price (minus fee we already collected)\n"
               "• If today's price < basis → update basis (buy cheaper)\n"
               "• Otherwise → hold\n\n"
               "This is essentially the same math as the DP approach but expressed greedily."),
        N.callout(
            "Analogy: Think of owning a fruit stand. You buy when price is low, sell when the "
            "margin covers your booth rent (fee). If the price keeps rising, you hold rather than "
            "paying booth rent twice on the same wave.",
            "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(
        "def maxProfit(prices: list[int], fee: int) -> int:\n"
        "    profit = 0\n"
        "    basis = prices[0]          # Treat first day as 'bought'\n"
        "\n"
        "    for price in prices[1:]:\n"
        "        if price > basis + fee:\n"
        "            # Profitable to sell; collect, but leave door open to extend run\n"
        "            profit += price - basis - fee\n"
        "            basis = price - fee  # New basis: if price keeps rising we re-collect cleanly\n"
        "        elif price < basis:\n"
        "            basis = price        # Found cheaper entry point; update basis\n"
        "        # else: hold — no profitable action this day\n"
        "\n"
        "    return profit\n"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("profit = 0", {"code": True}), " — Running total of profit collected so far."])),
    N.para(N.rich([("basis = prices[0]", {"code": True}), " — We conceptually 'buy' on day 0; basis tracks our current cost basis."])),
    N.para(N.rich([("if price > basis + fee:", {"code": True}), " — This sale would be profitable (covering the fee)."])),
    N.para(N.rich([("profit += price - basis - fee", {"code": True}), " — Collect the net gain."])),
    N.para(N.rich([("basis = price - fee", {"code": True}),
                   " — Trick: lower the basis by fee so that if price keeps rising tomorrow, "
                   "we can 'extend' the sale without double-counting the fee."])),
    N.para(N.rich([("elif price < basis:", {"code": True}), " — Found a cheaper buy point; update basis."])),
    N.para(N.rich([("return profit", {"code": True}), " — Total profit after all profitable sell decisions."])),
    N.divider(),
]

# ── SOLUTION 2 — DP State Machine (Interview Pick) ───────────────────────────
SOLUTION2_CODE = """\
def maxProfit(prices: list[int], fee: int) -> int:
    hold = -prices[0]  # State: holding stock after day 0 (cost = prices[0])
    cash = 0           # State: not holding stock after day 0

    for price in prices[1:]:
        # Update HOLD: either keep holding, or buy today from cash state
        hold = max(hold, cash - price)
        # Update CASH: either stay cash, or sell today (subtract fee once)
        cash = max(cash, hold + price - fee)

    return cash  # Maximum profit, ending without stock in hand
"""

blocks += [
    N.h2("Solution 2 — DP State Machine (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("At every day, you are in exactly one of two states:\n"
               "  • HOLD — you own one share\n"
               "  • CASH — you hold no share\n\n"
               "The answer is the maximum cash you can accumulate, ending in the CASH state."),
        N.h4("What Doesn't Work"),
        N.para("Simple greedy 'collect every up-day profit' fails because the fee makes small "
               "fluctuations unprofitable — you need to decide whether a price rise is worth "
               "triggering a transaction. The fee changes the break-even point dynamically."),
        N.h4("The Key Observation"),
        N.para("Optimal substructure: the best result for day i in state HOLD depends only on "
               "the best result for day i-1 in HOLD or CASH (not on how we got there). "
               "This is the hallmark of DP — we don't need to remember the full history."),
        N.h4("Building the Solution"),
        N.para("Define:\n"
               "  hold[i] = max profit ending day i while holding stock\n"
               "  cash[i] = max profit ending day i NOT holding stock\n\n"
               "Recurrences:\n"
               "  hold[i] = max(hold[i-1], cash[i-1] - prices[i])   ← keep holding OR buy today\n"
               "  cash[i] = max(cash[i-1], hold[i-1] + prices[i] - fee)  ← stay OR sell today\n\n"
               "Base cases: hold[0] = -prices[0], cash[0] = 0\n"
               "Answer: cash[n-1]  (always best to end without stock)\n\n"
               "Space optimisation: we only need the previous day's values, so we use two scalars."),
        N.callout(
            "Mnemonic: HOLD = 'I spent money to own a share.' CASH = 'I converted shares to money.' "
            "Fee is only charged on the CASH transition (one fee per complete trade).",
            "🧠", "blue_background"),
    ]),
    N.h3("🔬 Why is This Dynamic Programming?"),
    N.para(N.rich([
        ("Optimal Substructure: ", {"bold": True}),
        ("The best profit for day i in state HOLD only depends on the best profits for day i-1 "
         "(in either state). There's no need to track which specific days we bought/sold.", {}),
    ])),
    N.para(N.rich([
        ("Overlapping Subproblems: ", {"bold": True}),
        ("A naive recursion from the end would recompute dp(day, state) for the same (day, state) "
         "pairs repeatedly. DP avoids this by caching — or, equivalently, filling the table bottom-up.", {}),
    ])),
    N.code(
        "# Recurrence relations (the core of the DP)\n"
        "hold[i] = max(\n"
        "    hold[i-1],          # Keep holding (no transaction)\n"
        "    cash[i-1] - price   # Buy today (transition CASH → HOLD)\n"
        ")\n"
        "cash[i] = max(\n"
        "    cash[i-1],               # Stay in cash (no transaction)\n"
        "    hold[i-1] + price - fee  # Sell today (transition HOLD → CASH, pay fee)\n"
        ")",
        lang="python",
    ),
    N.h3("Code"),
    N.code(SOLUTION2_CODE),
    N.callout(
        "⚠️ Why return cash, not hold?\n"
        "Ending while holding stock means the stock value is not realized. We must sell to pocket "
        "profit, so the final answer is always cash[n-1]. hold[n-1] would represent unrealized value.",
        "⚠️", "yellow_background",
    ),
    N.callout(
        "🎯 Extension Patterns — this state machine adapts:\n"
        "• With cooldown (LC 309): add a third state COOLDOWN\n"
        "• At most K transactions (LC 188): add a k dimension — hold[i][k], cash[i][k]\n"
        "• At most 2 transactions (LC 123): K=2 version of the above\n"
        "• No fee (LC 122): remove '- fee' from the cash recurrence",
        "🎯", "green_background",
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("hold = -prices[0]", {"code": True}),
                   " — Base case day 0 HOLD: we spent prices[0] to buy, so profit = -prices[0]."])),
    N.para(N.rich([("cash = 0", {"code": True}),
                   " — Base case day 0 CASH: we did nothing on day 0, profit = 0."])),
    N.para(N.rich([("for price in prices[1:]:", {"code": True}),
                   " — Process days 1 through n-1."])),
    N.para(N.rich([("hold = max(hold, cash - price)", {"code": True}),
                   " — New HOLD = best of (keep holding yesterday's stock) OR (buy today from cash state)."])),
    N.para(N.rich([("cash = max(cash, hold + price - fee)", {"code": True}),
                   " — New CASH = best of (stay in cash) OR (sell today's stock, pay fee once). "
                   "Note: hold here is the already-updated value, which is fine because if we just "
                   "bought today (hold = cash - price), then hold + price - fee = cash - fee < cash, "
                   "so we'd never immediately sell what we just bought."])),
    N.para(N.rich([("return cash", {"code": True}),
                   " — Best profit achievable, ending without any stock."])),
    N.divider(),
]

# ── SOLUTION 3 — DP Memoization (Top-Down) ────────────────────────────────────
SOLUTION3_CODE = """\
from functools import lru_cache

def maxProfit(prices: list[int], fee: int) -> int:
    n = len(prices)

    @lru_cache(maxsize=None)
    def dp(day: int, holding: int) -> int:
        # Base case: no more days
        if day == n:
            return 0

        # Option 1: do nothing today
        best = dp(day + 1, holding)

        if holding:
            # Option 2: sell today (pay fee)
            best = max(best, prices[day] - fee + dp(day + 1, 0))
        else:
            # Option 2: buy today
            best = max(best, -prices[day] + dp(day + 1, 1))

        return best

    return dp(0, 0)  # Start on day 0, not holding
"""

blocks += [
    N.h2("Solution 3 — DP Memoization (Top-Down)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Think recursively: at each day, in each state (holding or not), what's the best "
               "total profit from now until the end? Cache the answer so we never recompute."),
        N.h4("The Key Observation"),
        N.para("The state space is just n × 2 — at most 2n unique (day, holding) pairs. "
               "With memoization, each is computed once → O(n) time."),
        N.h4("Building the Solution"),
        N.para("dp(day, holding) = maximum profit from day through end, given current holding state.\n\n"
               "At each call: try 'do nothing', and try the applicable transaction (buy or sell).\n"
               "The lru_cache handles deduplication automatically."),
        N.callout("This is easier to derive from the recurrence but uses O(n) stack space vs O(1) "
                  "for the bottom-up approach. In interviews, bottom-up is preferred for O(1) space.",
                  "💡", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(SOLUTION3_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("@lru_cache(maxsize=None)", {"code": True}),
                   " — Python's built-in memoization decorator; caches results by arguments."])),
    N.para(N.rich([("def dp(day: int, holding: int) -> int:", {"code": True}),
                   " — Recursive function: day=current index, holding=1 if we own stock, 0 if not."])),
    N.para(N.rich([("if day == n: return 0", {"code": True}),
                   " — Base case: past last day, no more profit possible."])),
    N.para(N.rich([("best = dp(day + 1, holding)", {"code": True}),
                   " — Always have the option to do nothing today."])),
    N.para(N.rich([("prices[day] - fee + dp(day + 1, 0)", {"code": True}),
                   " — Sell today: collect price, pay fee, then recurse in CASH state."])),
    N.para(N.rich([("-prices[day] + dp(day + 1, 1)", {"code": True}),
                   " — Buy today: spend price, then recurse in HOLD state."])),
    N.para(N.rich([("return dp(0, 0)", {"code": True}),
                   " — Start from day 0 not holding any stock."])),
    N.divider(),
]

# ── COMPLEXITY TABLE ──────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Greedy (Solution 1)", "O(n)", "O(1)"],
        ["DP State Machine — Tabulation (Solution 2)", "O(n)", "O(1)"],
        ["DP Memoization — Top-Down (Solution 3)", "O(n)", "O(n) stack"],
    ]),
    N.divider(),
]

# ── PATTERN CLASSIFICATION ────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Dynamic Programming", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("States hold and cash (DP State Machine)", {})])),
    N.callout(
        "When to recognize this pattern:\n"
        "• Problem asks for max profit over an array of prices with constraints on transactions\n"
        "• You can naturally enumerate a small finite set of states (holding/not holding)\n"
        "• Greedy 'local' decisions are complicated by a transaction cost or cooldown\n"
        "• The phrase 'at most K transactions' or 'with fee' signals state-machine DP\n"
        "• State transitions are: BUY (CASH→HOLD), SELL (HOLD→CASH), or HOLD/SKIP",
        "🔎", "green_background",
    ),
    N.divider(),
]

# ── RELATED PROBLEMS ─────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same State Machine DP technique:"),
    N.bullet(N.rich([("Best Time to Buy and Sell Stock II", {"bold": True}),
                     (" (Medium, LC 122) — Same state machine, no fee: cash[i] = max(cash[i-1], hold[i-1] + price)", {})])),
    N.bullet(N.rich([("Best Time to Buy and Sell Stock with Cooldown", {"bold": True}),
                     (" (Medium, LC 309) — Three states: HOLD, CASH, COOLDOWN. Same DP transitions.", {})])),
    N.bullet(N.rich([("Best Time to Buy and Sell Stock III", {"bold": True}),
                     (" (Hard, LC 123) — State machine with at most 2 transactions; track transaction count.", {})])),
    N.bullet(N.rich([("Best Time to Buy and Sell Stock IV", {"bold": True}),
                     (" (Hard, LC 188) — Generalized: at most K transactions. Same pattern, k dimension added.", {})])),
    N.bullet(N.rich([("Best Time to Buy and Sell Stock I", {"bold": True}),
                     (" (Easy, LC 121) — Simplified: exactly one transaction. No DP needed; just track min so far.", {})])),
    N.bullet(N.rich([("House Robber", {"bold": True}),
                     (" (Medium, LC 198) — Similar two-state machine: rob or skip each house.", {})])),
    N.bullet(N.rich([("Paint House", {"bold": True}),
                     (" (Medium) — State machine DP where state = last color used.", {})])),
    N.para("These problems share the same core technique: enumerate states, write recurrences for each state transition, reduce to O(1) space by keeping only the previous day's values."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 18 (Dynamic Programming), Sub-Pattern: DP State Machine",
              "📚", "gray_background"),
]

# ── EMBED ─────────────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"}),
    ])),
]

# ── Append all blocks ──────────────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks to page {PAGE_ID} ...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
