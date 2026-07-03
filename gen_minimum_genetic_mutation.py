"""
gen_minimum_genetic_mutation.py
Rebuild the Notion page for Minimum Genetic Mutation (#433) in-place.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81e2-b750-df186789a073"

# ── 1) Properties ──────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=433,
    pattern="Graph",
    subpatterns=["BFS Word Ladder"],
    tc="O(N × 32)",
    sc="O(N)",
    key_insight="BFS on an implicit gene graph: generate all 24 single-char mutations per gene, validate against bank set, enqueue unvisited — first discovery of end is the shortest path.",
    icon="🟡",
)
print("Properties set.")

# ── 2) Wipe old thin body ───────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3) Rebuild body ─────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a gene string ", {}),
        ("start", {"code": True}),
        (" and a target gene string ", {}),
        ("end", {"code": True}),
        (", both of length 8 and using only characters 'A', 'C', 'G', 'T', find the minimum number of mutations to transform ", {}),
        ("start", {"code": True}),
        (" into ", {}),
        ("end", {"code": True}),
        (". Each mutation changes exactly one character, and the result must be a valid gene present in the ", {}),
        ("bank", {"code": True}),
        (" array. Return -1 if no valid mutation path exists.", {}),
    ])),
    N.divider(),
]

# Solution 1 — BFS (Interview Pick)
SOL1_CODE = """\
from collections import deque

def minMutation(start: str, end: str, bank: list) -> int:
    if start == end:
        return 0                        # already at destination
    bank_set = set(bank)               # O(1) membership lookups
    if end not in bank_set:
        return -1                      # end unreachable if not a valid gene
    queue = deque([(start, 0)])        # (current_gene, mutations_so_far)
    visited = {start}                  # mark on enqueue, not dequeue
    while queue:
        gene, steps = queue.popleft()  # FIFO = shortest-first
        for i in range(len(gene)):     # try each of the 8 positions
            for c in 'ACGT':           # try each nucleotide
                if c == gene[i]:
                    continue           # skip no-op
                mutant = gene[:i] + c + gene[i+1:]
                if mutant not in bank_set:
                    continue           # invalid intermediate
                if mutant == end:
                    return steps + 1   # BFS guarantees shortest
                if mutant not in visited:
                    visited.add(mutant)
                    queue.append((mutant, steps + 1))
    return -1                          # path not found
"""

blocks += [
    N.h2("Solution 1 — BFS on Implicit Gene Graph (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need the fewest single-character changes to travel from one gene string to another, visiting only 'valid' intermediate strings. This is a shortest-path problem in a graph where nodes are genes and edges connect genes that differ by exactly one character and are both in the bank."),
        N.h4("What Doesn't Work"),
        N.para("DFS explores paths greedily and might find a long path before a short one. Without exhausting all paths, DFS cannot guarantee the minimum. Exhaustive DFS runs in O(N!) for N bank genes."),
        N.h4("The Key Observation"),
        N.para("The structure is identical to Word Ladder (LeetCode #127). BFS explores genes in order of increasing mutation distance. The first time BFS discovers the end gene as a valid mutation of a level-d gene, d+1 is provably the minimum — no shorter path can exist because BFS would have found it at an earlier level."),
        N.h4("Building the Solution"),
        N.para("1) Quick-exit checks (start==end, end not in bank). 2) BFS queue with (gene, steps). 3) For each dequeued gene, generate all 8 × 3 = 24 single-character mutations. 4) Validate against bank_set (O(1)). 5) If mutant == end, return steps+1. 6) Else enqueue unvisited mutants. 7) Return -1 if queue drains."),
        N.callout("Analogy: think of genes as cities on a map. Each valid single-character change is a direct road. BFS is like expanding a ripple from the starting city — the first ripple that touches the destination city reveals the shortest route.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(SOL1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("bank_set = set(bank)", {"code": True}), (" — converts the list to a hash set so every membership check is O(1) instead of O(N).", {})])),
    N.para(N.rich([("if end not in bank_set: return -1", {"code": True}), (" — end can only be reached if it is itself a valid gene; this short-circuits the entire BFS for impossible inputs.", {})])),
    N.para(N.rich([("queue = deque([(start, 0)])", {"code": True}), (" — initialize BFS with the starting gene at step count 0; deque gives O(1) popleft.", {})])),
    N.para(N.rich([("visited = {start}", {"code": True}), (" — start is marked visited immediately so no path can loop back to it at a longer distance.", {})])),
    N.para(N.rich([("gene, steps = queue.popleft()", {"code": True}), (" — FIFO guarantees we process all level-d genes before any level-(d+1) gene.", {})])),
    N.para(N.rich([("for i in range(len(gene)): for c in 'ACGT':", {"code": True}), (" — nested loop generates all 8 × 4 = 32 combinations; the ", {}), ("if c == gene[i]: continue", {"code": True}), (" skips the 8 no-op same-char cases, leaving 24 genuine mutations.", {})])),
    N.para(N.rich([("mutant = gene[:i] + c + gene[i+1:]", {"code": True}), (" — Python string slicing constructs the mutated string; O(L) where L=8, effectively O(1).", {})])),
    N.para(N.rich([("if mutant == end: return steps + 1", {"code": True}), (" — early return on discovery; BFS depth invariant guarantees minimality.", {})])),
    N.para(N.rich([("visited.add(mutant)", {"code": True}), (" — mark on enqueue, not dequeue, to prevent the same gene being queued multiple times from different parents.", {})])),
    N.para(N.rich([("return -1", {"code": True}), (" — queue exhausted without reaching end; no valid mutation path exists through the bank.", {})])),
    N.divider(),
]

# Solution 2 — Bidirectional BFS
SOL2_CODE = """\
from collections import deque

def minMutation_bidir(start: str, end: str, bank: list) -> int:
    bank_set = set(bank)
    if end not in bank_set:
        return -1
    if start == end:
        return 0
    front = {start}      # frontier from start side
    back  = {end}        # frontier from end side
    visited = {start, end}
    steps = 0
    while front and back:
        steps += 1
        # Always expand the smaller frontier (bidirectional BFS optimization)
        if len(front) > len(back):
            front, back = back, front
        next_front = set()
        for gene in front:
            for i in range(len(gene)):
                for c in 'ACGT':
                    if c == gene[i]:
                        continue
                    mutant = gene[:i] + c + gene[i+1:]
                    if mutant not in bank_set:
                        continue
                    if mutant in back:
                        return steps   # frontiers met
                    if mutant not in visited:
                        visited.add(mutant)
                        next_front.add(mutant)
        front = next_front
    return -1
"""

blocks += [
    N.h2("Solution 2 — Bidirectional BFS (Expert Follow-up)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Standard BFS from start may need to explore O(b^d) nodes (b = branching factor, d = distance). Can we do better?"),
        N.h4("The Key Observation"),
        N.para("Run BFS simultaneously from both start and end. When the two frontiers overlap (a gene appears in both), the total steps is the answer. Each frontier only grows to depth d/2, so the search space drops from O(b^d) to O(b^(d/2)) — a dramatic speedup for large banks or long paths."),
        N.h4("Building the Solution"),
        N.para("Use two sets (front, back) representing the current BFS frontiers. At each step, always expand the smaller set to balance work. When generating a mutation, if it appears in the other frontier, the path is complete: return steps."),
        N.callout("Trick: always expand the smaller frontier. This keeps both sides balanced and gives the best worst-case performance.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("front, back = {start}, {end}", {"code": True}), (" — two frontier sets; start-side and end-side search expand simultaneously.", {})])),
    N.para(N.rich([("if len(front) > len(back): front, back = back, front", {"code": True}), (" — swap to always expand the smaller frontier, balancing the BFS trees.", {})])),
    N.para(N.rich([("if mutant in back: return steps", {"code": True}), (" — frontiers met! The combined depth is the minimum path length.", {})])),
    N.divider(),
]

# Complexity table
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["DFS / Backtracking", "O(N!) worst case", "O(N) stack"],
        ["BFS (Interview Pick)", "O(N × 32) = O(N)", "O(N) visited + queue"],
        ["Bidirectional BFS", "O(√N × 32) in practice", "O(N)"],
    ]),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Graph — BFS Shortest Path (Unweighted)", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("BFS Word Ladder — implicit graph, on-the-fly neighbour generation, shortest path via BFS level traversal", {})])),
    N.callout(
        "When to recognise this pattern:\n"
        "• 'Minimum steps/mutations/transformations' between two states\n"
        "• Each step changes exactly one unit (char, digit, bit, position)\n"
        "• Intermediate states must satisfy a validity constraint (bank, dictionary, no-deadend set)\n"
        "• All steps have equal cost (unweighted) → BFS, not Dijkstra\n"
        "• Explicit start and end states given",
        "🔎", "green_background"
    ),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same BFS Word Ladder technique:"),
    N.bullet(N.rich([("Word Ladder", {"bold": True}), (" (Hard) — same pattern with full English dictionary, longer words, 26-char alphabet (#127)", {})])),
    N.bullet(N.rich([("Word Ladder II", {"bold": True}), (" (Hard) — all shortest transformation paths; BFS + backtracking on BFS tree (#126)", {})])),
    N.bullet(N.rich([("Open the Lock", {"bold": True}), (" (Medium) — 4-digit lock, rotate one digit per step, avoid deadends; exact same BFS template (#752)", {})])),
    N.bullet(N.rich([("Sliding Puzzle", {"bold": True}), (" (Hard) — 2×3 board state encoded as string; BFS on state-space (#773)", {})])),
    N.bullet(N.rich([("Rotting Oranges", {"bold": True}), (" (Medium) — multi-source BFS; count minimum time to spread (#994)", {})])),
    N.bullet(N.rich([("Shortest Path in Binary Matrix", {"bold": True}), (" (Medium) — BFS on a grid, 8-directional, minimum path (#1091)", {})])),
    N.bullet(N.rich([("Jump Game III", {"bold": True}), (" (Medium) — BFS/DFS on index-space reachability (#1306)", {})])),
    N.para("These problems share the core technique: BFS on an implicit graph where nodes are states and edges are valid single-step transitions, guaranteeing shortest-path discovery."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 6 (Graph: BFS Shortest Path Unweighted). Sub-Pattern: BFS Word Ladder. Source: Analysis (structural match to Word Ladder template).", "📚", "gray_background"),
]

# Embed
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("minimum_genetic_mutation")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})
    ])),
]

# Append all blocks
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks appended: {len(blocks)}")
