"""
gen_serialize_and_deserialize_binary_tree.py
Notion update for LeetCode #297 — Serialize and Deserialize Binary Tree
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-81eb-921a-f6024e3b8ba7"
SLUG = "serialize_and_deserialize_binary_tree"

# ── 1. Set properties ──────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=297,
    pattern="Trees",
    subpatterns=["Preorder with Nulls", "Serialization"],
    tc="O(n)",
    sc="O(n)",
    key_insight="Preorder DFS + '#' null markers uniquely encodes any binary tree; deserialize mirrors serialize with a deque.",
    icon="🔴"
)
print("Properties set.")

# ── 2. Wipe old body ────────────────────────────────────────────────
deleted = N.wipe_page(PAGE_ID)
print(f"Wiped {deleted} old blocks.")

# ── 3. Build body ───────────────────────────────────────────────────
blocks = []

# Problem
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Design an algorithm to serialize a binary tree to a string and deserialize that string back to the original tree structure. "),
        ("serialize", {"code": True}),
        (" and "),
        ("deserialize", {"code": True}),
        (" must be inverses — the reconstructed tree must have the exact same structure and values as the original. There is no restriction on how the serialization/deserialization format works; you just need to ensure that a binary tree can be serialized to a string and this string can be deserialized to the original tree structure.")
    ])),
    N.divider(),
]

# ── Solution 1: Preorder DFS + Null Markers (Interview Pick) ────────
sol1_code = """\
from collections import deque

class Codec:
    def serialize(self, root) -> str:
        tokens = []
        def dfs(node):
            if node is None:
                tokens.append('#')
                return
            tokens.append(str(node.val))
            dfs(node.left)
            dfs(node.right)
        dfs(root)
        return ','.join(tokens)

    def deserialize(self, data: str):
        q = deque(data.split(','))
        def build():
            val = q.popleft()
            if val == '#':
                return None
            node = TreeNode(int(val))
            node.left  = build()
            node.right = build()
            return node
        return build()
"""

blocks += [
    N.h2("Solution 1 — Preorder DFS + Null Markers (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need a string format that encodes not just node values but also tree structure — specifically, which positions are empty. Without structure encoding, any flat sequence of values is ambiguous about parent-child relationships."),
        N.h4("What Doesn't Work"),
        N.para("Standard preorder [1, 2, 3] is ambiguous — '2' could be a left child, right child, or left-of-left-child of '1'. Storing both preorder and inorder works but requires O(n) lookup during reconstruction. We need a single-pass approach."),
        N.h4("The Key Observation"),
        N.para("If we record null children explicitly with a sentinel '#', the preorder sequence becomes unambiguous. An n-node tree has exactly n+1 null pointers, so our output has exactly 2n+1 tokens — perfectly balanced. Each recursive deserialization call pops exactly one token."),
        N.h4("Building the Solution"),
        N.para("Serialize: preorder DFS. If node is None, append '#'. Otherwise append the value, recurse left, recurse right. Deserialize: mirror the same traversal. Use a deque for O(1) popleft. Pop the next token — if '#' return None, otherwise create a node and recurse for left and right children."),
        N.callout("Analogy: Think of the token stream as a playlist. Serialize writes the songs in order (with 'skip' markers for empty slots). Deserialize reads the playlist in the same order, creating nodes for songs and empty spots for 'skip' markers.", "🎵", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(sol1_code),
    N.h3("Line by Line"),
    N.para(N.rich([("tokens = []", {"code": True}), " — Collect tokens in a list; join at the end (avoids O(n²) string concatenation)."])),
    N.para(N.rich([("if node is None:", {"code": True}), " — Base case: null child → append sentinel '#' and return immediately."])),
    N.para(N.rich([("tokens.append(str(node.val))", {"code": True}), " — Preorder: record the current node's value before recursing into children."])),
    N.para(N.rich([("dfs(node.left)", {"code": True}), " — Serialize the entire left subtree; all its tokens appear before the right subtree's tokens."])),
    N.para(N.rich([("dfs(node.right)", {"code": True}), " — Serialize the entire right subtree."])),
    N.para(N.rich([("return ','.join(tokens)", {"code": True}), " — Comma-separated output; comma is the delimiter between values and '#' sentinels."])),
    N.para(N.rich([("q = deque(data.split(','))", {"code": True}), " — Split the string and wrap in a deque. deque.popleft() is O(1); list.pop(0) would be O(n)."])),
    N.para(N.rich([("val = q.popleft()", {"code": True}), " — Each build() call consumes exactly one token in preorder — the root of the current subtree."])),
    N.para(N.rich([("if val == '#': return None", {"code": True}), " — Null marker → this position is empty in the original tree; return None."])),
    N.para(N.rich([("node.left = build()", {"code": True}), " — Recurse for left subtree first (mirrors serialize's dfs(node.left) call order)."])),
    N.para(N.rich([("node.right = build()", {"code": True}), " — Then right subtree. The symmetry with serialize guarantees correctness."])),
    N.divider(),
]

# ── Solution 2: BFS Level-Order ─────────────────────────────────────
sol2_code = """\
from collections import deque

class Codec:
    def serialize(self, root) -> str:
        if not root:
            return '#'
        q, tokens = deque([root]), []
        while q:
            node = q.popleft()
            if node is None:
                tokens.append('#')
            else:
                tokens.append(str(node.val))
                q.append(node.left)
                q.append(node.right)
        return ','.join(tokens)

    def deserialize(self, data: str):
        tokens = deque(data.split(','))
        root_val = tokens.popleft()
        if root_val == '#':
            return None
        root = TreeNode(int(root_val))
        q = deque([root])
        while q:
            node = q.popleft()
            for attr in ['left', 'right']:
                val = tokens.popleft()
                if val != '#':
                    child = TreeNode(int(val))
                    setattr(node, attr, child)
                    q.append(child)
        return root
"""

blocks += [
    N.h2("Solution 2 — BFS Level-Order + Null Markers"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Instead of depth-first, we can serialize level by level (breadth-first). Each node in the BFS queue gets its two children recorded — either their values or '#' for null. This produces the same level-order format LeetCode itself uses."),
        N.h4("What Doesn't Work"),
        N.para("DFS recursion can hit Python's recursion limit (~1000) for very deep trees (e.g., a right-skewed chain of 10,000 nodes). BFS avoids recursion entirely."),
        N.h4("The Key Observation"),
        N.para("In BFS, every non-null node enqueues its two children (even null ones, encoded as '#'). During deserialization, every non-null node we create pops two more tokens for its children — either creating new nodes (and queuing them) or leaving slots as None."),
        N.h4("Building the Solution"),
        N.para("Serialize: standard BFS, but enqueue None children too, recording '#' for them. Deserialize: process the BFS queue, popping two tokens per node for its left and right children. Non-'#' tokens become new nodes added to the queue."),
        N.callout("When to prefer BFS: very deep trees where recursion stack overflow is a real concern. DFS is cleaner for most interview settings.", "⚡", "gray_background"),
    ]),
    N.h3("Code"),
    N.code(sol2_code),
    N.h3("Line by Line"),
    N.para(N.rich([("q.append(node.left); q.append(node.right)", {"code": True}), " — Enqueue both children, including None — they'll produce '#' tokens in the next iteration."])),
    N.para(N.rich([("for attr in ['left', 'right']:", {"code": True}), " — Each node has exactly two children slots to fill from the token stream."])),
    N.para(N.rich([("setattr(node, attr, child)", {"code": True}), " — Dynamically set node.left or node.right; queue child for further processing."])),
    N.divider(),
]

# ── Complexity ──────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["DFS Preorder + Nulls (Interview Pick)", "O(n)", "O(n) — tokens array + O(h) recursion stack"],
        ["BFS Level-Order + Nulls", "O(n)", "O(n) — tokens array + O(w) BFS queue (w = max width)"],
        ["BST Preorder (no nulls, BST only)", "O(n log n)", "O(n) — reconstruction needs sorted search"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Trees"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Preorder with Nulls, Serialization"])),
    N.callout(
        "When to recognize this pattern: 'serialize/deserialize' or 'encode/decode' a tree. "
        "Need to store tree structure as flat string. "
        "Compare entire subtree structures (hash-by-serialization). "
        "Single traversal must uniquely reconstruct the tree.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (Tree Serialization / Preorder with Nulls):"),
    N.bullet(N.rich([("Serialize and Deserialize BST", {"bold": True}), " (Medium) — BST property removes need for null markers; preorder alone suffices (#449)"])),
    N.bullet(N.rich([("Find Duplicate Subtrees", {"bold": True}), " (Medium) — Serialize each subtree as a string; use hash map to detect duplicates (#652)"])),
    N.bullet(N.rich([("Verify Preorder Serialization of a Binary Tree", {"bold": True}), " (Medium) — Validate a serialized string without reconstructing the tree (#331)"])),
    N.bullet(N.rich([("Construct Binary Tree from Preorder and Inorder Traversal", {"bold": True}), " (Medium) — Reconstruction from two traversals instead of one + nulls (#105)"])),
    N.bullet(N.rich([("Flatten Binary Tree to Linked List", {"bold": True}), " (Medium) — In-place preorder 'serialization' of tree to linked list (#114)"])),
    N.bullet(N.rich([("Serialize and Deserialize N-ary Tree", {"bold": True}), " (Hard) — Generalize to variable children per node; record child count or use delimiter (#428)"])),
    N.para("These problems share the core technique: encode tree structure into a flat sequence that can be uniquely reconstructed."),
    N.callout("📚 Reference: Trees → Serialization sub-pattern. Named technique: Preorder DFS Encoding with Sentinel Null Markers.", "📚", "gray_background"),
]

# ── Embed ────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

# ── Append all blocks ────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
