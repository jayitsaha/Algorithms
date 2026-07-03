"""
gen_delete_nodes_and_return_forest.py
Notion page creation for LeetCode #1110 — Delete Nodes And Return Forest
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = None  # notion_page_id is null — create fresh

if PAGE_ID is None:
    PAGE_ID = N.create_page("Delete Nodes And Return Forest", 1110, "Medium", "🟡")
    print(f"Created new Notion page: {PAGE_ID}")

# 1) Set properties
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=1110,
    pattern="Trees",
    subpatterns=["DFS: Postorder", "Post-order Check Parent"],
    tc="O(n)",
    sc="O(n)",
    key_insight="Post-order DFS: pass is_root flag down; return None to sever links; surviving orphans become forest roots.",
    icon="🟡"
)
print("Properties set.")

# 2) Build body blocks
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given the ", {}),
        ("root", {"code": True}),
        (" of a binary tree, each node in the tree has a distinct value, and a list ", {}),
        ("to_delete", {"code": True}),
        (" of node values to delete. After deleting all nodes with values in ", {}),
        ("to_delete", {"code": True}),
        (", we are left with a forest (a disjoint union of trees). Return the roots of the trees in the remaining forest. You may return the result in any order.", {})
    ])),
    N.divider(),
]

# ── Solution 1 ──
blocks += [
    N.h2("Solution 1 — Post-order DFS with is_root Flag (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to find all surviving tree roots after deletions. A node becomes a new forest root if and only if: (1) it is NOT deleted, AND (2) its parent WAS deleted (or it was the original root). So the core question is: 'Does this node have a living parent?' — this is the is_root signal."),
        N.h4("What Doesn't Work"),
        N.para("Pre-order DFS fails because we'd process the parent before its children. If we delete the parent first, we don't yet know whether the child should be severed or kept. We'd need a second pass. Storing explicit parent pointers works but adds O(n) extra space and complexity."),
        N.h4("The Key Observation"),
        N.para("When we delete a node P, its children become orphans. This 'orphan' signal can be passed downward as a boolean: is_root=True. If a child receives is_root=True and is not itself deleted, it is a new forest root. Post-order DFS (children before parents) means by the time we process P's deletion, its children have already been visited — everything lines up."),
        N.h4("Building the Solution"),
        N.para("1. Convert to_delete to a set (O(1) lookups). 2. DFS with is_root flag. 3. At each node: if is_root=True and not deleted, add to forest. 4. Recurse into children passing deleted as their is_root. 5. Return None if this node is deleted (severs parent's edge via assignment), else return the node."),
        N.callout("Analogy: Think of each node as a branch. When a branch is cut, its sub-branches fall to the ground and become independent trees. Post-order means we process leaves before trunks — we see the fallen branches before we cut.", "🌳", "green_background"),
    ]),
    N.h3("Code"),
    N.code("""\
def delNodes(root, to_delete):
    to_delete_set = set(to_delete)   # O(1) lookup
    forest = []

    def dfs(node, is_root):
        if not node: return None
        deleted = node.val in to_delete_set
        if is_root and not deleted:      # surviving orphan = new root
            forest.append(node)
        node.left  = dfs(node.left,  deleted)  # deleted => child is orphan
        node.right = dfs(node.right, deleted)
        return None if deleted else node        # None severs parent's edge

    dfs(root, is_root=True)   # root is always a candidate root
    return forest
"""),
    N.h3("Line by Line"),
    N.para(N.rich([("to_delete_set = set(to_delete)", {"code": True}), (" — Convert list to set. This is the single most impactful optimization: membership tests drop from O(k) to O(1) per node.", {})])),
    N.para(N.rich([("forest = []", {"code": True}), (" — Accumulate all surviving tree roots. Passed into the closure so dfs can append to it.", {})])),
    N.para(N.rich([("def dfs(node, is_root):", {"code": True}), (" — Inner function with closure over to_delete_set and forest. is_root encodes whether this node's parent was deleted (or it's the original root).", {})])),
    N.para(N.rich([("if not node: return None", {"code": True}), (" — Base case: null child. Return None immediately (no-op for the parent's assignment).", {})])),
    N.para(N.rich([("deleted = node.val in to_delete_set", {"code": True}), (" — Check if this node is scheduled for deletion. O(1) thanks to the set.", {})])),
    N.para(N.rich([("if is_root and not deleted: forest.append(node)", {"code": True}), (" — A node is a new forest root if it's an orphan (is_root=True) and it survived deletion. We add it before recursing to ensure it's captured.", {})])),
    N.para(N.rich([("node.left = dfs(node.left, deleted)", {"code": True}), (" — Recurse into left child. Pass deleted as the child's is_root: if we're deleting current node, the left child becomes an orphan. The return value (None or left child) is assigned back to node.left — this is how the link is severed.", {})])),
    N.para(N.rich([("node.right = dfs(node.right, deleted)", {"code": True}), (" — Same for right child.", {})])),
    N.para(N.rich([("return None if deleted else node", {"code": True}), (" — If deleted, return None so the parent's assignment severs this edge. If kept, return the node so the parent keeps the link. This is the return-value severance pattern.", {})])),
    N.para(N.rich([("dfs(root, is_root=True)", {"code": True}), (" — Start DFS at the original root. is_root=True because the root is always a potential forest root (it has no parent to be checked).", {})])),
    N.divider(),
]

# ── Solution 2 ──
blocks += [
    N.h2("Solution 2 — BFS with Parent Tracking (Iterative)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same goal: find surviving roots. But instead of recursion, we use a queue. Each queue entry tracks (node, parent, side) so we know exactly which parent pointer to nullify when a node is deleted."),
        N.h4("What Doesn't Work"),
        N.para("Pure BFS without parent tracking can't sever links — we process a node but don't know how to update its parent's left/right pointer. We need to carry parent context alongside each node."),
        N.h4("The Key Observation"),
        N.para("When we dequeue a node and it's in the delete set, we immediately: (1) sever it from its parent via setattr(parent, side, None), and (2) enqueue its children as orphans (no parent). When we dequeue a surviving node with no parent tracked, it's a forest root."),
        N.h4("Building the Solution"),
        N.para("Initialize queue with (root, None, None). Process each node: if deleted, sever from parent and enqueue children as orphans + add to forest. If kept and has no parent (parent=None), add to forest. Enqueue children normally with this node as their parent."),
    ]),
    N.h3("Code"),
    N.code("""\
from collections import deque

def delNodes(root, to_delete):
    to_delete_set = set(to_delete)
    forest = []
    queue = deque([(root, None, None)])  # (node, parent, side)

    while queue:
        node, parent, side = queue.popleft()
        if node.val in to_delete_set:
            if parent:
                setattr(parent, side, None)  # sever parent's pointer
            for child, s in [(node.left, 'left'), (node.right, 'right')]:
                if child:
                    forest.append(child)     # orphaned child = new root
                    queue.append((child, None, None))
        else:
            if parent is None:
                forest.append(node)          # undeleted node with no parent = root
            if node.left:  queue.append((node.left,  node, 'left'))
            if node.right: queue.append((node.right, node, 'right'))

    return forest
"""),
    N.h3("Line by Line"),
    N.para(N.rich([("queue = deque([(root, None, None)])", {"code": True}), (" — Seed the queue with the root. parent=None, side=None because the root has no parent to update.", {})])),
    N.para(N.rich([("if parent: setattr(parent, side, None)", {"code": True}), (" — Sever the deleted node from its parent. setattr lets us use the 'left'/'right' string to address the correct attribute dynamically.", {})])),
    N.para(N.rich([("forest.append(child)", {"code": True}), (" — Each surviving child of a deleted node immediately becomes a new root. Add it before re-enqueuing.", {})])),
    N.para(N.rich([("if parent is None: forest.append(node)", {"code": True}), (" — A surviving node with no parent tracked is either the original root or an orphan that was added to the queue after its parent's deletion.", {})])),
    N.callout("Note: BFS visits nodes level-by-level (top-down), unlike post-order DFS which is bottom-up. Both produce the correct result — they just process nodes in different orders. DFS is simpler for this problem.", "⚠️", "yellow_background"),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Post-order DFS (Solution 1)", "O(n)", "O(h) stack + O(k) set + O(n) result"],
        ["BFS with parent tracking (Solution 2)", "O(n)", "O(n) queue + O(k) set + O(n) result"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Trees — post-order traversal with structural modification.", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("DFS: Postorder — children processed before parents, enabling bottom-up link severance via return-value assignment. Also: Post-order, Check Parent — the is_root flag encodes whether the parent was deleted.", {})])),
    N.callout(
        "When to recognize this pattern: 'Delete nodes from a tree and return remaining roots' — anytime node deletion causes orphaned children that become new roots. Also triggers when a node's status depends on its parent's status (pass flag downward). The return-value assignment pattern (node.left = dfs(...)) signals post-order structural modification.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same post-order DFS with return-value severance technique:"),
    N.bullet(N.rich([("Binary Tree Pruning", {"bold": True}), (" (Medium) — Return null for subtrees with no 1s; same return-value severance pattern.", {})])),
    N.bullet(N.rich([("Delete Node in a BST", {"bold": True}), (" (Medium) — Post-order find and splice target node out via return value.", {})])),
    N.bullet(N.rich([("Lowest Common Ancestor of Binary Tree", {"bold": True}), (" (Medium) — Post-order: children report up the call stack; parent makes decision.", {})])),
    N.bullet(N.rich([("Flatten Binary Tree to Linked List", {"bold": True}), (" (Medium) — Post-order restructuring, rewiring left/right pointers.", {})])),
    N.bullet(N.rich([("House Robber III", {"bold": True}), (" (Medium) — Post-order DP on tree: children compute before parent decides to rob or skip.", {})])),
    N.bullet(N.rich([("Count Nodes Equal to Average of Subtree", {"bold": True}), (" (Medium) — Post-order aggregation: sum and count from children used at parent.", {})])),
    N.bullet(N.rich([("Binary Tree Maximum Path Sum", {"bold": True}), (" (Hard) — Post-order: each node returns the best gain to its parent.", {})])),
    N.para("These problems share the core technique: post-order DFS where children report information upward via return values, enabling parents to make structural decisions."),
    N.callout("Reference: DSA_Patterns_and_SubPatterns_Guide.md — Section on Trees, Sub-Pattern: DFS: Postorder", "📚", "gray_background"),
]

# ── Visual Explainer ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("delete_nodes_and_return_forest")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")

# Write status file
import json, os
status_dir = "/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms/.status"
os.makedirs(status_dir, exist_ok=True)
html_lines = sum(1 for _ in open("/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms/delete_nodes_and_return_forest_explainer.html"))
status = {
    "slug": "delete_nodes_and_return_forest",
    "html": "OK",
    "notion": "OK",
    "notion_page_id": PAGE_ID,
    "lines": html_lines,
    "notes": "Post-order DFS explainer, 14 interactive steps, 2 solutions, Notion page created fresh."
}
with open(f"{status_dir}/delete_nodes_and_return_forest.json", "w") as f:
    json.dump(status, f, indent=2)
print(f"RESULT delete_nodes_and_return_forest | html=OK | notion=OK | lines={html_lines}")
