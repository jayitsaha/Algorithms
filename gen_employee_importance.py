"""
Notion update script for Employee Importance (LC #690).
Run from: /Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms/
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-8168-a96b-e43775da7b0d"
SLUG = "employee_importance"

# ── 1) Set properties ──────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=690,
    pattern="Graph",
    subpatterns=["DFS Sum Values"],
    tc="O(n)",
    sc="O(n)",
    key_insight="Build a HashMap id→Employee for O(1) lookup, then DFS from target to sum importance of all reachable nodes.",
    icon="🟡"
)
print("Properties set.")

# ── 2) Wipe existing body ───────────────────────────────────────────────────
print("Wiping existing page body...")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3) Build new body ───────────────────────────────────────────────────────

PROBLEM_STATEMENT = (
    "You have a list of employees where each employee has an id (integer), "
    "an importance value (integer), and a list of direct subordinate ids. "
    "Given the list of employees and an integer id, return the total importance "
    "value of the employee with the given id and all their direct and indirect subordinates."
)

SOL1_CODE = """\
def getImportance(employees, id):
    # Build a hash map for O(1) lookup by employee id
    emp_map = {e.id: e for e in employees}

    def dfs(eid):
        emp = emp_map[eid]            # O(1) lookup
        total = emp.importance        # Count this employee's importance
        for sub_id in emp.subordinates:
            total += dfs(sub_id)      # Recursively sum subordinate subtrees
        return total

    return dfs(id)  # Launch DFS from the target employee
"""

SOL2_CODE = """\
from collections import deque

def getImportance(employees, id):
    emp_map = {e.id: e for e in employees}
    total, queue = 0, deque([id])

    while queue:
        eid = queue.popleft()         # popleft() is O(1) with deque
        emp = emp_map[eid]
        total += emp.importance
        queue.extend(emp.subordinates)  # Enqueue all direct subordinates

    return total
"""

SOL3_CODE = """\
def getImportance(employees, id):
    # Brute force: O(n) linear scan each lookup → O(n^2) total
    def find(eid):
        for e in employees:
            if e.id == eid: return e

    def dfs(eid):
        emp = find(eid)  # O(n) per call — the bottleneck
        return emp.importance + sum(dfs(s) for s in emp.subordinates)

    return dfs(id)
"""

blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(PROBLEM_STATEMENT),
    N.divider()
]

# ── Solution 1: DFS + HashMap ──
blocks += [
    N.h2("Solution 1 — DFS + HashMap (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "We need to sum importance values of an employee plus all employees "
            "reachable through subordinate links — in other words, everyone in their "
            "subtree. This is a 'visit all descendants and accumulate' problem on a tree."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Naively, when we encounter a subordinate id we could search the employees "
            "list to find that employee — but this is O(n) per lookup. With n employees "
            "in the subtree, we'd do O(n) lookups each taking O(n) time: O(n²) total. "
            "For n = 100,000 employees that's 10 billion operations — unusably slow."
        ),
        N.h4("The Key Observation"),
        N.para(
            "The data is given as a list but we need lookup by id. Preprocess once into "
            "a hash map (id → Employee) in O(n). Then every subordinate lookup during "
            "the traversal costs O(1). The total traversal becomes O(n)."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. Build emp_map = {e.id: e for e in employees}. "
            "2. Define dfs(eid): look up the employee, add their importance to a local total, "
            "then recursively call dfs for each subordinate id and add those subtotals. "
            "3. Return dfs(target_id). "
            "Because the structure is a tree (no cycles), each employee is visited exactly once."
        ),
        N.callout(
            "Analogy: think of a manager asking 'what is the total headcount cost under me?' "
            "They ask each of their direct reports, who each ask their reports, and so on. "
            "Each person reports their own cost + the sum from everyone below them. "
            "This is exactly DFS with a running sum.",
            "🧠", "blue_background"
        )
    ]),
    N.h3("Code"),
    N.code(SOL1_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("emp_map = {e.id: e for e in employees}", {"code": True}),
                   " — dict comprehension builds the hash map in one O(n) pass. "
                   "Every subsequent lookup by id is O(1) instead of O(n) linear scan."])),
    N.para(N.rich([("def dfs(eid):", {"code": True}),
                   " — inner function closes over emp_map so we don't need to pass it as a parameter on every recursive call."])),
    N.para(N.rich([("emp = emp_map[eid]", {"code": True}),
                   " — O(1) hash map lookup. This is the payoff for building the map first."])),
    N.para(N.rich([("total = emp.importance", {"code": True}),
                   " — start the local total with this employee's own importance value."])),
    N.para(N.rich([("for sub_id in emp.subordinates:", {"code": True}),
                   " — iterate over the list of direct subordinate ids. For a leaf employee this list is empty, so the loop body never runs — that is the natural base case."])),
    N.para(N.rich([("total += dfs(sub_id)", {"code": True}),
                   " — recursively compute the entire subtree importance for each subordinate and add it to our running total."])),
    N.para(N.rich([("return total", {"code": True}),
                   " — return this subtree's total importance to the caller frame above us on the call stack."])),
    N.para(N.rich([("return dfs(id)", {"code": True}),
                   " — launch the DFS from the target employee and return the final answer."])),
    N.divider()
]

# ── Solution 2: BFS ──
blocks += [
    N.h2("Solution 2 — BFS with deque (Iterative)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Same goal as Solution 1 — visit all employees in the target's subtree and sum "
            "importance. BFS processes nodes level-by-level instead of depth-first, but "
            "reaches the same set of nodes."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Using a regular Python list and list.pop(0) for the queue is O(n) per dequeue "
            "operation — making the overall algorithm O(n²). Always use collections.deque "
            "which provides O(1) popleft()."
        ),
        N.h4("The Key Observation"),
        N.para(
            "BFS with a deque avoids Python's recursion depth limit (default ~1000 frames). "
            "For a company with 10,000 employees all in one chain, DFS would hit a RecursionError; "
            "BFS handles it cleanly iteratively."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Seed the queue with the target id. While the queue is non-empty: dequeue an id, "
            "look up the employee, add their importance to total, enqueue all their subordinates. "
            "When the queue is empty, every reachable employee has been visited exactly once."
        ),
        N.callout(
            "DFS vs BFS here: both visit the same nodes in a tree. "
            "DFS via recursion is cleaner code. BFS via deque is safer for very deep hierarchies. "
            "Either is correct — mention the trade-off in your interview.",
            "🧠", "blue_background"
        )
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("total, queue = 0, deque([id])", {"code": True}),
                   " — initialize running total to 0; seed BFS queue with the target id."])),
    N.para(N.rich([("while queue:", {"code": True}),
                   " — continue until all reachable employees are processed."])),
    N.para(N.rich([("eid = queue.popleft()", {"code": True}),
                   " — dequeue the front element in O(1). Using list.pop(0) would be O(n) — always use deque for queues."])),
    N.para(N.rich([("total += emp.importance", {"code": True}),
                   " — accumulate this employee's importance into the running total."])),
    N.para(N.rich([("queue.extend(emp.subordinates)", {"code": True}),
                   " — enqueue all direct subordinate ids for later processing. They'll be visited in the next BFS 'level'."])),
    N.divider()
]

# ── Solution 3: Brute Force ──
blocks += [
    N.h2("Solution 3 — Brute Force (No HashMap, O(n²)) — Do Not Use"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "The simplest possible approach: whenever we need to find an employee by id, "
            "scan the entire employees list. No preprocessing."
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Each scan is O(n). With up to n recursive calls (one per employee), the total "
            "is O(n²). For n = 100,000 this is ~10 billion operations — too slow for any "
            "real use case. Always mention this as the naive starting point, then optimize."
        ),
        N.callout(
            "Always start with the brute force in an interview to establish correctness, "
            "then derive the optimization. Going straight to the optimal solution without "
            "acknowledging the naive approach can raise suspicion.",
            "🧠", "blue_background"
        )
    ]),
    N.h3("Code"),
    N.code(SOL3_CODE, "python"),
    N.divider()
]

# ── Complexity table ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (linear scan)", "O(n²)", "O(h) call stack"],
        ["DFS + HashMap (Interview Pick)", "O(n)", "O(n) map + O(h) stack"],
        ["BFS + HashMap", "O(n)", "O(n) map + O(n) queue"],
    ]),
    N.divider()
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Graph (tree-shaped hierarchy)"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "DFS Sum Values — DFS traversal that accumulates a value (sum, count, list) at each node visited"])),
    N.callout(
        "When to recognize this pattern: "
        "(1) Problem involves a hierarchical / tree structure (org chart, file system, family tree). "
        "(2) You need to aggregate (sum, count, collect) values from all nodes reachable from a given root. "
        "(3) Data is given as a list of objects with 'children' or 'subordinates' links — preprocess into a HashMap first for O(1) lookups.",
        "🔎", "green_background"
    ),
    N.para(
        "Note: 'DFS Sum Values' is classified based on analysis. "
        "The core technique — graph DFS with value accumulation — appears throughout tree and graph problems."
    ),
    N.divider()
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (DFS/BFS traversal with value accumulation):"),
    N.bullet(N.rich([("Number of Islands", {"bold": True}), " (Medium) — DFS from each unvisited land cell, mark all connected land as visited (#200)"])),
    N.bullet(N.rich([("All Paths From Source to Target", {"bold": True}), " (Medium) — DFS collecting all root-to-leaf paths in a DAG (#797)"])),
    N.bullet(N.rich([("Find if Path Exists in Graph", {"bold": True}), " (Easy) — DFS/BFS reachability from source to destination (#1971)"])),
    N.bullet(N.rich([("Count Good Nodes in Binary Tree", {"bold": True}), " (Medium) — DFS with running max, count nodes where val ≥ max on path (#1448)"])),
    N.bullet(N.rich([("Maximum Depth of N-ary Tree", {"bold": True}), " (Easy) — DFS/BFS on a multi-child tree to find maximum depth (#559)"])),
    N.bullet(N.rich([("Sum of Distances in Tree", {"bold": True}), " (Hard) — Two-pass DFS computing sum of all pairwise distances (#834)"])),
    N.para("These problems share the same core technique: build adjacency/map structures for O(1) access, then DFS/BFS to visit all reachable nodes and aggregate values."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Graph section; Sub-Pattern: DFS Sum Values (Analysis)", "📚", "gray_background"),
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([("Step through the DFS algorithm visually — use Next/Prev or arrow keys to see each recursive call and how the total accumulates.",
                    {"italic": True, "color": "gray"})]))
]

# ── Append all blocks ──
print(f"Appending {len(blocks)} blocks to Notion page...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
