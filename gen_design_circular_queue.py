"""
gen_design_circular_queue.py
Rebuild Notion page for Design Circular Queue (#622) in-place.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81ab-b3fb-cf1a04900310"

print("Step 1: Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=622,
    pattern="Design",
    subpatterns=["Array with Head/Tail"],
    tc="O(1)",
    sc="O(k)",
    key_insight="Use a fixed array with head/tail pointers and a count field; advance pointers with (ptr+1)%k to wrap around.",
    icon="🟡"
)
print("  Properties set.")

print("Step 2: Wiping old body...")
n = N.wipe_page(PAGE_ID)
print(f"  Wiped {n} blocks.")

print("Step 3: Building new body...")
blocks = []

# ── Problem Statement ──────────────────────────────────────────
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Design your implementation of the circular queue. The circular queue is a linear data structure in which the operations are performed based on FIFO (First In First Out) principle, and the last position is connected back to the first position to make a circle. It is also called a 'Ring Buffer'.\n\n"
         "Implement the "),
        ("MyCircularQueue", {"code": True}),
        (" class with capacity "),
        ("k", {"code": True}),
        (", supporting these operations:\n"
         "• enQueue(value) — Insert an element at the rear. Return True if successful, False if full.\n"
         "• deQueue() — Delete an element from the front. Return True if successful, False if empty.\n"
         "• Front() — Get the front item. Return -1 if empty.\n"
         "• Rear() — Get the last item. Return -1 if empty.\n"
         "• isEmpty() — Check whether the queue is empty.\n"
         "• isFull() — Check whether the queue is full.")
    ])),
    N.divider(),
]

# ── Solution 1 — Array with Head/Tail/Count (Interview Pick) ───
blocks += [
    N.h2("Solution 1 — Array with Head/Tail/Count (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need a queue that fits in fixed memory and never shifts elements. The insight: treat the array as a circular track where two runners (head and tail) chase each other. When a runner reaches the end of the track, it wraps to position 0 using modulo arithmetic."),
        N.h4("What Doesn't Work"),
        N.para("A naive queue that shifts all elements left on dequeue runs in O(n). A queue that tracks a front pointer without wrapping eventually runs out of right-side space, even though left-side slots are empty. Both fail the O(1) requirement or waste memory."),
        N.h4("The Key Observation"),
        N.para("The array is a ring: index (k-1) connects back to index 0. If we advance tail with (tail+1)%k and head with (head+1)%k, each pointer automatically recycles the slots freed by dequeue. No physical movement of data is needed."),
        N.h4("Building the Solution"),
        N.para("Fields: data[k] (the array), head (dequeue side), tail (next-write side), count (to tell empty from full). enQueue writes at tail then advances tail. deQueue advances head. count tracks occupancy. head==tail is ambiguous — count disambiguates."),
        N.callout(
            "Analogy: think of a circular conveyor belt at a sushi restaurant. Plates are placed at one end (tail) and picked up at the other (head). When the belt reaches the end of the track, new plates fill spots vacated at the front. The belt capacity is fixed; plates are never physically shuffled.",
            "🍣", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(
        "class MyCircularQueue:\n"
        "    def __init__(self, k: int):\n"
        "        self.data  = [0] * k   # Fixed-size array\n"
        "        self.head  = 0         # Front of queue (next dequeue)\n"
        "        self.tail  = 0         # Next write slot (after last element)\n"
        "        self.count = 0         # Current number of elements\n"
        "        self.k     = k         # Capacity\n"
        "\n"
        "    def enQueue(self, value: int) -> bool:\n"
        "        if self.isFull(): return False\n"
        "        self.data[self.tail] = value\n"
        "        self.tail = (self.tail + 1) % self.k\n"
        "        self.count += 1\n"
        "        return True\n"
        "\n"
        "    def deQueue(self) -> bool:\n"
        "        if self.isEmpty(): return False\n"
        "        self.head = (self.head + 1) % self.k\n"
        "        self.count -= 1\n"
        "        return True\n"
        "\n"
        "    def Front(self) -> int:\n"
        "        if self.isEmpty(): return -1\n"
        "        return self.data[self.head]\n"
        "\n"
        "    def Rear(self) -> int:\n"
        "        if self.isEmpty(): return -1\n"
        "        return self.data[(self.tail - 1 + self.k) % self.k]\n"
        "\n"
        "    def isEmpty(self) -> bool: return self.count == 0\n"
        "    def isFull(self)  -> bool: return self.count == self.k\n"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("self.data = [0] * k", {"code": True}),
                   " — Allocates the fixed storage array. Values are irrelevant until written; we use count to know which slots are live."])),
    N.para(N.rich([("self.head = 0", {"code": True}),
                   " — Points to the front of the queue. deQueue will advance this pointer."])),
    N.para(N.rich([("self.tail = 0", {"code": True}),
                   " — Points to the next slot to write. enQueue writes here, then advances. Tail is always one ahead of the last element."])),
    N.para(N.rich([("self.count = 0", {"code": True}),
                   " — Tracks occupancy. This field is the only way to tell empty (count=0) from full (count=k) when head==tail."])),
    N.para(N.rich([("if self.isFull(): return False", {"code": True}),
                   " — Guard clause. O(1) rejection when capacity is reached."])),
    N.para(N.rich([("self.data[self.tail] = value", {"code": True}),
                   " — Write the new value at the current tail slot."])),
    N.para(N.rich([("self.tail = (self.tail + 1) % self.k", {"code": True}),
                   " — Advance tail. The modulo wraps index k-1 back to 0, making the array circular."])),
    N.para(N.rich([("self.head = (self.head + 1) % self.k", {"code": True}),
                   " — Same wrap trick for dequeue. The old front element is logically discarded without clearing it."])),
    N.para(N.rich([("return self.data[(self.tail-1+self.k) % self.k]", {"code": True}),
                   " — Rear: tail-1 is the last written slot. Adding self.k before modulo prevents negative when tail==0."])),
    N.divider(),
]

# ── Solution 2 — Linked List ───────────────────────────────────
blocks += [
    N.h2("Solution 2 — Singly Linked List"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Instead of a fixed array, maintain a chain of nodes. head points to the front; tail points to the rear. No modulo arithmetic needed — Rear() is just self.tail.val."),
        N.h4("What Doesn't Work"),
        N.para("A naive linked list without a size counter cannot enforce capacity in O(1). We must traverse to count, which is O(n)."),
        N.h4("The Key Observation"),
        N.para("Track a size counter alongside head and tail. isFull() is size==k in O(1). enQueue appends; deQueue advances head. Both O(1)."),
        N.h4("Building the Solution"),
        N.para("When the list empties completely (head becomes None after dequeue), tail must also be reset to None — otherwise tail points to a freed node."),
        N.callout("Trade-off: Rear() is simpler (self.tail.val vs modulo expression), but every node allocation adds pointer overhead and cache pressure. Prefer the array solution when capacity is fixed.", "⚖️", "gray_background"),
    ]),
    N.h3("Code"),
    N.code(
        "class Node:\n"
        "    def __init__(self, val): self.val = val; self.next = None\n"
        "\n"
        "class MyCircularQueue:\n"
        "    def __init__(self, k):\n"
        "        self.size = 0; self.k = k\n"
        "        self.head = self.tail = None\n"
        "\n"
        "    def enQueue(self, val) -> bool:\n"
        "        if self.isFull(): return False\n"
        "        node = Node(val)\n"
        "        if self.tail: self.tail.next = node\n"
        "        self.tail = node\n"
        "        if not self.head: self.head = node  # first element\n"
        "        self.size += 1\n"
        "        return True\n"
        "\n"
        "    def deQueue(self) -> bool:\n"
        "        if self.isEmpty(): return False\n"
        "        self.head = self.head.next\n"
        "        if not self.head: self.tail = None  # list now empty\n"
        "        self.size -= 1\n"
        "        return True\n"
        "\n"
        "    def Front(self): return -1 if self.isEmpty() else self.head.val\n"
        "    def Rear(self):  return -1 if self.isEmpty() else self.tail.val\n"
        "    def isEmpty(self): return self.size == 0\n"
        "    def isFull(self):  return self.size == self.k\n"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("if not self.head: self.head = node", {"code": True}),
                   " — When adding the very first element, head and tail both point to the same node."])),
    N.para(N.rich([("if not self.head: self.tail = None", {"code": True}),
                   " — After dequeuing the last element, tail must be nulled; otherwise it's a dangling pointer to the removed node."])),
    N.para(N.rich([("def Rear(self): return self.tail.val", {"code": True}),
                   " — No modulo needed; we always have a direct pointer to the last node. This is simpler than the array version."])),
    N.divider(),
]

# ── Complexity ────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution",       "Time (all ops)", "Space"],
        ["Array Head/Tail/Count (optimal)", "O(1)",  "O(k)"],
        ["Linked List",    "O(1)",           "O(k) + O(k) pointers"],
    ]),
    N.divider(),
]

# ── Pattern Classification ─────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Design"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Array with Head/Tail (Circular Buffer / Ring Buffer)"])),
    N.callout(
        "When to recognize this pattern: problem says 'design a queue/buffer with fixed capacity', "
        "requires O(1) enqueue AND O(1) dequeue, and specifies that memory should be reused as "
        "elements are removed. Modulo arithmetic is the signature technique.",
        "🔎", "green_background"
    ),
    N.para(N.rich([("Note: ", {"italic": True}),
                   ("Array with Head/Tail", {"italic": True}),
                   (" is classified under the Design pattern category based on analysis. "
                    "The ring buffer technique is the canonical O(1) solution.", {"italic": True})])),
    N.divider(),
]

# ── Related Problems ───────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique (circular buffer / array with head and tail pointers):"),
    N.bullet(N.rich([("Design Circular Deque", {"bold": True}), " (Medium) — Same ring buffer; add enQueueFront and deQueueRear using (ptr-1+k)%k for backward pointer movement (#641)"])),
    N.bullet(N.rich([("Design Hit Counter", {"bold": True}), " (Medium) — Ring buffer of 300 slots tracking timestamps; hits older than 3000ms are evicted (#362)"])),
    N.bullet(N.rich([("Number of Recent Calls", {"bold": True}), " (Easy) — Queue-based sliding window; dequeue elements outside the 3000ms window (#933)"])),
    N.bullet(N.rich([("Sliding Window Maximum", {"bold": True}), " (Hard) — Monotonic deque over a fixed window; head and tail manage candidate retention (#239)"])),
    N.bullet(N.rich([("Implement Queue using Stacks", {"bold": True}), " (Easy) — Understand queue FIFO semantics before designing custom queue variants (#232)"])),
    N.bullet(N.rich([("Design Stack with Increment Operation", {"bold": True}), " (Medium) — Array-backed fixed stack with lazy O(1) bulk increment using a tag array (#1381)"])),
    N.para("These problems share the same core technique: fixed-size array with wrapping pointers to achieve O(1) amortized operations."),
    N.divider(),
]

# ── Interactive Embed ──────────────────────────────────────────
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("design_circular_queue")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.",
                    {"italic": True, "color": "gray"})])),
]

print(f"  Appending {len(blocks)} blocks...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
