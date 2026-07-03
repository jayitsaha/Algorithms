"""gen_reveal_cards_in_increasing_order.py — Update Notion page for LC#950."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-819b-a845-d52c93fb5226"

# ── 1. Properties ──────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=950,
    pattern="Queues",
    subpatterns=["Simulate Reverse Process"],
    tc="O(n log n)",
    sc="O(n)",
    key_insight="Simulate the reveal ritual on an index queue to find reveal-order positions; assign sorted cards to those positions.",
    icon="🟡",
)
print("Properties set.")

# ── 2. Wipe old body ────────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3. Build new body ───────────────────────────────────────────────────────
SLUG = "reveal_cards_in_increasing_order"

SOL1_CODE = """\
from collections import deque

def deckRevealedIncreasing(deck):
    n = len(deck)
    deck.sort()                                # Sort: smallest revealed first
    result = [0] * n                           # Output positions 0..n-1
    index_queue = deque(range(n))              # Queue of position indices [0,1,...,n-1]
    for card in deck:                          # Walk sorted values smallest to largest
        result[index_queue.popleft()] = card   # Pop front index -> assign card to that position
        if index_queue:
            index_queue.append(index_queue.popleft())  # Rotate: move new front to back (skip step)
    return result
"""

SOL2_CODE = """\
def deckRevealedIncreasing_brute(deck):
    n = len(deck)
    deck.sort()                                # Same sort step
    indices = list(range(n))                   # Regular list — pops are O(n)
    result = [0] * n
    for card in deck:
        result[indices.pop(0)] = card          # O(n) shift — bottleneck
        if indices:
            indices.append(indices.pop(0))     # O(n) shift again -> O(n^2) total
    return result
"""

blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given an integer array ", {}),
        ("deck", {"code": True}),
        (". The deck is initially sorted in any order. The ", {}),
        ("cards must be placed in a deck", {"bold": True}),
        (" such that when you reveal cards one at a time using the following ritual, they appear in increasing order: (1) Reveal the top card of the deck, (2) If there are still cards in the deck, take the next top card and move it to the bottom of the deck. Repeat until all cards are revealed. Return the ordering of the deck that would reveal the cards in increasing order.", {}),
    ])),
    N.divider(),
]

# Solution 1 — Index Queue Simulation (Interview Pick)
blocks += [
    N.h2("Solution 1 — Index Queue Simulation (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to arrange a deck so a specific ritual produces increasing reveals. Working forward is hard — each placement affects future state. The key reframe: 'In what order are positions revealed?' is a different, tractable question. Answer that first, then assign sorted values to those positions in order."),
        N.h4("What Doesn't Work"),
        N.para("Naively, you might try to simulate forward and greedily fill in values. But after each placement, the remaining positions shift in their relative reveal order — you'd need to re-simulate from scratch after every card, giving O(n²) complexity and mental confusion."),
        N.h4("The Key Observation"),
        N.para("The reveal ritual is fully deterministic on whatever sequence you hand it. So run the exact same ritual — reveal (pop front) and skip (rotate new front to back) — but on a queue of position indices instead of card values. The indices come out in exactly the order they'd be revealed. Assigning sorted values to those positions in that order guarantees increasing reveals."),
        N.h4("Building the Solution"),
        N.para("1) Sort the deck ascending. 2) Create a deque of indices [0..n-1]. 3) For each sorted card: pop the front index → assign card to result[index]. Then rotate: pop new front, push to back. 4) Return result. Use deque not list — popleft() is O(1) on deque vs O(n) on list."),
        N.callout("Analogy: Imagine the dealer performing the ritual blindfolded, but instead of real cards the deck contains numbered slips of paper. The slips come out in a fixed order regardless of what's written on the real cards. We're exploiting that fixed order to place values correctly.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(SOL1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("from collections import deque", {"code": True}), (" — Import deque. Critical: popleft() on a deque is O(1). On a regular list, pop(0) is O(n) because every element shifts. This single line is what makes the solution O(n log n) instead of O(n²).", {})])),
    N.para(N.rich([("n = len(deck)", {"code": True}), (" — Save deck length. We iterate exactly n times (one per card).", {})])),
    N.para(N.rich([("deck.sort()", {"code": True}), (" — Sort ascending. Smallest card = revealed first. This is the crucial ordering that makes the position assignment meaningful.", {})])),
    N.para(N.rich([("result = [0] * n", {"code": True}), (" — Output array with n slots. We'll fill each slot by position index, not sequentially.", {})])),
    N.para(N.rich([("index_queue = deque(range(n))", {"code": True}), (" — deque([0,1,2,...,n-1]). Represents position slots in 'deck order' — position 0 is on top (revealed first in a natural deck). Same structure as the actual deck but holding indices.", {})])),
    N.para(N.rich([("for card in deck:", {"code": True}), (" — Iterate sorted cards smallest to largest. Each iteration assigns one card to one position.", {})])),
    N.para(N.rich([("result[index_queue.popleft()] = card", {"code": True}), (" — Pop front index from queue (this is the next 'revealed' position). Assign current sorted card to that position. This is the 'reveal' step of the ritual on indices.", {})])),
    N.para(N.rich([("if index_queue:", {"code": True}), (" — Guard for the last card: don't try to rotate when the queue is empty. Without this, the next line would crash on an empty deque.", {})])),
    N.para(N.rich([("index_queue.append(index_queue.popleft())", {"code": True}), (" — Two operations: popleft() removes the new front index; append() adds it to the back. This mirrors 'move the new top card to the bottom of the deck' — the skip step of the ritual.", {})])),
    N.para(N.rich([("return result", {"code": True}), (" — The filled result array. When the reveal ritual is applied to this deck, cards appear in increasing order.", {})])),
    N.divider(),
]

# Solution 2 — Brute Force
blocks += [
    N.h2("Solution 2 — Brute Force List (O(n²))"),
    N.toggle_h3("💡 Intuition: Why the List Version is Correct but Slow", [
        N.h4("Reframe the Problem"),
        N.para("Same problem and same algorithm — but using a regular list instead of a deque."),
        N.h4("What Doesn't Work"),
        N.para("Python's list.pop(0) is O(n) because it shifts all remaining elements left. Calling it n times in a loop gives O(n²) total — too slow for large inputs."),
        N.h4("The Key Observation"),
        N.para("The brute force and optimal solutions implement the identical algorithm. The only difference is data structure. Deque gives O(1) popleft; list gives O(n). For n=10,000 cards this means ~100 operations vs ~100,000,000 — a 10^6x slowdown."),
        N.h4("Building the Solution"),
        N.para("Replace deque(range(n)) with list(range(n)). Replace popleft() with pop(0). Functionally identical output, quadratic runtime."),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("indices = list(range(n))", {"code": True}), (" — Regular list. Correct but O(n) for each pop(0) operation due to element shifting.", {})])),
    N.para(N.rich([("result[indices.pop(0)] = card", {"code": True}), (" — pop(0) is O(n) — every remaining element shifts left by one position in memory. The bottleneck.", {})])),
    N.para(N.rich([("indices.append(indices.pop(0))", {"code": True}), (" — Another O(n) pop(0). Total per iteration: O(n). Total over n cards: O(n²).", {})])),
    N.divider(),
]

# Complexity
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["Brute Force (list.pop(0))", "O(n²)", "O(n)", "Correct but too slow; list shifts on each pop"],
        ["Index Queue (deque) ✓", "O(n log n)", "O(n)", "Optimal; sort dominates, all queue ops O(1)"],
    ]),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Queues", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Simulate Reverse Process — use the same deterministic ritual on indices to determine reveal order, then assign sorted values to discovered positions.", {})])),
    N.callout(
        "When to recognize this pattern: items are 'revealed and skipped' in a cyclic/interleaved order; you need to find an arrangement that produces a specific output sequence; any problem where figuring out what-happens-when requires simulating a fixed deterministic ritual.",
        "🔎", "green_background"
    ),
    N.para(N.rich([("Note: ", {"italic": True, "bold": True}), ("The 'Simulate Reverse Process' sub-pattern is classified from problem analysis. The core idea — simulate the forward ritual on position indices to discover reveal order — is specific to this class of queue simulation problems.", {"italic": True})])),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same queue simulation technique:"),
    N.bullet(N.rich([("Design Circular Queue", {"bold": True}), (" (Medium) — Implement a queue with fixed capacity and wraparound. Core queue mechanics (#622).", {})])),
    N.bullet(N.rich([("Task Scheduler", {"bold": True}), (" (Medium) — Greedy + queue: schedule tasks with cooldown, maximize CPU utilization (#621).", {})])),
    N.bullet(N.rich([("Sliding Window Maximum", {"bold": True}), (" (Hard) — Monotonic deque keeps window maximum at front — the deque's O(1) popleft is essential (#239).", {})])),
    N.bullet(N.rich([("Dota2 Senate", {"bold": True}), (" (Medium) — Two queues simulate cyclic senator voting rounds to find winning party (#649).", {})])),
    N.bullet(N.rich([("Number of Recent Calls", {"bold": True}), (" (Easy) — Queue stores request timestamps; pop expired entries from front in O(1) (#933).", {})])),
    N.bullet(N.rich([("Design Hit Counter", {"bold": True}), (" (Medium) — Queue of (timestamp, count) pairs; same sliding-window-over-time idea (#362).", {})])),
    N.bullet(N.rich([("Josephus Problem (circular elimination)", {"bold": True}), (" (Interview classic) — Who survives k-step elimination? Identical deque pop+rotate structure.", {})])),
    N.para("These problems share the core technique: a deque enables O(1) operations at both ends, making cyclic/interleaved simulation efficient."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Queues section. Sub-pattern 'Simulate Reverse Process' classified via analysis of the index-queue reveal-order trick.", "📚", "gray_background"),
]

# Embed
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys. Shows the index queue evolving, result array being filled, and which code line is executing at each step.",
         {"italic": True, "color": "gray"})
    ])),
]

# Append all blocks
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
