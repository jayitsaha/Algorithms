"""
gen_design_a_text_editor.py
Notion page generator for LeetCode #2296 — Design a Text Editor (Hard)
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

SLUG = "design_a_text_editor"
PAGE_ID = None  # No existing page — create fresh

# ── Step 1: Create page ──────────────────────────────────────────────────────
PAGE_ID = N.create_page("Design a Text Editor", 2296, "Hard", "🔴")
print(f"Created page: {PAGE_ID}")

# ── Step 2: Set properties ───────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Hard",
    number=2296,
    pattern="Design",
    subpatterns=["Two Stacks"],
    tc="O(k) per operation",
    sc="O(n) total text length",
    key_insight="Split text at cursor into two stacks; every operation is a push/pop — no O(n) shifting needed.",
    icon="🔴"
)
print("Properties set.")

# ── Step 3: Wipe (fresh page, should be empty already) ──────────────────────
N.wipe_page(PAGE_ID)
print("Wiped page (was empty).")

# ── Step 4: Build body ────────────────────────────────────────────────────────
PROBLEM_STATEMENT = (
    "Design a text editor with a movable cursor that supports: "
    "addText(text) inserts text at the current cursor position; "
    "deleteText(k) deletes up to k characters to the left of the cursor and returns the count deleted; "
    "cursorLeft(k) moves the cursor k steps left and returns the last 10 characters to the left of the cursor; "
    "cursorRight(k) moves the cursor k steps right and returns the last 10 characters to the left of the cursor. "
    "Constraints: 1 <= text.length, k <= 40. At most 2*10^4 operations."
)

SOL1_CODE = """\
class TextEditor:
    def __init__(self):
        self.left = []   # chars before cursor; top = char just left of cursor
        self.right = []  # chars after cursor; top = char just right of cursor

    def addText(self, text: str) -> None:
        for ch in text:
            self.left.append(ch)  # push each char; cursor advances after each

    def deleteText(self, k: int) -> int:
        deleted = 0
        while self.left and k > 0:
            self.left.pop()   # remove char immediately left of cursor
            deleted += 1
            k -= 1
        return deleted

    def cursorLeft(self, k: int) -> str:
        while self.left and k > 0:
            self.right.append(self.left.pop())  # transfer: left-of-cursor → right-of-cursor
            k -= 1
        return ''.join(self.left[-10:])  # last 10 chars before new cursor position

    def cursorRight(self, k: int) -> str:
        while self.right and k > 0:
            self.left.append(self.right.pop())  # transfer: right-of-cursor → left-of-cursor
            k -= 1
        return ''.join(self.left[-10:])
"""

SOL2_CODE = """\
# Solution 2 — Doubly Linked List approach (conceptual; O(k) cursor move, O(k) insert)
class Node:
    def __init__(self, ch):
        self.ch = ch
        self.prev = self.next = None

class TextEditor:
    def __init__(self):
        # Sentinel head and tail nodes for easier edge handling
        self.head = Node('')   # sentinel before all text
        self.tail = Node('')   # sentinel after all text
        self.head.next = self.tail
        self.tail.prev = self.head
        self.cursor = self.head  # cursor points to node AFTER which insertion happens

    def _insert_after(self, node, ch):
        new = Node(ch)
        new.prev, new.next = node, node.next
        node.next.prev = new
        node.next = new
        return new

    def addText(self, text: str) -> None:
        for ch in text:
            self.cursor = self._insert_after(self.cursor, ch)

    def deleteText(self, k: int) -> int:
        deleted = 0
        while self.cursor != self.head and k > 0:
            prev_node = self.cursor.prev
            prev_node.next = self.cursor.next
            self.cursor.next.prev = prev_node
            self.cursor = prev_node
            deleted += 1
            k -= 1
        return deleted

    def _get_left(self) -> str:
        result, node, count = [], self.cursor, 10
        while node != self.head and count > 0:
            result.append(node.ch)
            node = node.prev
            count -= 1
        return ''.join(reversed(result))

    def cursorLeft(self, k: int) -> str:
        while self.cursor != self.head and k > 0:
            self.cursor = self.cursor.prev
            k -= 1
        return self._get_left()

    def cursorRight(self, k: int) -> str:
        while self.cursor.next != self.tail and k > 0:
            self.cursor = self.cursor.next
            k -= 1
        return self._get_left()
"""

blocks = []

# ── Problem ──────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(PROBLEM_STATEMENT),
    N.divider(),
]

# ── Solution 1 — Two Stacks ──────────────────────────────────────────────────
blocks += [
    N.h2("Solution 1 — Two Stacks / Gap Buffer (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para(
            "Think about what a text editor cursor actually does: it sits at a position "
            "in the text, and all edits happen around it. Characters to the left are the "
            "ones we delete (backspace). Moving left/right shifts which characters are "
            "'before' and 'after' the cursor. The question becomes: how do we model "
            "'before cursor' and 'after cursor' so that all operations are fast?"
        ),
        N.h4("What Doesn't Work"),
        N.para(
            "Storing the text as a Python string or list with a cursor index: "
            "addText requires inserting characters at the cursor position, which causes "
            "O(n) rightward shifting of all subsequent characters. With up to 2*10^4 "
            "operations each inserting up to 40 chars, this can be 8*10^5 character "
            "shifts — too slow."
        ),
        N.h4("The Key Observation"),
        N.para(
            "The cursor naturally splits the text into exactly two independent parts: "
            "everything to the LEFT and everything to the RIGHT. We never need to access "
            "the middle of either part — we only ever touch the ends nearest the cursor. "
            "That's exactly what a stack provides: O(1) push/pop at the top. "
            "Left stack top = char just left of cursor = the thing we delete. "
            "Right stack top = char just right of cursor = the thing we move over when going right."
        ),
        N.h4("Building the Solution"),
        N.para(
            "1. addText: push each character of text onto the left stack. Cursor advances. "
            "2. deleteText(k): pop k times from left stack. Return count. "
            "3. cursorLeft(k): pop k from left, push each to right. Cursor moves left. "
            "   Return last 10 of left (now smaller). "
            "4. cursorRight(k): pop k from right, push each to left. Cursor moves right. "
            "   Return last 10 of left (now larger). "
            "The right stack stores chars in REVERSE order — its top is the char "
            "immediately to the right of the cursor, ready for fast access."
        ),
        N.callout(
            "Analogy: Imagine a gap buffer — like filling a bathtub from the left and right. "
            "The gap (cursor) always sits between the two piles. Moving the gap just "
            "scoops water from one side to the other. Adding fills into the left pile. "
            "This is exactly how GNU Emacs stores its text internally.",
            "🛁", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOL1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("self.left = []", {"code": True}), " — left stack; bottom-to-top = text left of cursor; top element = character immediately left of cursor."])),
    N.para(N.rich([("self.right = []", {"code": True}), " — right stack; top element = character immediately right of cursor; stored in reverse order relative to text."])),
    N.para(N.rich([("addText:", {"bold": True}), " iterates over text and appends each character to the left stack. After all pushes, the cursor is after the last inserted character."])),
    N.para(N.rich([("deleteText:", {"bold": True}), " pops from left stack while stack is non-empty AND k > 0. Counts each deletion. Returns actual count (may be less than k if left stack runs dry)."])),
    N.para(N.rich([("cursorLeft:", {"bold": True}), " pops from left and pushes to right — each iteration moves cursor one step left. After k iterations (or until left is empty), returns ", ("''.join(self.left[-10:])", {"code": True}), " — the last min(10, len(left)) chars."])),
    N.para(N.rich([("cursorRight:", {"bold": True}), " pops from right and pushes to left — each iteration moves cursor one step right. Returns last 10 of left after movement."])),
    N.para(N.rich([("self.left[-10:]", {"code": True}), " — Python slice: safe even when left has fewer than 10 elements; no IndexError. Join gives the chars in correct left-to-right order."])),
    N.divider(),
]

# ── Solution 2 — DLL ─────────────────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Doubly Linked List"),
    N.toggle_h3("💡 Intuition: Explicit Node-Based Cursor", [
        N.h4("Reframe the Problem"),
        N.para(
            "Instead of implicitly modeling position via stack sizes, we can use a "
            "doubly linked list where the cursor is a pointer to a specific node. "
            "Insert = splice a new node after cursor. Delete = unlink cursor's predecessor. "
            "Move = follow prev/next pointers."
        ),
        N.h4("What Doesn't Work (vs Two Stacks)"),
        N.para(
            "The DLL approach has the same O(k) complexity for cursor movement but "
            "requires collecting the last-10 chars by traversing backward from the cursor node — "
            "an explicit O(10) traversal. The two-stacks approach has the left stack "
            "always precomputed, making _get_left O(1) after movement."
        ),
        N.h4("The Key Observation"),
        N.para(
            "A doubly linked list gives O(1) insert/delete at a known node. The cursor "
            "IS a node pointer. Sentinel head/tail nodes eliminate null-checking for empty "
            "edges. This approach maps more directly to how a real text editor might use "
            "a linked structure."
        ),
        N.h4("Building the Solution"),
        N.para(
            "Create dummy head and tail sentinel nodes. Cursor starts at head. "
            "addText: call _insert_after(cursor, ch) for each character and advance cursor. "
            "deleteText: unlink cursor, move cursor to predecessor, k times. "
            "cursorLeft/Right: follow prev/next pointers k times. "
            "get_last_10: walk backward from cursor up to 10 nodes, then reverse."
        ),
        N.callout(
            "Note: In Python, the two-stacks approach is simpler and more readable. "
            "The DLL approach is worth knowing for systems design discussions where you "
            "might need to explain trade-offs of gap buffer vs linked list for a real editor.",
            "📝", "gray_background"
        ),
    ]),
    N.h3("Code"),
    N.code(SOL2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("Sentinel nodes", {"bold": True}), " — head and tail are dummy nodes. The actual text lives between them. This eliminates special-casing for empty list or boundary insertions."])),
    N.para(N.rich([("self.cursor = self.head", {"code": True}), " — cursor starts at head sentinel meaning cursor is before all text (position 0)."])),
    N.para(N.rich([("_insert_after(node, ch)", {"bold": True}), " — standard DLL insert: wire new node's prev/next, update neighbors' pointers. Returns new node (cursor advances to it)."])),
    N.para(N.rich([("deleteText:", {"bold": True}), " unlinks self.cursor (the last char before cursor) by bridging prev and next of its neighbors. Cursor moves to prev_node."])),
    N.para(N.rich([("_get_left:", {"bold": True}), " walks backward from cursor collecting up to 10 characters, then reverses the list (since we collected right-to-left) for correct order."])),
    N.divider(),
]

# ── Complexity ───────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "addText", "deleteText", "cursorLeft/Right", "Space"],
        ["Plain String + Index", "O(n) shift", "O(n) shift", "O(k) move + O(10) slice", "O(n)"],
        ["Two Stacks (Gap Buffer) ✓", "O(|text|)", "O(k)", "O(k) transfer + O(1) slice", "O(n)"],
        ["Doubly Linked List", "O(|text|)", "O(k)", "O(k) traverse + O(10) collect", "O(n)"],
        ["Rope / Piece Table", "O(log n)", "O(log n)", "O(log n)", "O(n)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Design"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Two Stacks (Gap Buffer) — analysis-based classification. The 'gap buffer' data structure consists of two stacks (or a single array with a gap) that hold text before and after the cursor."])),
    N.callout(
        "When to recognize this pattern: "
        "Any time you design a data structure with a 'current position' or 'cursor' that divides a sequence into before/after segments. "
        "Operations always happen near the cursor. "
        "The split-at-cursor trick converts O(n) shifts into O(1) stack push/pop. "
        "Key signal: 'move cursor left/right', 'insert/delete at current position'.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same two-stacks or design pattern:"),
    N.bullet(N.rich([("Design Browser History", {"bold": True}), " (Medium) — Structurally identical: back/forward stacks; cursorLeft = go back, cursorRight = go forward (#1472)"])),
    N.bullet(N.rich([("Min Stack", {"bold": True}), " (Medium) — Two stacks: main + auxiliary minimum tracker; shows stacks augmenting each other (#155)"])),
    N.bullet(N.rich([("Implement Queue Using Stacks", {"bold": True}), " (Easy) — Two stacks simulate a queue by reversing order on demand; amortized O(1) dequeue (#232)"])),
    N.bullet(N.rich([("Basic Calculator II", {"bold": True}), " (Medium) — Stack-based expression evaluation; operator precedence via push/pop (#227)"])),
    N.bullet(N.rich([("LRU Cache", {"bold": True}), " (Medium) — Design problem with doubly linked list + hash map for O(1) position-aware eviction (#146)"])),
    N.bullet(N.rich([("All O'one Data Structure", {"bold": True}), " (Hard) — Design with O(1) increment/decrement/min/max using doubly linked list; cursor-like tracking (#432)"])),
    N.bullet(N.rich([("Maximum Frequency Stack", {"bold": True}), " (Hard) — Stack design where push/pop follow frequency rules; multiple stacks for state management (#895)"])),
    N.para("These problems share the core insight: a well-chosen data structure split makes otherwise O(n) operations O(1) or O(k)."),
    N.callout("Note: 'Two Stacks' as a design sub-pattern is analysis-based (not explicitly listed in DSA_Patterns_and_SubPatterns_Guide.md for the Design section). Classification source: Problem Analysis.", "📚", "gray_background"),
]

# ── Embed ─────────────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ─────────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")

# ── Write status file ─────────────────────────────────────────────────────────
import json
status_dir = os.path.join(os.path.dirname(__file__), ".status")
os.makedirs(status_dir, exist_ok=True)
status_path = os.path.join(status_dir, f"{SLUG}.json")
html_path = os.path.join(os.path.dirname(__file__), f"{SLUG}_explainer.html")
import subprocess
line_count = int(subprocess.check_output(["wc", "-l", html_path]).split()[0])

status = {
    "slug": SLUG,
    "html": "OK",
    "notion": "OK",
    "lines": line_count,
    "notes": "Two Stacks (Gap Buffer) design; 7-section HTML with live two-stack viz; fresh Notion page created."
}
with open(status_path, "w") as f:
    json.dump(status, f, indent=2)

print(f"RESULT {SLUG} | html=OK | notion=OK | lines={line_count}")
