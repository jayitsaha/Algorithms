"""
gen_find_the_winner_of_the_circular_game.py
Notion in-place update for LeetCode #1823 – Find the Winner of the Circular Game
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notion_lib as N

PAGE_ID = "39193418-809c-8159-bc50-e77239ea389a"
SLUG    = "find_the_winner_of_the_circular_game"

# ── 1. Properties ──────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty  = "Medium",
    number      = 1823,
    pattern     = "Queues",
    subpatterns = ["Josephus Problem / Queue"],
    tc          = "O(nk) queue simulation; O(n) Josephus recurrence",
    sc          = "O(n) queue simulation; O(1) Josephus recurrence",
    key_insight = "Rotate k−1 players to back per round; popleft eliminates the k-th. "
                  "Josephus recurrence J(i)=(J(i-1)+k)%i gives O(n) winner position.",
    icon        = "🟡",
)
print("Properties set.")

# ── 2. Wipe old content ─────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3. Build body blocks ────────────────────────────────────────────────────
blocks = []

# ─── Problem ───────────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        "There are ", ("n", {"code": True}),
        " friends that are playing a game. The friends are sitting in a circle and are numbered from ",
        ("1", {"code": True}), " to ", ("n", {"code": True}),
        " in clockwise order. More formally, moving clockwise from the ",
        ("i", {"code": True}), "-th friend brings you to the ",
        ("(i+1)", {"code": True}), "-th friend for ",
        ("1 <= i < n", {"code": True}), ", and moving clockwise from the ",
        ("n", {"code": True}), "-th friend brings you to the ",
        ("1", {"code": True}), "-st friend.\n\n"
        "The rules of the game are as follows:\n"
        "1. Start at the 1st friend.\n"
        "2. Count the next k friends in the clockwise direction including the friend you started at. "
        "The counting wraps around the circle and may count some friends more than once.\n"
        "3. The last friend you counted leaves the circle and loses the game.\n"
        "4. If there is still more than one friend in the circle, go back to step 2 starting from "
        "the friend immediately clockwise of the friend who just lost and repeat.\n"
        "5. Else, the last friend in the circle wins the game.\n\n"
        "Given the number of friends ", ("n", {"code": True}),
        " and an integer ", ("k", {"code": True}),
        ", return the winner of the game.\n\n"
        "Example: n=5, k=2 → Output: 3\n"
        "Explanation: Players are eliminated in order: 2, 4, 1, 5. Player 3 wins.\n\n"
        "Constraints: 1 <= k <= n <= 500"
    ])),
    N.divider(),
]

# ─── Solution 1 — Queue Simulation ─────────────────────────────────────────
blocks += [
    N.h2("Solution 1 — Queue Simulation (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("You have a circle of players and a counting elimination game. What data structure naturally models a circle where you can 'rotate' and 'remove the front element'? A deque (double-ended queue) — appending to the back and popping from the front."),
        N.h4("What Doesn't Work"),
        N.para("A plain Python list works but is slow: list.pop(idx) is O(n) since all elements shift. For n=500, k=500 this matters. A deque's popleft() is O(1), making the simulation much faster in practice."),
        N.h4("The Key Observation"),
        N.para("'Count k steps clockwise and eliminate' = 'skip k−1 players to the back of the queue (they survive), then the k-th player is now at the front — eliminate them (popleft).' The front player is always the current 'counting start.'"),
        N.h4("Building the Solution"),
        N.para("Initialize deque with [1..n]. Loop while size > 1: rotate (popleft → append) k−1 times, then popleft to eliminate. The remaining element is the winner."),
        N.callout(
            "Analogy: Think of the queue as a line that wraps around. "
            "You 'count past' (send to back of line) k−1 people, then the next person is eliminated. "
            "The line keeps shrinking until one person is left.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(
        "from collections import deque\n"
        "\n"
        "def findTheWinner(n: int, k: int) -> int:\n"
        "    q = deque(range(1, n + 1))\n"
        "    while len(q) > 1:\n"
        "        for _ in range(k - 1):\n"
        "            q.append(q.popleft())\n"
        "        q.popleft()\n"
        "    return q[0]"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("from collections import deque", {"code": True}),
                   " — Import the deque class (double-ended queue) from Python's standard library."])),
    N.para(N.rich([("q = deque(range(1, n + 1))", {"code": True}),
                   " — Create the circular queue: players 1 through n in order. Player 1 is at the front — counting starts here."])),
    N.para(N.rich([("while len(q) > 1:", {"code": True}),
                   " — Keep eliminating as long as more than one player remains."])),
    N.para(N.rich([("for _ in range(k - 1):", {"code": True}),
                   " — We need to skip k−1 players (they are 'counted past' but survive this round)."])),
    N.para(N.rich([("q.append(q.popleft())", {"code": True}),
                   " — Remove the front player and add them to the back. They counted as 1, 2, ..., k−1 but are NOT eliminated."])),
    N.para(N.rich([("q.popleft()", {"code": True}),
                   " — The player now at the front was the k-th in the count. Eliminate them (discard from queue)."])),
    N.para(N.rich([("return q[0]", {"code": True}),
                   " — Only one player remains. That is the winner — return their number."])),
    N.divider(),
]

# ─── Solution 2 — Josephus Recurrence ──────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Josephus Recurrence (Optimal, O(n) Time, O(1) Space)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Can we avoid simulating every elimination? Instead of actually moving players, can we mathematically predict which position the winner ends up in after all n−1 eliminations?"),
        N.h4("What Doesn't Work"),
        N.para("Jumping straight to the formula without understanding the recurrence leads to confusion. You must think recursively: 'If I know the winner's position for n−1 players, where is the same person in the n-player game?'"),
        N.h4("The Key Observation"),
        N.para("After the first elimination (player at position k−1 in 0-indexed), the remaining n−1 players form a new circle. The winner of this new n−1 game maps back to the original n-player game by shifting all positions by k (the amount we counted). This is the Josephus recurrence: J(i) = (J(i−1) + k) % i."),
        N.h4("Building the Solution"),
        N.para("Base case: J(1) = 0 (only one player, they're at position 0). Build up: for each i from 2 to n, apply J(i) = (J(i−1) + k) % i. The final J(n) is the 0-indexed winner position. Add 1 for 1-indexed player number."),
        N.callout(
            "Algorithm Deep-Dive: Josephus Problem (Flavius Josephus, 37 CE)\n"
            "Origin: The historian Josephus is said to have survived a mass suicide pact by computing this problem.\n"
            "Core invariant: J(i) always holds the 0-indexed position of the survivor in a game of i people.\n"
            "Why it works: Each elimination shifts all subsequent 0-indexed positions by k (mod current circle size).\n"
            "Recognize when: 'Circle + count + eliminate + find survivor' with O(1) space requirement.",
            "🔬", "purple_background"
        ),
    ]),
    N.h3("Code"),
    N.code(
        "def findTheWinner(n: int, k: int) -> int:\n"
        "    pos = 0\n"
        "    for i in range(2, n + 1):\n"
        "        pos = (pos + k) % i\n"
        "    return pos + 1"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("pos = 0", {"code": True}),
                   " — Base case J(1)=0: if there is only one player, they are at 0-indexed position 0."])),
    N.para(N.rich([("for i in range(2, n + 1):", {"code": True}),
                   " — Solve the game for 2 players, then 3, then 4, ..., up to n players. Build up from the base case."])),
    N.para(N.rich([("pos = (pos + k) % i", {"code": True}),
                   " — The Josephus recurrence: J(i) = (J(i−1) + k) % i. Adding k shifts the winner's position (mod i for circular wrap-around)."])),
    N.para(N.rich([("return pos + 1", {"code": True}),
                   " — pos is 0-indexed (positions 0..n−1). Players are numbered 1..n. Add 1 to convert."])),
    N.divider(),
]

# ─── Complexity ─────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution",               "Time",   "Space"],
        ["Queue Simulation",       "O(nk)",  "O(n)"],
        ["Josephus Recurrence",    "O(n)",   "O(1)"],
    ]),
    N.divider(),
]

# ─── Pattern Classification ─────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}),
                   "Queues — The queue (deque) directly models the circular elimination process."])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}),
                   "Josephus Problem / Queue — Circular counting-out elimination; mathematical recurrence for optimal solution."])),
    N.callout(
        "When to recognize this pattern:\n"
        "• 'n people in a circle' + 'count k steps' + 'eliminate' = Josephus variant\n"
        "• 'Hot potato', 'eeny meeny', 'round-robin elimination'\n"
        "• Need to find 'last survivor' in counting game → Josephus recurrence\n"
        "• Rotate-and-remove on circular sequence → deque with popleft/append",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ─── Related Problems ───────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Josephus Problem / Queue simulation):"),
    N.bullet(N.rich([("Dota2 Senate", {"bold": True}),
                     " (Medium) — Two-queue circular elimination between Radiant and Dire factions. Classic queue rotation. (#649)"])),
    N.bullet(N.rich([("Design Circular Queue", {"bold": True}),
                     " (Medium) — Implement a circular queue data structure from scratch with array. (#622)"])),
    N.bullet(N.rich([("Reveal Cards in Increasing Order", {"bold": True}),
                     " (Medium) — Use queue rotation to reconstruct the interleaved reveal order for sorted cards. (#950)"])),
    N.bullet(N.rich([("Task Scheduler", {"bold": True}),
                     " (Medium) — Simulate CPU task scheduling with round-robin queue rotation. (#621)"])),
    N.bullet(N.rich([("Number of Recent Calls", {"bold": True}),
                     " (Easy) — Maintain a sliding time window with a queue (deque popleft for expiry). (#933)"])),
    N.bullet(N.rich([("Time Needed to Buy Tickets", {"bold": True}),
                     " (Easy) — Circular queue simulation: count how many full/partial rounds until person k buys all tickets. (#2073)"])),
    N.para("These problems share the core technique: model a circle or sliding sequence with a deque, use popleft/append to rotate, and remove elements at defined positions."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Queues section\nSub-Pattern: Josephus Problem / Queue · Source: Analysis (well-known classical variant).\nNamed after Flavius Josephus (37–100 CE); formalized in Knuth's The Art of Computer Programming.", "📚", "gray_background"),
]

# ─── Visual Explainer Embed ─────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── 4. Append all blocks ────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"Appended {len(blocks)} blocks to Notion page {PAGE_ID}.")
print(f"NOTION OK {PAGE_ID}")
