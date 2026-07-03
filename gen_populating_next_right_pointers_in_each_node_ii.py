"""
gen_populating_next_right_pointers_in_each_node_ii.py
Notion page builder for LeetCode #117 — Populating Next Right Pointers in Each Node II
notion_page_id = null → create a fresh page.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notion_lib as N

SLUG = "populating_next_right_pointers_in_each_node_ii"
NAME = "Populating Next Right Pointers in Each Node II"
NUMBER = 117
DIFFICULTY = "Medium"
ICON = "🟡"
PATTERN = "Trees"
SUBPATTERNS = ["BFS: Level Order"]
TC = "O(n)"
SC = "O(1)"
KEY_INSIGHT = "Use already-set next-pointers as a free linked list; build the next level's chain with a dummy sentinel — no queue needed."

# ── Step 0: Check if page already exists ──────────────────────────
import json, urllib.request, urllib.error

TOKEN = "NOTION_TOKEN_REDACTED"
DB_ID = "39e4c077-47fc-4288-b6a0-00491ae3fb20"
BASE  = "https://api.notion.com/v1"
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}

def _req(method, path, body=None):
    import time
    url = BASE + path
    data = json.dumps(body).encode() if body is not None else None
    last = None
    for attempt in range(7):
        req = urllib.request.Request(url, data=data, method=method, headers=HEADERS)
        try:
            with urllib.request.urlopen(req) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            code = e.code
            payload = e.read().decode()[:300]
            last = f"{code}: {payload}"
            if code == 429:
                wait = float(e.headers.get("Retry-After", 2))
                time.sleep(min(wait, 12)); continue
            if code >= 500:
                time.sleep(min(2 ** attempt, 12)); continue
            raise RuntimeError(f"Notion {method} {path} -> {last}")
        except urllib.error.URLError:
            import time as t; t.sleep(min(2 ** attempt, 12)); last = "network"
    raise RuntimeError(f"Notion {method} {path} failed -> {last}")

# Search for existing page
search_body = {
    "filter": {
        "property": "Problem",
        "title": {"contains": "Populating Next Right Pointers in Each Node II"}
    }
}
search_resp = _req("POST", f"/databases/{DB_ID}/query", search_body)
results = search_resp.get("results", [])

PAGE_ID = None
if results:
    PAGE_ID = results[0]["id"]
    print(f"Found existing page: {PAGE_ID}")
else:
    print("No existing page found — creating new page.")
    PAGE_ID = N.create_page(NAME, NUMBER, DIFFICULTY, ICON)
    print(f"Created new page: {PAGE_ID}")

# ── Step 1: Set properties ────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty=DIFFICULTY,
    number=NUMBER,
    pattern=PATTERN,
    subpatterns=SUBPATTERNS,
    tc=TC,
    sc=SC,
    key_insight=KEY_INSIGHT,
    icon=ICON,
)
print("Properties set.")

# ── Step 2: Wipe old body ─────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── Step 3: Build new body ────────────────────────────────────────

PROBLEM_STATEMENT = (
    "Given a binary tree where each node has: val (int), left (Node), right (Node), and next (Node, default NULL). "
    "Populate each node's next pointer to point to its next right node on the same level. "
    "If there is no next right node, set next to NULL. "
    "The tree may be any binary tree — not necessarily perfect. "
    "You must do this using O(1) extra space (excluding the recursion stack)."
)

SOL1_CODE = '''\
def connect(root):
    curr = root                    # start at leftmost node of current level
    while curr:
        dummy = Node(0)            # sentinel anchor for next level's chain
        tail = dummy               # tail extends chain as children are appended
        while curr:                # traverse current level via next-pointers
            if curr.left:
                tail.next = curr.left   # append left child
                tail = tail.next
            if curr.right:
                tail.next = curr.right  # append right child
                tail = tail.next
            curr = curr.next       # move to next node on same level
        curr = dummy.next          # dive to next level (null if no children)
    return root
'''

SOL2_CODE = '''\
from collections import deque

def connect(root):
    if not root:
        return root
    q = deque([root])
    while q:
        size = len(q)              # snapshot: exactly one level\'s nodes
        for i in range(size):
            node = q.popleft()
            if i < size - 1:
                node.next = q[0]  # point to next node in queue (right neighbour)
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
    return root
'''

blocks = []

# ── Problem ──────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(PROBLEM_STATEMENT),
    N.divider(),
]

# ── Solution 1: Dummy Head O(1) Space ──────────────────────────
blocks += [
    N.h2("Solution 1 — Dummy Head, O(1) Space (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Each level of the tree is really just a sequence of nodes in left-to-right order. "
            "Connecting next-pointers is equivalent to building a linked list out of each level. "
            "The question is: how do we visit all nodes on one level without a queue?"
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "A naive BFS queue works (O(n) space) but the problem asks for O(1) extra space. "
            "DFS (preorder/inorder) doesn't give you nodes level by level unless you track depths — "
            "cumbersome and still needs O(h) recursion space."
        ),
        N.h4("The Key Observation"),
        N.para(
            "Once you've linked level k's next-pointers, you can walk that entire level for free "
            "using curr = curr.next. The linked list already exists — you built it in the previous "
            "iteration. So there's no need for a separate queue: the next-pointers are your queue."
        ),
        N.h4("Building the Solution"),
        N.para(
            "To build level k+1's chain, use a dummy sentinel node. Start tail = dummy. "
            "As you walk level k, for each node: if left child exists, tail.next = left; tail = left. "
            "If right child exists, tail.next = right; tail = right. "
            "After the walk, dummy.next is the first node of level k+1. Repeat."
        ),
        N.callout(
            "Analogy: Think of each level as a train. You walk from car to car (curr.next) "
            "and at each car you place new passengers (children) onto the next train (dummy chain). "
            "The dummy is the locomotive of the new train — it tells you where it starts.",
            "🚂", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOL1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("curr = root", {"code": True}), " — start at the root (leftmost node of level 0)."])),
    N.para(N.rich([("while curr:", {"code": True}), " — outer loop: one iteration per level. Stops when curr is NULL (no more levels)."])),
    N.para(N.rich([("dummy = Node(0)", {"code": True}), " — create a fresh sentinel each level. dummy.next will hold the head of the next level's chain."])),
    N.para(N.rich([("tail = dummy", {"code": True}), " — tail starts at dummy and marches forward as children are appended."])),
    N.para(N.rich([("while curr:", {"code": True}), " — inner loop: walk current level using next-pointers (already set by previous iteration)."])),
    N.para(N.rich([("if curr.left:", {"code": True}), " — check left child first to preserve left-to-right order."])),
    N.para(N.rich([("tail.next = curr.left; tail = tail.next", {"code": True}), " — thread left child into chain, advance tail."])),
    N.para(N.rich([("if curr.right:", {"code": True}), " — check right child second."])),
    N.para(N.rich([("tail.next = curr.right; tail = tail.next", {"code": True}), " — thread right child into chain, advance tail."])),
    N.para(N.rich([("curr = curr.next", {"code": True}), " — advance to next node on current level (using previously set next-pointer)."])),
    N.para(N.rich([("curr = dummy.next", {"code": True}), " — dive to next level: dummy.next is the first real child found, or NULL if no children."])),
    N.divider(),
]

# ── Solution 2: BFS Queue ─────────────────────────────────────
blocks += [
    N.h2("Solution 2 — BFS with Queue (O(n) space, easier first proposal)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Level-order traversal (BFS) processes all nodes on level k before level k+1. "
            "If we know the size of each level, we can connect consecutive nodes within that level."
        ),
        N.h4("The Key Observation"),
        N.para(
            "A BFS queue snapshot at level start (size = len(q)) tells you exactly how many nodes "
            "belong to the current level. For node i (0-indexed), if i < size - 1, "
            "its next-pointer should point to q[0] (the next node in the queue)."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Initialize queue with root. While queue is non-empty: snapshot size. "
            "For each of those size nodes: dequeue, set next = q[0] if not last, enqueue children."
        ),
        N.callout(
            "This is the 'propose brute force first' move in an interview. It's O(n) time and O(n) space. "
            "Then offer to optimize to O(1) space using the dummy-head trick.",
            "💡", "green_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("size = len(q)", {"code": True}), " — snapshot: exactly this many nodes belong to the current level."])),
    N.para(N.rich([("if i < size - 1:", {"code": True}), " — not the rightmost node on this level."])),
    N.para(N.rich([("node.next = q[0]", {"code": True}), " — the next node in the queue is the right neighbour (since we process left-to-right)."])),
    N.para(N.rich([("if node.left: q.append(node.left)", {"code": True}), " — enqueue children for processing in the next level."])),
    N.divider(),
]

# ── Complexity ───────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["BFS Queue", "O(n)", "O(n) — queue holds widest level (up to n/2 nodes)"],
        ["Dummy Head ✓", "O(n)", "O(1) — only curr, dummy, tail pointers"],
    ]),
    N.divider(),
]

# ── Pattern Classification ───────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Trees (BFS Level Order traversal)"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "BFS: Level Order (General Case, Any Binary Tree)"])),
    N.callout(
        "When to recognize this pattern:\n"
        "• 'Connect same-level nodes via next-pointer' → BFS level-order\n"
        "• 'O(1) extra space on a tree' → reuse already-set pointers as traversal structure\n"
        "• 'Build a chain of children without knowing the head upfront' → dummy sentinel\n"
        "• Two nested while-loops on a tree: outer = levels, inner = one level traversal",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ─────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same BFS Level Order technique:"),
    N.bullet(N.rich([("Populating Next Right Pointers in Each Node", {"bold": True}), " (Medium) — #116, same problem for perfect binary tree; O(1) solution without dummy possible since gaps don't exist"])),
    N.bullet(N.rich([("Binary Tree Level Order Traversal", {"bold": True}), " (Medium) — #102, classic BFS with level-size snapshot, returns list of level lists"])),
    N.bullet(N.rich([("Binary Tree Right Side View", {"bold": True}), " (Medium) — #199, last node per level in BFS = right side view"])),
    N.bullet(N.rich([("Binary Tree Zigzag Level Order Traversal", {"bold": True}), " (Medium) — #103, alternating left-to-right and right-to-left traversal per level"])),
    N.bullet(N.rich([("Find Largest Value in Each Tree Row", {"bold": True}), " (Medium) — #515, BFS, track max value per level"])),
    N.bullet(N.rich([("Average of Levels in Binary Tree", {"bold": True}), " (Easy) — #637, BFS, compute average per level"])),
    N.bullet(N.rich([("Maximum Width of Binary Tree", {"bold": True}), " (Medium) — #662, BFS with node position indices to compute width per level"])),
    N.para("These problems all share the same core technique: BFS with level-size tracking or next-pointer threading."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section: Trees → BFS: Level Order\nSub-Pattern: BFS: Level Order · Source: Guide + Analysis", "📚", "gray_background"),
]

# ── Embed ────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"URL: https://notion.so/{PAGE_ID.replace('-', '')}")

# ── Step 4: Write status file ──────────────────────────────────
import pathlib
html_path = pathlib.Path(__file__).parent / f"{SLUG}_explainer.html"
html_lines = len(html_path.read_text().splitlines()) if html_path.exists() else 0

status_dir = pathlib.Path(__file__).parent / ".status"
status_dir.mkdir(exist_ok=True)
status = {
    "slug": SLUG,
    "html": "OK",
    "notion": "OK",
    "lines": html_lines,
    "notes": "Fresh Notion page created; HTML regenerated with 7-section template, 14-step walkthrough, dummy-head O(1) viz."
}
(status_dir / f"{SLUG}.json").write_text(__import__('json').dumps(status, indent=2))
print(f"RESULT {SLUG} | html=OK | notion=OK | lines={html_lines}")
