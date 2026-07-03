"""Notion update script for LeetCode #753 - Cracking the Safe"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notion_lib as N

PAGE_ID = "39193418-809c-8127-be9a-f44e010e2cc5"

# ─── 1. Set page properties ───
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=753,
    pattern="Graph",
    subpatterns=["De Bruijn Sequence"],
    tc="O(n^k)",
    sc="O(n^k)",
    key_insight="Model k-combinations as edges in De Bruijn graph; Eulerian circuit via Hierholzer's DFS covers all combos in shortest string.",
    icon="🔴"
)
print("Properties set.")

# ─── 2. Wipe existing body ───
print("Wiping old body...")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ─── 3. Rebuild body ───
SOLUTION_1 = '''def crackSafe(n: int, k: int) -> str:
    visited = set()
    result = []
    start = "0" * (k - 1)

    def dfs(node):
        for d in range(n):
            edge = node + str(d)
            if edge not in visited:
                visited.add(edge)
                dfs(node[1:] + str(d))
                result.append(str(d))

    dfs(start)
    return start + "".join(reversed(result))'''

SOLUTION_2 = '''def crackSafe_backtrack(n: int, k: int) -> str:
    target = n ** k
    visited = set()
    result = list("0" * k)
    visited.add("0" * k)

    def backtrack() -> bool:
        if len(visited) == target:
            return True
        node = "".join(result[-(k-1):])
        for d in range(n - 1, -1, -1):
            nxt = node + str(d)
            if nxt not in visited:
                visited.add(nxt)
                result.append(str(d))
                if backtrack():
                    return True
                visited.discard(nxt)
                result.pop()
        return False

    backtrack()
    return "".join(result)'''

PROBLEM_STMT = (
    "There is a safe protected by a password. The password is a sequence of n digits where "
    "each digit is in the range [0, k - 1]. The safe has a peculiar way of checking passwords: "
    "it processes the last n digits entered at any time, and the safe unlocks if any sequence of "
    "n digits entered at any time matches the password. Given two integers n and k, return any "
    "string of minimum length that will unlock the safe at some point of entering it."
)

blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(PROBLEM_STMT),
    N.para(N.rich([
        ("Example: n=2, k=2 → ", {}),
        ('"00110"', {"code": True}),
        (" (contains all 2-digit combos over {0,1}: 00, 01, 11, 10 as substrings)", {})
    ])),
    N.divider(),
]

# ── Solution 1: Hierholzer's Eulerian Circuit DFS ──
blocks += [
    N.h2("Solution 1 — Hierholzer's Eulerian Circuit DFS (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We need the shortest string where every k-digit substring over {0..n-1} appears at least once. "
            "Consecutive substrings of length k overlap by k-1 characters. If we model each (k-1)-character "
            "string as a node, and each k-character combination as a directed edge between its prefix and suffix, "
            "we get the De Bruijn graph."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Naively listing all n^k passwords and concatenating them wastes k-1 characters on every "
            "transition boundary — giving a string of length k·n^k instead of the optimal n^k + k - 1. "
            "This is exponentially worse."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Each directed edge in the De Bruijn graph corresponds to exactly one k-digit combination. "
            "A circuit visiting every edge exactly once (Eulerian circuit) covers all n^k combinations "
            "exactly once. By Euler's theorem, such a circuit exists since every node has equal in-degree "
            "and out-degree (both equal to n)."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Use Hierholzer's algorithm: run DFS from the all-zeros node, marking edges as visited before "
            "recursing. Collect digits post-order (append after returning from recursion). Reverse the "
            "collected digits to get the forward traversal order. Prepend the start node to get the final "
            "string. Time O(n^k), Space O(n^k)."
        ),
        N.callout(
            "Analogy: Imagine a postal worker who must walk every street in a city exactly once. "
            "If every intersection has equal incoming and outgoing roads, such a tour always exists. "
            "Hierholzer finds it greedily, handling dead-ends by post-order backtracking.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("🔬 Algorithm Deep-Dive: Hierholzer's Algorithm"),
    N.para(
        "Hierholzer's Algorithm (Carl Hierholzer, 1873) finds Eulerian circuits in directed graphs in O(E) time. "
        "It works by DFS: at each node, greedily follow an unvisited edge. When stuck (no unvisited edges), "
        "insert the current path into the circuit. The post-order implementation in Python achieves this "
        "automatically via the call stack — each digit is appended only after all subsequent edges are explored."
    ),
    N.para(N.rich([
        ("Core Invariant: ", {"bold": True}),
        ("When dfs(node) returns, all edges reachable via any outgoing edge from 'node' (that weren't "
         "already visited before entering) have been visited. Post-order collection places each edge "
         "label at the correct position in the reversed circuit.", {})
    ])),
    N.para(N.rich([
        ("When to recognize: ", {"bold": True}),
        ('"Visit every edge exactly once" + equal in/out degree → Eulerian circuit → Hierholzer\'s. '
         'Classic tells: Reconstruct Itinerary, Cracking the Safe, Valid Arrangement of Pairs.', {})
    ])),
    N.h3("Code"),
    N.code(SOLUTION_1),
    N.h3("Line by Line"),
    N.para(N.rich([("visited = set()", {"code": True}), (" — Set of visited edge-keys (k-digit combo strings). Each edge is encoded as node + digit = k chars.", {})])),
    N.para(N.rich([("result = []", {"code": True}), (" — Post-order collection of digits. Will be reversed at the end.", {})])),
    N.para(N.rich([("start = '0' * (k - 1)", {"code": True}), (" — Starting node of DFS: the all-zeros (k-1)-length string. For k=1, start is empty string ''.", {})])),
    N.para(N.rich([("edge = node + str(d)", {"code": True}), (" — Edge key = current node prefix + digit = exactly one k-digit combination. This is the identifier for each k-combo.", {})])),
    N.para(N.rich([("if edge not in visited:", {"code": True}), (" — Only traverse each k-combination once (each edge once in the Eulerian circuit).", {})])),
    N.para(N.rich([("visited.add(edge)", {"code": True}), (" — Pre-mark the edge BEFORE recursing to prevent re-entry during the same DFS path.", {})])),
    N.para(N.rich([("dfs(node[1:] + str(d))", {"code": True}), (" — Slide the node window: drop the first character, append the new digit. This is the next node in the De Bruijn graph.", {})])),
    N.para(N.rich([("result.append(str(d))", {"code": True}), (" — POST-ORDER: append the digit AFTER recursion returns. Hierholzer's trick — builds circuit in reverse.", {})])),
    N.para(N.rich([("return start + ''.join(reversed(result))", {"code": True}), (" — Reverse result to get forward order, prepend start node. Total length = (k-1) + n^k = n^k + k - 1.", {})])),
    N.divider(),
]

# ── Solution 2: Backtracking ──
blocks += [
    N.h2("Solution 2 — Backtracking (Brute Force)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Build the result string character by character. At each step, we know the last k-1 characters (the current De Bruijn node). Try each digit: if it creates a new unvisited k-combination, extend the result and recurse."),
        N.h4("What Doesn't Work"),
        N.para("Pure greedy without backtracking can get stuck — choosing digits that close off unvisited combinations. Backtracking ensures we always find the complete sequence."),
        N.h4("The Key Observation"),
        N.para("This is the same graph traversal problem, but approached as explicit backtracking search instead of the mathematical guarantee of Hierholzer's. Trying digits in reverse (n-1 down to 0) is a heuristic that tends to find solutions faster (fewer backtracks in practice)."),
        N.h4("Building the Solution"),
        N.para("Start with '0'*k (covers the first combination). At each step, look at the last k-1 chars as the current 'node'. Try each digit to form a new k-combo. If unvisited, mark and recurse. If all combos covered, return True. Otherwise backtrack."),
    ]),
    N.h3("Code"),
    N.code(SOLUTION_2),
    N.h3("Line by Line"),
    N.para(N.rich([("result = list('0' * k)", {"code": True}), (" — Start with k zeros. This already covers the first k-combo '0'*k.", {})])),
    N.para(N.rich([("node = ''.join(result[-(k-1):])", {"code": True}), (" — Current De Bruijn node = last k-1 chars of result so far.", {})])),
    N.para(N.rich([("for d in range(n-1, -1, -1):", {"code": True}), (" — Try digits in reverse; heuristic to minimize backtracking.", {})])),
    N.para(N.rich([("visited.discard(nxt); result.pop()", {"code": True}), (" — Undo the choice: remove from visited set and pop from result list.", {})])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Backtracking (brute)", "O(n^k · k) worst case", "O(n^k)"],
        ["Hierholzer DFS (optimal)", "O(n^k)", "O(n^k)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Graph — specifically Eulerian Circuit on De Bruijn Graph", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("De Bruijn Sequence (Eulerian Circuit variant)", {})])),
    N.para(N.rich([("Named Algorithm: ", {"bold": True}), ("Hierholzer's Algorithm (1873) for finding Eulerian circuits in O(E)", {})])),
    N.callout(
        "When to recognize this pattern: 'Shortest string containing every k-length combination' → "
        "De Bruijn sequence. 'Visit every edge exactly once in directed graph' → Eulerian circuit → "
        "Hierholzer's. 'Directed graph with equal in/out degree everywhere' → Eulerian circuit exists.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Eulerian Circuit / De Bruijn):"),
    N.bullet(N.rich([("Reconstruct Itinerary", {"bold": True}), (" (Hard) — Eulerian path in directed flight graph; same Hierholzer's DFS post-order pattern (#332)", {})])),
    N.bullet(N.rich([("Valid Arrangement of Pairs", {"bold": True}), (" (Hard) — Find Eulerian path through directed pairs; identical approach (#2097)", {})])),
    N.bullet(N.rich([("Find the Shortest Superstring", {"bold": True}), (" (Hard) — DP on subsets covering all strings with maximum overlap (#943)", {})])),
    N.bullet(N.rich([("Concatenated Words", {"bold": True}), (" (Hard) — Word-level coverage using trie + DP (#472)", {})])),
    N.bullet(N.rich([("Maximum Number of Occurrences of a Substring", {"bold": True}), (" (Medium) — Sliding window frequency over k-length substrings (#1297)", {})])),
    N.bullet(N.rich([("All Paths from Source Lead to Destination", {"bold": True}), (" (Medium) — Graph DFS with cycle detection (#1059)", {})])),
    N.para("These problems share core De Bruijn / Eulerian circuit technique: model combinations as edges, traverse all edges exactly once."),
    N.callout("📚 Reference: De Bruijn Sequence — specialized sub-pattern under Graph / Eulerian Circuit. Hierholzer's algorithm is the standard O(E) solver.", "📚", "gray_background"),
]

# ── Interactive Explainer Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("cracking_the_safe")),
    N.para(N.rich([
        ("Step through the Hierholzer DFS on the De Bruijn graph — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

print(f"Appending {len(blocks)} blocks to Notion...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
