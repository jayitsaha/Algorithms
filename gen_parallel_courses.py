"""
gen_parallel_courses.py — Notion page rebuild for Parallel Courses (LC #1136)
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-818c-a217-ecf0978ae0f7"

# ── 1) Set properties ──────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=1136,
    pattern="Graph",
    subpatterns=["BFS Level by Level", "Topological Sort"],
    tc="O(V+E)",
    sc="O(V+E)",
    key_insight="Kahn's BFS: each BFS level = one semester; indegree-0 nodes are ready to take; taken<n detects cycles.",
    icon="🟡"
)
print("Properties set.")

# ── 2) Wipe old body ───────────────────────────────────────────────
print("Wiping old blocks...")
deleted = N.wipe_page(PAGE_ID)
print(f"Deleted {deleted} blocks.")

# ── 3) Build new body ─────────────────────────────────────────────
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given an integer ", {}),
        ("n", {"code": True}),
        (" representing the number of courses (labeled 1 to n) and a list ", {}),
        ("relations", {"code": True}),
        (" where ", {}),
        ("relations[i] = [prevCourse, nextCourse]", {"code": True}),
        (" indicates that ", {}),
        ("prevCourse", {"code": True}),
        (" must be completed before ", {}),
        ("nextCourse", {"code": True}),
        (", find the minimum number of semesters to complete all n courses. In each semester you may take any number of courses simultaneously, provided all their prerequisites have been completed. Return ", {}),
        ("-1", {"code": True}),
        (" if it is impossible (i.e., a cycle exists).", {}),
    ])),
    N.divider(),
]

# ── Solution 1: BFS Kahn's Algorithm ──
blocks += [
    N.h2("Solution 1 — BFS Kahn's Algorithm (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We have courses that form a dependency graph: some courses can only be taken after others. We want to complete all of them as quickly as possible, taking as many as possible in parallel each semester. The question becomes: what is the minimum number of 'waves' to process all nodes in a DAG?"),
        N.h4("What Doesn't Work"),
        N.para("A naive brute-force approach of trying all possible orderings would be O(n!) — completely impractical for large n. Even trying all subsets of available courses each semester is exponential. We need a smarter approach that builds the solution incrementally."),
        N.h4("The Key Observation"),
        N.para("Courses with no prerequisites can all be taken in the SAME semester. After completing them, new courses become available — those whose only remaining prerequisites have just been satisfied. This 'unlocking' structure is exactly what BFS captures: each BFS level (wave) corresponds to one semester."),
        N.h4("Building the Solution"),
        N.para("Track 'in-degree' — the count of unsatisfied prerequisites for each course. Seed a queue with all in-degree 0 courses (semester 1 candidates). Process the entire queue (one semester), then for each completed course, reduce in-degrees of dependent courses. Any that hit 0 join the next semester. Count levels. If after BFS we haven't taken all n courses, a cycle prevented some from ever reaching in-degree 0 — return -1."),
        N.callout("Analogy: Think of a college curriculum where you take every course you're eligible for each semester. This greedy 'take all available now' strategy is provably optimal: waiting never helps.", "🎓", "blue_background"),
    ]),
    N.h3("Code"),
    N.code("""from collections import deque

def minNumberOfSemesters(n: int, relations: list[list[int]]) -> int:
    indegree = [0] * (n + 1)
    graph = [[] for _ in range(n + 1)]

    for prev, nxt in relations:
        graph[prev].append(nxt)
        indegree[nxt] += 1

    queue = deque(c for c in range(1, n + 1) if indegree[c] == 0)
    semesters, taken = 0, 0

    while queue:
        semesters += 1
        for _ in range(len(queue)):   # process exactly this level
            course = queue.popleft()
            taken += 1
            for nxt in graph[course]:
                indegree[nxt] -= 1
                if indegree[nxt] == 0:
                    queue.append(nxt)

    return semesters if taken == n else -1"""),
    N.h3("Line by Line"),
    N.para(N.rich([("indegree = [0] * (n + 1)", {"code": True}), (" — Array tracking how many unmet prerequisites each course has. Index 0 is unused (courses are 1-indexed).", {})])),
    N.para(N.rich([("graph = [[] for _ in range(n + 1)]", {"code": True}), (" — Adjacency list: graph[u] contains all courses that require course u as a prerequisite.", {})])),
    N.para(N.rich([("for prev, nxt in relations:", {"code": True}), (" — For each dependency: record the edge and increment the in-degree of the dependent course.", {})])),
    N.para(N.rich([("queue = deque(c for c in range(1, n+1) if indegree[c] == 0)", {"code": True}), (" — Seed queue with all courses that have no prerequisites — the semester-1 candidates.", {})])),
    N.para(N.rich([("while queue:", {"code": True}), (" — Each outer iteration of this loop represents one complete semester.", {})])),
    N.para(N.rich([("semesters += 1", {"code": True}), (" — We're starting a new semester; increment the count before processing.", {})])),
    N.para(N.rich([("for _ in range(len(queue)):", {"code": True}), (" — CRITICAL: snapshot the queue size to process EXACTLY this level's courses. Without this, newly added courses from the current semester bleed into the same semester count.", {})])),
    N.para(N.rich([("course = queue.popleft(); taken += 1", {"code": True}), (" — Take the course, increment the running total for cycle detection.", {})])),
    N.para(N.rich([("indegree[nxt] -= 1", {"code": True}), (" — Remove this course from nxt's unmet-prerequisites count.", {})])),
    N.para(N.rich([("if indegree[nxt] == 0: queue.append(nxt)", {"code": True}), (" — If all prerequisites are now met, the course is ready for the next semester.", {})])),
    N.para(N.rich([("return semesters if taken == n else -1", {"code": True}), (" — If taken < n, some courses are stuck in a cycle and were never dequeued.", {})])),
    N.divider(),
]

# ── Solution 2: DFS Longest Path ──
blocks += [
    N.h2("Solution 2 — DFS Longest Path"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The minimum number of semesters is the length of the longest dependency chain. If we can compute depth[c] = the earliest semester course c can be taken, the answer is max(depth[1..n])."),
        N.h4("What Doesn't Work"),
        N.para("Simple iterative computation doesn't work because in a general DAG, computing depth[c] requires knowing depth[all predecessors] first — which is a recursive dependency."),
        N.h4("The Key Observation"),
        N.para("DFS with memoization can compute the longest incoming path to each node. depth[c] = 1 + max(depth[pred] for all predecessors of c). A cycle is detected when we revisit a node that is currently in the recursion stack."),
        N.h4("Building the Solution"),
        N.para("Run DFS from each node. Use a visited array with states: 0=unvisited, 1=in-stack (cycle if revisited), 2=fully computed. If we hit state 1 during DFS, a cycle exists — return infinity. Otherwise, depth[u] = 1 + max(DFS(v) for v in graph[u]). The answer is max over all depth[u]."),
        N.callout("Note: BFS (Solution 1) is cleaner and more natural for this problem. Use DFS longest-path when you need to know the exact depth of each node for other purposes.", "💡", "gray_background"),
    ]),
    N.h3("Code"),
    N.code("""def minNumberOfSemesters_dfs(n: int, relations: list[list[int]]) -> int:
    graph = [[] for _ in range(n + 1)]
    for prev, nxt in relations:
        graph[prev].append(nxt)

    depth = [0] * (n + 1)
    visited = [0] * (n + 1)  # 0=unvisited, 1=in-stack, 2=done

    def dfs(u):
        if visited[u] == 1:
            return float('inf')  # cycle detected
        if visited[u] == 2:
            return depth[u]
        visited[u] = 1
        depth[u] = 1 + max((dfs(v) for v in graph[u]), default=0)
        visited[u] = 2
        return depth[u]

    result = max(dfs(c) for c in range(1, n + 1))
    return -1 if result == float('inf') else result"""),
    N.h3("Line by Line"),
    N.para(N.rich([("visited[u] == 1", {"code": True}), (" — Node is currently on the DFS call stack. Encountering it again means we've found a cycle.", {})])),
    N.para(N.rich([("depth[u] = 1 + max(dfs(v) for v in graph[u])", {"code": True}), (" — The earliest semester for u is one more than the latest predecessor's semester. The max gives the critical (longest) path.", {})])),
    N.para(N.rich([("result = max(dfs(c) for c in range(1, n+1))", {"code": True}), (" — We need the maximum over all courses — this is the bottleneck determining total semesters needed.", {})])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["BFS Kahn's Algorithm (Interview Pick)", "O(V+E)", "O(V+E)"],
        ["DFS Longest Path", "O(V+E)", "O(V+E)"],
        ["Brute Force (enumerate orderings)", "O(n!)", "O(n)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Graph (specifically: Directed Acyclic Graph processing)", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("BFS Level by Level (Kahn's Algorithm), Topological Sort", {})])),
    N.callout(
        "When to recognize this pattern: 'Must complete X before Y', 'minimum rounds/waves/semesters', 'dependency ordering', 'parallel processing of tasks'. If the answer is the minimum number of stages and items can be processed in parallel per stage — it's BFS topo sort.",
        "🔎", "green_background"
    ),
    N.para(N.rich([("Source: ", {"bold": True}), ("DSA Patterns Guide Section 17.3 — Topological Sort: 'Parallel Courses | Medium | BFS Level by Level'", {})])),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same BFS Topological Sort (Kahn's) technique:"),
    N.bullet(N.rich([("Course Schedule", {"bold": True}), (" (Medium) — Cycle detection only using Kahn's; same setup, just return taken == n as bool", {})])),
    N.bullet(N.rich([("Course Schedule II", {"bold": True}), (" (Medium) — Return actual topological ordering (record dequeue order in Kahn's)", {})])),
    N.bullet(N.rich([("Minimum Height Trees", {"bold": True}), (" (Medium) — Iteratively remove degree-1 leaves; same 'peel outer layer' BFS pattern", {})])),
    N.bullet(N.rich([("Find All Possible Recipes from Given Supplies", {"bold": True}), (" (Medium) — Kahn's with an initial set of 'available' nodes as seeds", {})])),
    N.bullet(N.rich([("Alien Dictionary", {"bold": True}), (" (Hard) — Build character-ordering DAG from word comparisons, then Kahn's BFS", {})])),
    N.bullet(N.rich([("Parallel Courses III", {"bold": True}), (" (Hard) — Same structure but courses have durations; BFS tracks cumulative completion time", {})])),
    N.bullet(N.rich([("Sequence Reconstruction", {"bold": True}), (" (Medium) — Verify unique topo ordering: Kahn's queue must always have size exactly 1", {})])),
    N.para("These problems all share the same core technique: build adjacency list + in-degree array, BFS with level tracking, check total processed for cycle detection."),
    N.callout("Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 17.3 — Topological Sort", "📚", "gray_background"),
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed("https://jayitsaha.github.io/Algorithms/parallel_courses_explainer.html"),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

# ── Append all blocks ──────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks to Notion...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
