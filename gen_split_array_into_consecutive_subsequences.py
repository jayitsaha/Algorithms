"""gen_split_array_into_consecutive_subsequences.py
Update Notion page in-place for LeetCode #659: Split Array into Consecutive Subsequences.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8181-addf-fc53f8fbaa4a"

# ─── 1) Properties ───────────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=659,
    pattern="Hash Tables",
    subpatterns=["Greedy + Two Maps (Freq & Tails)"],
    tc="O(n)",
    sc="O(n)",
    key_insight="Greedily extend existing runs before starting new ones using freq and tails maps.",
    icon="🟡"
)
print("Properties set OK")

# ─── 2) Wipe old body ────────────────────────────────────────────────────────
print("Wiping old page body...")
n_deleted = N.wipe_page(PAGE_ID)
print(f"Wiped {n_deleted} blocks")

# ─── 3) Rebuild body ─────────────────────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a sorted integer array ", {}),
        ("nums", {"code": True}),
        (", return ", {}),
        ("True", {"code": True}),
        (" if it is possible to divide it into one or more subsequences such that each subsequence consists of consecutive integers and has length at least ", {}),
        ("3", {"code": True}),
        (". Each element must belong to exactly one subsequence.", {}),
    ])),
    N.para("Example: nums = [1,2,3,3,4,5] → True ([1,2,3] and [3,4,5]). nums = [1,2,3,4,4,5] → False."),
    N.divider(),
]

# ─── Solution 1: Greedy + Two Maps (Optimal, Interview Pick) ─────────────────
blocks += [
    N.h2("Solution 1 — Greedy + Two Hash Maps (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to assign every element of a sorted array to a 'run' — a group of consecutive integers of length ≥ 3. Think of it like assigning workers to assembly lines: each line must have at least 3 stations and they must be numbered consecutively."),
        N.h4("What Doesn't Work"),
        N.para("Brute force: repeatedly find the smallest number, try to grab the next two to form a run, remove them. This is O(n²) because list removal is O(n). It also doesn't generalize easily to extending existing runs."),
        N.h4("The Key Observation"),
        N.para("When processing a number n in sorted order, we have exactly two options: (1) attach it to an existing open subsequence that currently ends at n-1, or (2) start a brand-new subsequence [n, n+1, n+2]. If neither is possible, the answer is False. The greedy insight: ALWAYS prefer option 1. Extending an open run is never worse — it uses fewer future elements than starting fresh."),
        N.h4("Building the Solution"),
        N.para("Maintain two Counter maps: freq[v] = how many copies of v still need placement, tails[v] = how many open subsequences currently end at value v. Process each number left to right. If freq[n]==0, skip (already placed). If tails[n-1]>0, extend: tails[n-1]--, tails[n]++, freq[n]--. Else if freq[n+1]>0 and freq[n+2]>0, start new run: freq[n]--, freq[n+1]--, freq[n+2]--, tails[n+2]++. Else return False."),
        N.callout("Analogy: Imagine distributing dominoes into chains. You always snap a new domino onto an existing chain rather than starting a fresh chain — unless no chain ends at the right value. Starting fresh always costs 3 dominoes; extending costs only 1.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(
        "from collections import Counter\n\n"
        "def isPossible(nums: list[int]) -> bool:\n"
        "    freq = Counter(nums)     # remaining count of each number\n"
        "    tails = Counter()        # tails[v] = # open runs ending at v\n"
        "\n"
        "    for n in nums:\n"
        "        if freq[n] == 0:     # already placed, skip\n"
        "            continue\n"
        "        if tails[n - 1] > 0:  # extend existing run\n"
        "            tails[n - 1] -= 1\n"
        "            tails[n] += 1\n"
        "            freq[n] -= 1\n"
        "        elif freq[n + 1] > 0 and freq[n + 2] > 0:  # start new run\n"
        "            freq[n] -= 1\n"
        "            freq[n + 1] -= 1\n"
        "            freq[n + 2] -= 1\n"
        "            tails[n + 2] += 1\n"
        "        else:\n"
        "            return False      # n cannot be placed\n"
        "    return True\n"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("freq = Counter(nums)", {"code": True}), (" — Build the initial frequency count of all numbers. This is what we 'must place'.", {})])),
    N.para(N.rich([("tails = Counter()", {"code": True}), (" — Start with no open subsequences. tails[v] tracks how many runs currently end at value v.", {})])),
    N.para(N.rich([("if freq[n] == 0: continue", {"code": True}), (" — This copy of n was already consumed when we formed a run earlier. Skip it.", {})])),
    N.para(N.rich([("if tails[n-1] > 0:", {"code": True}), (" — At least one open run ends at n-1. We can append n to it.", {})])),
    N.para(N.rich([("tails[n-1] -= 1; tails[n] += 1; freq[n] -= 1", {"code": True}), (" — The run that ended at n-1 now ends at n. Decrement freq[n] to mark it placed.", {})])),
    N.para(N.rich([("elif freq[n+1] > 0 and freq[n+2] > 0:", {"code": True}), (" — No tail to extend, but we have the next two successors available. Start a fresh run.", {})])),
    N.para(N.rich([("freq[n]-=1; freq[n+1]-=1; freq[n+2]-=1; tails[n+2]+=1", {"code": True}), (" — Consume three numbers; the new run ends at n+2.", {})])),
    N.para(N.rich([("else: return False", {"code": True}), (" — Can neither extend nor start. This number is unplaceable — provably impossible.", {})])),
    N.para(N.rich([("return True", {"code": True}), (" — Every number was legally placed into a valid run of length ≥ 3.", {})])),
    N.divider(),
]

# ─── Solution 2: Brute Force (for contrast) ──────────────────────────────────
blocks += [
    N.h2("Solution 2 — Brute Force (O(n²), conceptual only)"),
    N.toggle_h3("💡 Intuition: Naive Greedy", [
        N.h4("Reframe the Problem"),
        N.para("Repeatedly find the smallest unplaced number. Try to grab the next two consecutive values to form a run. If they are not available, return False."),
        N.h4("What Doesn't Work"),
        N.para("List removal is O(n) per operation, making this O(n²) overall. Also does not handle extending runs intelligently — it only starts fresh runs."),
        N.h4("The Key Observation"),
        N.para("This approach is correct for small inputs and makes the problem concrete. But it is too slow for n=50,000 (LeetCode's constraint)."),
        N.h4("Building the Solution"),
        N.para("While the list is non-empty, take the smallest element, check if consecutive neighbors exist, remove all three, repeat. If at any point a neighbor is missing, return False."),
    ]),
    N.h3("Code"),
    N.code(
        "def isPossible_brute(nums: list[int]) -> bool:\n"
        "    nums = sorted(nums)  # ensure sorted\n"
        "    while nums:\n"
        "        start = nums[0]\n"
        "        # need start, start+1, start+2\n"
        "        for v in range(start, start + 3):\n"
        "            if v not in nums:\n"
        "                return False\n"
        "            nums.remove(v)  # O(n) each time -> O(n^2) total\n"
        "    return True\n"
    ),
    N.divider(),
]

# ─── Complexity ───────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Greedy + Two Maps (optimal)", "O(n)", "O(n)"],
        ["Brute Force (list removal)", "O(n^2)", "O(1) extra"],
    ]),
    N.divider(),
]

# ─── Pattern Classification ───────────────────────────────────────────────────
blocks += [
    N.h2("Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Hash Tables", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Greedy + Two Maps (Freq & Tails)", {})])),
    N.callout(
        "When to recognize this pattern: sorted array + 'partition elements into groups with a minimum size constraint' + need to track 'open threads' or 'ongoing sequences'. "
        "Two cooperating maps — one for remaining frequency, one for open endpoints — is the signature of this sub-pattern.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ─── Related Problems ─────────────────────────────────────────────────────────
blocks += [
    N.h2("Related Problems"),
    N.para("Problems using the same Greedy + Two Maps / scheduling technique:"),
    N.bullet(N.rich([("Divide Array in Sets of K Consecutive Numbers", {"bold": True}), (" (Medium) — Identical logic generalized to groups of exactly k consecutive numbers (#1296).", {})])),
    N.bullet(N.rich([("Hand of Straights", {"bold": True}), (" (Medium) — Split cards into groups of W consecutive values — same greedy approach (#846).", {})])),
    N.bullet(N.rich([("Task Scheduler", {"bold": True}), (" (Medium) — Greedy CPU scheduling with cooldowns; frequency analysis of task types (#621).", {})])),
    N.bullet(N.rich([("Non-overlapping Intervals", {"bold": True}), (" (Medium) — Greedy interval scheduling to minimize removed intervals (#435).", {})])),
    N.bullet(N.rich([("Meeting Rooms II", {"bold": True}), (" (Medium) — Count minimum meeting rooms; greedy with a min-heap of end times (#253).", {})])),
    N.bullet(N.rich([("Reconstruct Itinerary", {"bold": True}), (" (Hard) — Greedy assignment of edges in a directed graph; similar 'consume as you go' pattern (#332).", {})])),
    N.para("These problems share the core technique: process elements in order, greedily assign to existing threads before creating new ones, use frequency maps to track state."),
    N.divider(),
]

# ─── Interactive Visual Explainer ─────────────────────────────────────────────
blocks += [
    N.h2("Interactive Visual Explainer"),
    N.embed(N.embed_url_for("split_array_into_consecutive_subsequences")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

print(f"Appending {len(blocks)} blocks to Notion...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")

import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-8181-addf-fc53f8fbaa4a"
SLUG    = "split_array_into_consecutive_subsequences"

# ── 1) Set properties ────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=659,
    pattern="Hash Tables",
    subpatterns=["Greedy + Two Maps (Freq & Tails)"],
    tc="O(n)",
    sc="O(n)",
    key_insight="Maintain freq (inventory) and tails (open runs): greedily extend before starting; pre-commit x+1 and x+2 when opening new triple.",
    icon="🟡"
)
print("Properties set.")

# ── 2) Wipe old body ─────────────────────────────────────────────────
print("Wiping old page body...")
deleted = N.wipe_page(PAGE_ID)
print(f"Deleted {deleted} blocks.")

# ── 3) Build new body ────────────────────────────────────────────────
print("Building new content blocks...")

OPTIMAL_CODE = '''\
from collections import Counter

def isPossible(nums: list[int]) -> bool:
    freq  = Counter(nums)     # inventory: freq[x] = unused copies of x
    tails = Counter()         # open runs: tails[x] = runs waiting for x
    for x in freq:
        if tails[x - 1] > 0:
            tails[x - 1] -= 1   # extend run ending at x-1
            tails[x]     += 1   # run now ends at x, needs x+1
        elif freq[x+1] and freq[x+2]:
            freq[x+1] -= 1      # pre-commit x+1 from inventory
            freq[x+2] -= 1      # pre-commit x+2 from inventory
            tails[x+2] += 1     # new run [x,x+1,x+2] ends at x+2
        else:
            return False        # x has nowhere valid to go
    return True
'''

BRUTE_CODE = '''\
from collections import Counter

def isPossible_brute(nums):
    # O(n * 2^n) — for intuition only; TLE on large inputs
    def backtrack(freq):
        if not any(freq.values()):
            return True
        for s in sorted(k for k, v in freq.items() if v > 0):
            for length in range(3, sum(freq.values()) + 1):
                if all(freq.get(s+i, 0) > 0 for i in range(length)):
                    for i in range(length):
                        freq[s+i] -= 1
                    if backtrack(freq):
                        return True
                    for i in range(length):
                        freq[s+i] += 1
            return False
        return False
    return backtrack(Counter(nums))
'''

blocks = []

# ── Problem section ──────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a sorted integer array ", {}),
        ("nums", {"code": True}),
        (", return ", {}),
        ("true", {"code": True}),
        (" if it can be split into one or more subsequences such that each subsequence consists of consecutive integers and has a length of at least 3.", {})
    ])),
    N.para("Example 1: nums = [1,2,3,3,4,5] → True ([1,2,3] and [3,4,5])"),
    N.para("Example 2: nums = [1,2,3,4,4,5] → False (4,5 can't form a triple)"),
    N.divider(),
]

# ── Solution 1 — Greedy + Two Maps ───────────────────────────────────
blocks += [
    N.h2("Solution 1 — Greedy + Two Maps (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We must assign every element of a sorted array to a 'consecutive run' of length ≥ 3. Think of it as placing numbers onto open chains. Each number either joins an existing chain that is waiting for it, or starts a new chain of exactly [x, x+1, x+2]."),
        N.h4("What Doesn't Work"),
        N.para("Brute-force backtracking tries all possible groupings — exponential time. Even greedy approaches that 'start as long a run as possible' can fail because they may starve future elements of needed neighbours."),
        N.h4("The Key Observation"),
        N.para("For each x, two choices exist: extend a run ending at x-1, or start [x, x+1, x+2]. Extending is always at least as good as starting — by an exchange argument. If you extend, you save x+1 and x+2 for future use. If you start instead, you might leave a run at x-1 incomplete."),
        N.h4("Building the Solution"),
        N.para("Two hash maps: freq[x] = unused copies of x; tails[x] = runs waiting for x. Process values left-to-right: if tails[x-1] > 0, extend. Else if freq[x+1] and freq[x+2] both positive, start new triple and pre-commit those future elements. Else return False."),
        N.callout("Analogy: Think of chains on a conveyor belt. Each number either attaches itself to an existing chain waiting at the end, or starts a brand-new chain that immediately grabs the next two boxes.", "🔗", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(OPTIMAL_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("freq = Counter(nums)", {"code": True}), (" — Build inventory: count every occurrence of each value. This is our full supply of numbers.", {})])),
    N.para(N.rich([("tails = Counter()", {"code": True}), (" — Initialize open-run tracker as empty Counter. tails[x] will count runs currently ending at x.", {})])),
    N.para(N.rich([("for x in freq:", {"code": True}), (" — Iterate over each unique value. Since nums is sorted, Counter preserves insertion order here.", {})])),
    N.para(N.rich([("if tails[x - 1] > 0:", {"code": True}), (" — Is there a run ending at x-1 waiting for x? If yes, extend it (greedy preference).", {})])),
    N.para(N.rich([("tails[x-1] -= 1; tails[x] += 1", {"code": True}), (" — Move the run's tail from x-1 to x. The run grows by one element.", {})])),
    N.para(N.rich([("elif freq[x+1] and freq[x+2]:", {"code": True}), (" — No existing run to extend. Check if we can start triple [x, x+1, x+2]: both x+1 and x+2 must be available.", {})])),
    N.para(N.rich([("freq[x+1] -= 1; freq[x+2] -= 1", {"code": True}), (" — Pre-commit: consume one copy each of x+1 and x+2 from inventory right now, preventing double use.", {})])),
    N.para(N.rich([("tails[x+2] += 1", {"code": True}), (" — Register new run ending at x+2. It needs x+3 to extend further.", {})])),
    N.para(N.rich([("else: return False", {"code": True}), (" — Neither option works: x is unplaceable. Impossible.", {})])),
    N.para(N.rich([("return True", {"code": True}), (" — All unique values processed without failure. Every element is in a valid run.", {})])),
    N.divider(),
]

# ── Solution 2 — Brute Force ─────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Brute Force Backtracking (For Understanding)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Try every possible partition of nums into consecutive subsequences. At each step, pick a starting number and try all possible run lengths from 3 up to the remaining elements."),
        N.h4("What Doesn't Work"),
        N.para("This is exponential — O(n * 2^n) worst case. It correctly identifies the answer but TLEs on any reasonably-sized input. It's shown here only to illustrate why greedy is necessary."),
        N.h4("The Key Observation"),
        N.para("Backtracking is correct because it exhaustively explores all possibilities. The greedy solution works because it makes the locally optimal choice (extend before starting) that is also globally optimal."),
        N.h4("Building the Solution"),
        N.para("Recurse with the current frequency map. Pick the smallest available number as a run start. Try extending it as far as possible (up to remaining count). If the rest is solvable, return True. Otherwise, backtrack and try a different length."),
    ]),
    N.h3("Code"),
    N.code(BRUTE_CODE, "python"),
    N.divider(),
]

# ── Complexity table ──────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force Backtracking", "O(n · 2^n)", "O(n)"],
        ["Greedy + Two Maps (optimal)", "O(n)", "O(n)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Hash Tables (Greedy with frequency counting)", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Greedy + Two Maps (Freq & Tails)", {})])),
    N.callout(
        "When to recognize this pattern: sorted array + partition into consecutive groups + feasibility question + 'extend vs start' decision for each element = Greedy + Two Maps. Key signals: 'consecutive subsequences', 'length ≥ k', sorted input, partitioning all elements.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique — Greedy with frequency/tail tracking:"),
    N.bullet(N.rich([("Hand of Straights", {"bold": True}), (" (Medium) — Partition hand into groups of size W; identical two-map greedy. #846", {})])),
    N.bullet(N.rich([("Divide Array in Sets of K Consecutive Numbers", {"bold": True}), (" (Medium) — Generalized version of Hand of Straights. #1296", {})])),
    N.bullet(N.rich([("Task Scheduler", {"bold": True}), (" (Medium) — Greedy scheduling with frequency tracking; maximize CPU utilization. #621", {})])),
    N.bullet(N.rich([("Reorganize String", {"bold": True}), (" (Medium) — Greedy + frequency: interleave to avoid adjacent repeats. #767", {})])),
    N.bullet(N.rich([("Maximum Number of Weeks for Which You Can Work", {"bold": True}), (" (Medium) — Greedy feasibility with frequency constraints. #1953", {})])),
    N.bullet(N.rich([("Non-Decreasing Array", {"bold": True}), (" (Medium) — Greedy feasibility on sorted arrays with local ordering constraints. #665", {})])),
    N.para("These problems share the core technique: process sorted/ordered input greedily, track availability with one map and open state with a second map."),
    N.callout("Reference: DSA_Patterns_and_SubPatterns_Guide.md — Hash Tables section · Sub-Pattern: Greedy + Two Maps (Freq & Tails)", "📚", "gray_background"),
]

# ── Interactive Visual Explainer ──────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ─────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks to Notion page...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
