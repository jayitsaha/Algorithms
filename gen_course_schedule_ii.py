"""
gen_course_schedule_ii.py — Notion update for Course Schedule II (LC #210)
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notion_lib as N

PAGE_ID = "39193418-809c-8175-b4fe-da1011603ded"

# ── 1. Set properties ──────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=210,
    pattern="Graph",
    subpatterns=["Topological Sort", "Kahn's BFS"],
    tc="O(V+E)",
    sc="O(V+E)",
    key_insight="Use Kahn's BFS: peel nodes with indegree 0; cycle = not all scheduled.",
    icon="🟡"
)
print("Properties set.")

# ── 2. Wipe old body ───────────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3. Build new body ──────────────────────────────────────────────────────────
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("There are ", {}),
        ("numCourses", {"code": True}),
        (" courses labeled ", {}),
        ("0", {"code": True}),
        (" to ", {}),
        ("numCourses - 1", {"code": True}),
        (". You are given an array ", {}),
        ("prerequisites", {"code": True}),
        (" where ", {}),
        ("prerequisites[i] = [aᵢ, bᵢ]", {"code": True}),
        (" indicates that you must take course ", {}),
        ("bᵢ", {"code": True}),
        (" first if you want to take course ", {}),
        ("aᵢ", {"code": True}),
        (". Return the ordering of courses you should take to finish all courses. If there are many valid answers, return any of them. If it is impossible to finish all courses, return an empty array.", {}),
    ])),
    N.divider(),
]

# ── Solution 1: Kahn's BFS ──
KAHNS_CODE = """\
from collections import deque

def findOrder(numCourses: int, prerequisites: list) -> list:
    graph = [[] for _ in range(numCourses)]   # graph[b] = courses b unlocks
    indegree = [0] * numCourses               # remaining prereqs per course
    for a, b in prerequisites:
        graph[b].append(a)                    # edge b→a: b unlocks a
        indegree[a] += 1                      # a has one more prereq

    # Seed queue with all courses that have no prerequisites
    queue = deque(i for i in range(numCourses) if indegree[i] == 0)
    order = []

    while queue:
        course = queue.popleft()
        order.append(course)                  # "complete" this course
        for neighbor in graph[course]:
            indegree[neighbor] -= 1           # one fewer prereq remaining
            if indegree[neighbor] == 0:
                queue.append(neighbor)        # now available!

    # If all courses scheduled, no cycle exists
    return order if len(order) == numCourses else []
"""

blocks += [
    N.h2("Solution 1 — Kahn's BFS Topological Sort (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Model courses as nodes and prerequisites as directed edges. Pair [a,b] means b must come before a → edge b→a ('b unlocks a'). The question becomes: find a topological order of this directed graph, or report that one doesn't exist (because of a cycle)."),
        N.h4("What Doesn't Work"),
        N.para("Brute force: try every permutation of numCourses and validate each — O(V! × E). With even 10 courses, 10! = 3.6 million permutations, each requiring E checks. Completely infeasible. We need a smarter structure."),
        N.h4("The Key Observation"),
        N.para("A course can be taken as soon as all its prerequisites are done. Track this with in-degrees: a course's in-degree is the count of prerequisites it still needs. When that hits 0, the course is available. This gives us a natural BFS ordering."),
        N.h4("Building the Solution"),
        N.para("1) Compute in-degrees while building the graph. 2) Seed a queue with all in-degree-0 courses — they can start immediately. 3) BFS: dequeue a course, append to result, decrement its neighbors' in-degrees, enqueue those that hit 0. 4) If result.length == numCourses, return it. Otherwise a cycle blocked some nodes."),
        N.callout("Analogy: University registration. You can enroll in a course the moment all its prerequisites are cleared. Kahn's is exactly this: a queue of 'courses you can take right now,' refreshed as you complete each one.", "🎓", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(KAHNS_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("graph = [[] for _ in range(numCourses)]", {"code": True}), (" — Adjacency list where graph[b] holds the list of courses that course b unlocks (b→a edges).", {})])),
    N.para(N.rich([("indegree = [0] * numCourses", {"code": True}), (" — For each course, count how many prerequisites it still needs. Starts at 0 for all; incremented per prerequisite pair.", {})])),
    N.para(N.rich([("for a, b in prerequisites: graph[b].append(a); indegree[a] += 1", {"code": True}), (" — Build the graph and compute in-degrees in one pass. Edge direction is b→a (b unlocks a, NOT a unlocks b — this is a common bug).", {})])),
    N.para(N.rich([("queue = deque(i for i in range(numCourses) if indegree[i] == 0)", {"code": True}), (" — Seed the queue with every course that has zero prerequisites. These are immediately available. If none exist and prerequisites is non-empty, a cycle is already present.", {})])),
    N.para(N.rich([("course = queue.popleft()", {"code": True}), (" — Take the next available course (FIFO). Any order within the queue is valid — any topological ordering works.", {})])),
    N.para(N.rich([("order.append(course)", {"code": True}), (" — Mark this course as 'completed.' Everything after this is about unlocking dependents.", {})])),
    N.para(N.rich([("indegree[neighbor] -= 1", {"code": True}), (" — Consuming this course removes one prerequisite from each course that depended on it.", {})])),
    N.para(N.rich([("if indegree[neighbor] == 0: queue.append(neighbor)", {"code": True}), (" — When the last prerequisite is cleared, the neighbor becomes available immediately.", {})])),
    N.para(N.rich([("return order if len(order) == numCourses else []", {"code": True}), (" — The single cycle-detection check. If a cycle exists, at least one course is stuck with in-degree > 0 forever, so it never enters the result.", {})])),
    N.divider(),
]

# ── Solution 2: DFS 3-Color ──
DFS_CODE = """\
def findOrder(numCourses: int, prerequisites: list) -> list:
    graph = [[] for _ in range(numCourses)]
    for a, b in prerequisites:
        graph[b].append(a)          # same direction: b→a

    WHITE, GRAY, BLACK = 0, 1, 2   # unvisited, in-stack, done
    color = [WHITE] * numCourses
    result = []

    def dfs(node) -> bool:
        if color[node] == GRAY:     # back-edge to ancestor → cycle!
            return False
        if color[node] == BLACK:    # already fully explored → skip
            return True
        color[node] = GRAY          # mark as "in current DFS path"
        for neighbor in graph[node]:
            if not dfs(neighbor):
                return False
        color[node] = BLACK         # fully done; all descendants OK
        result.append(node)         # post-order: add AFTER all dependencies
        return True

    for i in range(numCourses):
        if not dfs(i):
            return []

    return result[::-1]             # reverse post-order = topological order
"""

blocks += [
    N.h2("Solution 2 — DFS with 3-Color Marking"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same graph model. Instead of tracking in-degrees, we DFS through the graph. The key observation: if during a DFS we encounter a node that is already in our current path (GRAY), we've found a cycle. If we reach a node that's fully explored (BLACK), we can skip it."),
        N.h4("What Doesn't Work"),
        N.para("A simple visited/unvisited boolean can't detect cycles in directed graphs — it conflates 'visited in this DFS path' with 'visited ever.' We need three states: WHITE (not yet seen), GRAY (currently in the DFS stack / call chain), BLACK (fully processed)."),
        N.h4("The Key Observation"),
        N.para("Post-order DFS appends a node AFTER all its dependencies are processed. Reverse that post-order sequence to get topological order. A GRAY node encountered during DFS means we've looped back — a cycle."),
        N.h4("Building the Solution"),
        N.para("Color all nodes WHITE. For each unvisited node, run DFS. Set to GRAY on entry, BLACK on exit. Append to result on BLACK. At the end, reverse result for the topological order."),
        N.callout("Analogy: Detecting deadlock in a dependency graph. GRAY = 'currently being resolved.' If you need something GRAY, you need something that needs you — deadlock (cycle).", "🔄", "red_background"),
    ]),
    N.h3("Code"),
    N.code(DFS_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("WHITE, GRAY, BLACK = 0, 1, 2", {"code": True}), (" — Three-state coloring: unvisited, currently in recursion stack, fully explored.", {})])),
    N.para(N.rich([("if color[node] == GRAY: return False", {"code": True}), (" — We're revisiting a node in the current DFS path — this is a back-edge, which means a cycle. Return False immediately.", {})])),
    N.para(N.rich([("if color[node] == BLACK: return True", {"code": True}), (" — Already fully explored this node in a previous DFS call. All its dependencies are safe. Skip.", {})])),
    N.para(N.rich([("color[node] = GRAY", {"code": True}), (" — Mark as in-progress. If we encounter this node again before marking it BLACK, we've found a cycle.", {})])),
    N.para(N.rich([("color[node] = BLACK; result.append(node)", {"code": True}), (" — Fully done. All reachable descendants are safe. Append in post-order — this node's dependencies all came before it in the result list.", {})])),
    N.para(N.rich([("return result[::-1]", {"code": True}), (" — Post-order DFS appends a node after all its dependencies. Reversing gives the correct order (dependencies first).", {})])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (all permutations)", "O(V! × E)", "O(V)"],
        ["Kahn's BFS (Interview Pick) ✓", "O(V+E)", "O(V+E)"],
        ["DFS 3-Color", "O(V+E)", "O(V+E) + O(V) stack"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Graph — directed graph with topological ordering requirement.", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Topological Sort (Kahn's BFS) — in-degree based BFS peeling; DFS post-order reversal as alternative.", {})])),
    N.callout(
        "When to recognize this pattern: 'Must do X before Y.' 'Is this schedule possible?' 'Return an ordering of tasks/courses/modules with dependencies.' 'Detect circular dependency.' Any time you see directed edges between tasks and need ordering or feasibility.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Topological Sort technique:"),
    N.bullet(N.rich([("Course Schedule I", {"bold": True}), (" (Medium) — Same Kahn's BFS, return boolean instead of ordering.", {})])),
    N.bullet(N.rich([("Alien Dictionary", {"bold": True}), (" (Hard) — Build character order graph from word comparisons, then topo sort.", {})])),
    N.bullet(N.rich([("Minimum Height Trees", {"bold": True}), (" (Medium) — Peel leaf nodes iteratively; same BFS in-degree peeling principle.", {})])),
    N.bullet(N.rich([("Parallel Courses", {"bold": True}), (" (Medium) — Kahn's BFS + track BFS level depth = minimum semesters.", {})])),
    N.bullet(N.rich([("All Ancestors of a Node in a DAG", {"bold": True}), (" (Medium) — Topo sort then propagate ancestor sets forward.", {})])),
    N.bullet(N.rich([("Find All Possible Recipes from Given Supplies", {"bold": True}), (" (Medium) — Kahn's BFS with supplies as initial in-degree-0 sources.", {})])),
    N.bullet(N.rich([("Longest Increasing Path in a Matrix", {"bold": True}), (" (Hard) — DFS + memo on an implicit DAG formed by increasing values.", {})])),
    N.para("These problems share the same core technique: model dependencies as directed edges, then use Kahn's BFS or DFS post-order to find a valid ordering or detect infeasibility."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section: Graph → Topological Sort.", "📚", "gray_background"),
]

# ── Interactive Visual Explainer ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("course_schedule_ii")),
    N.para(N.rich([("Step through Kahn's BFS topological sort visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

# ── Append all blocks ──
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
