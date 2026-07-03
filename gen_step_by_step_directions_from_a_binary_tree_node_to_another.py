"""
Notion regeneration script for:
  LeetCode #2096 — Step-By-Step Directions From a Binary Tree Node to Another
  Notion Page ID: 39193418-809c-8105-ad97-c7f725390114
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8105-ad97-c7f725390114"
SLUG    = "step_by_step_directions_from_a_binary_tree_node_to_another"

# ── 1. Update page properties ──────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=2096,
    pattern="Trees",
    subpatterns=["Find LCA + Build Paths"],
    tc="O(n)",
    sc="O(n)",
    key_insight="Find LCA, then replace src-path with U's and concat dst-path.",
    icon="🟡",
)
print("Properties set.")

# ── 2. Wipe old body ───────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3. Build new body ──────────────────────────────────────────────────────
SOL1 = """\
def getDirections(root, startValue, destValue):
    def lca(node):
        if not node: return None
        if node.val in (startValue, destValue): return node
        L = lca(node.left)
        R = lca(node.right)
        if L and R: return node   # BOTH found → this IS the LCA
        return L or R

    def findPath(node, target, path):
        if not node: return False
        if node.val == target: return True
        path.append('L')
        if findPath(node.left, target, path): return True
        path.pop()
        path.append('R')
        if findPath(node.right, target, path): return True
        path.pop()
        return False

    lca_node = lca(root)          # Stage 1: find LCA
    src_path, dst_path = [], []
    findPath(lca_node, startValue,  src_path)  # Stage 2: LCA → start
    findPath(lca_node, destValue,   dst_path)  # Stage 3: LCA → dest
    return 'U' * len(src_path) + ''.join(dst_path)  # Stage 4: combine
"""

SOL2 = """\
from collections import deque

def getDirections(root, startValue, destValue):
    par, nmap = {}, {}
    stk = [root]
    while stk:
        nd = stk.pop()
        nmap[nd.val] = nd
        if nd.left:
            par[nd.left.val] = (nd.val, 'L')
            stk.append(nd.left)
        if nd.right:
            par[nd.right.val] = (nd.val, 'R')
            stk.append(nd.right)

    vis = set()
    q = deque([(startValue, "")])
    while q:
        v, path = q.popleft()
        if v == destValue: return path
        vis.add(v)
        nd = nmap[v]
        if nd.left  and nd.left.val  not in vis:
            q.append((nd.left.val,  path + 'L'))
        if nd.right and nd.right.val not in vis:
            q.append((nd.right.val, path + 'R'))
        if v in par and par[v][0] not in vis:
            q.append((par[v][0], path + 'U'))
"""

blocks = []

# ── Problem statement ───────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        "Given the ", ("root", {"code": True}),
        " of a binary tree and two integers ", ("startValue", {"code": True}),
        " and ", ("destValue", {"code": True}),
        ", return a string of instructions to get from the node with value ",
        ("startValue", {"code": True}), " to the node with value ",
        ("destValue", {"code": True}),
        ". Each character is 'L' (go to left child), 'R' (go to right child), ",
        "or 'U' (go to parent). The answer represents the lexicographically ",
        "shortest path in the tree. All node values are unique."
    ])),
    N.callout(
        "Example: root=[5,1,2,3,null,6,4], startValue=3, destValue=6 → \"UURL\"",
        "📌", "blue_background"
    ),
    N.divider(),
]

# ── Solution 1 ──────────────────────────────────────────────────────────────
blocks += [
    N.h2("Solution 1 — LCA + DFS Path Building (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to navigate from node A to node B in a tree. In any tree, "
               "there is exactly one path between two nodes. That path always goes UP "
               "from A to some common ancestor, then DOWN to B. The deepest such "
               "ancestor is the Lowest Common Ancestor (LCA)."),
        N.h4("What Doesn't Work"),
        N.para("Finding paths from the root to both nodes, then stripping the common prefix — "
               "this works logically but requires careful string slicing (off-by-one errors) "
               "and does not clearly express the 'U' direction logic. Also, going sideways "
               "is impossible in a tree — there is only one path."),
        N.h4("The Key Observation"),
        N.para("The path shape is always: (UP from start to LCA) + (DOWN from LCA to dest). "
               "The upward segment is all 'U's — regardless of whether each step was a left "
               "or right child relationship. So we only need the COUNT of upward steps, not "
               "the actual directions. 'U' × len(src_path) gives us the upward part. "
               "Then a fresh DFS from LCA to dest gives us the downward L/R sequence."),
        N.h4("Building the Solution"),
        N.para("Step 1: Find LCA using standard recursive logic (return node if it equals "
               "start or dest; if both subtrees return non-null, current node is LCA). "
               "Step 2: DFS from LCA to startValue with backtracking — gives src_path. "
               "Step 3: DFS from LCA to destValue — gives dst_path. "
               "Step 4: return 'U' * len(src_path) + ''.join(dst_path)."),
        N.callout(
            "Analogy: You're in a company org chart. To get from one employee to another, "
            "you climb up to the common manager (LCA), then walk down to the target. "
            "Climbing is always 'U'; walking down follows the org structure (L/R).",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOL1),
    N.h3("Line by Line"),
    N.para(N.rich([("lca(node)", {"code": True}),
        " — Recursive LCA. Returns the node itself if it is start or dest (so LCA is at or above). "
        "Recurses left and right; if both return non-null, this node IS the LCA."])),
    N.para(N.rich([("if not node: return None", {"code": True}),
        " — Base case: empty subtree contains neither target."])),
    N.para(N.rich([("if node.val in (...): return node", {"code": True}),
        " — Early return: no need to search deeper once we find a target node."])),
    N.para(N.rich([("if L and R: return node", {"code": True}),
        " — The LCA condition: one target found in the left subtree, the other in the right. "
        "This node is the deepest node with both targets in its subtree."])),
    N.para(N.rich([("return L or R", {"code": True}),
        " — Only one side found: bubble up that result to the caller."])),
    N.para(N.rich([("path.append('L')", {"code": True}), " + ", ("path.pop()", {"code": True}),
        " — The backtracking idiom: tentatively record the direction, recurse, undo if "
        "the target is NOT in that subtree. Without pop(), stale directions corrupt the result."])),
    N.para(N.rich([("'U' * len(src_path)", {"code": True}),
        " — We only need the length of the LCA→start path. Every step of going "
        "from start back to LCA is 'go to parent' = 'U'. The actual L/R directions "
        "are irrelevant for the upward traversal."])),
    N.callout(
        "⚠️ Common Bug: Forgetting path.pop() causes stale directions from failed branches "
        "to accumulate in the path list, producing completely wrong output.",
        "⚠️", "orange_background"
    ),
    N.divider(),
]

# ── Solution 2 ──────────────────────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Parent Map + BFS"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Think of the binary tree as an undirected graph where you can move to "
               "left child ('L'), right child ('R'), or parent ('U'). Finding the shortest "
               "path in an unweighted graph = BFS."),
        N.h4("What Doesn't Work"),
        N.para("Standard tree BFS can only go down. We also need to go up (to parent). "
               "The tree structure doesn't store parent pointers by default, so we need "
               "to build a parent map first in a preprocessing step."),
        N.h4("The Key Observation"),
        N.para("Once we have a parent map, every node has at most 3 neighbors: left child, "
               "right child, and parent. BFS from startValue with a visited set gives the "
               "shortest path to destValue naturally."),
        N.h4("Building the Solution"),
        N.para("DFS to build parent map (child.val → parent.val). Then BFS from startValue, "
               "exploring all three neighbor directions at each step, carrying the path string "
               "as BFS state. When we reach destValue, return the accumulated path."),
    ]),
    N.h3("Code"),
    N.code(SOL2),
    N.h3("Line by Line"),
    N.para(N.rich([("par[child.val] = (parent.val, dir)", {"code": True}),
        " — Build parent map during DFS. Stores both the parent's value and the direction "
        "('L' or 'R') from parent to child, though for BFS we only use the parent's val."])),
    N.para(N.rich([("q = deque([(startValue, \"\")] )", {"code": True}),
        " — BFS queue stores (current_node_val, path_string_so_far)."])),
    N.para(N.rich([("if v in par and par[v][0] not in vis", {"code": True}),
        " — Move UP to parent. The root has no parent (not in par dict), "
        "so this naturally stops at the root. visited set prevents revisiting."])),
    N.callout(
        "Trade-off: BFS is easier to reason about and doesn't need the LCA insight. "
        "But it uses 2× memory (par + nmap dicts on top of BFS queue). "
        "LCA+DFS (Solution 1) is more elegant and space-efficient.",
        "💡", "green_background"
    ),
    N.divider(),
]

# ── Complexity ──────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space", "Notes"],
        ["LCA + DFS (optimal)", "O(n)", "O(n)", "3 tree passes; no extra hash maps"],
        ["Parent Map + BFS",    "O(n)", "O(n)", "Extra O(n) for par/nmap dicts; BFS queue grows O(n)"],
        ["Brute Force (strip prefix)", "O(n)", "O(n)", "Same complexity; tricky string slicing"],
    ]),
    N.divider(),
]

# ── Pattern Classification ───────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Trees"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}),
        "Find LCA + Build Paths, DFS: Postorder, LCA"])),
    N.callout(
        "When to recognize this pattern: "
        "(1) Problem asks for a path or directions between two nodes in a tree. "
        "(2) Directions involve going UP ('U') and DOWN ('L'/'R'). "
        "(3) The phrase 'shortest path between two nodes' in a tree always implies LCA.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ─────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (LCA, DFS path building, tree path navigation):"),
    N.bullet(N.rich([
        ("Lowest Common Ancestor of a Binary Tree", {"bold": True}),
        " (Medium) — #236, the foundational LCA algorithm this problem builds on."
    ])),
    N.bullet(N.rich([
        ("Lowest Common Ancestor of a Binary Search Tree", {"bold": True}),
        " (Easy) — #235, simpler because BST ordering lets you skip subtrees."
    ])),
    N.bullet(N.rich([
        ("Binary Tree Paths", {"bold": True}),
        " (Easy) — #257, same DFS+backtracking for root-to-leaf paths."
    ])),
    N.bullet(N.rich([
        ("Path Sum II", {"bold": True}),
        " (Medium) — #113, collect root-to-leaf paths with target sum; same path DFS idiom."
    ])),
    N.bullet(N.rich([
        ("All Nodes Distance K in Binary Tree", {"bold": True}),
        " (Medium) — #863, parent map + BFS; exactly Solution 2 of this problem generalized."
    ])),
    N.bullet(N.rich([
        ("Sum of Distances in Tree", {"bold": True}),
        " (Hard) — #834, path distances in a general tree via re-rooting DP."
    ])),
    N.para("These problems share the same core technique: DFS to find paths in trees, "
           "LCA as the decomposition point for paths between arbitrary node pairs."),
    N.callout(
        "Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section Trees → LCA sub-pattern. "
        "Sub-pattern classification: 'Find LCA + Build Paths' (analysis-based; problem not explicitly listed in guide).",
        "📚", "gray_background"
    ),
]

# ── Embed ────────────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ────────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"Notion page rebuilt. Total blocks appended: {len(blocks)}")
print(f"NOTION OK {PAGE_ID}")
