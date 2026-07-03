"""
Notion in-place update for: Time Needed to Inform All Employees (#1376)
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-8103-9893-e92d28253ddd"

# ── 1) Set properties ──────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=1376,
    pattern="Graph",
    subpatterns=["DFS from Root"],
    tc="O(n)",
    sc="O(n)",
    key_insight="Invert manager[] to children[], DFS from head passing accumulated time; answer = max time at any node.",
    icon="🟡"
)
print("Properties set.")

# ── 2) Wipe existing body ──────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3) Build body ──────────────────────────────────────────────────────────
blocks = []

# ─── Problem ──────────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given "), ("n", {"code": True}), (" employees (0 to n-1), "),
        ("headID", {"code": True}), (" (the head), "),
        ("manager[i]", {"code": True}), (" (who manages employee i; "),
        ("manager[headID] = -1", {"code": True}), ("), and "),
        ("informTime[i]", {"code": True}),
        (" (minutes for employee i to relay to all direct reports). "
         "Return the total number of minutes needed for all employees to receive the urgent message.")
    ])),
    N.divider(),
]

# ─── Solution 1: Top-Down DFS (Interview Pick) ────────────────────────────
blocks += [
    N.h2("Solution 1 — Top-Down DFS: Accumulated Time (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The manager[] array is a parent-pointer tree. We need the maximum root-to-any-node path sum, where edge weights are the informTime of the source node. All branches relay in parallel — the answer is the MAX, not sum."),
        N.h4("What Doesn't Work"),
        N.para("BFS level-by-level fails because edges have different weights — levels don't correspond to time. Tracing each employee's path up to the root is O(n²) for a linear chain."),
        N.h4("The Key Observation"),
        N.para("Time for any employee to be informed = sum of informTime values along the path from headID to that employee. This accumulated sum is exactly what we track as a DFS parameter."),
        N.h4("Building the Solution"),
        N.para("Step 1: Invert manager[] → children[]. Step 2: DFS from headID with time=0. Step 3: At each node, update global max. Step 4: Recurse into children with time + informTime[node]."),
        N.callout("Analogy: Think of a telephone tree. Each manager calls all their reports at once (parallel), but it takes them some time before they're ready to call. The last employee to hear = slowest chain of calls from the top.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(
        "def numOfMinutes(n, headID, manager, informTime):\n"
        "    from collections import defaultdict\n"
        "    # Step 1: Build children adjacency list (invert manager[])\n"
        "    children = defaultdict(list)\n"
        "    for emp, mgr in enumerate(manager):\n"
        "        if mgr != -1:\n"
        "            children[mgr].append(emp)\n"
        "    \n"
        "    ans = 0\n"
        "    \n"
        "    def dfs(node, time):\n"
        "        nonlocal ans\n"
        "        # time = minute this node received the message\n"
        "        ans = max(ans, time)  # every node is a candidate for the answer\n"
        "        for child in children[node]:\n"
        "            # child hears after parent's relay delay\n"
        "            dfs(child, time + informTime[node])\n"
        "    \n"
        "    dfs(headID, 0)  # head informed at time 0\n"
        "    return ans"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("children = defaultdict(list)", {"code": True}), " — adjacency list mapping each manager to their direct reports."])),
    N.para(N.rich([("for emp, mgr in enumerate(manager)", {"code": True}), " — iterate all employees, building parent→child relationships."])),
    N.para(N.rich([("if mgr != -1: children[mgr].append(emp)", {"code": True}), " — skip the head (whose manager is -1); add all others as children of their manager."])),
    N.para(N.rich([("ans = 0", {"code": True}), " — global maximum of inform times across all visited nodes."])),
    N.para(N.rich([("def dfs(node, time)", {"code": True}), " — time is the minute this node was informed; passed down from parent calls."])),
    N.para(N.rich([("ans = max(ans, time)", {"code": True}), " — update the answer at every node (leaf or not), since every employee's inform-time matters."])),
    N.para(N.rich([("for child in children[node]", {"code": True}), " — iterate all direct reports of this manager."])),
    N.para(N.rich([("dfs(child, time + informTime[node])", {"code": True}), " — child hears at: current time + this manager's relay delay."])),
    N.para(N.rich([("dfs(headID, 0)", {"code": True}), " — kick off DFS from the head at time 0."])),
    N.divider(),
]

# ─── Solution 2: Bottom-Up DFS ────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Bottom-Up DFS: Return Subtree Max"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Instead of passing time down, each DFS call returns the maximum additional time needed within its subtree. The root call accumulates and returns the total answer."),
        N.h4("The Key Observation"),
        N.para("For any node: max_time_in_subtree = informTime[node] + max(max_time in each child's subtree). Leaves return 0 (they relay to nobody). This bottom-up recurrence naturally gives the answer at the root."),
        N.h4("Building the Solution"),
        N.para("Base case: leaf nodes return 0. Recursive case: return informTime[node] + max(dfs(c) for c in children[node]). The default=0 handles the case where children is empty (leaf node)."),
        N.callout("This is the more functional style — no global variable, pure recursive return. Use this if you prefer returning values over side effects.", "💡", "green_background"),
    ]),
    N.h3("Code"),
    N.code(
        "def numOfMinutes(n, headID, manager, informTime):\n"
        "    from collections import defaultdict\n"
        "    children = defaultdict(list)\n"
        "    for emp, mgr in enumerate(manager):\n"
        "        if mgr != -1:\n"
        "            children[mgr].append(emp)\n"
        "    \n"
        "    def dfs(node):\n"
        "        # Returns max inform time within this node's subtree\n"
        "        if not children[node]:  # leaf: no relay time\n"
        "            return 0\n"
        "        return informTime[node] + max(dfs(c) for c in children[node])\n"
        "    \n"
        "    return dfs(headID)"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("def dfs(node)", {"code": True}), " — returns the max time from this node to the furthest-reached employee in its subtree."])),
    N.para(N.rich([("if not children[node]: return 0", {"code": True}), " — leaf base case: a leaf relays to nobody, adds 0 time."])),
    N.para(N.rich([("return informTime[node] + max(dfs(c) for c in children[node])", {"code": True}), " — node relays in informTime[node] minutes, then the worst-case child subtree determines additional time."])),
    N.para(N.rich([("return dfs(headID)", {"code": True}), " — the root call returns the total answer directly."])),
    N.divider(),
]

# ─── Complexity ────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Top-Down DFS (Accumulated Time)", "O(n)", "O(n)"],
        ["Bottom-Up DFS (Return Max)", "O(n)", "O(n)"],
        ["Iterative BFS/DFS with queue", "O(n)", "O(n)"],
    ]),
    N.divider(),
]

# ─── Pattern Classification ────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Graph (tree is a special connected acyclic graph)"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "DFS from Root — propagate accumulated value from root to leaves, track global maximum of path sums."])),
    N.callout(
        "When to recognize this pattern: manager/employee hierarchy → rooted tree; "
        "'inform all employees' → propagate from head; edge weights differ (informTime varies) → DFS with accumulated time, not BFS levels; "
        "answer = 'total time' → maximum path sum.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ─── Related Problems ──────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same DFS from Root / Weighted Tree Path technique:"),
    N.bullet(N.rich([("Maximum Depth of Binary Tree", {"bold": True}), " (Easy) — unweighted DFS from root, count depth (#104)"])),
    N.bullet(N.rich([("Path Sum II", {"bold": True}), " (Medium) — DFS accumulating root-to-leaf path, collect matching sums (#113)"])),
    N.bullet(N.rich([("Binary Tree Maximum Path Sum", {"bold": True}), " (Hard) — DFS where path can pass through any node; max over all paths (#124)"])),
    N.bullet(N.rich([("Sum of Distances in Tree", {"bold": True}), " (Hard) — two DFS passes to compute sum of distances from every node (#834)"])),
    N.bullet(N.rich([("Amount of Time for Binary Tree to Be Infected", {"bold": True}), " (Medium) — BFS/DFS spread from a given node (#2385)"])),
    N.bullet(N.rich([("Minimum Time to Collect All Apples in a Tree", {"bold": True}), " (Medium) — DFS cost only on edges leading to apples (#1443)"])),
    N.bullet(N.rich([("All Nodes Distance K in Binary Tree", {"bold": True}), " (Medium) — DFS/BFS spread from a given node in all directions (#863)"])),
    N.para("These problems share the core technique: build or traverse a rooted tree, accumulate a value along the path from root, and find the maximum or all such accumulated values."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section 7 (Graph Traversal). Sub-Pattern: DFS from Root.", "📚", "gray_background"),
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("time_needed_to_inform_all_employees")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

# ─── Append all blocks ─────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
print("All blocks appended successfully.")
