"""
gen_best_time_to_buy_and_sell_stock_with_cooldown.py
Notion page for LeetCode 309 — Best Time to Buy and Sell Stock with Cooldown
DP sub-pattern: State Machine DP (States: hold / sold / rest)
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notion_lib as N

# ── Step 1: Create page (notion_page_id was null) ──────────────────────────
PAGE_ID = N.create_page(
    "Best Time to Buy and Sell Stock with Cooldown", 309, "Medium", "🟡"
)
print("Created page:", PAGE_ID)

# ── Step 2: Set properties ─────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=309,
    pattern="Dynamic Programming",
    subpatterns=["States hold sold rest"],
    tc="O(n)",
    sc="O(1)",
    key_insight="Model buy/sell with three mutually exclusive states — hold, sold, rest — and transition between them daily.",
    icon="🟡",
)
print("Properties set.")

# ── Step 3: Build body blocks ──────────────────────────────────────────────
blocks = []

# Problem section
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given an array ", {}),
        ("prices", {"code": True}),
        (" where ", {}),
        ("prices[i]", {"code": True}),
        (" is the price of a given stock on the ", {}),
        ("i", {"code": True}),
        ("-th day. Find the maximum profit you can achieve. You may complete as many transactions as you like with one constraint: ", {}),
        ("after you sell your stock you must wait one day before buying again (cooldown)", {"bold": True}),
        (". You may not engage in multiple transactions simultaneously (you must sell before you buy).", {}),
    ])),
    N.divider(),
]

# ── Solution 1 — State Machine DP (Interview Pick) ─────────────────────────
sol1_code = '''\
def maxProfit(prices: list[int]) -> int:
    # Three states on any given day:
    #   hold : we currently own a stock
    #   sold : we just sold today (must rest tomorrow)
    #   rest : we have no stock and are free to buy
    hold = -prices[0]   # bought on day 0
    sold = 0            # impossible on day 0, but 0 is safe floor
    rest = 0            # did nothing on day 0

    for price in prices[1:]:
        prev_hold = hold
        prev_sold = sold
        prev_rest = rest

        # To hold tomorrow: keep holding OR buy from rest
        hold = max(prev_hold, prev_rest - price)
        # To sold tomorrow: sell from hold
        sold = prev_hold + price
        # To rest tomorrow: stay resting OR cool down after sold
        rest = max(prev_rest, prev_sold)

    return max(sold, rest)   # never return hold (stock unsold = lost value)
'''

blocks += [
    N.h2("Solution 1 — State Machine DP (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "On every calendar day you are in exactly one of three situations: "
            "(1) you OWN a stock, (2) you JUST SOLD one (today was a sell day, so tomorrow is forced cooldown), "
            "or (3) you are FREE — no stock and not cooling down. "
            "Those three situations are your states. Your job is to find the best total profit "
            "by making the optimal transition each day."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "A greedy 'buy every valley, sell every peak' approach breaks down because selling creates a "
            "mandatory cooldown — you might sell at a local peak but then miss a much bigger gain the next day. "
            "Brute force (enumerate all buy/sell pairs) is O(2^n). "
            "Even the classic unlimited-transactions trick (sum all positive day-over-day differences) "
            "does not handle the cooldown constraint."
        ),
        N.h4("The Key Observation"),
        N.para(
            "There are only THREE mutually exclusive states you can be in each day. "
            "The maximum profit achievable in each state on day i depends ONLY on the three state values "
            "from day i-1. No earlier history is needed — optimal substructure + no full recursion tree needed."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Define: hold[i] = best profit ending day i while HOLDING a stock; "
            "sold[i] = best profit ending day i having JUST SOLD; "
            "rest[i] = best profit ending day i while resting (free, no stock). "
            "Transitions: "
            "hold[i] = max(hold[i-1],  rest[i-1] - price)  — keep holding OR buy from rest; "
            "sold[i] = hold[i-1] + price  — sell the stock we held; "
            "rest[i] = max(rest[i-1], sold[i-1])  — stay free OR come off cooldown. "
            "Since each new day depends only on the previous day, we can use three scalar variables."
        ),
        N.callout(
            "Analogy: Think of a traffic light. GREEN (rest) = free to buy. "
            "YELLOW (hold) = actively invested. RED (sold) = mandatory cooldown. "
            "At each tick you may advance through transitions or stay put — but you cannot skip the red.",
            "🚦", "blue_background"
        ),
    ]),
    N.h3("🔬 Algorithm Deep-Dive: State Machine DP"),
    N.para(
        "State Machine DP encodes the problem as a directed graph where nodes are states "
        "(hold / sold / rest) and edges are valid transitions (buy / sell / wait). "
        "Each edge carries a cost or reward (e.g., –price for buying, +price for selling). "
        "The DP fills in the maximum cumulative reward reachable at each (day, state) pair. "
        "Pattern recognition signal: 'you may not perform action X immediately after action Y' — "
        "cooldown, transaction-fee, or at-most-k-transactions variants all fall here."
    ),
    N.code(
        "# General template for 2-state stock DP\n"
        "hold = -prices[0]   # cost of entering hold on day 0\n"
        "free = 0            # profit while not holding\n"
        "for price in prices[1:]:\n"
        "    hold, free = max(hold, free - price), max(free, hold + price)\n"
        "return free\n\n"
        "# With cooldown: split 'free' into sold (just sold) and rest (fully free)\n"
        "hold, sold, rest = -prices[0], 0, 0\n"
        "for price in prices[1:]:\n"
        "    hold, sold, rest = (\n"
        "        max(hold, rest - price),   # keep holding or buy from rest\n"
        "        hold + price,               # sell today\n"
        "        max(rest, sold),            # stay free or come off cooldown\n"
        "    )\n"
        "return max(sold, rest)",
        lang="python"
    ),
    N.h3("Code"),
    N.code(sol1_code, lang="python"),
    N.h3("Line by Line"),
    N.para(N.rich([("hold = -prices[0]", {"code": True}),
                   (" — On day 0 our only option is to buy (or do nothing). If we buy, profit starts at −price[0]. Initialize hold to this worst-case purchased state.", {})])),
    N.para(N.rich([("sold = 0", {"code": True}),
                   (" — We cannot have sold on day 0 (nothing to sell yet). 0 is a safe floor that won't pollute later maxes.", {})])),
    N.para(N.rich([("rest = 0", {"code": True}),
                   (" — If we do nothing on day 0 our profit is 0.", {})])),
    N.para(N.rich([("prev_hold, prev_sold, prev_rest = hold, sold, rest", {"code": True}),
                   (" — Snapshot yesterday's values before we overwrite. Essential: transitions reference the PREVIOUS day, not today mid-update.", {})])),
    N.para(N.rich([("hold = max(prev_hold, prev_rest - price)", {"code": True}),
                   (" — To end today HOLDING: either we were already holding (do nothing), or we were resting (free to buy) and bought at today's price.", {})])),
    N.para(N.rich([("sold = prev_hold + price", {"code": True}),
                   (" — To end today SOLD: the only path is to have been holding yesterday and sell today. There is no max — this is the unique incoming transition.", {})])),
    N.para(N.rich([("rest = max(prev_rest, prev_sold)", {"code": True}),
                   (" — To end today RESTING: either we were already resting (stayed put) or we sold yesterday and served our cooldown.", {})])),
    N.para(N.rich([("return max(sold, rest)", {"code": True}),
                   (" — The answer is the best profit with no stock in hand. Never return hold — an unsold stock is unrealised; the cash hasn't changed hands.", {})])),
    N.divider(),
]

# ── Solution 2 — Greedy (unlimited without cooldown — contrast) ────────────
sol2_code = '''\
# Brute-force recursive with memoization — illustrates overlapping subproblems
from functools import lru_cache

def maxProfit_memo(prices: list[int]) -> int:
    n = len(prices)

    @lru_cache(maxsize=None)
    def dp(day: int, holding: bool, cooldown: bool) -> int:
        if day >= n:
            return 0
        # Option 1: do nothing today
        best = dp(day + 1, holding, False)
        if holding:
            # Option 2: sell
            best = max(best, prices[day] + dp(day + 1, False, True))
        elif not cooldown:
            # Option 2: buy
            best = max(best, -prices[day] + dp(day + 1, True, False))
        return best

    return dp(0, False, False)
'''

blocks += [
    N.h2("Solution 2 — Top-Down Memoization (Illustrative)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Model it as a recursive decision tree: at each day, and for each combination of "
            "(holding?, in cooldown?), choose the action that maximises total profit from this day onwards."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Without memoization the same (day, holding, cooldown) triple is recomputed exponentially many times. "
            "With n=300 days and 2 boolean flags the state space is 300×2×2 = 1200 entries — tiny — "
            "so @lru_cache makes this O(n) time."
        ),
        N.h4("The Key Observation"),
        N.para(
            "The state (day, holding, cooldown) fully determines future profit. "
            "No earlier history matters beyond these three values — classic optimal substructure. "
            "This directly proves why the bottom-up tabulation with 3 scalars is correct."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Base case: beyond the last day, profit is 0. "
            "Recursive case: try all valid actions for the current state and take the max. "
            "Memoize to avoid redundant subproblems."
        ),
    ]),
    N.h3("Code"),
    N.code(sol2_code, lang="python"),
    N.callout(
        "Use the bottom-up Solution 1 in interviews — it is O(1) space and avoids recursion overhead. "
        "This memoization version is excellent for deriving the recurrence before optimising.",
        "⚠️", "yellow_background"
    ),
    N.divider(),
]

# ── Complexity table ───────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["State Machine DP (bottom-up)", "O(n)", "O(1)"],
        ["Top-Down Memoization", "O(n)", "O(n) — call stack + cache"],
        ["Brute Force (no memo)", "O(3ⁿ)", "O(n)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ─────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Dynamic Programming", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("DP: State Machine (States hold sold rest)", {})])),
    N.callout(
        "When to recognise this pattern: "
        "(1) Buy/sell problem with a rule about adjacent transactions (cooldown, fee, at-most-k). "
        "(2) 'You cannot do X immediately after Y' — signals distinct day-level states. "
        "(3) State on day i depends only on state on day i−1 → O(1) space DP.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ───────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same State Machine DP technique:"),
    N.bullet(N.rich([("Best Time to Buy and Sell Stock II", {"bold": True}),
                     (" (Medium) — Unlimited transactions, no cooldown; simplifies to 2-state DP.", {})])),
    N.bullet(N.rich([("Best Time to Buy and Sell Stock with Transaction Fee", {"bold": True}),
                     (" (Medium) — Same 2-state structure, subtract fee on sell.", {})])),
    N.bullet(N.rich([("Best Time to Buy and Sell Stock III", {"bold": True}),
                     (" (Hard) — At most 2 transactions; extend to (day, txn_count, holding) states.", {})])),
    N.bullet(N.rich([("Best Time to Buy and Sell Stock IV", {"bold": True}),
                     (" (Hard) — At most k transactions; generalised state machine.", {})])),
    N.bullet(N.rich([("Best Time to Buy and Sell Stock I", {"bold": True}),
                     (" (Easy) — Single transaction; track min-so-far, not a full state machine but same family.", {})])),
    N.bullet(N.rich([("House Robber", {"bold": True}),
                     (" (Medium) — 2-state DP (rob / skip) with an implicit 'skip' cooldown on adjacent houses.", {})])),
    N.bullet(N.rich([("Paint House", {"bold": True}),
                     (" (Medium) — 3-state DP (3 colours); cannot paint same colour on consecutive days.", {})])),
    N.para("These problems share the core insight: model constraints as state-machine nodes and fill DP forward in O(n)."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 18 — Dynamic Programming, Sub-Pattern: DP State Machine", "📚", "gray_background"),
]

# ── Embed ──────────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("best_time_to_buy_and_sell_stock_with_cooldown")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ──────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
