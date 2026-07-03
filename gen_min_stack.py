"""gen_min_stack.py — Notion page builder for Min Stack (LC #155)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-8187-a132-f18ebce563b8"

# ── 1) Set properties ─────────────────────────────────────────────────────
print("Setting properties...")
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=155,
    pattern="Stacks",
    subpatterns=["Auxiliary Stack for Mins"],
    tc="O(1) all ops",
    sc="O(n)",
    key_insight="Parallel min stack records global minimum at every depth; pop both stacks to restore previous min in O(1).",
    icon="🟡",
)
print("Properties set.")

# ── 2) Wipe old body ──────────────────────────────────────────────────────
print("Wiping old body...")
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} blocks.")

# ── 3) Build new body ─────────────────────────────────────────────────────
blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Design a stack that supports ", {}),
        ("push", {"code": True}),
        (", ", {}),
        ("pop", {"code": True}),
        (", ", {}),
        ("top", {"code": True}),
        (", and ", {}),
        ("getMin", {"code": True}),
        (" operations, all in O(1) time.\n\n"
         "Implement the MinStack class:\n"
         "• MinStack() initializes the stack object.\n"
         "• void push(int val) pushes the element val onto the stack.\n"
         "• void pop() removes the element on top of the stack.\n"
         "• int top() gets the top element of the stack.\n"
         "• int getMin() retrieves the minimum element in the stack.", {})
    ])),
    N.divider(),
]

# ── Solution 1 — Auxiliary Min Stack ──────────────────────────────────────
blocks += [
    N.h2("Solution 1 — Auxiliary Min Stack (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need a stack where querying the current minimum is always O(1), even after arbitrary pushes and pops. The key difficulty: pop() can change the minimum, so we can't just track a single global min variable."),
        N.h4("What Doesn't Work"),
        N.para("A single 'cur_min' variable updates correctly on push (take the smaller of incoming val and cur_min), but breaks on pop: if we pop the current minimum, we have no way to recover the previous minimum without scanning the entire remaining stack — O(n)."),
        N.h4("The Key Observation"),
        N.para("At every depth level d, there is a well-defined 'minimum of stack[0..d]'. This value is stable until an element is popped. If we store this value alongside each main-stack entry, we can retrieve it in O(1) at any point."),
        N.h4("Building the Solution"),
        N.para("Maintain two stacks in lockstep: self.stack (all values) and self.min_stack (min_stack[i] = min(stack[0..i])). On push: append val to stack, append min(val, min_stack[-1]) to min_stack. On pop: pop both stacks simultaneously — the previous min is automatically revealed. getMin() reads min_stack[-1]. All ops are O(1)."),
        N.callout(
            "Analogy: Think of min_stack as a 'shadow record' of history. Every time you add something to the main stack, your shadow records what the minimum was at that moment. When you remove an item, the shadow removes that moment too, instantly revealing the previous record.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("Code"),
    N.code(
        "class MinStack:\n"
        "    def __init__(self):\n"
        "        self.stack = []\n"
        "        self.min_stack = []  # min_stack[i] = min(stack[0..i])\n"
        "\n"
        "    def push(self, val: int) -> None:\n"
        "        self.stack.append(val)\n"
        "        if self.min_stack:\n"
        "            self.min_stack.append(min(val, self.min_stack[-1]))\n"
        "        else:\n"
        "            self.min_stack.append(val)  # first element is trivially the min\n"
        "\n"
        "    def pop(self) -> None:\n"
        "        self.stack.pop()\n"
        "        self.min_stack.pop()  # pop both to reveal previous min\n"
        "\n"
        "    def top(self) -> int:\n"
        "        return self.stack[-1]\n"
        "\n"
        "    def getMin(self) -> int:\n"
        "        return self.min_stack[-1]  # always the global minimum"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("self.stack = []; self.min_stack = []", {"code": True}), (" — Two parallel lists initialized empty. They will always have equal length.", {})])),
    N.para(N.rich([("self.stack.append(val)", {"code": True}), (" — Push the incoming value onto the main stack unconditionally.", {})])),
    N.para(N.rich([("min(val, self.min_stack[-1])", {"code": True}), (" — The new global minimum is the smaller of the incoming value and the existing global minimum (min_stack top).", {})])),
    N.para(N.rich([("self.min_stack.append(val)", {"code": True}), (" (else branch) — First element ever pushed: it is trivially the minimum of a one-element stack.", {})])),
    N.para(N.rich([("self.stack.pop(); self.min_stack.pop()", {"code": True}), (" — Pop both stacks simultaneously. The paired min record is removed, revealing the previous min at min_stack[-1].", {})])),
    N.para(N.rich([("return self.stack[-1]", {"code": True}), (" — top(): single O(1) array index into the main stack.", {})])),
    N.para(N.rich([("return self.min_stack[-1]", {"code": True}), (" — getMin(): single O(1) array index into the min stack. This is always the global minimum of all current elements.", {})])),
    N.divider(),
]

# ── Solution 2 — Tuple-based ──────────────────────────────────────────────
blocks += [
    N.h2("Solution 2 — Store (val, cur_min) Tuples"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Instead of two separate stacks, can we pack both pieces of information (the value, and the minimum at this depth) into a single data structure? Yes — store tuples."),
        N.h4("What Doesn't Work"),
        N.para("Two separate stacks are perfectly correct but carry two separate objects. In Python, a single list of 2-tuples (val, cur_min) achieves identical semantics with one fewer data structure to manage."),
        N.h4("The Key Observation"),
        N.para("Both approaches store exactly the same information — (val, min_at_this_depth) per level. The tuple approach packs it tighter and makes the pairing explicit and impossible to de-sync."),
        N.h4("Building the Solution"),
        N.para("Each push appends (val, min(val, stack[-1][1])) if stack is non-empty, else (val, val). Pop removes the top tuple. top() returns stack[-1][0]. getMin() returns stack[-1][1]. All O(1)."),
    ]),
    N.h3("Code"),
    N.code(
        "class MinStack:\n"
        "    def __init__(self):\n"
        "        self.stack = []  # each entry: (value, min_at_this_depth)\n"
        "\n"
        "    def push(self, val: int) -> None:\n"
        "        cur_min = min(val, self.stack[-1][1]) if self.stack else val\n"
        "        self.stack.append((val, cur_min))\n"
        "\n"
        "    def pop(self) -> None:\n"
        "        self.stack.pop()\n"
        "\n"
        "    def top(self) -> int:\n"
        "        return self.stack[-1][0]  # first element of top tuple\n"
        "\n"
        "    def getMin(self) -> int:\n"
        "        return self.stack[-1][1]  # second element of top tuple"
    ),
    N.h3("Line by Line"),
    N.para(N.rich([("self.stack[-1][1]", {"code": True}), (" (in push) — Access the cur_min from the previous top tuple; use it to compute the new cur_min.", {})])),
    N.para(N.rich([("self.stack.append((val, cur_min))", {"code": True}), (" — Pack value and its corresponding minimum into a tuple; a single pop() later removes both atomically.", {})])),
    N.para(N.rich([("return self.stack[-1][0]", {"code": True}), (" — top(): index [0] of the top tuple is the actual value.", {})])),
    N.para(N.rich([("return self.stack[-1][1]", {"code": True}), (" — getMin(): index [1] of the top tuple is the minimum at this depth. O(1).", {})])),
    N.divider(),
]

# ── Complexity ────────────────────────────────────────────────────────────
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "push", "pop", "top", "getMin", "Space"],
        ["Naive (scan for min)", "O(1)", "O(1)", "O(1)", "O(n)", "O(n)"],
        ["Auxiliary Min Stack (✓ Interview Pick)", "O(1)", "O(1)", "O(1)", "O(1)", "O(n)"],
        ["Tuple (val, cur_min)", "O(1)", "O(1)", "O(1)", "O(1)", "O(n)"],
    ]),
    N.divider(),
]

# ── Pattern Classification ────────────────────────────────────────────────
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Stacks", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Auxiliary Stack for Mins — tracking running minimum at every depth level with a parallel stack.", {})])),
    N.callout(
        "When to recognize this pattern:\n"
        "• 'O(1) access to min/max/sum of a changing stack'\n"
        "• 'History-dependent query' — answer depends on when elements were pushed\n"
        "• Design problems requiring rollback or undo capabilities\n"
        "• Any scenario where a naive aggregate requires O(n) scan but O(1) is required",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──────────────────────────────────────────────────────
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same or closely related auxiliary-stack technique:"),
    N.bullet(N.rich([("Max Stack", {"bold": True}), (" (Hard) — Auxiliary stack for running maximum; same structure, replace min() with max() (#716)", {})])),
    N.bullet(N.rich([("Sliding Window Maximum", {"bold": True}), (" (Hard) — Monotonic deque tracks running max for a sliding window; generalizes the idea (#239)", {})])),
    N.bullet(N.rich([("Online Stock Span", {"bold": True}), (" (Medium) — Stack tracks spans of non-increasing prices; auxiliary structure idea (#901)", {})])),
    N.bullet(N.rich([("Daily Temperatures", {"bold": True}), (" (Medium) — Monotonic stack tracks 'next greater element' for each day (#739)", {})])),
    N.bullet(N.rich([("Valid Parentheses", {"bold": True}), (" (Easy) — Classic stack usage; stack maintains match history (#20)", {})])),
    N.bullet(N.rich([("Implement Queue using Stacks", {"bold": True}), (" (Easy) — Stack-based data structure design question (#232)", {})])),
    N.para("These problems share the core insight: a stack (or deque) can maintain an ordering invariant or historical aggregate with O(1) updates and reads."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Stack/Queue section · Sub-Pattern: Auxiliary Stack for Mins", "📚", "gray_background"),
]

# ── Visual Explainer embed ────────────────────────────────────────────────
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("min_stack")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

# ── Append all blocks ─────────────────────────────────────────────────────
print(f"Appending {len(blocks)} blocks...")
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK {PAGE_ID}")
