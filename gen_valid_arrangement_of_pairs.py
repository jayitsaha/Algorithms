"""
Notion regeneration for: Valid Arrangement of Pairs (LeetCode #2097)
Run from the Algorithms directory alongside notion_lib.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notion_lib as N

PAGE_ID = "39193418-809c-8138-bf31-e391aa68551b"
SLUG = "valid_arrangement_of_pairs"

print(f"[1/4] Setting properties on page {PAGE_ID} ...")
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=2097,
    pattern="Graph Algorithms",
    subpatterns=["Hierholzer's Algorithm"],
    tc="O(V + E)",
    sc="O(V + E)",
    key_insight="Model pairs as directed edges, find Eulerian path via Hierholzer's iterative DFS: follow edges until stuck, backtrack by appending to result, then reverse.",
    icon="🔴",
    status="Solved",
    source="LeetCode",
)
print("   Properties set.")

print("[2/4] Wiping existing page body ...")
wiped = N.wipe_page(PAGE_ID)
print(f"   Wiped {wiped} blocks.")

print("[3/4] Building new page body ...")

PROBLEM_STATEMENT = (
    "Given a 0-indexed 2D integer array pairs where pairs[i] = [starti, endi], "
    "an arrangement of pairs is valid if for every index i where 1 <= i < pairs.length, "
    "we have endi-1 == starti. Return any valid arrangement of pairs. "
    "Note: The inputs will be generated such that there exists a valid arrangement of pairs."
)

SOL1_CODE = """\
from collections import defaultdict

def validArrangement(pairs):
    graph = defaultdict(list)        # adj list: node -> [neighbors]
    indeg  = defaultdict(int)        # in-degree per node
    outdeg = defaultdict(int)        # out-degree per node

    for s, e in pairs:
        graph[s].append(e)           # directed edge s -> e
        outdeg[s] += 1
        indeg[e]  += 1

    # Find start: node with out-degree - in-degree == 1
    start = pairs[0][0]              # default (Eulerian circuit case)
    for node in outdeg:
        if outdeg[node] - indeg[node] == 1:
            start = node
            break

    path, stack = [], [start]

    while stack:
        node = stack[-1]             # peek (don't pop yet)
        if graph[node]:
            stack.append(graph[node].pop())   # follow edge, consume it
        else:
            path.append(stack.pop())          # dead end -> backtrack to path

    path.reverse()                   # built backwards; reverse for correct order

    return [[path[i], path[i + 1]] for i in range(len(path) - 1)]
"""

SOL2_CODE = """\
def validArrangement_brute(pairs):
    \"\"\"O(n!) backtracking — correct but TLE for large inputs.\"\"\"
    def backtrack(chain, remaining):
        if not remaining:
            return chain
        cur_end = chain[-1][1]
        for i, (s, e) in enumerate(remaining):
            if s == cur_end:
                res = backtrack(chain + [[s, e]], remaining[:i] + remaining[i+1:])
                if res:
                    return res
        return None

    for i in range(len(pairs)):
        res = backtrack([pairs[i]], pairs[:i] + pairs[i+1:])
        if res:
            return res
"""

blocks = []

# ── Problem ──────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(PROBLEM_STATEMENT),
    N.divider(),
]

# ── Solution 1: Hierholzer's ─────────────────────────────────────────
blocks += [
    N.h2("Solution 1 — Hierholzer's Iterative DFS (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Each pair [a, b] says 'something starts at a and ends at b.' "
            "The chaining constraint — end of one pair must be start of the next — "
            "means we need a sequence of connected edges. This is exactly a path through "
            "a directed graph where each pair is an edge."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Brute-force backtracking tries all permutations: O(n!) time. "
            "For n=10 pairs that's 3.6M attempts; for n=200,000 it's astronomically infeasible. "
            "We need to exploit the mathematical structure of the problem."
        ),
        N.h4("The Key Observation"),
        N.para(
            "This is an Eulerian Path problem! In graph theory, an Eulerian path visits every "
            "edge exactly once. The existence conditions are simple: at most one node has "
            "out-degree exceeding in-degree by 1 (the start), at most one has in-degree "
            "exceeding out-degree by 1 (the end), all others are balanced. "
            "The problem guarantees these hold."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. Build adjacency list from pairs. "
            "2. Find start node (out-in=1, or any node if all balanced). "
            "3. Hierholzer's DFS: follow edges until stuck, then backtrack by appending to result. "
            "4. Reverse result, convert consecutive nodes to pairs."
        ),
        N.callout(
            "Analogy: Imagine planning a road trip where each road segment's destination "
            "must be the next segment's origin. You drive until you reach a dead end (no more "
            "roads), then 'record' that city and backtrack. Reverse your notes = the correct route.",
            "🚗", "blue_background"
        ),
    ]),
    N.h3("🔬 Algorithm Deep-Dive: Hierholzer's Algorithm"),
    N.para(
        "Invented by Carl Hierholzer (1873), published posthumously. "
        "Finds Eulerian paths/circuits in O(V+E) time. "
        "Core invariant: a node is added to the result path when it has no remaining outgoing edges — "
        "at that point it occupies its correct final position relative to the current DFS stack. "
        "Building the path in reverse (appending on backtrack, then reversing) correctly merges "
        "all sub-circuits into the main Eulerian path."
    ),
    N.code(
        "# Hierholzer's Template (Iterative)\n"
        "def hierholzer(graph, start):\n"
        "    path, stack = [], [start]\n"
        "    while stack:\n"
        "        node = stack[-1]               # peek\n"
        "        if graph[node]:                # unused edges remain\n"
        "            stack.append(graph[node].pop())  # follow and consume\n"
        "        else:                          # dead end\n"
        "            path.append(stack.pop())   # record and backtrack\n"
        "    path.reverse()\n"
        "    return path\n"
        "# Recognize when: 'chain all items where end of one = start of next'"
    ),
    N.h3("Code"),
    N.code(SOL1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("graph = defaultdict(list)", {"code": True}),
                   " — Adjacency list mapping each node to its list of destination nodes."])),
    N.para(N.rich([("indeg, outdeg = defaultdict(int)...", {"code": True}),
                   " — Track in-degree and out-degree for every node to find the Eulerian path start."])),
    N.para(N.rich([("for s, e in pairs: graph[s].append(e)...", {"code": True}),
                   " — Build the directed graph: each pair [s,e] becomes a directed edge s→e."])),
    N.para(N.rich([("start = pairs[0][0]", {"code": True}),
                   " — Default start; will be overridden if a node with out−in=1 is found."])),
    N.para(N.rich([("if outdeg[node] - indeg[node] == 1: start = node", {"code": True}),
                   " — The true Eulerian path start has exactly one more outgoing edge than incoming."])),
    N.para(N.rich([("path, stack = [], [start]", {"code": True}),
                   " — path builds the result (in reverse). stack drives the DFS traversal."])),
    N.para(N.rich([("node = stack[-1]", {"code": True}),
                   " — Peek at the current node without removing it. We decide based on whether it has edges."])),
    N.para(N.rich([("stack.append(graph[node].pop())", {"code": True}),
                   " — Follow the next outgoing edge: pop the neighbor (consuming the edge) and push it."])),
    N.para(N.rich([("path.append(stack.pop())", {"code": True}),
                   " — Dead end: this node's sub-path is complete. Pop it from the DFS stack, append to result."])),
    N.para(N.rich([("path.reverse()", {"code": True}),
                   " — path was built in backtrack order (reversed). Reversing gives the correct forward Eulerian path."])),
    N.para(N.rich([("return [[path[i], path[i+1]] for i in range(len(path)-1)]", {"code": True}),
                   " — Convert the node sequence to output pairs: consecutive nodes form each [start, end] pair."])),
    N.divider(),
]

# ── Solution 2: Brute Force ──────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Backtracking / Brute Force"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Try every possible ordering of the pairs, checking if each forms a valid chain."),
        N.h4("What Doesn't Work at Scale"),
        N.para("O(n!) time makes this feasible only for tiny inputs (n ≤ 12). Useful to mention as a baseline to show you understand the problem before optimizing."),
        N.h4("The Key Observation"),
        N.para("At each step, only pairs whose start equals the current chain's tail are valid candidates. This prunes the search space but worst case is still factorial."),
        N.h4("Building the Solution"),
        N.para("Try each pair as the starting pair. For each choice, recursively try all pairs whose start matches the current chain's end. Return on first valid complete arrangement."),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("if not remaining: return chain", {"code": True}),
                   " — Base case: all pairs placed successfully — this is a valid arrangement."])),
    N.para(N.rich([("cur_end = chain[-1][1]", {"code": True}),
                   " — The tail value that the next pair must start with."])),
    N.para(N.rich([("if s == cur_end:", {"code": True}),
                   " — Only try pairs that can extend the chain at this position."])),
    N.para(N.rich([("backtrack(chain + [[s,e]], remaining[:i]+remaining[i+1:])", {"code": True}),
                   " — Recurse with updated chain and the remaining unused pairs."])),
    N.divider(),
]

# ── Complexity ────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Backtracking (Brute Force)", "O(n!)", "O(n)"],
        ["Hierholzer's Iterative DFS (Optimal)", "O(V + E)", "O(V + E)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}),
                   "Graph Algorithms (Section 17 — DSA_Patterns_and_SubPatterns_Guide.md)"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}),
                   "Hierholzer's Algorithm (Section 17.7 — Eulerian Circuit/Path)"])),
    N.callout(
        "When to recognize this pattern:\n"
        "• 'Arrange items so each item's end property equals the next item's start property'\n"
        "• 'Use every edge / ticket / domino exactly once in a sequence'\n"
        "• Chaining directed relationships where end-of-one = start-of-next\n"
        "• Keywords: 'valid arrangement', 'reconstruct itinerary', 'Eulerian'",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Hierholzer's / Eulerian Path):"),
    N.bullet(N.rich([("Reconstruct Itinerary", {"bold": True}),
                     " (Hard) — Identical algorithm with lexicographic ordering of adjacency lists; airports as nodes, flights as directed edges. (#332)"])),
    N.bullet(N.rich([("Cracking the Safe", {"bold": True}),
                     " (Hard) — De Bruijn sequence construction via Eulerian circuit on a de Bruijn graph. (#753)"])),
    N.bullet(N.rich([("Find the Shortest Superstring", {"bold": True}),
                     " (Hard) — Overlapping strings modeled as directed graph; Eulerian path gives shortest superstring. (#943 variant)"])),
    N.bullet(N.rich([("All Paths From Source to Target", {"bold": True}),
                     " (Medium) — DFS path enumeration in a DAG; related graph traversal pattern. (#797)"])),
    N.bullet(N.rich([("Course Schedule II", {"bold": True}),
                     " (Medium) — Topological sort; another 'ordering with constraints in a directed graph' problem. (#210)"])),
    N.bullet(N.rich([("Word Ladder II", {"bold": True}),
                     " (Hard) — Find all shortest transformation sequences; BFS + path reconstruction. (#126)"])),
    N.para("These problems share the core technique: model relationships as directed edges, then traverse/order them using graph algorithms (Eulerian path, topological sort, BFS)."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 17.7 (Graph Algorithms → Eulerian Circuit/Path)\nSub-Pattern verified: Guide Section 17.7, row 'Valid Arrangement of Pairs | Hard | Hierholzer's Algorithm'", "📚", "gray_background"),
]

# ── Embed ─────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.",
                    {"italic": True, "color": "gray"})])),
]

print(f"   Total blocks to append: {len(blocks)}")
N.append_blocks(PAGE_ID, blocks)
print("   Blocks appended successfully.")

print("[4/4] Writing status file ...")
import json, pathlib

status_dir = pathlib.Path(__file__).parent / ".status"
status_dir.mkdir(exist_ok=True)

html_path = pathlib.Path(__file__).parent / "valid_arrangement_of_pairs_explainer.html"
html_lines = len(html_path.read_text().splitlines())

status = {
    "slug": SLUG,
    "html": "OK",
    "notion": "OK",
    "lines": html_lines,
    "notes": "Hierholzer Eulerian Path — full 7-section explainer, 14-step walkthrough, graph node viz"
}
status_path = status_dir / f"{SLUG}.json"
status_path.write_text(json.dumps(status, indent=2))
print(f"   Status written to {status_path}")

print(f"\nRESULT {SLUG} | html=OK | notion=OK | lines={html_lines}")
