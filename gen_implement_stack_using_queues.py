"""
gen_implement_stack_using_queues.py
Notion page creator for LeetCode #225 — Implement Stack using Queues
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

# ── 1. Create the page (notion_page_id was null) ──────────────────────────────
PAGE_ID = "39293418-809c-81b2-9d49-fd506b526d91"  # already created
print(f"Using page: {PAGE_ID}")

# ── 2. Set properties ─────────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=225,
    pattern="Data Structure Design",
    subpatterns=["One Queue Rotate"],  # no comma in multi_select option
    tc="O(n) push, O(1) pop/top/empty",
    sc="O(n)",
    key_insight="Rotate all old elements behind the new push so the queue front always equals the stack top.",
    icon="🟢"
)
print("Properties set.")

# ── 3. Build page body ────────────────────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Implement a last-in-first-out (LIFO) stack using only two queues. The implemented stack should support all the functions of a normal stack ("), ("push", {"code": True}), (", "), ("pop", {"code": True}), (", "), ("top", {"code": True}), (", and "), ("empty", {"code": True}), (").\n\n"),
        ("push(x)", {"code": True}), (" — Push element x to the top of the stack.\n"),
        ("pop()", {"code": True}), (" — Removes the element on top of the stack and returns it.\n"),
        ("top()", {"code": True}), (" — Get the top element.\n"),
        ("empty()", {"code": True}), (" — Returns true if the stack is empty, false otherwise.\n\n"),
        ("Constraint: You must use only standard queue operations — push to back, peek/pop from front, size, and isEmpty."),
    ])),
    N.divider(),
]

# ── Solution 1: One Queue Rotate (Interview Pick) ──────────────────────────────
sol1_code = """\
from collections import deque

class MyStack:
    def __init__(self):
        self.q = deque()         # one queue; front = stack top (invariant)

    def push(self, x: int) -> None:
        self.q.append(x)         # enqueue at back (not top yet)
        for _ in range(len(self.q) - 1):  # rotate n-1 old elements behind x
            self.q.append(self.q.popleft())   # dequeue front, re-enqueue at back

    def pop(self) -> int:
        return self.q.popleft()  # front = stack top; O(1)

    def top(self) -> int:
        return self.q[0]         # peek front; O(1)

    def empty(self) -> bool:
        return not self.q        # empty deque is falsy; O(1)
"""

blocks += [
    N.h2("Solution 1 — One Queue, Rotate on Push (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("A queue hands you elements oldest-first (FIFO). A stack needs elements newest-first (LIFO). The orderings are exact opposites. I need to reverse the order using only queue operations."),
        N.h4("What Doesn't Work"),
        N.para("Simply enqueuing elements gives them in insertion order — the exact opposite of what stack.pop() should return. I can't peek at the back of a queue (only the front), so I can't just 'read' the most-recent element without restructuring."),
        N.h4("The Key Observation"),
        N.para("If I maintain the invariant that the QUEUE FRONT always holds the STACK TOP, then pop() becomes a trivial dequeue and top() is a trivial peek. The question is: how do I maintain that invariant on each push?"),
        N.h4("Building the Solution"),
        N.para("After enqueuing x at the back, there are n-1 old elements in front of it. If I cycle each of those old elements through (dequeue front, enqueue back) n-1 times, they all move behind x, leaving x at the front. Cost: O(n) per push. Reward: O(1) pop and top forever."),
        N.callout("Analogy: Imagine a line of people. The newest arrival joins the back. Then every person in front of them goes to the end of the line, one by one. When the cycle ends, the new arrival is at the head of the line.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(sol1_code),
    N.h3("Line by Line"),
    N.para(N.rich([("from collections import deque", {"code": True}), " — Python's deque gives O(1) popleft(). A plain list's pop(0) is O(n) and would violate the spirit of 'queue operations only'."])),
    N.para(N.rich([("self.q = deque()", {"code": True}), " — Single queue. Invariant we maintain: after every push, the queue front = the stack top."])),
    N.para(N.rich([("self.q.append(x)", {"code": True}), " — Enqueue x at the back. At this point x is not the top yet; it's stuck at the end."])),
    N.para(N.rich([("for _ in range(len(self.q) - 1):", {"code": True}), " — Rotate exactly n-1 times (not n). After appending, the queue has n elements; we cycle the n-1 old ones behind x."])),
    N.para(N.rich([("self.q.append(self.q.popleft())", {"code": True}), " — Each iteration: dequeue the front element and re-enqueue it at the back. After n-1 such moves, x is at the front."])),
    N.para(N.rich([("return self.q.popleft()", {"code": True}), " — Dequeue the front = stack top. O(1). No rotation needed — the invariant is auto-maintained after a pop (next element slides to front)."])),
    N.para(N.rich([("return self.q[0]", {"code": True}), " — Peek front without removing. O(1). Always the current stack top by our invariant."])),
    N.para(N.rich([("return not self.q", {"code": True}), " — An empty deque is falsy in Python. O(1) check."])),
    N.divider(),
]

# ── Solution 2: Two Queues ────────────────────────────────────────────────────
sol2_code = """\
from collections import deque

class MyStack:
    def __init__(self):
        self.q1 = deque()   # main queue (front = stack top)
        self.q2 = deque()   # helper queue (empty except during push)

    def push(self, x: int) -> None:
        self.q2.append(x)              # push x into helper
        while self.q1:                 # drain main into helper
            self.q2.append(self.q1.popleft())
        self.q1, self.q2 = self.q2, self.q1  # swap — q1 now has x at front

    def pop(self) -> int:
        return self.q1.popleft()       # O(1)

    def top(self) -> int:
        return self.q1[0]              # O(1)

    def empty(self) -> bool:
        return not self.q1             # O(1)
"""

blocks += [
    N.h2("Solution 2 — Two Queues, Drain on Push"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same goal: keep the most-recently-pushed element accessible in O(1). Instead of rotating in a single queue, use a helper queue to rebuild the queue with x at the front."),
        N.h4("What Doesn't Work"),
        N.para("Using two queues doesn't improve worst-case complexity — still O(n) push. It trades the in-place rotation for a drain-and-swap idiom. Some find this easier to reason about; it requires tracking two queue references."),
        N.h4("The Key Observation"),
        N.para("After pushing x into the empty helper queue, drain the entire main queue into helper. Now helper has [x, ...old elements]. Swap q1 and q2 references — q1 is now the 'full' queue with x at front, q2 is empty and ready for next push."),
        N.h4("Building the Solution"),
        N.para("push: enqueue x to q2, drain all of q1 into q2, swap. This gives the same invariant: q1's front = stack top. pop/top/empty are identical to Solution 1 — they only touch q1."),
        N.callout("Trade-off: Two queues uses the same O(n) push and O(1) pop, but at the cost of tracking two queue objects and a reference swap. One-queue rotate is preferred in interviews for simplicity.", "⚖️", "yellow_background"),
    ]),
    N.h3("Code"),
    N.code(sol2_code),
    N.h3("Line by Line"),
    N.para(N.rich([("self.q1, self.q2 = deque(), deque()", {"code": True}), " — q1 is the active queue (front = stack top); q2 is always empty except during a push."])),
    N.para(N.rich([("self.q2.append(x)", {"code": True}), " — Push x into the helper (it will become the new front)."])),
    N.para(N.rich([("while self.q1: self.q2.append(self.q1.popleft())", {"code": True}), " — Drain all of q1 into q2 behind x. Now q2 = [x, old...]."])),
    N.para(N.rich([("self.q1, self.q2 = self.q2, self.q1", {"code": True}), " — Swap references. q1 now holds [x, old...] with x at front; q2 is empty for next use."])),
    N.divider(),
]

# ── Complexity ────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "push(x)", "pop()", "top()", "empty()", "Space"],
        ["One Queue Rotate", "O(n)", "O(1)", "O(1)", "O(1)", "O(n)"],
        ["Two Queues", "O(n)", "O(1)", "O(1)", "O(1)", "O(n)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ─────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Data Structure Design"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "One Queue, Rotate — verified in DSA_Patterns_and_SubPatterns_Guide.md Section 15 (Data Structure Design)."])),
    N.callout(
        "When to recognise this pattern:\n"
        "• Asked to implement ADT X using only operations of ADT Y\n"
        "• The two ADTs have opposite access order (FIFO vs LIFO)\n"
        "• You cannot use any data structure outside the permitted set\n"
        "• Interview problem says 'only push to back / pop from front'",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique or design theme:"),
    N.bullet(N.rich([("Implement Queue using Stacks", {"bold": True}), " (Easy, LC 232) — symmetric problem; two stacks + amortized O(1) dequeue"])),
    N.bullet(N.rich([("Min Stack", {"bold": True}), " (Medium, LC 155) — augment stack for O(1) getMin; auxiliary stack tracks running minimum"])),
    N.bullet(N.rich([("Design Circular Queue", {"bold": True}), " (Medium, LC 622) — fixed-size queue with array, head/tail pointers, modulo wrap"])),
    N.bullet(N.rich([("Max Stack", {"bold": True}), " (Hard, LC 716) — stack that supports O(1) popMax; two stacks or doubly linked list + TreeMap"])),
    N.bullet(N.rich([("Design Hit Counter", {"bold": True}), " (Medium, LC 362) — deque or circular buffer; same 'keep only recent' design theme"])),
    N.bullet(N.rich([("LRU Cache", {"bold": True}), " (Medium, LC 146) — doubly linked list + hash map; exemplary data structure composition design"])),
    N.bullet(N.rich([("Maximum Frequency Stack", {"bold": True}), " (Hard, LC 895) — frequency buckets + stacks; pop the most-frequent element design"])),
    N.para("These problems share the core theme: composing one data structure from another, maintaining a carefully chosen invariant to achieve the required access pattern."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 15 (Data Structure Design)", "📚", "gray_background"),
    N.divider(),
]

# ── Embed ─────────────────────────────────────────────────────────────────────
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("implement_stack_using_queues")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ─────────────────────────────────────────────────────────
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
print(f"Page URL: https://www.notion.so/{PAGE_ID.replace('-','')}")
