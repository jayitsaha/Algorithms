import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-8134-bb8b-f8f9c0c733d6"

print("Step 1: Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=269,
    pattern="Graph",
    subpatterns=["Build Graph + Topo Sort"],
    tc="O(C)",
    sc="O(U)",
    key_insight="Compare adjacent sorted words to extract char ordering edges, then topologically sort the directed graph (Kahn's BFS); cycle = invalid.",
    icon="\U0001f534"
)
print("Properties set.")

print("Step 2: Wiping old content...")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

print("Step 3: Building new content...")
blocks = []

# ── Problem ──────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para("There is a new alien language that uses the English alphabet. The words are sorted lexicographically by the rules of this new language. Return a string of the unique letters sorted in the alien language's order. If there is no solution (cycle), return \"\". If multiple solutions exist, return any."),
    N.para("Example: words = [\"wrt\",\"wrf\",\"er\",\"ett\",\"rftt\"] → Output: \"wertf\" (one valid ordering)"),
    N.divider(),
]

# ── Solution 1: BFS Topo Sort ────────────────────────────
blocks += [
    N.h2("Solution 1 — BFS Topological Sort / Kahn's Algorithm (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("You have sorted words but don't know the alphabet order. Think of it as a constraint problem: each adjacent word pair tells you one ordering constraint — 'character A comes before character B'. Once you collect all constraints, find an ordering of all characters that satisfies them. That is exactly topological sort on a directed graph."),
        N.h4("What Doesn't Work"),
        N.para("Trying all permutations of the alphabet: if there are U unique characters, that is U! orderings to try, each taking O(C) to verify — completely impractical. You need to derive the order directly from the constraints."),
        N.h4("The Key Observation"),
        N.para("In a sorted list, when two adjacent words first differ at position i, the character in the earlier word MUST precede the character in the later word in the alien alphabet. This gives exactly one directed edge per adjacent pair. Collect all edges, then topological sort. Cycle = invalid input."),
        N.h4("Building the Solution"),
        N.para("1) Initialize every character as a graph node (indegree 0, empty adjacency set). 2) For each adjacent pair, zip and find first mismatch — add directed edge c1->c2, increment indegree[c2]. Use sets to deduplicate edges. 3) Seed BFS queue with zero-indegree nodes. 4) Kahn's BFS: dequeue, append to result, decrement neighbors' indegrees, enqueue newly-zero nodes. 5) If result length < unique chars: cycle detected, return ''."),
        N.callout("Analogy: Like resolving task dependencies. Each 'A must come before B' is a prerequisite edge. Kahn's BFS processes tasks whose prerequisites are all done. Circular dependency = unsolvable.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code('''from collections import deque

def alienOrder(words):
    # Initialize every character seen in any word
    adj = {c: set() for w in words for c in w}
    indegree = {c: 0 for c in adj}

    # Extract ordering constraints from adjacent word pairs
    for i in range(len(words) - 1):
        w1, w2 = words[i], words[i + 1]
        min_len = min(len(w1), len(w2))
        # Prefix conflict: longer word before its shorter prefix is impossible
        if len(w1) > len(w2) and w1[:min_len] == w2:
            return ""
        for c1, c2 in zip(w1, w2):
            if c1 != c2:
                if c2 not in adj[c1]:  # Dedup: avoid double-counting indegree
                    adj[c1].add(c2)
                    indegree[c2] += 1
                break  # Only first mismatch tells us anything

    # Kahn\'s BFS Topological Sort
    queue = deque([c for c in indegree if indegree[c] == 0])
    result = []
    while queue:
        c = queue.popleft()
        result.append(c)
        for neighbor in adj[c]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)

    # Cycle check: if output shorter than unique chars, cycle exists
    if len(result) != len(adj):
        return ""
    return "".join(result)'''),
    N.h3("Line by Line"),
    N.para("adj = {c: set() ...} — Initialize every character seen in any word as a graph node with an empty adjacency set (set prevents duplicate edges)."),
    N.para("indegree = {c: 0 for c in adj} — Every character starts with 0 prerequisites."),
    N.para("for i in range(len(words)-1) — Compare each adjacent word pair (consecutive in sorted order)."),
    N.para("if len(w1) > len(w2) and w1[:min_len]==w2: return \"\" — Prefix conflict: longer word appearing before its shorter prefix is impossible."),
    N.para("for c1, c2 in zip(w1, w2): if c1 != c2: — Scan positions until first mismatch — that gives the ordering constraint."),
    N.para("if c2 not in adj[c1]: — Deduplicate: multiple word pairs might imply the same edge; without dedup, indegree gets double-counted."),
    N.para("adj[c1].add(c2); indegree[c2]+=1; break — Add edge c1->c2, increment c2's prerequisite count, STOP (only first diff matters)."),
    N.para("queue = deque([c for c in indegree if indegree[c]==0]) — Seed BFS with chars that have no prerequisites — they can appear first."),
    N.para("c = queue.popleft(); result.append(c) — Dequeue: this char's all prereqs are done. Safe to place in the alien alphabet."),
    N.para("indegree[neighbor]-=1; if indegree[neighbor]==0: queue.append(neighbor) — Unlock neighbors. If all prereqs met (indegree hits 0), enqueue."),
    N.para("if len(result) != len(adj): return \"\" — Cyclic nodes never reached indegree 0, never got enqueued, never appeared in result."),
    N.divider(),
]

# ── Solution 2: DFS ──────────────────────────────────────
blocks += [
    N.h2("Solution 2 — DFS Topological Sort"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same graph, different traversal strategy. DFS explores as deep as possible before backtracking. Post-order DFS (append AFTER visiting all descendants) naturally produces reverse topological order. Reverse at the end to get correct topo order."),
        N.h4("What Doesn't Work"),
        N.para("A simple 'visited' boolean set won't detect cycles — you need three states: unvisited, currently-on-path (in recursion stack), and fully-done. A 'currently-on-path' node visited again means a back edge = cycle."),
        N.h4("The Key Observation"),
        N.para("In DFS, a node is appended AFTER all its dependencies are processed (post-order). Reversing gives topological order. A node encountered while still on the current DFS path means we found a cycle."),
        N.h4("Building the Solution"),
        N.para("Use visited dict: True = currently on DFS path (cycle if revisited), False = fully done. For each character: if not visited, run DFS. If DFS returns True (cycle found), propagate. Post-order append to result, then reverse at the end."),
        N.callout("Mnemonic: DFS is like exploring a maze — if you loop back to a room still on your trail, you are in a cycle. The 'on-current-path' flag is your breadcrumb trail.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code('''def alienOrder_dfs(words):
    adj = {c: set() for w in words for c in w}
    # ... (same edge-building logic as BFS approach) ...

    visited = {}  # True = on current path (cycle), False = fully done
    result = []

    def dfs(c):
        if c in visited:
            return visited[c]  # True = cycle; False = already fully processed
        visited[c] = True      # Mark as on current DFS path
        for neighbor in adj[c]:
            if dfs(neighbor):  # Recurse; propagate cycle detection
                return True
        visited[c] = False     # Done with this node
        result.append(c)       # Post-order: append AFTER all descendants done
        return False

    for c in adj:
        if c not in visited:
            if dfs(c):
                return ""  # Cycle found
    return "".join(reversed(result))  # Reverse post-order = topological order'''),
    N.h3("Line by Line"),
    N.para("visited = {} — Maps char to True (on current path) or False (fully done). Absence means not yet visited."),
    N.para("if c in visited: return visited[c] — If True (on path) -> cycle detected. If False (done) -> skip, already processed."),
    N.para("visited[c] = True — Mark current node as part of the active DFS path (breadcrumb)."),
    N.para("visited[c] = False; result.append(c) — Done with this subtree. Post-order append: all descendants already in result."),
    N.para("return ''.join(reversed(result)) — Post-order gives reverse topo order. Reverse to get correct topological order."),
    N.divider(),
]

# ── Complexity ───────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["BFS Kahn's (Interview Pick)", "O(C)", "O(U)"],
        ["DFS Topological Sort", "O(C)", "O(U)"],
        ["Brute Force (all permutations)", "O(U! x C)", "O(U!)"],
    ]),
    N.para("C = total characters across all words (input size). U = number of unique characters (at most 26 for English alphabet). Edge count is at most U-1 since each adjacent pair contributes at most 1 edge, and a DAG on U nodes has at most U-1 edges."),
    N.divider(),
]

# ── Pattern Classification ────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Graph"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Build Graph + Topo Sort (Kahn's BFS)"])),
    N.callout(
        "When to recognize this pattern: 'derive an ordering/ranking' + 'validity check' + constraints given implicitly (sorted list, prerequisites, sequences) → build directed graph, topological sort, cycle = invalid.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Build Graph + Topological Sort technique:"),
    N.bullet(N.rich([("Course Schedule", {"bold": True}), " (Medium) — Can you finish all courses? Identical graph + cycle detection. #207"])),
    N.bullet(N.rich([("Course Schedule II", {"bold": True}), " (Medium) — Return the topological ordering of courses, [] if cycle. #210"])),
    N.bullet(N.rich([("Sequence Reconstruction", {"bold": True}), " (Medium) — Unique shortest supersequence check via topo sort. #444"])),
    N.bullet(N.rich([("Minimum Height Trees", {"bold": True}), " (Medium) — Iterative leaf-pruning is topological sort from outside in. #310"])),
    N.bullet(N.rich([("Sort Items by Groups Respecting Dependencies", {"bold": True}), " (Hard) — Two-level topo sort on groups and items. #1203"])),
    N.bullet(N.rich([("Find All Possible Recipes from Given Supplies", {"bold": True}), " (Medium) — Ingredients as prerequisites for recipes. #2115"])),
    N.para("These problems share the same core structure: model constraints as directed edges, extract topological ordering, detect cycles via Kahn's or DFS."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 6 (Graph → Topological Sort). Sub-Pattern verified: Build Graph + Topo Sort.", "📚", "gray_background"),
    N.divider(),
]

# ── Embed ─────────────────────────────────────────────────
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("alien_dictionary")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

print(f"Total blocks to append: {len(blocks)}")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
