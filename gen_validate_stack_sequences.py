"""
gen_validate_stack_sequences.py
Notion in-place update for LeetCode #946 Validate Stack Sequences
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = "39193418-809c-81c3-a55e-ecf20eb76558"

# ── 1) Set properties ──────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=946,
    pattern="Stacks",
    subpatterns=["Simulate Push/Pop"],
    tc="O(n)",
    sc="O(n)",
    key_insight="Push each element in order, then greedily pop while top matches the next expected pop; stack empty at end = valid.",
    icon="🟡"
)
print("Properties set.")

# ── 2) Wipe old content ────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# ── 3) Build new body ──────────────────────────────────────────────
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given two integer arrays ", {}),
        ("pushed", {"code": True}),
        (" and ", {}),
        ("popped", {"code": True}),
        (" of distinct values, return ", {}),
        ("true", {"code": True}),
        (" if this could have been the result of a sequence of push and pop operations on an initially empty stack, and ", {}),
        ("false", {"code": True}),
        (" otherwise.", {}),
    ])),
    N.para(N.rich([
        ("Example: pushed=[1,2,3,4,5], popped=[4,5,3,2,1] → True.\n"
         "Trace: push 1,2,3,4 → pop 4; push 5 → pop 5; pop 3,2,1. Valid!\n\n"
         "Example: pushed=[1,2,3,4,5], popped=[4,3,5,1,2] → False.\n"
         "After popping 4,3,5 the stack is [1,2]; popped wants 1 before 2 but 2 is on top. Invalid!", {})
    ])),
    N.divider(),
]

# ── Solution 1 — Greedy Stack Simulation ──
sol1_code = """\
def validateStackSequences(pushed: list[int], popped: list[int]) -> bool:
    stk = []          # simulation stack
    pop_idx = 0       # next expected pop index
    for x in pushed:
        stk.append(x)
        while stk and stk[-1] == popped[pop_idx]:
            stk.pop()
            pop_idx += 1
    return stk == []
"""

blocks += [
    N.h2("Solution 1 — Greedy Stack Simulation (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("We need to check whether a given pop ordering is achievable when pushing elements in a fixed order. A stack is LIFO — you can only remove the top element. The question is: can you interleave pushes (in the given order) and pops (in the given order) so both sequences are satisfied?"),
        N.h4("What Doesn't Work"),
        N.para("Brute force: try all possible interleavings of push/pop operations and see if any produce the given popped sequence. There are O(2^n) possible interleavings — exponential and completely impractical."),
        N.h4("The Key Observation"),
        N.para("You MUST push elements in order — no choice there. After each push, if the stack top equals the next expected pop, you SHOULD pop immediately. Delaying is strictly worse: any future push buries the element deeper, requiring more pops to reach it. But those future elements come later in the pop sequence — so our element must be popped before them. Delaying creates a contradiction. Therefore: greedy immediate pop is always correct."),
        N.h4("Building the Solution"),
        N.para("Maintain a simulation stack stk and a pointer pop_idx. For each x in pushed: push x unconditionally. Then while stk is non-empty and stk[-1] == popped[pop_idx], pop and advance pop_idx. After all pushes: stk empty = True, else False."),
        N.callout("Analogy: Imagine a valet parking lot where cars arrive in a fixed order (pushed) and customers pick up in a different order (popped). The lot is a dead-end lane — LIFO. The valet can only give you the last car parked. The simulation checks if the customer pickup order is achievable given the parking order.", "🚗", "blue_background"),
    ]),
    N.h3("Code"),
    N.code(sol1_code, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("stk = []", {"code": True}), (" — Simulation stack. Starts empty, just like the actual stack in the problem.", {})])),
    N.para(N.rich([("pop_idx = 0", {"code": True}), (" — Pointer into the popped array. popped[pop_idx] is the next value we expect to be popped.", {})])),
    N.para(N.rich([("for x in pushed:", {"code": True}), (" — We must push every element in pushed in order. This is mandatory — no skipping, no reordering.", {})])),
    N.para(N.rich([("stk.append(x)", {"code": True}), (" — Push x unconditionally. Every element must be pushed exactly once.", {})])),
    N.para(N.rich([("while stk and stk[-1] == popped[pop_idx]:", {"code": True}), (" — The greedy pop loop. Check two things: stack is non-empty (so stk[-1] is valid), and the top equals the next expected pop. Note: while not if — one push can trigger many pops.", {})])),
    N.para(N.rich([("stk.pop()", {"code": True}), (" — Remove the top element from the simulation stack.", {})])),
    N.para(N.rich([("pop_idx += 1", {"code": True}), (" — Advance to the next expected pop. We just satisfied one entry of the popped sequence.", {})])),
    N.para(N.rich([("return stk == []", {"code": True}), (" — If stack is empty, all elements were popped in the correct order. If non-empty, some element couldn't be reached at the right time.", {})])),
    N.divider(),
]

# ── Solution 2 — In-Place O(1) Space ──
sol2_code = """\
def validateStackSequences(pushed: list[int], popped: list[int]) -> bool:
    # Reuse pushed[] as the stack: write elements into it, track top index
    top = 0       # stack top pointer (0 means empty)
    pop_idx = 0
    for x in pushed:
        pushed[top] = x   # "push": overwrite at top position
        top += 1
        while top > 0 and pushed[top - 1] == popped[pop_idx]:
            top -= 1      # "pop": just decrement top pointer
            pop_idx += 1
    return top == 0       # empty stack iff top == 0
"""

blocks += [
    N.h2("Solution 2 — In-Place Simulation (O(1) Space Follow-up)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Same algorithm as Solution 1, but we want to avoid allocating a separate stack. Can we reuse the input array?"),
        N.h4("What Doesn't Work"),
        N.para("We cannot modify popped (we need it for matching). But we can overwrite pushed — once we process pushed[i] (push it), we no longer need it in its original form."),
        N.h4("The Key Observation"),
        N.para("We can use the pushed array itself as the stack: write x into pushed[top], increment top to push; decrement top to pop. The write position is always at or before the read position (since we process pushed left to right), so we never overwrite a value we still need."),
        N.h4("Building the Solution"),
        N.para("Replace stk.append(x) with pushed[top] = x; top += 1. Replace stk.pop() with top -= 1. Replace stk[-1] with pushed[top-1]. Replace stk == [] with top == 0."),
        N.callout("This is a classic 'reuse input as auxiliary storage' trick. Works here because the 'stack top' index is always ≤ current loop index i, so we never read a pushed[j] we've already overwritten.", "⚡", "yellow_background"),
    ]),
    N.h3("Code"),
    N.code(sol2_code, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("top = 0", {"code": True}), (" — Stack top pointer. top=0 means stack empty. pushed[0..top-1] is the stack contents.", {})])),
    N.para(N.rich([("pushed[top] = x; top += 1", {"code": True}), (" — 'Push' by writing x into pushed[top], then incrementing top. Equivalent to stk.append(x).", {})])),
    N.para(N.rich([("while top > 0 and pushed[top-1] == popped[pop_idx]:", {"code": True}), (" — 'Stack non-empty' becomes top > 0. 'Stack top' becomes pushed[top-1].", {})])),
    N.para(N.rich([("top -= 1", {"code": True}), (" — 'Pop' by decrementing top. The value is effectively discarded (overwritten on next push).", {})])),
    N.para(N.rich([("return top == 0", {"code": True}), (" — Empty stack iff top pointer is at 0.", {})])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Greedy Simulation", "O(n)", "O(n)"],
        ["In-Place Simulation", "O(n)", "O(1)"],
        ["Brute Force (all interleavings)", "O(2^n)", "O(n)"],
    ]),
    N.para("Time is O(n) amortized for both optimal solutions — each of the n elements is pushed once and popped at most once. The while loop does O(n) total work across the entire for loop, not O(n) per iteration."),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Stacks", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Simulate Push/Pop", {})])),
    N.callout(
        "When to recognize this pattern: The problem asks whether a sequence of events is achievable under stack (LIFO) constraints. Key phrases: 'could this be the result of push/pop operations', 'validate a stack sequence', 'is this pop order achievable'. Direct tell: you are given an ordered push sequence AND an ordered pop sequence.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Simulate Push/Pop technique:"),
    N.bullet(N.rich([("Valid Parentheses", {"bold": True}), (" (Easy) — Push opening brackets; pop and verify matching on closing bracket (#20)", {})])),
    N.bullet(N.rich([("Min Stack", {"bold": True}), (" (Medium) — Augment stack simulation to track running minimum alongside each element (#155)", {})])),
    N.bullet(N.rich([("Evaluate Reverse Polish Notation", {"bold": True}), (" (Medium) — Push operands onto stack; pop two and apply operator on every operator token (#150)", {})])),
    N.bullet(N.rich([("Exclusive Time of Functions", {"bold": True}), (" (Medium) — Stack simulates call/return events on a CPU timeline; pop on return (#636)", {})])),
    N.bullet(N.rich([("Basic Calculator II", {"bold": True}), (" (Medium) — Stack holds operands while processing operators with precedence (#227)", {})])),
    N.bullet(N.rich([("Remove All Adjacent Duplicates in String", {"bold": True}), (" (Easy) — Stack simulates greedy adjacent-pair removal in one pass (#1047)", {})])),
    N.bullet(N.rich([("Simplify Path", {"bold": True}), (" (Medium) — Stack simulates directory navigation; '..' triggers a pop (#71)", {})])),
    N.para("These problems share the core technique: use a stack to replay or validate a sequence of operations that obey LIFO ordering."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md Section 6.1 (Stack/Queue — Stack Simulation)", "📚", "gray_background"),
]

# ── Embed ──
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("validate_stack_sequences")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})
    ])),
]

# ── Append all blocks ──
N.append_blocks(PAGE_ID, blocks)
print(f"NOTION OK — {len(blocks)} blocks appended to {PAGE_ID}")
