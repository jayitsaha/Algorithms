"""
gen_implement_queue_using_stacks.py
Regenerate Notion page for LeetCode #232 — Implement Queue using Stacks.
"""
import sys
sys.path.insert(0, '/Users/j0s0yz3/Documents/PersonalSkillUp/Algorithms')
import notion_lib as N

PAGE_ID = "39193418-809c-81f7-b2cc-eeb6a1803efe"
SLUG = "implement_queue_using_stacks"

# ── Step 1: Set properties ────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Easy",
    number=232,
    pattern="Design",
    subpatterns=["Two Stacks"],
    tc="O(1) amortized",
    sc="O(n)",
    key_insight="Two stacks cancel each other's reversal: inbox receives pushes, outbox serves pops in FIFO order via lazy transfer.",
    icon="🟢"
)
print("Properties set.")

# ── Step 2: Wipe existing body ────────────────────────────────────────────────
print("Wiping old content...")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── Step 3: Build new body ────────────────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Implement a first in first out (FIFO) queue using only two stacks. The implemented queue should support all the functions of a normal queue — ", {}),
        ("push", {"code": True}), (", ", {}),
        ("pop", {"code": True}), (", ", {}),
        ("peek", {"code": True}), (", and ", {}),
        ("empty", {"code": True}), (".\n\n", {}),
        ("Implement the MyQueue class:\n", {"bold": True}),
        ("push(int x)", {"code": True}), (" — Pushes element x to the back of the queue.\n", {}),
        ("int pop()", {"code": True}), (" — Removes the element from the front of the queue and returns it.\n", {}),
        ("int peek()", {"code": True}), (" — Returns the element at the front of the queue.\n", {}),
        ("boolean empty()", {"code": True}), (" — Returns true if the queue is empty, false otherwise.\n\n", {}),
        ("Constraints: ", {"bold": True}),
        ("You must use only standard operations of a stack — push to top, peek/pop from top, size, and is empty. You may simulate a stack using a list or deque.", {}),
    ])),
    N.divider(),
]

# ── Solution 1: Two Stacks Lazy Transfer ──────────────────────────────────────
SOLUTION_1_CODE = '''\
class MyQueue:
    def __init__(self):
        self.stack_in = []   # inbox: receives all pushes
        self.stack_out = []  # outbox: serves pop/peek in FIFO order

    def _transfer(self):
        """Pour inbox → outbox only when outbox is empty (lazy)."""
        if not self.stack_out:
            while self.stack_in:
                self.stack_out.append(self.stack_in.pop())

    def push(self, x: int) -> None:
        self.stack_in.append(x)  # Always O(1)

    def pop(self) -> int:
        self._transfer()          # Ensure outbox has elements
        return self.stack_out.pop()  # Outbox top = queue front

    def peek(self) -> int:
        self._transfer()
        return self.stack_out[-1]  # Read without popping

    def empty(self) -> bool:
        # Must check BOTH stacks — element can be in either
        return not self.stack_in and not self.stack_out
'''

blocks += [
    N.h2("Solution 1 — Two Stacks, Lazy Transfer (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need FIFO using LIFO primitives. A stack reverses insertion order. Two stacks reverse twice — restoring original order. The question is just where and when to do the second reversal."),
        N.h4("What Doesn't Work"),
        N.para("A single stack can't give FIFO — popping always returns the most recently pushed element. You can't reorder elements without a second structure. Using a list with arbitrary access would violate the stack-only constraint."),
        N.h4("The Key Observation"),
        N.para("If we pour stack A into stack B, B's top is A's bottom — the oldest element. So if we pour inbox (stack_in) into outbox (stack_out), the outbox top is the queue front. This is exactly what pop/peek need."),
        N.h4("Building the Solution"),
        N.para("push always goes to stack_in — O(1). When we need to pop/peek, check if stack_out is empty. If so, pour everything from stack_in into stack_out (the lazy transfer). Then serve from stack_out top. Since elements stay in stack_out until consumed, subsequent pops are O(1)."),
        N.callout("Analogy: Inbox/Outbox tray on a desk. New mail goes to inbox (top = newest). When you process mail, flip the inbox stack into the outbox tray — now the oldest mail is on top. Work through the outbox; refill only when empty.", "🧠", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(SOLUTION_1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("__init__", {"code": True}), (" — Initialize two empty lists: stack_in receives all pushes; stack_out serves all pops and peeks.", {})])),
    N.para(N.rich([("_transfer()", {"code": True}), (" — Guard: only transfer when stack_out is empty. Inner loop pops from stack_in top and pushes to stack_out, reversing the order. Elements nearer the front (pushed earlier) end up closer to stack_out's top.", {})])),
    N.para(N.rich([("push(x)", {"code": True}), (" — Simply append to stack_in. O(1) unconditionally. No need to inspect stack_out.", {})])),
    N.para(N.rich([("pop()", {"code": True}), (" — Call _transfer() (may be a no-op if stack_out has elements), then pop from stack_out. The top of stack_out is always the queue front.", {})])),
    N.para(N.rich([("peek()", {"code": True}), (" — Identical setup to pop(), but use stack_out[-1] to read without removing.", {})])),
    N.para(N.rich([("empty()", {"code": True}), (" — Must check both stacks with 'and'. An element could be in stack_in (not yet transferred) or in stack_out (ready to serve). Checking only one gives wrong results.", {})])),
    N.divider(),
]

# ── Solution 2: Eager Transfer ─────────────────────────────────────────────────
SOLUTION_2_CODE = '''\
class MyQueue:
    def __init__(self):
        self.stack_in = []
        self.stack_out = []

    def push(self, x: int) -> None:
        # O(n): pour outbox back to inbox, insert x at bottom, pour back
        while self.stack_out:
            self.stack_in.append(self.stack_out.pop())
        self.stack_in.append(x)
        while self.stack_in:
            self.stack_out.append(self.stack_in.pop())

    def pop(self) -> int:
        return self.stack_out.pop()  # O(1): outbox always ready

    def peek(self) -> int:
        return self.stack_out[-1]    # O(1): outbox always ready

    def empty(self) -> bool:
        return not self.stack_out    # Only need to check stack_out
'''

blocks += [
    N.h2("Solution 2 — Two Stacks, Eager Transfer (O(n) push, O(1) pop)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("What if we do the work upfront on push, so pop is always trivially O(1)? Make the push expensive; make pop free."),
        N.h4("What Doesn't Work"),
        N.para("Doing this with one stack is impossible — we'd have no place to temporarily hold elements while inserting at the bottom."),
        N.h4("The Key Observation"),
        N.para("On each push: (1) pour stack_out back into stack_in (restore original push-order), (2) append the new element, (3) pour everything back to stack_out. Stack_out now always has the oldest element at top — ready for O(1) pop/peek."),
        N.h4("Building the Solution"),
        N.para("Push is O(n) due to the double transfer. Pop and peek are O(1) — no conditionals. Note: since stack_out is always kept current, empty() only needs to check stack_out."),
        N.callout("Trade-off: This approach is simpler to reason about for pop (always O(1)) but push is costly. Lazy transfer (Solution 1) is generally preferred because push is more frequent than pop in many real systems.", "⚠️", "yellow_background"),
    ]),
    N.h3("Code"),
    N.code(SOLUTION_2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("push — first while loop:", {"bold": True}), (" Restores elements from stack_out back to stack_in (undo previous ordering) so we can insert the new element in proper position.", {})])),
    N.para(N.rich([("push — stack_in.append(x):", {"bold": True}), (" Insert x into stack_in. After the first loop, stack_in holds elements in original push order, so appending x puts it at the back (newest).", {})])),
    N.para(N.rich([("push — second while loop:", {"bold": True}), (" Pour everything back to stack_out. Now stack_out has oldest at top, newest at bottom — correct FIFO serving order.", {})])),
    N.para(N.rich([("pop() / peek():", {"bold": True}), (" Simply read from stack_out top. O(1) always — no conditions needed because push always kept stack_out up-to-date.", {})])),
    N.para(N.rich([("empty():", {"bold": True}), (" Only stack_out needs checking since all elements always live in stack_out after each push completes.", {})])),
    N.divider(),
]

# ── Complexity ─────────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "push", "pop", "peek", "empty", "Space"],
        ["Lazy Transfer (Interview Pick)", "O(1)", "O(1) amortized", "O(1) amortized", "O(1)", "O(n)"],
        ["Eager Transfer", "O(n)", "O(1)", "O(1)", "O(1)", "O(n)"],
    ]),
    N.para(N.rich([
        ("Amortized analysis for Lazy Transfer: ", {"bold": True}),
        ("Each element is pushed to stack_in once, transferred once, and popped from stack_out once — at most 4 operations per element lifetime. Total cost for n elements: O(4n) = O(n) → O(1) amortized per operation.", {}),
    ])),
    N.divider(),
]

# ── Pattern Classification ────────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Design — implementing one abstract data type using another's primitives.", {})])),
    N.para(N.rich([("Sub-Pattern: ", {"bold": True}), ("Two Stacks — using two LIFO structures to simulate FIFO behavior via double reversal.", {})])),
    N.callout(
        "When to recognize this pattern: (1) Problem says 'implement X using only Y' where X and Y have opposite orderings. (2) You need FIFO behavior with only LIFO access. (3) Amortized O(1) is acceptable. (4) 'Double reversal = restoration' is the core trick.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique or closely related design patterns:"),
    N.bullet(N.rich([("Implement Stack using Queues", {"bold": True}), (" (Easy) — Reverse problem: simulate LIFO using FIFO queues. O(n) push or O(n) pop. LeetCode #225.", {})])),
    N.bullet(N.rich([("Min Stack", {"bold": True}), (" (Medium) — Augment stack with O(1) min-tracking using a parallel auxiliary stack. LeetCode #155.", {})])),
    N.bullet(N.rich([("Maximum Frequency Stack", {"bold": True}), (" (Hard) — Pop most-frequent element; stacks keyed by frequency level. LeetCode #895.", {})])),
    N.bullet(N.rich([("Design Circular Queue", {"bold": True}), (" (Medium) — Fixed-capacity FIFO queue using an array with head and tail pointers. LeetCode #622.", {})])),
    N.bullet(N.rich([("Sliding Window Maximum", {"bold": True}), (" (Hard) — Monotonic deque combining FIFO expiration with O(1) max access per window. LeetCode #239.", {})])),
    N.bullet(N.rich([("Design Browser History", {"bold": True}), (" (Medium) — Two stacks (back stack / forward stack) to simulate browser navigation. LeetCode #1472.", {})])),
    N.para("These problems share the core design insight: use auxiliary structures to bridge incompatible access patterns, trading worst-case cost for amortized efficiency."),
    N.callout("📚 Pattern: Design → Two Stacks (Queue Simulation). Amortized analysis is the mathematical justification for why this works efficiently.", "📚", "gray_background"),
]

# ── Embed ─────────────────────────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for(SLUG)),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys. Watch how elements move between stack_in and stack_out during the lazy transfer.",
         {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ─────────────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks to Notion...")
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
