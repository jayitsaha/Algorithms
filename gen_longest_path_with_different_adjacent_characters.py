"""
Notion update script for LeetCode #2246:
Longest Path With Different Adjacent Characters
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-8110-bd6c-fb7be19d9010"

# ── Step 1: Set properties ──
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=2246,
    pattern="Graph",
    subpatterns=["DFS + Two Max Children"],
    tc="O(n)",
    sc="O(n)",
    key_insight="At each apex node, track the two longest valid arms from children with different chars; path = top1 + top2 + 1.",
    icon="🔴"
)
print("Properties set.")

# ── Step 2: Wipe old body ──
print("Wiping old page body...")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── Step 3: Build body ──
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("You are given a tree with ", {}),
        ("n", {"code": True}),
        (" nodes (numbered 0 to n-1), each assigned a single lowercase character stored in string ", {}),
        ("s", {"code": True}),
        (". The tree is rooted at node 0, and each node's parent is given by array ", {}),
        ("parent", {"code": True}),
        (" (with parent[0] = -1). A ", {}),
        ("path", {"bold": True}),
        (" is any sequence of nodes where each consecutive pair is connected by an edge, with no repeated nodes. Return the length of the ", {}),
        ("longest", {"bold": True}),
        (" such path where no two adjacent nodes share the same character.", {}),
    ])),
    N.para("Constraints: 1 <= s.length <= 10^5, parent.length == s.length, parent[0] == -1."),
    N.divider(),
]

# ── Solution 1: DFS + Two Max Children (Optimal) ──
sol1_code = '''\
def longestPath(parent: List[int], s: str) -> int:
    n = len(parent)
    children = [[] for _ in range(n)]
    for i in range(1, n):
        children[parent[i]].append(i)

    ans = 1  # minimum: single node is always valid

    def dfs(node):
        nonlocal ans
        top1 = top2 = 0  # two best valid child arm lengths
        for child in children[node]:
            child_len = dfs(child)          # always recurse (post-order)
            if s[child] == s[node]:         # same char: edge is blocked
                continue
            if child_len > top1:
                top2 = top1
                top1 = child_len
            elif child_len > top2:
                top2 = child_len
        ans = max(ans, top1 + top2 + 1)    # path through node as apex
        return top1 + 1                     # best arm: includes this node

    dfs(0)
    return ans\
'''

blocks += [
    N.h2("Solution 1 — DFS + Two Max Children (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need the longest path in a tree where no two adjacent nodes have the same character. A path in a tree is a sequence of nodes connected by edges, with no branching. The key reframe: every path has a unique 'apex' — the highest node on the path. If we enumerate all possible apex nodes and find the best path through each, we find the global answer."),
        N.h4("What Doesn't Work"),
        N.para("Brute force: DFS from every node to find the longest valid path starting there. This is O(n²) — for n=10^5 nodes that's 10^10 operations. TLE guaranteed."),
        N.h4("The Key Observation"),
        N.para("When a path passes through apex node u, it consists of at most TWO downward arms from u into two different subtrees. The longest path through u = (best valid arm from child A) + (best valid arm from child B) + 1 (for u itself). 'Valid arm' means the immediate child has a different character than u — the constraint only needs to hold at each edge, and the arm is pre-validated by the recursive call."),
        N.h4("Building the Solution"),
        N.para("1. Build children list from parent array. 2. DFS post-order: recurse into every child first. 3. Only count child arms where s[child] != s[node]. 4. Track top1 and top2 (the two longest valid arms). 5. Update global ans = max(ans, top1+top2+1). 6. Return top1+1 (the best arm this node can offer to its parent)."),
        N.callout(
            "Analogy: Think of it like finding the widest span of a bridge. Each pier (node) can support two cables (arms) going down. The widest bridge through pier u uses the two longest cables from u. We check every pier and record the maximum span.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(sol1_code),
    N.h3("Line by Line"),
    N.para(N.rich([("children = [[] for _ in range(n)]", {"code": True}), (" — Create adjacency list: node → list of its children in the tree.", {})])),
    N.para(N.rich([("for i in range(1, n): children[parent[i]].append(i)", {"code": True}), (" — For each non-root node i, add i to its parent's children list. Root (node 0) skipped since parent[0]=-1.", {})])),
    N.para(N.rich([("ans = 1", {"code": True}), (" — Initialize global answer to 1. A single node is always a valid path of length 1.", {})])),
    N.para(N.rich([("top1 = top2 = 0", {"code": True}), (" — Two trackers for the longest and second-longest valid child arms. Default 0 means no valid arms yet.", {})])),
    N.para(N.rich([("child_len = dfs(child)", {"code": True}), (" — Always recurse into the child first (post-order). Even if the edge is blocked, the child's subtree may contain valid internal paths that update the global ans.", {})])),
    N.para(N.rich([("if s[child] == s[node]: continue", {"code": True}), (" — If the child has the same char as the current node, the edge 0→child is blocked. Skip this arm — it cannot extend through this edge to the current node.", {})])),
    N.para(N.rich([("if child_len > top1: top2=top1; top1=child_len", {"code": True}), (" — New best arm found. The old best becomes second-best.", {})])),
    N.para(N.rich([("elif child_len > top2: top2=child_len", {"code": True}), (" — Beats second-best but not best — update second-best only.", {})])),
    N.para(N.rich([("ans = max(ans, top1 + top2 + 1)", {"code": True}), (" — Longest path through current node as apex: best arm + second arm + the node itself. Update global max.", {})])),
    N.para(N.rich([("return top1 + 1", {"code": True}), (" — Return the best single arm. The +1 includes the current node itself. The parent will use this value when deciding if extending through this node is beneficial.", {})])),
    N.divider(),
]

# ── Solution 2: Iterative ──
sol2_code = '''\
def longestPath(parent: List[int], s: str) -> int:
    n = len(parent)
    children = [[] for _ in range(n)]
    for i in range(1, n):
        children[parent[i]].append(i)

    arm = [1] * n   # arm[i] = best arm length from node i downward
    ans = 1

    # BFS traversal order (root first)
    order = []
    stack = [0]
    while stack:
        node = stack.pop()
        order.append(node)
        for c in children[node]:
            stack.append(c)

    # Process in reverse order: leaves before parents
    for node in reversed(order):
        top1 = top2 = 0
        for child in children[node]:
            if s[child] == s[node]:
                continue
            cl = arm[child]
            if cl > top1:
                top2 = top1
                top1 = cl
            elif cl > top2:
                top2 = cl
        ans = max(ans, top1 + top2 + 1)
        arm[node] = top1 + 1

    return ans\
'''

blocks += [
    N.h2("Solution 2 — Iterative DFS (Stack-Safe for Large Inputs)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same algorithm as Solution 1, but Python's recursive DFS crashes with RecursionError for n=10^5 (default limit ~1000). We simulate the post-order traversal iteratively."),
        N.h4("What Doesn't Work"),
        N.para("Recursive DFS with Python default recursion limit fails for linear chains of 10^5 nodes. sys.setrecursionlimit works but is a code smell for production."),
        N.h4("The Key Observation"),
        N.para("Post-order DFS = process children before parents. We can achieve this with two passes: (1) BFS/DFS to record traversal order (parent before children), then (2) iterate in reverse (children before parents). This gives us the same post-order guarantee without recursion."),
        N.h4("Building the Solution"),
        N.para("Use a stack-based DFS to record nodes in pre-order (root first). Reverse this list to get post-order (leaves first). Then iterate: for each node, look up arm[] values of its already-processed children. Same top1/top2 logic. Store result in arm[node] = top1+1."),
    ]),
    N.h3("Code"),
    N.code(sol2_code),
    N.callout(
        "When to use this: Always in Python for tree problems where n can be large (10^4+). The iterative version has identical time and space complexity but avoids RecursionError. In C++/Java, the recursive version is fine.",
        "💡", "green_background"
    ),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (DFS from every node)", "O(n²)", "O(n)"],
        ["DFS + Two Max Children (recursive)", "O(n)", "O(n)"],
        ["Iterative (topological order)", "O(n)", "O(n)"],
    ]),
    N.para("For the optimal solutions: each of the n nodes is visited exactly once in the DFS. At each node, we iterate over its children (total children across all nodes = n-1). So total work = O(n). Space = O(n) for the children list, the recursion stack (depth up to n for a linear tree), or the explicit arm[] array."),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Graph / Tree DFS", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("DFS + Two Max Children (Tree Diameter Pattern)", {})])),
    N.callout(
        "When to recognize this pattern:\n"
        "• 'Longest path in a tree' or 'diameter' — immediately think apex-node DFS\n"
        "• 'Path through each node as a bend point' — collect top 2 sub-results\n"
        "• Any condition on adjacent pairs (chars, weights, parity) along the path — filter arms before tracking top1/top2\n"
        "• 'Binary Tree Maximum Path Sum' is the same structure with potential negatives",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same DFS + Two Max Children technique:"),
    N.bullet(N.rich([("Diameter of Binary Tree", {"bold": True}), (" (Easy) — Classic apex-node DFS; path = left depth + right depth + 2 (#543).", {})])),
    N.bullet(N.rich([("Binary Tree Maximum Path Sum", {"bold": True}), (" (Hard) — Same two-arm structure; prune negative arms (take max(arm, 0)) before including (#124).", {})])),
    N.bullet(N.rich([("Longest Univalue Path", {"bold": True}), (" (Medium) — Identical structure but constraint is 'same' char (not 'different'); arm is 0 if chars differ (#687).", {})])),
    N.bullet(N.rich([("Sum of Distances in Tree", {"bold": True}), (" (Hard) — Two-pass DFS (re-rooting): first pass collects subtree sums, second re-propagates to all nodes (#834).", {})])),
    N.bullet(N.rich([("Count Nodes Equal to Average of Subtree", {"bold": True}), (" (Medium) — Post-order DFS returning (sum, count) tuple from each subtree (#2265).", {})])),
    N.bullet(N.rich([("Path Sum III", {"bold": True}), (" (Medium) — DFS with prefix sum dictionary to count paths summing to target; different accumulation pattern (#437).", {})])),
    N.para("These problems share the core insight: run post-order DFS, let each node compute an aggregate from its subtree, and update a global answer using values from multiple children."),
    N.callout("📚 Sub-Pattern: DFS + Two Max Children (Tree Diameter Pattern) · Classification source: Analysis (not explicitly in guide — grouped under Graph / Tree DFS sub-patterns).", "📚", "gray_background"),
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("longest_path_with_different_adjacent_characters")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

print(f"Appending {len(blocks)} blocks to Notion...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Total blocks appended: {len(blocks)}")
