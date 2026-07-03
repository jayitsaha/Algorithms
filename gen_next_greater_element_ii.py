"""
gen_next_greater_element_ii.py
Notion page creation for LeetCode #503 Next Greater Element II
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import notion_lib as N

PAGE_ID = None  # No existing page — create one

if PAGE_ID is None:
    PAGE_ID = N.create_page("Next Greater Element II", 503, "Medium", "🟡")
    print("Created new page:", PAGE_ID)

# 1) Set properties
N.set_properties(
    PAGE_ID,
    difficulty="Medium",
    number=503,
    pattern="Stack / Queue",
    subpatterns=["Circular Array + 2 Passes"],
    tc="O(n)",
    sc="O(n)",
    key_insight="Simulate two passes with i % n; push only in first pass; monotonic stack resolves each element exactly once.",
    icon="🟡"
)
print("Properties set.")

# 2) Wipe any old body
wiped = N.wipe_page(PAGE_ID)
print(f"Wiped {wiped} old blocks.")

# 3) Build body blocks
blocks = []

# ── Problem ──
blocks += [
    N.h2("Problem"),
    N.para(N.rich([
        ("Given a ", {}),
        ("circular", {"bold": True}),
        (" integer array ", {}),
        ("nums", {"code": True}),
        (", return the next greater number for every element in ", {}),
        ("nums", {"code": True}),
        (". The next greater number of a number x is the first greater number to its traversal-order next in the array. If it doesn't exist, return ", {}),
        ("-1", {"code": True}),
        (" for this number. Because the array is ", {}),
        ("circular", {"bold": True}),
        (", the next element of the last element is the first element of the array.", {}),
    ])),
    N.divider(),
]

# ── Solution 1 ──
SOLUTION_1_CODE = """def nextGreaterElements(nums: list[int]) -> list[int]:
    n = len(nums)
    result = [-1] * n   # default: no next greater
    stack = []          # monotonic stack of indices (waiting for next greater)
    for i in range(2 * n):         # simulate two circular passes
        while stack and nums[stack[-1]] < nums[i % n]:
            result[stack.pop()] = nums[i % n]  # found the answer!
        if i < n:                  # only push in first pass
            stack.append(i)
    return result"""

blocks += [
    N.h2("Solution 1 — Monotonic Stack, 2-Pass Circular (Interview Pick)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("For each index, we need the first value to its right (circularly) that is strictly larger. This is the classic 'next greater element' pattern, but with a circular twist."),
        N.h4("What Doesn't Work"),
        N.para("Brute force: for each element, scan all n-1 others using modulo. This is O(n²). We need a way to avoid re-scanning elements we've already 'decided' about."),
        N.h4("The Key Observation"),
        N.para("A monotonic decreasing stack lets us defer answering each element's question until we encounter something larger. Elements on the stack are 'waiting' in non-increasing value order. When a larger value arrives, it answers everything it beats — in one sweep from left to right."),
        N.h4("Building the Solution"),
        N.para("To handle circularity: loop 2n times, use i % n to access array values. Push indices only in the first pass (i < n). In the second pass, only pop to resolve remaining unresolved entries. Each index is pushed once and popped at most once → O(n) amortized."),
        N.callout(
            "Analogy: Imagine people in a circular queue, each looking for the next taller person. A monotonic stack lets us 'announce' each person's answer the moment a taller person walks by — without scanning the whole queue each time.",
            "🧠", "blue_background"
        ),
    ]),
    N.h3("🔬 Algorithm Deep-Dive: Monotonic Stack"),
    N.para(N.rich([
        ("Monotonic Stack", {"bold": True}),
        (" — A stack that maintains a monotonically increasing or decreasing sequence of values. For 'next greater element' problems, we use a decreasing stack: when the current value is greater than the top, pop and record the answer. Runs in O(n) amortized because each element is pushed once and popped once.", {}),
    ])),
    N.code(
        "# Monotonic stack template for 'next greater element'\nresult = [-1] * n\nstack = []  # indices\nfor i in range(n):\n    while stack and nums[stack[-1]] < nums[i]:\n        result[stack.pop()] = nums[i]  # found next greater!\n    stack.append(i)\n# Circular variant: loop range(2*n), use i%n, push only if i<n",
        "python"
    ),
    N.para("Core invariant: stack values are non-increasing from bottom to top. When a larger value arrives, it is the FIRST greater element for everything it beats on the stack (because we process left to right without skipping)."),
    N.h3("Code"),
    N.code(SOLUTION_1_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("n = len(nums)", {"code": True}), (" — store array length; used in modulo i%n and push guard i<n.", {})])),
    N.para(N.rich([("result = [-1] * n", {"code": True}), (" — initialize all answers to -1 (default: no next greater found). Elements with global max value keep this answer.", {})])),
    N.para(N.rich([("stack = []", {"code": True}), (" — empty monotonic stack that will hold indices (not values) of elements waiting for their next greater.", {})])),
    N.para(N.rich([("for i in range(2 * n):", {"code": True}), (" — the 2-pass loop. i=0..n-1 is pass 1 (first traversal); i=n..2n-1 is pass 2 (simulated wrap-around). Both use nums[i%n].", {})])),
    N.para(N.rich([("while stack and nums[stack[-1]] < nums[i % n]:", {"code": True}), (" — as long as the stack is non-empty AND the current value is STRICTLY greater than the value at the stack top index, we have found the next greater for that top.", {})])),
    N.para(N.rich([("result[stack.pop()] = nums[i % n]", {"code": True}), (" — pop the top index, write the current value as its answer. This index is now fully resolved.", {})])),
    N.para(N.rich([("if i < n:", {"code": True}), (" — ONLY push during the first pass. Each index must appear on the stack at most once. Second pass uses values only to trigger pops.", {})])),
    N.para(N.rich([("stack.append(i)", {"code": True}), (" — push the current index; it's waiting for something greater to its circular right.", {})])),
    N.para(N.rich([("return result", {"code": True}), (" — any indices still on the stack have no greater element even after a full circle. Their -1 default stands.", {})])),
    N.divider(),
]

# ── Solution 2 ──
SOLUTION_2_CODE = """def nextGreaterElements_brute(nums: list[int]) -> list[int]:
    n = len(nums)
    result = [-1] * n
    for i in range(n):             # for each element
        for j in range(1, n):      # check up to n-1 circular neighbors
            nxt = nums[(i + j) % n]
            if nxt > nums[i]:
                result[i] = nxt
                break              # stop at the FIRST greater
    return result"""

blocks += [
    N.h2("Solution 2 — Brute Force, O(n²)"),
    N.toggle_h3("💡 Intuition: How to Arrive at This", [
        N.h4("Reframe the Problem"),
        N.para("For each position, search the remaining n-1 circular neighbors one by one until we find a larger value. Simple and direct."),
        N.h4("What Doesn't Work"),
        N.para("This approach is O(n²) — for each of n elements, we scan up to n-1 others. Fine for small arrays or interview clarity, but will TLE for large n."),
        N.h4("The Key Observation"),
        N.para("The modulo trick (i + j) % n correctly wraps the search around the circular array. The inner break ensures we stop at the FIRST greater element, not just any."),
        N.h4("Building the Solution"),
        N.para("Double loop: outer over all indices, inner starting 1 position ahead and going up to n-1 positions ahead (wrapping). When we find nxt > nums[i], record and break."),
    ]),
    N.h3("Code"),
    N.code(SOLUTION_2_CODE, "python"),
    N.h3("Line by Line"),
    N.para(N.rich([("for i in range(n):", {"code": True}), (" — outer loop over each element in the array.", {})])),
    N.para(N.rich([("for j in range(1, n):", {"code": True}), (" — inner loop: j=1 means one step ahead, j=n-1 means one step before wrapping full circle. We never look at i itself (j starts at 1).", {})])),
    N.para(N.rich([("nums[(i + j) % n]", {"code": True}), (" — circular indexing. When (i+j) exceeds n-1, modulo wraps it back to the front.", {})])),
    N.para(N.rich([("break", {"code": True}), (" — stop inner loop as soon as we find the FIRST greater element (not just any greater). This is the definition of 'next greater'.", {})])),
    N.divider(),
]

# ── Complexity ──
blocks += [
    N.h2("Complexity"),
    N.table([
        ["Solution", "Time", "Space"],
        ["Brute Force (nested loops)", "O(n²)", "O(n) output only"],
        ["Monotonic Stack + 2 Passes", "O(n)", "O(n) stack + output"],
    ]),
    N.divider(),
]

# ── Pattern Classification ──
blocks += [
    N.h2("🏷️ Pattern Classification"),
    N.para(N.rich([("Main Pattern: ", {"bold": True}), ("Stack / Queue — Monotonic Stack", {})])),
    N.para(N.rich([("Sub-Pattern(s): ", {"bold": True}), ("Circular Array, 2 Passes", {})])),
    N.callout(
        "When to recognize this pattern: 'next greater/smaller element to the right' + 'circular array' or 'wrap around'. The combination of monotonic stack (for O(n) next-greater) and 2-pass with i%n (for circular) is the canonical solution.",
        "🔎", "green_background"
    ),
    N.divider(),
]

# ── Related Problems ──
blocks += [
    N.h2("🔗 Related Problems"),
    N.para("Problems using the same technique:"),
    N.bullet(N.rich([("Next Greater Element I", {"bold": True}), (" (Easy) — Non-circular version; find next greater using a hash map for element-to-answer lookup. #496", {})])),
    N.bullet(N.rich([("Daily Temperatures", {"bold": True}), (" (Medium) — Same monotonic stack, but store number of days (index distance) instead of value. #739", {})])),
    N.bullet(N.rich([("Largest Rectangle in Histogram", {"bold": True}), (" (Hard) — Monotonic increasing stack to find nearest smaller bars on both left and right. #84", {})])),
    N.bullet(N.rich([("Trapping Rain Water", {"bold": True}), (" (Hard) — Monotonic stack approach: find left/right boundaries for each bar. #42", {})])),
    N.bullet(N.rich([("132 Pattern", {"bold": True}), (" (Medium) — Monotonic stack scanning right to left with a tracked third element. #456", {})])),
    N.bullet(N.rich([("Sum of Subarray Minimums", {"bold": True}), (" (Medium) — Contribution counting via monotonic stack (find span where each element is minimum). #907", {})])),
    N.para("These problems share the core technique: maintain a monotonic stack to process 'next greater/smaller' relationships in O(n)."),
    N.callout("📚 Reference: DSA_Patterns_and_SubPatterns_Guide.md — Stack/Queue section → Monotonic Stack: Next Greater · Sub-Pattern: Circular Array, 2 Passes", "📚", "gray_background"),
    N.divider(),
]

# ── Interactive Visual Explainer ──
blocks += [
    N.h2("🎯 Interactive Visual Explainer"),
    N.embed(N.embed_url_for("next_greater_element_ii")),
    N.para(N.rich([
        ("Step through the algorithm visually — use Next/Prev or arrow keys.", {"italic": True, "color": "gray"})
    ])),
]

# 4) Append all blocks
N.append_blocks(PAGE_ID, blocks)
print("NOTION OK", PAGE_ID)
