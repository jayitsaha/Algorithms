"""
gen_next_greater_node_in_linked_list.py
Update Notion page for LeetCode #1019 — Next Greater Node In Linked List
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notion_lib as N

PAGE_ID = "39193418-809c-8149-853f-e9c5e6f4cd86"

# ── 1. Set properties ──────────────────────────────────────────────────────
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=1019,
    pattern="Stack / Queue",
    subpatterns=["Monotonic Stack (Next Greater)", "Convert to Array + Stack"],
    tc="O(n)",
    sc="O(n)",
    key_insight="Flatten linked list to array, then use a monotonic decreasing stack of indices; each element is pushed once and popped at most once, giving O(n) total.",
    icon="🟡"
)
print("Properties set OK")

# ── 2. Wipe old content ────────────────────────────────────────────────────
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks")

# ── 3. Build body ──────────────────────────────────────────────────────────

SOLUTION1_CODE = '''def nextLargerNodes(head):
    vals = []
    node = head
    while node:
        vals.append(node.val)
        node = node.next
    result = [0] * len(vals)
    stack = []                   # stores indices
    for i, val in enumerate(vals):
        while stack and vals[stack[-1]] < val:
            result[stack.pop()] = val
        stack.append(i)
    return result'''

SOLUTION2_CODE = '''def nextLargerNodes_brute(head):
    vals, node = [], head
    while node:
        vals.append(node.val)
        node = node.next
    result = [0] * len(vals)
    for i in range(len(vals)):
        for j in range(i + 1, len(vals)):
            if vals[j] > vals[i]:
                result[i] = vals[j]
                break
    return result'''

blocks = []

# Problem statement
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        "Given the ", ("head", {"code": True}),
        " of a linked list, return an array of answers where ",
        ("answers[i]", {"code": True}),
        " is the value of the next node that is strictly greater than the value of the ",
        ("i", {"code": True}), "-th node. If no such node exists, set ",
        ("answers[i] = 0", {"code": True}), "."
    ])),
    N.para("Example: 2 → 7 → 4 → 3 → 5 → Output: [7, 0, 5, 5, 0]. Node 0 (val=2): next greater is 7. Node 1 (val=7): no node greater than 7 to the right → 0. Nodes 2 and 3 (val=4, val=3): both answered by the 5 at position 4."),
    N.divider(),
]

# Solution 1 — Monotonic Stack
blocks += [
    N.h2("Solution 1 — Monotonic Stack (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("Strip away the linked list wrapper. The question is: for each position in a sequence, find the first value to the right that is strictly greater. This is the classic 'Next Greater Element' sub-problem."),
        N.h4("What Doesn't Work"),
        N.para("Naive O(n²): for each element, scan everything to the right. For n=50,000 nodes, that's 2.5 billion comparisons. The linked list also lacks random access, but we solve that by flattening to an array first."),
        N.h4("The Key Observation"),
        N.para("When scanning left to right, any element that hasn't yet 'met' a larger value is still waiting for its answer. A stack is perfect for holding these waiting elements. When a larger value arrives, it can resolve multiple waiting elements in one sweep — that's the O(n) magic."),
        N.h4("Building the Solution"),
        N.para("1. Flatten list to array vals[]. 2. Create result = [0]*n and stack = []. 3. For each i, val: while stack non-empty and vals[stack[-1]] < val, pop j and set result[j] = val. Push i. 4. Leftover stack = no answer (stays 0)."),
        N.callout("Analogy: Think of people in a queue watching a parade float to their right. Each person is 'waiting' to see a float taller than them. When a super-tall float comes, it simultaneously resolves the view for many people behind it. The stack is the queue of waiting viewers.", "🎡", "blue_background"),
    ]),
    N.h3("🔬 Algorithm Deep-Dive: Monotonic Stack"),
    N.para("The Monotonic Stack is a general pattern for problems asking 'what is the first/last element to the left/right satisfying condition X?' It maintains a stack of elements in monotonically increasing or decreasing order, popping when the invariant would be violated."),
    N.code('''# Monotonic Decreasing Stack Template (Next Greater)
result = [-1] * n
stack = []          # stores indices; values at these indices are non-increasing
for i in range(n):
    while stack and nums[stack[-1]] < nums[i]:
        result[stack.pop()] = nums[i]  # found the next greater!
    stack.append(i)
# Key: each element is pushed once and popped at most once → O(n) total'''),
    N.para("Why it's O(n): In the worst case, every element is pushed exactly once and popped exactly once. That's 2n operations total, regardless of the while loop's nesting inside the for loop. The amortized cost per element is O(1)."),
    N.para("When to recognize: 'For each element, find the first X to its right/left' — especially when X is a comparison (greater, smaller, equal). Also: histogram problems (largest rectangle), span problems (stock span), and water-trapping problems."),
    N.h3("Code"),
    N.code(SOLUTION1_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("vals = []", {"code": True}), " — Initialize an empty list to collect all linked list values."])),
    N.para(N.rich([("while node:", {"code": True}), " — Traverse the full linked list from head to tail."])),
    N.para(N.rich([("vals.append(node.val)", {"code": True}), " — Collect each node's integer value into the array."])),
    N.para(N.rich([("result = [0] * len(vals)", {"code": True}), " — Pre-fill result with 0 (the default for 'no next greater')."])),
    N.para(N.rich([("stack = []", {"code": True}), " — Monotonic stack storing indices of unresolved elements."])),
    N.para(N.rich([("for i, val in enumerate(vals):", {"code": True}), " — Scan every position left to right."])),
    N.para(N.rich([("while stack and vals[stack[-1]] < val:", {"code": True}), " — While the top of the stack has a smaller value than current, pop it."])),
    N.para(N.rich([("result[stack.pop()] = val", {"code": True}), " — Popped index j found its answer: the current val. Write result[j] = val."])),
    N.para(N.rich([("stack.append(i)", {"code": True}), " — Push current index; it is now waiting for something greater to the right."])),
    N.para(N.rich([("return result", {"code": True}), " — Remaining stack indices have 0 already (pre-initialized). Return the complete answer."])),
    N.divider(),
]

# Solution 2 — Brute Force
blocks += [
    N.h2("Solution 2 — Brute Force O(n²)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("The direct translation: for each node, look at everything to its right and return the first one that's larger."),
        N.h4("What Doesn't Work"),
        N.para("This is correct but too slow. O(n²) time — for n=10,000, that's 50M operations. For n=50,000, it's 1.25B operations. LeetCode will TLE."),
        N.h4("The Key Observation"),
        N.para("The brute force re-scans elements that have already been seen. The monotonic stack eliminates this redundancy by resolving multiple questions in one pass."),
        N.h4("Building the Solution"),
        N.para("1. Flatten to array. 2. For each index i, inner loop from i+1 to end. 3. First j where vals[j] > vals[i]: record it and break. 4. If inner loop exhausts, result[i] stays 0."),
    ]),
    N.h3("Code"),
    N.code(SOLUTION2_CODE),
    N.h3("Line by Line"),
    N.para(N.rich([("for i in range(len(vals)):", {"code": True}), " — Outer loop: each element is the 'query' element."])),
    N.para(N.rich([("for j in range(i+1, len(vals)):", {"code": True}), " — Inner loop: scan every element to the right."])),
    N.para(N.rich([("if vals[j] > vals[i]:", {"code": True}), " — Found the first larger element."])),
    N.para(N.rich([("break", {"code": True}), " — Stop at the FIRST greater element, not the maximum."])),
    N.divider(),
]

# Complexity
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (nested loops)", "O(n²)", "O(n)"],
        ["Monotonic Stack (optimal)", "O(n)", "O(n)"],
    ]),
    N.divider(),
]

# Pattern Classification
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), "Stack / Queue (specifically: Monotonic Stack)"])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), "Monotonic Stack (Next Greater), Convert to Array + Stack"])),
    N.callout("When to recognize this pattern: 'Next greater / smaller / warmer element for each position', 'for each element find the first X to its right', 'elements waiting for a condition to be met by future elements'. Also: histogram largest rectangle (previous smaller variant), water trapping problems.", "🔎", "green_background"),
    N.divider(),
]

# Related Problems
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same Monotonic Stack technique:"),
    N.bullet(N.rich([("Next Greater Element I", {"bold": True}), " (Easy) — Next greater from a second array, same stack pattern (#496)"])),
    N.bullet(N.rich([("Next Greater Element II", {"bold": True}), " (Medium) — Circular array, scan twice (#503)"])),
    N.bullet(N.rich([("Daily Temperatures", {"bold": True}), " (Medium) — Output days until next warmer; same exact pattern (#739)"])),
    N.bullet(N.rich([("Largest Rectangle in Histogram", {"bold": True}), " (Hard) — Previous smaller element variant (#84)"])),
    N.bullet(N.rich([("Trapping Rain Water", {"bold": True}), " (Hard) — 'Waiting for taller walls' — same intuition (#42)"])),
    N.bullet(N.rich([("Remove Nodes From Linked List", {"bold": True}), " (Medium) — Monotonic stack on a linked list, same idea (#2487)"])),
    N.bullet(N.rich([("Sum of Subarray Minimums", {"bold": True}), " (Medium) — Previous and next smaller combined (#907)"])),
    N.para("These problems share the core technique: a monotonic stack that keeps 'waiting' elements until the right condition is met by a future element."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Stack/Queue section → Monotonic Stack: Next Greater", "📚", "gray_background"),
]

# Embed
blocks += [
    N.divider(),
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("next_greater_node_in_linked_list")),
    N.para(N.rich([("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})])),
]

# Append all blocks
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
