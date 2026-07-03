"""
gen_reconstruct_itinerary.py
Rebuild Notion page for #332 Reconstruct Itinerary in-place.
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-8159-ad6b-f120e9bb01ea"

# ── 1) Set Properties ──
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=332,
    pattern="Graph",
    subpatterns=["Hierholzer's Algorithm"],
    tc="O(E log E)",
    sc="O(E)",
    key_insight="Post-order DFS: append airport after exhausting all outgoing edges, then reverse. Handles cycles and lexicographic order simultaneously.",
    icon="🔴"
)
print("Properties set OK.")

# ── 2) Wipe existing blocks ──
print("Wiping old content...")
n = N.wipe_page(PAGE_ID)
print(f"Wiped {n} blocks.")

# ── 3) Build body blocks ──
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a list of airline ", {}),
        ("tickets", {"code": True}),
        (" represented as pairs ", {}),
        ("[from, to]", {"code": True}),
        (", reconstruct the itinerary in order. All of the tickets belong to a man who departs from ", {}),
        ('"JFK"', {"code": True}),
        (". Thus, the itinerary must begin with ", {}),
        ('"JFK"', {"code": True}),
        (". If there are multiple valid itineraries, return the itinerary that has the smallest lexical order when read as a single string. You may assume all tickets form at least one valid itinerary. You must use all the tickets once and only once.", {})
    ])),
    N.para(N.rich([
        ("Example 1: ", {"bold": True}),
        ('tickets = [["MUC","LHR"],["JFK","MUC"],["LHR","SFO"],["SFO","SJC"]]', {"code": True}),
        (" → Output: ", {}),
        ('["JFK","MUC","LHR","SFO","SJC"]', {"code": True})
    ])),
    N.para(N.rich([
        ("Example 2: ", {"bold": True}),
        ('tickets = [["JFK","SFO"],["JFK","ATL"],["SFO","ATL"],["ATL","JFK"],["ATL","SFO"]]', {"code": True}),
        (" → Output: ", {}),
        ('["JFK","ATL","JFK","SFO","ATL","SFO"]', {"code": True})
    ])),
    N.divider(),
]

# ── Solution 1: Hierholzer's Iterative ──
blocks += [
    N.h2("Solution 1 — Hierholzer's Algorithm Iterative (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Each ticket is a directed edge from one airport to another. We need to find a path through this directed graph that uses every edge exactly once — starting from JFK. This is the classic Eulerian path problem. The question is: which algorithm finds an Eulerian path efficiently?"),
        N.h4("What Doesn't Work"),
        N.para("Brute-force backtracking tries all permutations of edge use — O(E!) time, which is completely infeasible for even 50 tickets. Greedy 'always pick the lexicographically smallest next airport' seems promising but fails when it enters a sub-graph that dead-ends too early, leaving other tickets unused and no way back."),
        N.h4("The Key Observation"),
        N.para("The insight is post-order insertion. Instead of building the path forward, we build it backwards. When an airport has no more outgoing edges (a dead end), we know it must be the last stop in any path that reaches it — so we add it to the result immediately. Then we unwind backwards. Reversing the result at the end gives the correct forward itinerary."),
        N.h4("Building the Solution"),
        N.para("1) Sort all tickets so adjacency lists are in lexicographic order. 2) Push 'JFK' onto a DFS stack. 3) While the stack is non-empty: if the top airport has outgoing edges, push the smallest destination and consume that edge. If no edges remain, pop the airport to the result list (post-order). 4) Reverse result."),
        N.callout(
            "Analogy: Think of it like exploring a maze. You keep going deeper until you hit a dead end. When stuck, you mark that room as 'last visited' and backtrack. Reversing your 'last visited' list gives the forward path.",
            "🧠", "blue_background"
        )
    ]),
    N.h3("🔬 Algorithm Deep-Dive: Hierholzer's Algorithm"),
    N.para(N.rich([
        ("Origin: ", {"bold": True}),
        ("Carl Hierholzer, 1873. Finds Eulerian circuits (every edge once, return to start) and Eulerian paths (every edge once, start ≠ end) in O(E) time after sorting. The modern DFS formulation builds on his original two-phase approach.", {})
    ])),
    N.para(N.rich([
        ("Core invariant: ", {"bold": True}),
        ("When a vertex is appended post-order, all edges reachable from it have already been explored and their destinations are already in the result. Reversing then places the vertex correctly before all of its successors in the itinerary.", {})
    ])),
    N.para(N.rich([
        ("Why it handles cycles: ", {"bold": True}),
        ("A cycle like JFK→ATL→JFK is traversed completely before JFK is added to result. The second JFK (from the cycle) is added before ATL, and ATL before the first JFK. After reversal: JFK, ATL, JFK — correct!", {})
    ])),
    N.para(N.rich([
        ("Recognize when: ", {"bold": True}),
        ('"Use every edge exactly once" · "Reconstruct a sequence from pairs" · Eulerian path/circuit problems · Directed graph traversal with all-edge coverage.', {})
    ])),
    N.h3("Code"),
    N.code(
        "from collections import defaultdict\n"
        "import heapq\n\n"
        "def findItinerary(tickets):\n"
        "    # Build adjacency list with heap for lexicographic order\n"
        "    graph = defaultdict(list)\n"
        "    for src, dst in sorted(tickets):  # sort ensures lex order\n"
        "        graph[src].append(dst)\n"
        "    \n"
        "    result = []\n"
        "    stack = ['JFK']\n"
        "    \n"
        "    while stack:\n"
        "        top = stack[-1]          # peek: don't pop yet\n"
        "        if graph[top]:           # still has outgoing edges\n"
        "            stack.append(graph[top].pop(0))  # push smallest dest\n"
        "        else:                    # dead end: no outgoing edges\n"
        "            result.append(stack.pop())  # POST-ORDER append\n"
        "    \n"
        "    return result[::-1]          # reverse to get forward itinerary\n\n"
        "# Heapq variant (O(log E) per pop instead of O(E)):\n"
        "def findItinerary_heap(tickets):\n"
        "    graph = defaultdict(list)\n"
        "    for src, dst in tickets:\n"
        "        heapq.heappush(graph[src], dst)\n"
        "    result = []\n"
        "    stack = ['JFK']\n"
        "    while stack:\n"
        "        while graph[stack[-1]]:\n"
        "            stack.append(heapq.heappop(graph[stack[-1]]))\n"
        "        result.append(stack.pop())\n"
        "    return result[::-1]"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("for src, dst in sorted(tickets)", {"code": True}), (" — Sort tickets upfront so each airport's destinations are appended in lexicographic order. This is the key to getting the smallest itinerary without extra comparison later.", {})])),
    N.para(N.rich([("graph[src].append(dst)", {"code": True}), (" — Build the adjacency list. Each entry in the list is one ticket (one directed edge).", {})])),
    N.para(N.rich([("stack = ['JFK']", {"code": True}), (" — Initialize the DFS stack with the mandatory start airport.", {})])),
    N.para(N.rich([("top = stack[-1]", {"code": True}), (" — Peek at the current airport without popping. We only pop when there are no more edges (post-order condition).", {})])),
    N.para(N.rich([("if graph[top]:", {"code": True}), (" — Check if the current airport has any unused outgoing edges.", {})])),
    N.para(N.rich([("stack.append(graph[top].pop(0))", {"code": True}), (" — Consume the smallest destination (pop from front of sorted list) and push it onto the DFS stack. The edge JFK→dest is now 'used'.", {})])),
    N.para(N.rich([("result.append(stack.pop())", {"code": True}), (" — POST-ORDER: when no edges remain, pop the current airport and add it to result. This is the Hierholzer key move.", {})])),
    N.para(N.rich([("return result[::-1]", {"code": True}), (" — Reverse the post-order result to get the correct forward itinerary: JFK first, final destination last.", {})])),
    N.divider(),
]

# ── Solution 2: Recursive DFS ──
blocks += [
    N.h2("Solution 2 — Hierholzer's Recursive (Cleaner Code)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same Eulerian path problem — but expressed recursively. The recursive version is often easier to read and reason about, though it risks hitting Python's recursion limit for very large inputs (10,000+ tickets)."),
        N.h4("What Doesn't Work"),
        N.para("A plain recursive DFS that appends the airport on entry (pre-order) fails on cycles — the same issue as the iterative version."),
        N.h4("The Key Observation"),
        N.para("The while loop inside dfs(airport) exhausts all outgoing edges before appending. This is the recursive equivalent of the iterative post-order pop. The recursion call stack mirrors the explicit stack in Solution 1."),
        N.h4("Building the Solution"),
        N.para("Use a deque for O(1) popleft(). Define dfs(airport): while graph[airport] has entries, pop the smallest destination and recurse into it. After the while loop (all edges exhausted), append airport to result. Call dfs('JFK'), then reverse."),
        N.callout("The recursive version is equivalent to Solution 1 — use whichever is clearer to explain. In interviews, the iterative version avoids potential stack overflow questions.", "💡", "green_background")
    ]),
    N.h3("Code"),
    N.code(
        "from collections import defaultdict, deque\n\n"
        "def findItinerary(tickets):\n"
        "    # Build adjacency with deque for O(1) popleft\n"
        "    graph = defaultdict(deque)\n"
        "    for src, dst in sorted(tickets):\n"
        "        graph[src].append(dst)\n"
        "    \n"
        "    result = []\n"
        "    \n"
        "    def dfs(airport):\n"
        "        # While there are outgoing edges, explore them first\n"
        "        while graph[airport]:\n"
        "            next_dest = graph[airport].popleft()  # smallest lex\n"
        "            dfs(next_dest)\n"
        "        # POST-ORDER: append only after all outgoing exhausted\n"
        "        result.append(airport)\n"
        "    \n"
        "    dfs('JFK')\n"
        "    return result[::-1]  # reverse to get forward order"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("graph = defaultdict(deque)", {"code": True}), (" — Using deque instead of list gives O(1) popleft() vs O(n) list.pop(0). Better performance for large inputs.", {})])),
    N.para(N.rich([("while graph[airport]:", {"code": True}), (" — Keep consuming edges from this airport as long as any remain. This loop ensures we exhaust all outgoing edges before post-order append.", {})])),
    N.para(N.rich([("dfs(next_dest)", {"code": True}), (" — Recurse into the next airport. Python's call stack mirrors the explicit stack in Solution 1.", {})])),
    N.para(N.rich([("result.append(airport)", {"code": True}), (" — POST-ORDER: this line executes only after the while loop finishes — i.e., after all outgoing edges from this airport are consumed.", {})])),
    N.divider(),
]

# ── Complexity Table ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute-force Backtracking", "O(E!)", "O(E)"],
        ["Hierholzer's Iterative (list.pop(0))", "O(E² + E log E)", "O(E)"],
        ["Hierholzer's Iterative (heapq)", "O(E log E)", "O(E)"],
        ["Hierholzer's Recursive (deque)", "O(E log E)", "O(E)"],
    ]),
    N.para(N.rich([
        ("E = number of tickets (edges). Sorting dominates at O(E log E). Each edge is visited exactly once in Hierholzer's — the DFS is O(E). Space is O(E) for the graph, result array, and stack/recursion depth.", {})
    ])),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Graph", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Hierholzer's Algorithm (Eulerian Path)", {})])),
    N.callout(
        "When to recognize this pattern:\n"
        "• 'Use every edge exactly once' — Eulerian path\n"
        "• Reconstruct a sequence from directed pairs — post-order DFS\n"
        "• 'Lexicographically smallest' + graph — sort adjacency lists first\n"
        "• Dead-end nodes must appear last — post-order guarantees this\n"
        "• Airline itineraries, DNA sequence reconstruction, Chinese Postman Problem",
        "🔎", "green_background"
    ),
    N.para(N.rich([
        ("Note: Hierholzer's Algorithm is classified here as a graph sub-pattern based on analysis. It is a specific named algorithm for Eulerian paths, related to but distinct from generic DFS/BFS sub-patterns in the pattern guide.", {"italic": True})
    ])),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Hierholzer's / Eulerian Path / Post-Order Graph DFS):"),
    N.bullet(N.rich([("Valid Arrangement of Pairs", {"bold": True}), (" (Hard, #2097) — Direct Eulerian path on [predecessor, successor] pairs; find start node first, then same Hierholzer's DFS.", {})])),
    N.bullet(N.rich([("Cracking the Safe", {"bold": True}), (" (Hard, #753) — Find shortest string containing all k-length combinations; models as Eulerian circuit on de Bruijn graph.", {})])),
    N.bullet(N.rich([("Course Schedule II", {"bold": True}), (" (Medium, #210) — Topological sort via post-order DFS on DAG; same post-order + reversal insight, no cycles allowed.", {})])),
    N.bullet(N.rich([("All Paths From Source to Target", {"bold": True}), (" (Medium, #797) — DFS to enumerate all paths in DAG; simpler since no cycles and no Eulerian requirement.", {})])),
    N.bullet(N.rich([("Network Delay Time", {"bold": True}), (" (Medium, #743) — Shortest path in directed weighted graph using Dijkstra's; same graph modeling skills.", {})])),
    N.bullet(N.rich([("Minimum Height Trees", {"bold": True}), (" (Medium, #310) — Iterative leaf-peeling on undirected graph; uses post-order thinking to identify roots.", {})])),
    N.para("These problems share the core insight: directed graph traversal where edge consumption order matters and post-order processing is needed."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Graph section. Hierholzer's is classified as Analysis (problem-specific algorithm not explicitly listed in guide tables).", "📚", "gray_background"),
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed("https://jayitsaha.github.io/Algorithms/reconstruct_itinerary_explainer.html"),
    N.para(N.rich([
        ("Step through Hierholzer's algorithm visually — watch the DFS stack, post-order pops, and final reversal. Use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ]))
]

# ── Append all blocks ──
print(f"Appending {len(blocks)} blocks to Notion...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
