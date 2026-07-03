"""
gen_time_needed_to_buy_tickets.py
Notion IN-PLACE update for LeetCode #2073 — Time Needed to Buy Tickets.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81c6-8f42-d0a801f833c4"
SLUG    = "time_needed_to_buy_tickets"

# ── 1) Properties ────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=2073,
    pattern="Queues",
    subpatterns=["Queue Simulation"],
    tc="O(n)",
    sc="O(1)",
    key_insight="Each person's contribution is min(tickets[i], tickets[k]) if i<=k, else min(tickets[i], tickets[k]-1).",
    icon="🟢",
)
print("Properties set.")

# ── 2) Wipe old body ────────────────────────────────────────────
print("Wiping old blocks...")
removed = N.wipe_page(PAGE_ID)
print(f"Removed {removed} old blocks.")

# ── 3) Rebuild body ─────────────────────────────────────────────
blocks = []

# ── Problem statement ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an array ", {}),
        ("tickets", {"code": True}),
        (" where ", {}),
        ("tickets[i]", {"code": True}),
        (" is the number of tickets person ", {}),
        ("i", {"code": True}),
        (" wants to buy, and an integer ", {}),
        ("k", {"code": True}),
        (", simulate a queue where each person buys one ticket per second then rejoins the back (or leaves if done). Return the total seconds until person ", {}),
        ("k", {"code": True}),
        (" has bought all their tickets.", {}),
    ])),
    N.divider(),
]

# ── Solution 1 — Direct Formula (Interview Pick) ──
sol1_code = """\
def timeRequiredToBuy(tickets: list[int], k: int) -> int:
    time = 0
    for i in range(len(tickets)):
        if i <= k:
            time += min(tickets[i], tickets[k])
        else:
            time += min(tickets[i], tickets[k]-1)
    return time"""

blocks += [
    N.h2("Solution 1 — Direct Formula (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.para(N.rich([("Reframe the Problem", {"bold": True})])),
        N.para("Don't simulate the queue literally. Instead, ask: how many times does each person buy a ticket before person k finishes? The simulation runs for exactly tickets[k] rounds. Each person's contribution is bounded by their own ticket supply and the number of rounds."),
        N.para(N.rich([("What Doesn't Work", {"bold": True})])),
        N.para("A literal deque simulation works but costs O(n × max_tickets). With tickets up to 10^6, that's up to 10^8 operations. We need a smarter approach."),
        N.para(N.rich([("The Key Observation", {"bold": True})])),
        N.para("Each person's total purchases depend only on (1) their position relative to k, and (2) their ticket count vs k's count. People at or before k get min(tickets[i], tickets[k]) rounds. People after k get min(tickets[i], tickets[k]-1) rounds — they miss k's final round because the simulation stops before reaching them."),
        N.para(N.rich([("Building the Solution", {"bold": True})])),
        N.para("Scan once. For each i: if i <= k, add min(tickets[i], tickets[k]) to time. Else add min(tickets[i], tickets[k]-1). The i==k case degenerates to min(tickets[k], tickets[k]) = tickets[k], correctly counting k's own purchases with no special case needed."),
        N.callout("Analogy: The simulation is like a classroom test that ends the moment the target student turns in their paper. Students seated before them finish submitting during the same round; students after never get that final submission.", "🎯", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(sol1_code),
    N.h3("Line by Line"),
    N.para(N.rich([("time = 0", {"code": True}), (" — Accumulate total seconds elapsed.", {})])),
    N.para(N.rich([("for i in range(len(tickets)):", {"code": True}), (" — Single pass over every person.", {})])),
    N.para(N.rich([("if i <= k:", {"code": True}), (" — Persons before AND at k: they share every round k participates in.", {})])),
    N.para(N.rich([("time += min(tickets[i], tickets[k])", {"code": True}), (" — Capped by whoever's supply runs out first.", {})])),
    N.para(N.rich([("else:", {"code": True}), (" — Persons after k: they miss the final round.", {})])),
    N.para(N.rich([("time += min(tickets[i], tickets[k]-1)", {"code": True}), (" — The -1 accounts for the round k finishes before reaching them.", {})])),
    N.para(N.rich([("return time", {"code": True}), (" — Total seconds for k to buy all tickets.", {})])),
    N.divider(),
]

# ── Solution 2 — Queue Simulation (Brute Force) ──
sol2_code = """\
from collections import deque

def timeRequiredToBuy(tickets: list[int], k: int) -> int:
    q = deque(range(len(tickets)))
    time = 0
    while True:
        i = q.popleft()
        tickets[i] -= 1
        time += 1
        if tickets[i] == 0 and i == k:
            return time
        if tickets[i] > 0:
            q.append(i)"""

blocks += [
    N.h2("Solution 2 — Queue Simulation (Brute Force)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.para(N.rich([("Reframe the Problem", {"bold": True})])),
        N.para("Model the problem exactly as stated: a queue, one buy per second, rejoin at back if not done, stop when k finishes."),
        N.para(N.rich([("What Doesn't Work", {"bold": True})])),
        N.para("This approach works correctly but is slow — O(n × max_tickets). With tickets up to 10^6, it can timeout on large inputs."),
        N.para(N.rich([("The Key Observation", {"bold": True})])),
        N.para("Store indices (not ticket values) in the deque so we can identify when person k finishes. Decrement tickets[i] directly in the original array."),
        N.para(N.rich([("Building the Solution", {"bold": True})])),
        N.para("Dequeue front person, decrement their ticket count, increment time. If tickets[i] hits 0 AND i==k, return time. Otherwise if tickets[i]>0, re-enqueue. Repeat."),
        N.callout("This is the 'derive-first' solution. Always write this in an interview first, then propose the O(n) optimization.", "💡", "yellow_background"),
    ]),
    N.h3("Code"),
    N.code(sol2_code),
    N.h3("Line by Line"),
    N.para(N.rich([("q = deque(range(len(tickets)))", {"code": True}), (" — Queue of indices 0..n-1, preserving order.", {})])),
    N.para(N.rich([("i = q.popleft()", {"code": True}), (" — The front person steps up.", {})])),
    N.para(N.rich([("tickets[i] -= 1; time += 1", {"code": True}), (" — Buy one ticket; one second passes.", {})])),
    N.para(N.rich([("if tickets[i] == 0 and i == k:", {"code": True}), (" — k just bought their last ticket — simulation ends.", {})])),
    N.para(N.rich([("if tickets[i] > 0: q.append(i)", {"code": True}), (" — Still needs more tickets; rejoin at the back.", {})])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Queue Simulation (deque)", "O(n × max_tickets)", "O(n)"],
        ["Direct Formula (optimal)", "O(n)", "O(1)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Queues", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Queue Simulation", {})])),
    N.callout(
        "When to recognize this pattern: 'people in a line', 'one ticket/task per second', 'rejoin at back', 'stop when person X finishes'. Also: round-robin with unequal demands where you can compute contributions independently.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Queue Simulation technique:"),
    N.bullet(N.rich([("Number of Students Unable to Eat Lunch", {"bold": True}), (" (Easy) — Students cycle through a stack of sandwiches; classic queue+stack simulation (#1700)", {})])),
    N.bullet(N.rich([("Reveal Cards in Increasing Order", {"bold": True}), (" (Medium) — Reverse-engineer queue operations to find original card order (#950)", {})])),
    N.bullet(N.rich([("Task Scheduler", {"bold": True}), (" (Medium) — CPU round-robin scheduling with cooldown idle periods; formula approach also works (#621)", {})])),
    N.bullet(N.rich([("Dota2 Senate", {"bold": True}), (" (Medium) — Two-faction greedy queue simulation: greedily ban the nearest opponent (#649)", {})])),
    N.bullet(N.rich([("Design Circular Queue", {"bold": True}), (" (Medium) — Implement the fixed-size circular buffer underlying this problem (#622)", {})])),
    N.bullet(N.rich([("Number of Recent Calls", {"bold": True}), (" (Easy) — Sliding-window queue for ping count within a time window (#933)", {})])),
    N.para("These problems all share the core pattern: items cycle through a queue-like structure and you need to track when a specific condition is met."),
    N.callout("📚 Sub-Pattern: Queue Simulation · Source: Guide Section (Stacks & Queues / Queue Simulation). The 'direct formula' trick of reasoning about contribution counts instead of simulating is the key insight for Easy/Medium variants.", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})
    ])),
]

# ── Append everything ──
print(f"Appending {len(blocks)} blocks to Notion...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
