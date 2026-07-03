"""
gen_design_circular_deque.py
Notion in-place update for LeetCode #641 Design Circular Deque
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-810b-82f1-e5343249c47c"

# ── 1) Properties ──────────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=641,
    pattern="Design",
    subpatterns=["Array + Modulo"],
    tc="O(1)",
    sc="O(k)",
    key_insight="Circular array with two modulo-wrapped pointers (front, rear) plus a size counter gives O(1) insert/delete at both ends without shifting.",
    icon="🟡"
)
print("Properties set.")

# ── 2) Wipe old content ─────────────────────────────────────────────────────
print("Wiping old page body...")
deleted = N.wipe_page(PAGE_ID)
print(f"Deleted {deleted} blocks.")

# ── 3) Build body ───────────────────────────────────────────────────────────
blocks = []

# ── Problem ─────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Design your implementation of the circular double-ended queue (deque).\n\n"
         "Implement the "),
        ("MyCircularDeque", {"code": True}),
        (" class:\n\n"
         "• MyCircularDeque(k) — Initializes the deque with a maximum size of k.\n"
         "• insertFront(value) — Adds an item at the front. Returns true if successful, false if full.\n"
         "• insertLast(value) — Adds an item at the rear. Returns true if successful, false if full.\n"
         "• deleteFront() — Deletes an item from the front. Returns true if successful, false if empty.\n"
         "• deleteLast() — Deletes an item from the rear. Returns true if successful, false if empty.\n"
         "• getFront() — Gets the front item. Returns -1 if deque is empty.\n"
         "• getRear() — Gets the last item. Returns -1 if deque is empty.\n"
         "• isEmpty() — Returns true if the deque is empty.\n"
         "• isFull() — Returns true if the deque is full.\n\n"
         "Constraints: 1 ≤ k ≤ 1000, 0 ≤ value ≤ 1000, at most 2000 calls per test.")
    ])),
    N.divider(),
]

# ── Solution 1 — Array + Modulo (Interview Pick) ────────────────────────────
blocks += [
    N.h2("Solution 1 — Fixed Array + Modulo Wrapping (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need a data structure that lets us add and remove from both ends in O(1). An array normally can't do that — inserting at the front means shifting all elements, which is O(n). The key is to stop thinking of the array as having a fixed 'front at index 0'. Instead, let front and rear be floating labels that can point at any index."),
        N.h4("What Doesn't Work"),
        N.para("A regular list with list.insert(0, v) for insertFront costs O(n) per call. A dynamic list with appendleft doesn't give us a fixed-capacity guarantee. A naively indexed array wastes memory or requires shifting."),
        N.h4("The Key Observation"),
        N.para("If we treat the array as a ring — where index k-1 wraps back to index 0 — then 'move left by one' is just (idx - 1 + k) % k. There is no actual movement of data. Only the pointers move. This gives O(1) for every operation."),
        N.h4("Building the Solution"),
        N.para("Step 1: Allocate array of size k. Set front=rear=0, size=0.\n"
               "Step 2: For insertLast, if not empty advance rear=(rear+1)%k, then write.\n"
               "Step 3: For insertFront, if not empty retreat front=(front-1+k)%k, then write.\n"
               "Step 4: deleteFront advances front forward; deleteLast retreats rear backward.\n"
               "Step 5: getFront/getRear are single array reads at the pointer positions.\n"
               "Step 6: Use size (not front==rear) to distinguish empty from full."),
        N.callout(
            "Analogy: Imagine 4 chairs in a circle. 'Front' and 'rear' are two people who walk around the ring choosing which chair to sit in. They never move the chairs — only themselves.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code("""\
class MyCircularDeque:
    def __init__(self, k: int):
        self.q = [0] * k        # Pre-allocate fixed array
        self.front = 0          # Index of front element
        self.rear  = 0          # Index of rear element
        self.size  = 0          # Current element count
        self.k     = k          # Capacity

    def insertFront(self, value: int) -> bool:
        if self.isFull(): return False
        if not self.isEmpty():
            self.front = (self.front - 1 + self.k) % self.k  # Step backwards
        self.q[self.front] = value
        self.size += 1
        return True

    def insertLast(self, value: int) -> bool:
        if self.isFull(): return False
        if not self.isEmpty():
            self.rear = (self.rear + 1) % self.k              # Step forwards
        self.q[self.rear] = value
        self.size += 1
        return True

    def deleteFront(self) -> bool:
        if self.isEmpty(): return False
        self.front = (self.front + 1) % self.k               # Advance front
        self.size -= 1
        return True

    def deleteLast(self) -> bool:
        if self.isEmpty(): return False
        self.rear = (self.rear - 1 + self.k) % self.k        # Retreat rear
        self.size -= 1
        return True

    def getFront(self) -> int:
        return -1 if self.isEmpty() else self.q[self.front]

    def getRear(self) -> int:
        return -1 if self.isEmpty() else self.q[self.rear]

    def isEmpty(self) -> bool:
        return self.size == 0

    def isFull(self) -> bool:
        return self.size == self.k
"""),
    N.h3("Line by Line"),
    N.para(N.rich([("self.q = [0] * k", {"code": True}), " — Pre-allocate a fixed array of k zeros. This is the only memory allocation that ever happens — all operations reuse it."])),
    N.para(N.rich([("self.front = self.rear = 0", {"code": True}), " — Both pointers start at index 0. They are only meaningful once size > 0."])),
    N.para(N.rich([("self.size = 0", {"code": True}), " — Tracks live element count. Critical: we use this (not front==rear) to tell empty from full."])),
    N.para(N.rich([("if self.isFull(): return False", {"code": True}), " — Guard at the top of every insert. Prevents overwriting live data."])),
    N.para(N.rich([("if not self.isEmpty():", {"code": True}), " — Skip pointer movement on the very first insert. If we moved the pointer before the first write, front and rear would point to different slots for a single-element deque — a bug."])),
    N.para(N.rich([("self.front = (self.front - 1 + self.k) % self.k", {"code": True}), " — Move front one step backwards in the ring. The +k prevents negative indices in non-Python languages; we include it for clarity even in Python."])),
    N.para(N.rich([("self.rear = (self.rear + 1) % self.k", {"code": True}), " — Move rear one step forwards in the ring. Wraps from k-1 back to 0."])),
    N.para(N.rich([("self.front = (self.front + 1) % self.k", {"code": True}), " — deleteFront: advance front forward to 'uncover' the second element as the new front."])),
    N.para(N.rich([("self.rear = (self.rear - 1 + self.k) % self.k", {"code": True}), " — deleteLast: retreat rear to 'uncover' the second-to-last as the new rear."])),
    N.para(N.rich([("return -1 if self.isEmpty() else self.q[self.front]", {"code": True}), " — getFront/getRear: single O(1) array lookup. Return -1 for empty deque as specified."])),
    N.divider(),
]

# ── Solution 2 — Doubly Linked List ─────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Doubly Linked List"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Any doubly-linked list with a head and tail pointer naturally supports O(1) insert/delete at both ends — that's the classic reason you'd choose a linked list over an array."),
        N.h4("What Doesn't Work"),
        N.para("A singly linked list only gives O(1) at the head; removing the tail requires traversal to find the second-to-last node, which is O(n)."),
        N.h4("The Key Observation"),
        N.para("A doubly linked list with head, tail, and a size counter can do all 6 operations in O(1). We don't need modulo — the pointers already wrap around conceptually via next/prev."),
        N.h4("Building the Solution"),
        N.para("Sentinel (dummy) nodes at head and tail simplify edge cases — no special handling for the empty case during insert/delete."),
    ]),
    N.h3("Code"),
    N.code("""\
class Node:
    def __init__(self, val=0):
        self.val  = val
        self.prev = None
        self.next = None

class MyCircularDeque:
    def __init__(self, k: int):
        self.head = Node()         # Sentinel head
        self.tail = Node()         # Sentinel tail
        self.head.next = self.tail
        self.tail.prev = self.head
        self.size = 0
        self.k    = k

    def _insert_after(self, node, val):
        new = Node(val)
        new.next       = node.next
        new.prev       = node
        node.next.prev = new
        node.next      = new
        self.size += 1

    def _remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev
        self.size -= 1

    def insertFront(self, value):
        if self.isFull(): return False
        self._insert_after(self.head, value)
        return True

    def insertLast(self, value):
        if self.isFull(): return False
        self._insert_after(self.tail.prev, value)
        return True

    def deleteFront(self):
        if self.isEmpty(): return False
        self._remove(self.head.next)
        return True

    def deleteLast(self):
        if self.isEmpty(): return False
        self._remove(self.tail.prev)
        return True

    def getFront(self):
        return -1 if self.isEmpty() else self.head.next.val

    def getRear(self):
        return -1 if self.isEmpty() else self.tail.prev.val

    def isEmpty(self):  return self.size == 0
    def isFull(self):   return self.size == self.k
"""),
    N.h3("Line by Line"),
    N.para(N.rich([("Sentinel nodes (dummy head/tail)", {"bold": True}), " — By having dummy nodes at both ends, insert/delete never needs to handle 'what if the list is empty?' — there are always valid prev/next pointers."])),
    N.para(N.rich([("_insert_after(node, val)", {"code": True}), " — Generic insertion helper: create a new node and stitch it in immediately after 'node'. Works for both front (node=head) and rear (node=tail.prev)."])),
    N.para(N.rich([("_remove(node)", {"code": True}), " — Generic removal: bypass 'node' by linking its prev to its next. Decrement size."])),
    N.para(N.rich([("insertFront: _insert_after(self.head, value)", {"code": True}), " — New node goes right after the sentinel head — making it the new first real element."])),
    N.para(N.rich([("insertLast: _insert_after(self.tail.prev, value)", {"code": True}), " — New node goes right before the sentinel tail — making it the new last real element."])),
    N.divider(),
]

# ── Complexity ───────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time (all ops)", "Space"],
        ["Array + Modulo (optimal)", "O(1)", "O(k) — array only"],
        ["Doubly Linked List", "O(1)", "O(k) — nodes + pointer overhead"],
    ]),
    N.divider(),
]

# ── Pattern Classification ───────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Design"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Array + Modulo (circular buffer / ring buffer technique)"])),
    N.callout(
        "When to recognize this pattern:\n"
        "• Problem asks you to implement a queue, deque, or stack with O(1) ops\n"
        "• Fixed capacity is given (capacity k in the constructor)\n"
        "• Need insert/delete at BOTH ends (deque) or one end (queue/stack)\n"
        "• 'Design' problems that say 'do not use built-in deque/queue implementations'",
        "🔎", "green_background"
    ),
    N.para(N.rich([("Note: ", {"italic": True}),
                   ("Array + Modulo is the canonical sub-pattern for circular buffer / ring buffer designs. "
                    "It is confirmed by analysis; the DSA_Patterns_and_SubPatterns_Guide.md covers Design "
                    "patterns in section 19.", {"italic": True})])),
    N.divider(),
]

# ── Related Problems ─────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same circular array / modulo-wrapping technique:"),
    N.bullet(N.rich([("Design Circular Queue", {"bold": True}), " (Medium) — Single-ended version; same array+modulo approach, simpler boundary logic (LC 622)"])),
    N.bullet(N.rich([("Sliding Window Maximum", {"bold": True}), " (Hard) — Uses a monotonic deque with identical circular array mechanics for O(1) window max (LC 239)"])),
    N.bullet(N.rich([("Design Hit Counter", {"bold": True}), " (Medium) — Circular array of size 300 for rolling time-window counting (LC 362)"])),
    N.bullet(N.rich([("Moving Average from Data Stream", {"bold": True}), " (Easy) — Sliding window sum using a circular queue variant (LC 346)"])),
    N.bullet(N.rich([("LRU Cache", {"bold": True}), " (Medium) — Doubly linked list + hashmap; alternative deque-based design without fixed capacity (LC 146)"])),
    N.bullet(N.rich([("Implement Queue using Stacks", {"bold": True}), " (Easy) — Classic queue design for contrast; no wrap-around needed (LC 232)"])),
    N.para("These problems share the same core technique: fixed-capacity array with modulo-wrapped indices to simulate a ring."),
    N.callout("📚 Reference: Design pattern problems in DSA_Patterns_and_SubPatterns_Guide.md Section 19. Array + Modulo is the defining sub-technique for all circular buffer designs.", "📚", "gray_background"),
]

# ── Embed ────────────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("design_circular_deque")),
    N.para(N.rich([
        ("Step through each operation visually — use Next/Prev or arrow keys to see how front/rear pointers move around the ring.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ────────────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks to Notion page...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
